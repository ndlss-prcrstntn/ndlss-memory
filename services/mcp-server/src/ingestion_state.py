from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Any
from uuid import uuid4


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class IngestionRunRecord:
    run_id: str
    workspace_path: str
    status: str = "queued"
    accepted_at: str = field(default_factory=_now_iso)
    started_at: str | None = None
    finished_at: str | None = None
    last_event_at: str = field(default_factory=_now_iso)
    total_files: int = 0
    total_chunks: int = 0
    embedded_chunks: int = 0
    failed_chunks: int = 0
    retry_count: int = 0
    error_code: str | None = None
    error_message: str | None = None
    summary: dict[str, Any] | None = None

    def as_status(self) -> dict[str, Any]:
        return {
            "runId": self.run_id,
            "status": self.status,
            "totalFiles": self.total_files,
            "totalChunks": self.total_chunks,
            "embeddedChunks": self.embedded_chunks,
            "failedChunks": self.failed_chunks,
            "retryCount": self.retry_count,
            "lastEventAt": self.last_event_at,
            "errorCode": self.error_code,
            "errorMessage": self.error_message,
        }


class IngestionState:
    def __init__(self) -> None:
        self._lock = Lock()
        self._runs: dict[str, IngestionRunRecord] = {}
        self._active_run_id: str | None = None

    def create_run(self, workspace_path: str) -> IngestionRunRecord:
        with self._lock:
            if self._active_run_id:
                active = self._runs.get(self._active_run_id)
                if active and active.status in {"queued", "running"}:
                    raise RuntimeError("INGESTION_ALREADY_RUNNING")
            record = IngestionRunRecord(run_id=uuid4().hex, workspace_path=workspace_path)
            record.status = "running"
            record.started_at = _now_iso()
            self._runs[record.run_id] = record
            self._active_run_id = record.run_id
            return record

    def get_run(self, run_id: str) -> IngestionRunRecord | None:
        with self._lock:
            return self._runs.get(run_id)

    def update_run(self, run_id: str, **fields: Any) -> IngestionRunRecord | None:
        with self._lock:
            record = self._runs.get(run_id)
            if not record:
                return None
            for key, value in fields.items():
                if hasattr(record, key):
                    setattr(record, key, value)
            record.last_event_at = _now_iso()
            return record

    def finish_run(self, run_id: str, *, summary: dict[str, Any], status: str) -> IngestionRunRecord | None:
        with self._lock:
            record = self._runs.get(run_id)
            if not record:
                return None
            record.summary = summary
            record.status = status
            record.finished_at = _now_iso()
            record.last_event_at = record.finished_at
            record.total_files = int(summary.get("totalFiles", record.total_files))
            record.total_chunks = int(summary.get("totalChunks", record.total_chunks))
            record.embedded_chunks = int(summary.get("embeddedChunks", record.embedded_chunks))
            record.failed_chunks = int(summary.get("failedChunks", record.failed_chunks))
            record.retry_count = int(summary.get("retryCount", record.retry_count))
            if self._active_run_id == run_id:
                self._active_run_id = None
            return record


STATE = IngestionState()

