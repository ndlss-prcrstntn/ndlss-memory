from __future__ import annotations


class ChunkingConfigError(ValueError):
    pass


def validate_chunking_config(
    *,
    chunk_size: int,
    chunk_overlap: int,
    retry_max_attempts: int,
    retry_backoff_seconds: float,
    max_chunks_per_file: int | None = None,
) -> None:
    if chunk_size < 1:
        raise ChunkingConfigError("INGESTION_CHUNK_SIZE must be >= 1")
    if chunk_overlap < 0:
        raise ChunkingConfigError("INGESTION_CHUNK_OVERLAP must be >= 0")
    if chunk_overlap >= chunk_size:
        raise ChunkingConfigError("INGESTION_CHUNK_OVERLAP must be < INGESTION_CHUNK_SIZE")
    if retry_max_attempts < 1:
        raise ChunkingConfigError("INGESTION_RETRY_MAX_ATTEMPTS must be >= 1")
    if retry_backoff_seconds <= 0:
        raise ChunkingConfigError("INGESTION_RETRY_BACKOFF_SECONDS must be > 0")
    if max_chunks_per_file is not None and max_chunks_per_file < 1:
        raise ChunkingConfigError("INGESTION_MAX_CHUNKS_PER_FILE must be >= 1 when set")
