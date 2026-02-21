from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Any
from uuid import uuid4


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class IdempotencyRunRecord:
    run_id: str
    workspace_path: str
    status: str = "queued"
    accepted_at: str = field(default_factory=_now_iso)
    started_at: str | None = None
    finished_at: str | None = None
    last_event_at: str = field(default_factory=_now_iso)
    total_files: int = 0
    updated_chunks: int = 0
    skipped_chunks: int = 0
    deleted_chunks: int = 0
    failed_chunks: int = 0
    error_code: str | None = None
    error_message: str | None = None
    summary: dict[str, Any] | None = None

    def as_status(self) -> dict[str, Any]:
        return {
            "runId": self.run_id,
            "status": self.status,
            "totalFiles": self.total_files,
            "updatedChunks": self.updated_chunks,
            "skippedChunks": self.skipped_chunks,
            "deletedChunks": self.deleted_chunks,
            "failedChunks": self.failed_chunks,
            "lastEventAt": self.last_event_at,
            "errorCode": self.error_code,
            "errorMessage": self.error_message,
        }


class IdempotencyState:
    def __init__(self) -> None:
        self._lock = Lock()
        self._runs: dict[str, IdempotencyRunRecord] = {}
        self._active_run_id: str | None = None

    def create_run(self, workspace_path: str) -> IdempotencyRunRecord:
        with self._lock:
            if self._active_run_id:
                active = self._runs.get(self._active_run_id)
                if active and active.status in {"queued", "running"}:
                    raise RuntimeError("IDEMPOTENCY_ALREADY_RUNNING")
            record = IdempotencyRunRecord(run_id=uuid4().hex, workspace_path=workspace_path)
            record.status = "running"
            record.started_at = _now_iso()
            self._runs[record.run_id] = record
            self._active_run_id = record.run_id
            return record

    def get_run(self, run_id: str) -> IdempotencyRunRecord | None:
        with self._lock:
            return self._runs.get(run_id)

    def update_run(self, run_id: str, **fields: Any) -> IdempotencyRunRecord | None:
        with self._lock:
            record = self._runs.get(run_id)
            if not record:
                return None
            for key, value in fields.items():
                if hasattr(record, key):
                    setattr(record, key, value)
            record.last_event_at = _now_iso()
            return record

    def finish_run(self, run_id: str, *, summary: dict[str, Any], status: str) -> IdempotencyRunRecord | None:
        with self._lock:
            record = self._runs.get(run_id)
            if not record:
                return None
            record.summary = summary
            record.status = status
            record.finished_at = _now_iso()
            record.last_event_at = record.finished_at
            record.total_files = int(summary.get("totalFiles", record.total_files))
            record.updated_chunks = int(summary.get("updatedChunks", record.updated_chunks))
            record.skipped_chunks = int(summary.get("skippedChunks", record.skipped_chunks))
            record.deleted_chunks = int(summary.get("deletedChunks", record.deleted_chunks))
            record.failed_chunks = int(summary.get("failedChunks", record.failed_chunks))
            if self._active_run_id == run_id:
                self._active_run_id = None
            return record


STATE = IdempotencyState()

