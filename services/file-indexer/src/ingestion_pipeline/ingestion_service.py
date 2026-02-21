from __future__ import annotations

import os
from pathlib import Path
from typing import Callable, Iterable
from uuid import uuid4

from file_size_guard import is_file_too_large
from file_type_filter import is_supported_file, parse_supported_types
from ingestion_pipeline.chunk_models import ChunkingConfig
from ingestion_pipeline.chunk_record_builder import build_chunk_records
from ingestion_pipeline.embedding_models import EmbeddingTask, VectorRecord
from ingestion_pipeline.embedding_provider import EmbeddingProvider, provider_from_env
from ingestion_pipeline.embedding_retry import generate_embedding_with_retry
from ingestion_pipeline.metadata_mapper import map_chunk_metadata
from ingestion_pipeline.run_summary import IngestionRunSummary, SummaryAccumulator
from ingestion_pipeline.vector_upsert_repository import UpsertError, VectorUpsertRepository, repository_from_env
from path_exclude_filter import is_excluded_path, parse_exclude_patterns


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


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
    ) -> None:
        self.config = config
        self.provider = provider or provider_from_env()
        self.repository = repository or repository_from_env()
        self.file_types_csv = file_types_csv or os.getenv("INDEX_FILE_TYPES", ".md,.txt,.json,.yml,.yaml")
        self.exclude_patterns_csv = exclude_patterns_csv or os.getenv("INDEX_EXCLUDE_PATTERNS", ".git,node_modules,dist,build")
        self.max_file_size_bytes = max_file_size_bytes or int(os.getenv("INDEX_MAX_FILE_SIZE_BYTES", "1048576"))

    def run(
        self,
        *,
        run_id: str,
        workspace_path: str,
        progress_callback: Callable[[dict[str, int]], None] | None = None,
    ) -> IngestionRunSummary:
        root = Path(workspace_path)
        summary = SummaryAccumulator(run_id)
        if not root.exists() or not root.is_dir():
            summary.on_embedding_failure()
            return summary.finalize()

        for file_path in self._iter_candidate_files(root):
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
                except UpsertError:
                    summary.on_embedding_failure()
                self._emit_progress(summary, progress_callback)
        return summary.finalize()

    def _iter_candidate_files(self, root: Path) -> Iterable[Path]:
        supported_types = parse_supported_types(self.file_types_csv)
        exclude_patterns = parse_exclude_patterns(self.exclude_patterns_csv)
        candidates = sorted(path for path in root.rglob("*") if path.is_file())
        for path in candidates:
            rel = path.relative_to(root)
            if is_excluded_path(rel, exclude_patterns):
                continue
            if not is_supported_file(path, supported_types):
                continue
            too_large, size = is_file_too_large(path, self.max_file_size_bytes)
            if size <= 0 or too_large:
                continue
            yield path

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


def run_ingestion_pipeline(
    workspace_path: str,
    run_id: str | None = None,
    progress_callback: Callable[[dict[str, int]], None] | None = None,
) -> IngestionRunSummary:
    effective_run_id = run_id or uuid4().hex
    config = ChunkingConfig.from_env()
    service = IngestionService(config=config)
    return service.run(run_id=effective_run_id, workspace_path=workspace_path, progress_callback=progress_callback)
