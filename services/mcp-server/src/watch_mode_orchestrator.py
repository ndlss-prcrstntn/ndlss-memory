from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from threading import Event, Lock, Thread
from typing import Any
from uuid import uuid4

from watch_mode_coalescer import coalesce_events
from watch_mode_models import IncrementalIndexResult, WatchEvent, now_iso
from watch_mode_state import WatchModeState
from watch_mode_watcher import PollingWorkspaceWatcher, WatchRetryPolicy


def _ensure_file_indexer_src_path() -> None:
    candidates = [
        Path("/workspace/services/file-indexer/src"),
        Path(__file__).resolve().parents[2] / "file-indexer" / "src",
    ]
    explicit = os.getenv("FILE_INDEXER_SRC_PATH", "")
    if explicit:
        candidates.insert(0, Path(explicit))
    for candidate in candidates:
        if candidate.exists():
            as_text = str(candidate)
            if as_text not in sys.path:
                sys.path.insert(0, as_text)
            return


def _env_flag(name: str, default: str = "1") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


class WatchModeOrchestrator:
    def __init__(self, *, workspace_path: str, state: WatchModeState) -> None:
        self.workspace_path = workspace_path
        self.state = state
        self._lock = Lock()
        self._thread: Thread | None = None
        self._stop_event = Event()
        self._last_processed_hash: dict[str, str] = {}

        retry_policy = WatchRetryPolicy(
            max_attempts=int(os.getenv("WATCH_RETRY_MAX_ATTEMPTS", "5")),
            base_delay_seconds=float(os.getenv("WATCH_RETRY_BASE_DELAY_SECONDS", "1")),
            max_delay_seconds=float(os.getenv("WATCH_RETRY_MAX_DELAY_SECONDS", "30")),
        )
        self.watcher = PollingWorkspaceWatcher(
            workspace_path=workspace_path,
            poll_interval_seconds=int(os.getenv("WATCH_POLL_INTERVAL_SECONDS", "5")),
            max_events_per_cycle=int(os.getenv("WATCH_MAX_EVENTS_PER_CYCLE", "200")),
            file_types_csv=os.getenv("INDEX_FILE_TYPES", ".md,.txt,.json,.yml,.yaml"),
            exclude_patterns_csv=os.getenv("INDEX_EXCLUDE_PATTERNS", ".git,node_modules,dist,build"),
            retry_policy=retry_policy,
        )

    @property
    def is_running(self) -> bool:
        with self._lock:
            return bool(self._thread and self._thread.is_alive())

    def start(self) -> bool:
        with self._lock:
            if self._thread and self._thread.is_alive():
                return False
            self._stop_event = Event()
            self.state.start(self.workspace_path)
            self._thread = Thread(target=self._run, name="watch-mode-loop", daemon=True)
            self._thread.start()
            return True

    def stop(self) -> None:
        with self._lock:
            if self._thread is None:
                self.state.stop()
                return
            self._stop_event.set()
            self._thread.join(timeout=2.0)
            self._thread = None
            self.state.stop()

    def get_status(self) -> dict:
        return self.state.get_status()

    def get_summary(self) -> dict | None:
        return self.state.get_last_summary()

    def _run(self) -> None:
        self.state.set_state("running")
        self.state.clear_error()
        try:
            self.watcher.watch_loop(
                stop_event=self._stop_event,
                coalesce_window_seconds=int(os.getenv("WATCH_COALESCE_WINDOW_SECONDS", "2")),
                reconcile_interval_seconds=int(os.getenv("WATCH_RECONCILE_INTERVAL_SECONDS", "60")),
                on_events=self._on_events,
                on_reconcile=self._build_reconcile_events,
                on_heartbeat=self.state.heartbeat,
                on_retry=self._on_retry,
            )
            if self.state.get_status().get("state") != "stopped":
                self.state.set_state("running")
        except Exception as exc:  # noqa: BLE001
            self.state.record_retry(
                error_code="WATCH_LOOP_FAILED",
                error_message=str(exc),
                recoverable=False,
            )
            self._log_event("watch-loop-failed", {"error": str(exc)})

    def _on_retry(self, exc: Exception, attempt: int, delay: float, exhausted: bool) -> None:
        snapshot = self.state.record_retry(
            error_code="WATCH_RUNTIME_ERROR",
            error_message=str(exc),
            recoverable=not exhausted,
        )
        self.state.set_backoff(delay)
        self._log_event(
            "watch-retry",
            {
                "attempt": attempt,
                "delaySeconds": delay,
                "exhausted": exhausted,
                "state": snapshot.state,
                "error": str(exc),
            },
        )

    def _on_events(self, events: list[WatchEvent]) -> None:
        if not events:
            return

        self.state.enqueue_events(events)
        batch = self.state.dequeue_events(int(os.getenv("WATCH_MAX_EVENTS_PER_CYCLE", "200")))
        if not batch:
            return

        coalesced = coalesce_events(batch)
        summary = self.process_events(coalesced)
        self.state.mark_processed(len(coalesced), summary.failed_files)
        self.state.set_last_summary(summary)
        if summary.failed_files == 0:
            self.state.clear_error()
            if self.state.get_status().get("state") in {"recovering", "failed"}:
                self.state.set_state("running")
        self._log_event("watch-batch-processed", summary.to_payload())

    def _build_reconcile_events(self) -> list[WatchEvent]:
        repository = self._load_dependencies()["repository_from_env"]()
        indexed_files = repository.list_indexed_files()
        events = self.watcher.reconcile(indexed_files=indexed_files)
        if events:
            self._log_event(
                "watch-reconcile",
                {
                    "events": len(events),
                    "indexedFiles": len(indexed_files),
                },
            )
        return events

    def process_events(self, events: list[WatchEvent]) -> IncrementalIndexResult:
        deps = self._load_dependencies()
        config = deps["ChunkingConfig"].from_env()
        provider = deps["provider_from_env"]()
        repository = deps["repository_from_env"]()
        root = Path(self.workspace_path)

        indexed_files = 0
        deleted_records = 0
        skipped_files = 0
        failed_files = 0
        affected_files: list[str] = []
        reason_breakdown: dict[str, int] = {}

        def _reason(code: str) -> None:
            reason_breakdown[code] = reason_breakdown.get(code, 0) + 1

        for event in events:
            affected_files.append(event.path)
            if event.event_type == "deleted":
                deleted = repository.delete_file_records(event.path)
                deleted_records += deleted
                if deleted == 0:
                    skipped_files += 1
                    _reason("DELETE_NO_RECORDS")
                self._last_processed_hash.pop(event.path, None)
                continue

            file_path = root / event.path
            if not file_path.exists() or not file_path.is_file():
                skipped_files += 1
                _reason("SOURCE_MISSING")
                continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                failed_files += 1
                _reason("READ_ERROR")
                continue

            if not content.strip():
                skipped_files += 1
                _reason("EMPTY_FILE")
                continue

            previous_hash = repository.get_file_hash(event.path)
            fingerprint = deps["FileFingerprint"].from_content(
                file_path=event.path,
                content=content,
                previous_hash=previous_hash,
            )
            if self._last_processed_hash.get(event.path) == fingerprint.content_hash:
                skipped_files += 1
                _reason("SKIPPED_ALREADY_PROCESSED")
                continue

            skip_unchanged = _env_flag("IDEMPOTENCY_SKIP_UNCHANGED", "1")
            decision = deps["should_upsert"](
                current_hash=fingerprint.content_hash,
                previous_hash=fingerprint.previous_hash,
                skip_unchanged=skip_unchanged,
            )
            if not decision.should_upsert:
                skipped_files += 1
                _reason("SKIPPED_UNCHANGED")
                self._last_processed_hash[event.path] = fingerprint.content_hash
                continue

            previous_chunk_ids = repository.get_file_chunk_ids(event.path)
            current_chunk_ids: set[str] = set()
            file_failed = False

            chunks = deps["build_chunk_records"](
                root=root,
                file_path=file_path,
                content=content,
                config=config,
            )
            for chunk in chunks:
                current_chunk_ids.add(chunk.chunk_id)
                retry_result = deps["generate_embedding_with_retry"](
                    task=deps["EmbeddingTask"](
                        task_id=f"watch:{event.path}:{chunk.chunk_id}",
                        chunk_id=chunk.chunk_id,
                    ),
                    content=chunk.content,
                    provider=provider,
                    max_attempts=config.retry_max_attempts,
                    backoff_seconds=config.retry_backoff_seconds,
                )
                if retry_result.embedding is None:
                    file_failed = True
                    _reason("EMBEDDING_FAILED")
                    continue

                metadata = deps["map_chunk_metadata"](chunk)
                metadata["fileFingerprint"] = fingerprint.content_hash
                record = deps["VectorRecord"](
                    vector_id=chunk.chunk_id,
                    chunk_id=chunk.chunk_id,
                    embedding=retry_result.embedding,
                    metadata=metadata,
                )
                try:
                    repository.upsert(record)
                except deps["UpsertError"]:
                    file_failed = True
                    _reason("UPSERT_FAILED")

            stale_cleanup = _env_flag("IDEMPOTENCY_ENABLE_STALE_CLEANUP", "1")
            if stale_cleanup:
                stale_ids = deps["stale_chunk_ids"](previous_chunk_ids, current_chunk_ids)
                deleted_records += repository.delete_points(stale_ids)

            repository.set_file_index(
                file_path=event.path,
                file_hash=fingerprint.content_hash,
                chunk_ids=current_chunk_ids,
            )

            self._last_processed_hash[event.path] = fingerprint.content_hash
            if file_failed:
                failed_files += 1
            elif current_chunk_ids:
                indexed_files += 1
            else:
                skipped_files += 1
                _reason("EMPTY_FILE")

        return IncrementalIndexResult(
            affected_files=sorted(set(affected_files)),
            indexed_files=indexed_files,
            deleted_records=deleted_records,
            skipped_files=skipped_files,
            failed_files=failed_files,
            reason_breakdown=reason_breakdown,
            summary_id=uuid4().hex,
            window_started_at=now_iso(),
        )

    @staticmethod
    def _load_dependencies() -> dict[str, Any]:
        _ensure_file_indexer_src_path()
        from ingestion_pipeline.chunk_models import ChunkingConfig
        from ingestion_pipeline.chunk_record_builder import build_chunk_records
        from ingestion_pipeline.embedding_models import EmbeddingTask, VectorRecord
        from ingestion_pipeline.embedding_provider import provider_from_env
        from ingestion_pipeline.embedding_retry import generate_embedding_with_retry
        from ingestion_pipeline.file_fingerprint import FileFingerprint
        from ingestion_pipeline.idempotency_guard import should_upsert, stale_chunk_ids
        from ingestion_pipeline.metadata_mapper import map_chunk_metadata
        from ingestion_pipeline.vector_upsert_repository import UpsertError, repository_from_env

        return {
            "ChunkingConfig": ChunkingConfig,
            "EmbeddingTask": EmbeddingTask,
            "FileFingerprint": FileFingerprint,
            "UpsertError": UpsertError,
            "VectorRecord": VectorRecord,
            "build_chunk_records": build_chunk_records,
            "generate_embedding_with_retry": generate_embedding_with_retry,
            "map_chunk_metadata": map_chunk_metadata,
            "provider_from_env": provider_from_env,
            "repository_from_env": repository_from_env,
            "should_upsert": should_upsert,
            "stale_chunk_ids": stale_chunk_ids,
        }

    @staticmethod
    def _log_event(event: str, payload: dict[str, Any]) -> None:
        print(json.dumps({"event": event, "watch": payload}, ensure_ascii=False))
