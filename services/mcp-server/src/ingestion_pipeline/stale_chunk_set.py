from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StaleChunkSet:
    file_path: str
    obsolete_chunk_ids: set[str]
    computed_from_hash: str

