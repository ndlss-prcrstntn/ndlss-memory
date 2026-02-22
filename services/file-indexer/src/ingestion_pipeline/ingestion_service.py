from __future__ import annotations

import os
from pathlib import Path
from typing import Callable, Iterable
from uuid import uuid4

from file_size_guard import is_file_too_large
from file_type_filter import is_supported_file, parse_supported_types
from full_scan_walker import path_depth
from ingestion_pipeline.chunk_models import ChunkingConfig
from ingestion_pipeline.chunk_record_builder import build_chunk_records
from ingestion_pipeline.embedding_models import EmbeddingTask, VectorRecord
from ingestion_pipeline.embedding_provider import EmbeddingProvider, provider_from_env
from ingestion_pipeline.embedding_retry import generate_embedding_with_retry
from ingestion_pipeline.file_fingerprint import FileFingerprint
from ingestion_pipeline.idempotency_guard import should_upsert, stale_chunk_ids
from ingestion_pipeline.index_sync_summary import IndexSyncSummary, IndexSyncSummaryAccumulator
from ingestion_pipeline.metadata_mapper import map_chunk_metadata
from ingestion_pipeline.run_summary import IngestionRunSummary, SummaryAccumulator
from ingestion_pipeline.vector_upsert_repository import UpsertError, VectorUpsertRepository, repository_from_env
from path_exclude_filter import is_excluded_path, parse_exclude_patterns
from skip_reasons import LIMIT_DEPTH_EXCEEDED, LIMIT_MAX_FILES_REACHED


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _env_flag(name: str, default: str = "1") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def _relative(root: Path, path: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")


class IngestionService:
    def __init__(
        self,
        *,
        config: ChunkingConfig,
        provider: EmbeddingProvider | None = None,
        repository: VectorUpsertRepository | None = None,
        file_types_csv: str | None = None,
        exclude_patterns_csv: str | None = None,
        max_file_size_bytes: int | None = None,
        max_traversal_depth: int | None = None,
        max_files_per_run: int | None = None,
    ) -> None:
        self.config = config
        self.provider = provider or provider_from_env()
        self.repository = repository or repository_from_env()
        self.file_types_csv = file_types_csv or os.getenv("INDEX_FILE_TYPES", ".md,.txt,.json,.yml,.yaml")
        self.exclude_patterns_csv = exclude_patterns_csv or os.getenv("INDEX_EXCLUDE_PATTERNS", ".git,node_modules,dist,build")
        self.max_file_size_bytes = max_file_size_bytes or int(os.getenv("INDEX_MAX_FILE_SIZE_BYTES", "1048576"))
        self.max_traversal_depth = self._optional_limit(max_traversal_depth, "INDEX_MAX_TRAVERSAL_DEPTH", minimum=0)
        self.max_files_per_run = self._optional_limit(max_files_per_run, "INDEX_MAX_FILES_PER_RUN", minimum=1)

    def run(
        self,
        *,
        run_id: str,
        workspace_path: str,
        progress_callback: Callable[[dict[str, int]], None] | None = None,
    ) -> IngestionRunSummary:
        root = Path(workspace_path)
        summary = SummaryAccumulator(
            run_id,
            max_traversal_depth=self.max_traversal_depth,
            max_files_per_run=self.max_files_per_run,
        )
        if not root.exists() or not root.is_dir():
            summary.on_embedding_failure()
            return summary.finalize()

        for file_path in self._iter_candidate_files(root, summary=summary):
            summary.on_file()
            try:
                content = _read_text(file_path)
            except OSError:
                summary.on_embedding_failure()
                continue

            if not content.strip():
                continue

            records = build_chunk_records(root=root, file_path=file_path, content=content, config=self.config)
            for chunk in records:
                summary.on_chunk()
                task = EmbeddingTask(task_id=f"{run_id}:{chunk.chunk_id}", chunk_id=chunk.chunk_id)
                retry_result = generate_embedding_with_retry(
                    task=task,
                    content=chunk.content,
                    provider=self.provider,
                    max_attempts=self.config.retry_max_attempts,
                    backoff_seconds=self.config.retry_backoff_seconds,
                )
                summary.on_retry(retry_result.retries_used)
                if retry_result.embedding is None:
                    summary.on_embedding_failure()
                    self._emit_progress(summary, progress_callback)
                    continue

                metadata = map_chunk_metadata(chunk)
                record = VectorRecord(
                    vector_id=chunk.chunk_id,
                    chunk_id=chunk.chunk_id,
                    embedding=retry_result.embedding,
                    metadata=metadata,
                )
                try:
                    self.repository.upsert(record)
                    summary.on_embedding_success(metadata)
                except UpsertError as exc:
                    summary.on_embedding_failure()
                    self._emit_progress(summary, progress_callback)
                    raise UpsertError(f"Persistence upsert failed for chunk '{chunk.chunk_id}': {exc}") from exc
                self._emit_progress(summary, progress_callback)
        return summary.finalize()

    def run_idempotency_sync(
        self,
        *,
        run_id: str,
        workspace_path: str,
        progress_callback: Callable[[dict[str, int]], None] | None = None,
    ) -> IndexSyncSummary:
        root = Path(workspace_path)
        summary = IndexSyncSummaryAccumulator(run_id)
        if not root.exists() or not root.is_dir():
            summary.on_failed("WORKSPACE_NOT_FOUND")
            return summary.finalize()

        skip_unchanged = _env_flag("IDEMPOTENCY_SKIP_UNCHANGED", "1")
        stale_cleanup = _env_flag("IDEMPOTENCY_ENABLE_STALE_CLEANUP", "1")
        seen_files: set[str] = set()

        for file_path in self._iter_candidate_files(root):
            summary.on_file()
            relative_path = _relative(root, file_path)
            seen_files.add(relative_path)

            try:
                content = _read_text(file_path)
            except OSError:
                summary.on_failed("READ_ERROR")
                self._emit_idempotency_progress(summary, progress_callback)
                continue

            previous_hash = self.repository.get_file_hash(relative_path)
            fingerprint = FileFingerprint.from_content(file_path=relative_path, content=content, previous_hash=previous_hash)
            decision = should_upsert(
                current_hash=fingerprint.content_hash,
                previous_hash=fingerprint.previous_hash,
                skip_unchanged=skip_unchanged,
            )

            previous_chunk_ids = self.repository.get_file_chunk_ids(relative_path)
            if not decision.should_upsert:
                for _ in previous_chunk_ids:
                    summary.on_skipped("SKIPPED_UNCHANGED")
                self._emit_idempotency_progress(summary, progress_callback)
                continue

            current_chunk_ids: set[str] = set()
            records = build_chunk_records(root=root, file_path=file_path, content=content, config=self.config)
            for chunk in records:
                current_chunk_ids.add(chunk.chunk_id)
                try:
                    embedding = self.provider.generate_embedding(chunk.content)
                except Exception:
                    summary.on_failed("EMBEDDING_FAILED")
                    continue

                metadata = map_chunk_metadata(chunk)
                metadata["fileFingerprint"] = fingerprint.content_hash
                record = VectorRecord(
                    vector_id=chunk.chunk_id,
                    chunk_id=chunk.chunk_id,
                    embedding=embedding,
                    metadata=metadata,
                )
                try:
                    self.repository.upsert(record)
                    summary.on_updated("UPDATED")
                except UpsertError:
                    summary.on_failed("UPSERT_FAILED")

            stale_ids = stale_chunk_ids(previous_chunk_ids, current_chunk_ids)
            if stale_cleanup and stale_ids:
                deleted = self.repository.delete_points(stale_ids)
                for _ in range(deleted):
                    summary.on_deleted("DELETED_STALE")

            self.repository.set_file_index(
                file_path=relative_path,
                file_hash=fingerprint.content_hash,
                chunk_ids=current_chunk_ids,
            )
            self._emit_idempotency_progress(summary, progress_callback)

        if stale_cleanup:
            removed_files = self.repository.list_indexed_files() - seen_files
            for file_path in sorted(removed_files):
                stale_ids = self.repository.get_file_chunk_ids(file_path)
                deleted = self.repository.delete_points(stale_ids)
                for _ in range(deleted):
                    summary.on_deleted("DELETED_SOURCE_REMOVED")
                self.repository.remove_file(file_path)
                self._emit_idempotency_progress(summary, progress_callback)

        return summary.finalize()

    def _iter_candidate_files(self, root: Path, summary: SummaryAccumulator | None = None) -> Iterable[Path]:
        supported_types = parse_supported_types(self.file_types_csv)
        exclude_patterns = parse_exclude_patterns(self.exclude_patterns_csv)
        candidates = sorted(path for path in root.rglob("*") if path.is_file())
        selected_files = 0
        for path in candidates:
            rel = path.relative_to(root)
            depth = path_depth(root, path)
            if self.max_traversal_depth is not None and depth > self.max_traversal_depth:
                if summary is not None:
                    summary.on_skip(LIMIT_DEPTH_EXCEEDED)
                continue
            if is_excluded_path(rel, exclude_patterns):
                continue
            if not is_supported_file(path, supported_types):
                continue
            too_large, size = is_file_too_large(path, self.max_file_size_bytes)
            if size <= 0 or too_large:
                continue
            if self.max_files_per_run is not None and selected_files >= self.max_files_per_run:
                if summary is not None:
                    summary.on_skip(LIMIT_MAX_FILES_REACHED)
                continue
            selected_files += 1
            yield path

    @staticmethod
    def _optional_limit(explicit_value: int | None, env_name: str, *, minimum: int) -> int | None:
        if explicit_value is not None:
            return explicit_value
        raw = os.getenv(env_name, "")
        if raw is None or str(raw).strip() == "":
            return None
        value = int(raw)
        if value < minimum:
            raise ValueError(f"{env_name} must be >= {minimum}")
        return value

    @staticmethod
    def _emit_progress(summary: SummaryAccumulator, callback: Callable[[dict[str, int]], None] | None) -> None:
        if callback is None:
            return
        callback(
            {
                "totalFiles": summary.total_files,
                "totalChunks": summary.total_chunks,
                "embeddedChunks": summary.embedded_chunks,
                "failedChunks": summary.failed_chunks,
                "retryCount": summary.retry_count,
            }
        )

    @staticmethod
    def _emit_idempotency_progress(
        summary: IndexSyncSummaryAccumulator,
        callback: Callable[[dict[str, int]], None] | None,
    ) -> None:
        if callback is None:
            return
        callback(
            {
                "totalFiles": summary.total_files,
                "updatedChunks": summary.updated_chunks,
                "skippedChunks": summary.skipped_chunks,
                "deletedChunks": summary.deleted_chunks,
                "failedChunks": summary.failed_chunks,
            }
        )


def run_ingestion_pipeline(
    workspace_path: str,
    run_id: str | None = None,
    progress_callback: Callable[[dict[str, int]], None] | None = None,
) -> IngestionRunSummary:
    effective_run_id = run_id or uuid4().hex
    config = ChunkingConfig.from_env()
    service = IngestionService(config=config)
    return service.run(run_id=effective_run_id, workspace_path=workspace_path, progress_callback=progress_callback)


def run_idempotency_sync_pipeline(
    workspace_path: str,
    run_id: str | None = None,
    progress_callback: Callable[[dict[str, int]], None] | None = None,
) -> IndexSyncSummary:
    effective_run_id = run_id or uuid4().hex
    config = ChunkingConfig.from_env()
    service = IngestionService(config=config)
    return service.run_idempotency_sync(run_id=effective_run_id, workspace_path=workspace_path, progress_callback=progress_callback)
