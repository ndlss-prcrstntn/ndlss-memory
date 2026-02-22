from __future__ import annotations

from ingestion_pipeline.chunking_validation import validate_chunking_config


def chunk_text(
    content: str,
    *,
    chunk_size: int,
    chunk_overlap: int,
    max_chunks_per_file: int | None = None,
) -> list[str]:
    validate_chunking_config(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        retry_max_attempts=1,
        retry_backoff_seconds=1.0,
        max_chunks_per_file=max_chunks_per_file,
    )

    if not content:
        return []

    step = chunk_size - chunk_overlap
    chunks: list[str] = []
    for start in range(0, len(content), step):
        chunk = content[start : start + chunk_size]
        if not chunk:
            continue
        chunks.append(chunk)
        if max_chunks_per_file is not None and len(chunks) >= max_chunks_per_file:
            break
        if start + chunk_size >= len(content):
            break
    return chunks

