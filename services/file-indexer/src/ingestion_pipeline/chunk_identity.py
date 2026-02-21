from __future__ import annotations

import hashlib
from dataclasses import dataclass

from ingestion_pipeline.content_hash import build_text_hash


@dataclass(frozen=True)
class ChunkIdentity:
    chunk_id: str
    file_path: str
    chunk_index: int
    chunk_text_hash: str


def build_chunk_identity(*, file_path: str, chunk_index: int, chunk_text: str) -> ChunkIdentity:
    chunk_text_hash = build_text_hash(chunk_text)
    raw = f"{file_path}:{chunk_index}:{chunk_text_hash}".encode("utf-8")
    chunk_id = hashlib.sha256(raw).hexdigest()
    return ChunkIdentity(
        chunk_id=chunk_id,
        file_path=file_path,
        chunk_index=chunk_index,
        chunk_text_hash=chunk_text_hash,
    )

