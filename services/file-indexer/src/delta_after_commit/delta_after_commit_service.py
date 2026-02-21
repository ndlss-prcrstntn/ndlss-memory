from __future__ import annotations

import os
from pathlib import Path
from typing import Callable

from delta_after_commit.change_classifier import classify_changes
from delta_after_commit.delta_run_summary import DeltaRunSummary, DeltaRunSummaryAccumulator
from delta_after_commit.fallback_policy import FallbackPolicy
from delta_after_commit.git_diff_reader import read_git_change_set
from file_type_filter import parse_supported_types
from ingestion_pipeline.chunk_models import ChunkingConfig
from ingestion_pipeline.chunk_record_builder import build_chunk_records
from ingestion_pipeline.embedding_models import VectorRecord
from ingestion_pipeline.file_fingerprint import FileFingerprint
from ingestion_pipeline.idempotency_guard import should_upsert, stale_chunk_ids
from ingestion_pipeline.ingestion_service import IngestionService
from ingestion_pipeline.metadata_mapper import map_chunk_metadata
from ingestion_pipeline.vector_upsert_repository import UpsertError, repository_from_env
from path_exclude_filter import parse_exclude_patterns


class DeltaAfterCommitService:
    def __init__(
        self,
        *,
        config: ChunkingConfig,
        fallback_policy: FallbackPolicy | None = None,
        file_types_csv: str | None = None,
        exclude_patterns_csv: str | None = None,
        max_file_size_bytes: int | None = None,
    ) -> None:
        self.config = config
        self.fallback_policy = fallback_policy or FallbackPolicy()
        self.ingestion_service = IngestionService(config=config)
        self.repository = repository_from_env()
        self.provider = self.ingestion_service.provider
        self.file_types_csv = file_types_csv or os.getenv("INDEX_FILE_TYPES", ".md,.txt,.json,.yml,.yaml")
        self.exclude_patterns_csv = exclude_patterns_csv or os.getenv("INDEX_EXCLUDE_PATTERNS", ".git,node_modules,dist,build")
        self.max_file_size_bytes = max_file_size_bytes or int(os.getenv("INDEX_MAX_FILE_SIZE_BYTES", "1048576"))

    def run(
        self,
        *,
        run_id: str,
        workspace_path: str,
        base_ref: str,
        target_ref: str,
        progress_callback: Callable[[dict[str, int | str]], None] | None = None,
    ) -> DeltaRunSummary:
        summary = DeltaRunSummaryAccumulator(run_id=run_id, base_ref=base_ref, target_ref=target_ref)
        root = Path(workspace_path)
        if not root.exists() or not root.is_dir():
            summary.on_failed("WORKSPACE_NOT_FOUND")
            return summary.finalize()

        include_renames = os.getenv("DELTA_INCLUDE_RENAMES", "1").strip() in {"1", "true", "yes", "on"}
        try:
            change_set = read_git_change_set(
                workspace_path=workspace_path,
                base_ref=base_ref,
                target_ref=target_ref,
                include_renames=include_renames,
            )
        except Exception as exc:
            decision = self.fallback_policy.for_exception(exc)
            if not decision.should_fallback:
                summary.on_failed("GIT_DIFF_FAILED")
                return summary.finalize()
            summary.set_fallback(decision.reason_code or "GIT_DIFF_FAILED")
            return self._run_fallback(summary=summary, workspace_path=workspace_path, progress_callback=progress_callback)

        supported_types = parse_supported_types(self.file_types_csv)
        exclude_patterns = parse_exclude_patterns(self.exclude_patterns_csv)
        candidates = classify_changes(
            run_id=run_id,
            root=root,
            change_set=change_set,
            supported_types=supported_types,
            exclude_patterns=exclude_patterns,
            max_file_size_bytes=self.max_file_size_bytes,
            include_renames=include_renames,
        )

        for change in change_set:
            summary.on_change(change.change_type)

        deletes = [item for item in candidates if item.decision == "delete"]
        indexes = [item for item in candidates if item.decision == "index"]
        skips = [item for item in candidates if item.decision == "skip"]

        for item in deletes:
            deleted_count = self._delete_file_records(item.path)
            if deleted_count == 0:
                summary.on_skipped("DELETE_NO_RECORDS")
            else:
                for _ in range(deleted_count):
                    summary.on_removed(item.decision_reason_code)
            self._emit_progress(summary, progress_callback)

        for item in indexes:
            self._index_file(root=root, relative_path=item.path, summary=summary)
            self._emit_progress(summary, progress_callback)

        for item in skips:
            summary.on_skipped(item.decision_reason_code)
            self._emit_progress(summary, progress_callback)

        return summary.finalize()

    def _run_fallback(
        self,
        *,
        summary: DeltaRunSummaryAccumulator,
        workspace_path: str,
        progress_callback: Callable[[dict[str, int | str]], None] | None,
    ) -> DeltaRunSummary:
        fallback_summary = self.ingestion_service.run_idempotency_sync(
            run_id=summary.run_id,
            workspace_path=workspace_path,
        )
        fallback_payload = fallback_summary.to_dict()
        summary.absorb_fallback_sync(
            updated_chunks=int(fallback_payload.get("updatedChunks", 0)),
            skipped_chunks=int(fallback_payload.get("skippedChunks", 0)),
            deleted_chunks=int(fallback_payload.get("deletedChunks", 0)),
            failed_chunks=int(fallback_payload.get("failedChunks", 0)),
        )
        self._emit_progress(summary, progress_callback)
        return summary.finalize()

    def _delete_file_records(self, relative_path: str) -> int:
        return self.repository.delete_file_records(relative_path)

    def _index_file(self, *, root: Path, relative_path: str, summary: DeltaRunSummaryAccumulator) -> None:
        file_path = root / relative_path
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            summary.on_failed("READ_ERROR")
            return

        previous_hash = self.repository.get_file_hash(relative_path)
        fingerprint = FileFingerprint.from_content(file_path=relative_path, content=content, previous_hash=previous_hash)
        previous_chunk_ids = self.repository.get_file_chunk_ids(relative_path)

        skip_unchanged = os.getenv("IDEMPOTENCY_SKIP_UNCHANGED", "1").strip() in {"1", "true", "yes", "on"}
        decision = should_upsert(
            current_hash=fingerprint.content_hash,
            previous_hash=fingerprint.previous_hash,
            skip_unchanged=skip_unchanged,
        )
        if not decision.should_upsert:
            summary.on_skipped("SKIPPED_UNCHANGED")
            return

        chunk_records = build_chunk_records(root=root, file_path=file_path, content=content, config=self.config)
        current_ids: set[str] = set()
        for chunk in chunk_records:
            current_ids.add(chunk.chunk_id)
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
                summary.on_indexed("INDEXED")
            except UpsertError:
                summary.on_failed("UPSERT_FAILED")

        stale_cleanup = os.getenv("IDEMPOTENCY_ENABLE_STALE_CLEANUP", "1").strip() in {"1", "true", "yes", "on"}
        stale_ids = stale_chunk_ids(previous_chunk_ids, current_ids)
        if stale_cleanup and stale_ids:
            deleted = self.repository.delete_points(stale_ids)
            for _ in range(deleted):
                summary.on_removed("DELETED_STALE")

        self.repository.set_file_index(
            file_path=relative_path,
            file_hash=fingerprint.content_hash,
            chunk_ids=current_ids,
        )

    @staticmethod
    def _emit_progress(
        summary: DeltaRunSummaryAccumulator,
        callback: Callable[[dict[str, int | str]], None] | None,
    ) -> None:
        if callback is None:
            return
        callback(
            {
                "requestedMode": summary.requested_mode,
                "effectiveMode": summary.effective_mode,
                "addedFiles": summary.added_files,
                "modifiedFiles": summary.modified_files,
                "deletedFiles": summary.deleted_files,
                "renamedFiles": summary.renamed_files,
                "indexedFiles": summary.indexed_files,
                "removedRecords": summary.removed_records,
                "skippedFiles": summary.skipped_files,
                "failedFiles": summary.failed_files,
                "fallbackReasonCode": summary.fallback_reason_code,
            }
        )


def run_delta_after_commit_pipeline(
    *,
    run_id: str,
    workspace_path: str,
    base_ref: str,
    target_ref: str,
    progress_callback: Callable[[dict[str, int | str]], None] | None = None,
) -> DeltaRunSummary:
    config = ChunkingConfig.from_env()
    service = DeltaAfterCommitService(config=config)
    return service.run(
        run_id=run_id,
        workspace_path=workspace_path,
        base_ref=base_ref,
        target_ref=target_ref,
        progress_callback=progress_callback,
    )
