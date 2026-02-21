from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path

from ingestion_pipeline.chunk_identity import build_chunk_identity
from ingestion_pipeline.chunk_models import ChunkRecord, ChunkingConfig
from ingestion_pipeline.chunker import chunk_text
from ingestion_pipeline.content_hash import build_text_hash


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_chunk_records(
    *,
    root: Path,
    file_path: Path,
    content: str,
    config: ChunkingConfig,
    processed_at: str | None = None,
) -> list[ChunkRecord]:
    if processed_at is None:
        processed_at = _now_iso()

    relative_path = str(file_path.relative_to(root)).replace("\\", "/")
    file_name = file_path.name
    file_type = file_path.suffix.lower()
    content_hash = build_text_hash(content)
    chunks = chunk_text(
        content,
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        max_chunks_per_file=config.max_chunks_per_file,
    )

    records: list[ChunkRecord] = []
    for idx, chunk in enumerate(chunks):
        identity = build_chunk_identity(file_path=relative_path, chunk_index=idx, chunk_text=chunk)
        records.append(
            ChunkRecord(
                chunk_id=identity.chunk_id,
                file_path=relative_path,
                file_name=file_name,
                file_type=file_type,
                chunk_index=idx,
                content=chunk,
                content_hash=content_hash,
                processed_at=processed_at,
            )
        )
    return records

