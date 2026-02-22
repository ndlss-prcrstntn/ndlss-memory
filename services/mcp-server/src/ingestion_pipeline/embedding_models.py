from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class EmbeddingTask:
    task_id: str
    chunk_id: str
    status: str = "queued"
    attempt_count: int = 0
    last_error_code: str | None = None
    last_error_message: str | None = None
    started_at: str | None = None
    finished_at: str | None = None

    def mark_running(self) -> None:
        if self.started_at is None:
            self.started_at = _now_iso()
        self.status = "running"
        self.attempt_count += 1

    def mark_success(self) -> None:
        self.status = "success"
        self.finished_at = _now_iso()
        self.last_error_code = None
        self.last_error_message = None

    def mark_failed(self, error_code: str, message: str) -> None:
        self.status = "failed"
        self.finished_at = _now_iso()
        self.last_error_code = error_code
        self.last_error_message = message

    def to_dict(self) -> dict[str, Any]:
        return {
            "taskId": self.task_id,
            "chunkId": self.chunk_id,
            "status": self.status,
            "attemptCount": self.attempt_count,
            "lastErrorCode": self.last_error_code,
            "lastErrorMessage": self.last_error_message,
            "startedAt": self.started_at,
            "finishedAt": self.finished_at,
        }


@dataclass(frozen=True)
class VectorRecord:
    vector_id: str
    chunk_id: str
    embedding: list[float]
    metadata: dict[str, Any]
    created_at: str = field(default_factory=_now_iso)

    def to_qdrant_point(self) -> dict[str, Any]:
        payload = dict(self.metadata)
        payload["chunkId"] = self.chunk_id
        payload["vectorCreatedAt"] = self.created_at
        return {"id": self.vector_id, "vector": self.embedding, "payload": payload}

