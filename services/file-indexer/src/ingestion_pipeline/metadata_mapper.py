from __future__ import annotations

from ingestion_pipeline.chunk_models import ChunkRecord


def map_chunk_metadata(chunk: ChunkRecord) -> dict[str, str | int]:
    return {
        "path": chunk.file_path,
        "fileName": chunk.file_name,
        "fileType": chunk.file_type,
        "chunkIndex": chunk.chunk_index,
        "contentHash": chunk.content_hash,
        "timestamp": chunk.processed_at,
    }

