from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from ingestion_pipeline.chunking_validation import validate_chunking_config


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_optional_int(value: str | None) -> int | None:
    if value is None or value.strip() == "":
        return None
    return int(value)


@dataclass(frozen=True)
class ChunkingConfig:
    chunk_size: int
    chunk_overlap: int
    retry_max_attempts: int
    retry_backoff_seconds: float
    max_chunks_per_file: int | None = None

    def validate(self) -> None:
        validate_chunking_config(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            retry_max_attempts=self.retry_max_attempts,
            retry_backoff_seconds=self.retry_backoff_seconds,
            max_chunks_per_file=self.max_chunks_per_file,
        )

    @classmethod
    def from_env(cls) -> "ChunkingConfig":
        config = cls(
            chunk_size=int(os.getenv("INGESTION_CHUNK_SIZE", "800")),
            chunk_overlap=int(os.getenv("INGESTION_CHUNK_OVERLAP", "120")),
            retry_max_attempts=int(os.getenv("INGESTION_RETRY_MAX_ATTEMPTS", "3")),
            retry_backoff_seconds=float(os.getenv("INGESTION_RETRY_BACKOFF_SECONDS", "1.0")),
            max_chunks_per_file=_parse_optional_int(os.getenv("INGESTION_MAX_CHUNKS_PER_FILE")),
        )
        config.validate()
        return config

    def to_dict(self) -> dict[str, Any]:
        return {
            "chunkSize": self.chunk_size,
            "chunkOverlap": self.chunk_overlap,
            "retryMaxAttempts": self.retry_max_attempts,
            "retryBackoffSeconds": self.retry_backoff_seconds,
            "maxChunksPerFile": self.max_chunks_per_file,
        }


@dataclass(frozen=True)
class ChunkRecord:
    chunk_id: str
    file_path: str
    file_name: str
    file_type: str
    chunk_index: int
    content: str
    content_hash: str
    processed_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "chunkId": self.chunk_id,
            "filePath": self.file_path,
            "fileName": self.file_name,
            "fileType": self.file_type,
            "chunkIndex": self.chunk_index,
            "content": self.content,
            "contentHash": self.content_hash,
            "processedAt": self.processed_at or _now_iso(),
        }
