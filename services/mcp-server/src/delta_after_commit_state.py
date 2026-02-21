from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Any
from uuid import uuid4


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class DeltaAfterCommitRunRecord:
    run_id: str
    workspace_path: str
    base_ref: str
    target_ref: str
    requested_mode: str = "delta-after-commit"
    effective_mode: str = "delta-after-commit"
    status: str = "queued"
    accepted_at: str = field(default_factory=_now_iso)
    started_at: str | None = None
    finished_at: str | None = None
    last_event_at: str = field(default_factory=_now_iso)
    added_files: int = 0
    modified_files: int = 0
    deleted_files: int = 0
    renamed_files: int = 0
    indexed_files: int = 0
    removed_records: int = 0
    skipped_files: int = 0
    failed_files: int = 0
    fallback_reason_code: str | None = None
    error_code: str | None = None
    error_message: str | None = None
    summary: dict[str, Any] | None = None

    def as_status(self) -> dict[str, Any]:
        payload = {
            "runId": self.run_id,
            "status": self.status,
            "requestedMode": self.requested_mode,
            "effectiveMode": self.effective_mode,
            "baseRef": self.base_ref,
            "targetRef": self.target_ref,
            "addedFiles": self.added_files,
            "modifiedFiles": self.modified_files,
            "deletedFiles": self.deleted_files,
            "renamedFiles": self.renamed_files,
            "indexedFiles": self.indexed_files,
            "removedRecords": self.removed_records,
            "skippedFiles": self.skipped_files,
            "failedFiles": self.failed_files,
            "lastEventAt": self.last_event_at,
            "errorCode": self.error_code,
            "errorMessage": self.error_message,
        }
        if self.fallback_reason_code:
            payload["fallbackReasonCode"] = self.fallback_reason_code
        return payload


class DeltaAfterCommitState:
    def __init__(self) -> None:
        self._lock = Lock()
        self._runs: dict[str, DeltaAfterCommitRunRecord] = {}
        self._active_run_id: str | None = None

    def create_run(self, *, workspace_path: str, base_ref: str, target_ref: str) -> DeltaAfterCommitRunRecord:
        with self._lock:
            if self._active_run_id:
                active = self._runs.get(self._active_run_id)
                if active and active.status in {"queued", "running"}:
                    raise RuntimeError("DELTA_ALREADY_RUNNING")
            record = DeltaAfterCommitRunRecord(
                run_id=uuid4().hex,
                workspace_path=workspace_path,
                base_ref=base_ref,
                target_ref=target_ref,
            )
            record.status = "running"
            record.started_at = _now_iso()
            self._runs[record.run_id] = record
            self._active_run_id = record.run_id
            return record

    def get_run(self, run_id: str) -> DeltaAfterCommitRunRecord | None:
        with self._lock:
            return self._runs.get(run_id)

    def update_run(self, run_id: str, **fields: Any) -> DeltaAfterCommitRunRecord | None:
        with self._lock:
            record = self._runs.get(run_id)
            if not record:
                return None
            for key, value in fields.items():
                if hasattr(record, key):
                    setattr(record, key, value)
            record.last_event_at = _now_iso()
            return record

    def finish_run(self, run_id: str, *, summary: dict[str, Any], status: str) -> DeltaAfterCommitRunRecord | None:
        with self._lock:
            record = self._runs.get(run_id)
            if not record:
                return None
            record.summary = summary
            record.status = status
            record.finished_at = _now_iso()
            record.last_event_at = record.finished_at
            record.effective_mode = str(summary.get("effectiveMode", record.effective_mode))
            record.fallback_reason_code = summary.get("fallbackReasonCode")
            record.added_files = int(summary.get("addedFiles", record.added_files))
            record.modified_files = int(summary.get("modifiedFiles", record.modified_files))
            record.deleted_files = int(summary.get("deletedFiles", record.deleted_files))
            record.renamed_files = int(summary.get("renamedFiles", record.renamed_files))
            record.indexed_files = int(summary.get("indexedFiles", record.indexed_files))
            record.removed_records = int(summary.get("removedRecords", record.removed_records))
            record.skipped_files = int(summary.get("skippedFiles", record.skipped_files))
            record.failed_files = int(summary.get("failedFiles", record.failed_files))
            if self._active_run_id == run_id:
                self._active_run_id = None
            return record


STATE = DeltaAfterCommitState()
