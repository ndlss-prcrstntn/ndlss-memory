from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Any
from uuid import uuid4

LIMIT_DEPTH_EXCEEDED = "LIMIT_DEPTH_EXCEEDED"
LIMIT_MAX_FILES_REACHED = "LIMIT_MAX_FILES_REACHED"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class FullScanJobRecord:
    job_id: str
    workspace_path: str
    max_file_size_bytes: int
    max_traversal_depth: int | None = None
    max_files_per_run: int | None = None
    status: str = "queued"
    accepted_at: str = field(default_factory=_now_iso)
    started_at: str | None = None
    finished_at: str | None = None
    last_event_at: str = field(default_factory=_now_iso)
    processed_count: int = 0
    indexed_count: int = 0
    skip_count: int = 0
    error_count: int = 0
    percent_complete: float | None = None
    skip_breakdown: dict[str, int] = field(default_factory=dict)

    def as_progress(self) -> dict[str, Any]:
        return {
            "jobId": self.job_id,
            "status": self.status,
            "processedCount": self.processed_count,
            "indexedCount": self.indexed_count,
            "skipCount": self.skip_count,
            "errorCount": self.error_count,
            "percentComplete": self.percent_complete,
            "lastEventAt": self.last_event_at,
        }

    def as_summary(self) -> dict[str, Any]:
        if not self.started_at:
            duration = 0.0
        else:
            start_dt = datetime.fromisoformat(self.started_at)
            end_dt = datetime.fromisoformat(self.finished_at) if self.finished_at else datetime.now(timezone.utc)
            duration = (end_dt - start_dt).total_seconds()
        return {
            "jobId": self.job_id,
            "result": self.status if self.status in {"completed", "failed", "cancelled"} else "running",
            "durationSeconds": duration,
            "appliedLimits": {
                "maxTraversalDepth": self.max_traversal_depth,
                "maxFilesPerRun": self.max_files_per_run,
            },
            "totals": {
                "processedCount": self.processed_count,
                "indexedCount": self.indexed_count,
                "skipCount": self.skip_count,
                "errorCount": self.error_count,
            },
            "skipBreakdown": [{"code": code, "count": count} for code, count in sorted(self.skip_breakdown.items())],
        }


class FullScanState:
    def __init__(self) -> None:
        self._lock = Lock()
        self._jobs: dict[str, FullScanJobRecord] = {}
        self._active_job_id: str | None = None

    def create_job(
        self,
        workspace_path: str,
        max_file_size_bytes: int,
        *,
        max_traversal_depth: int | None = None,
        max_files_per_run: int | None = None,
    ) -> FullScanJobRecord:
        with self._lock:
            if self._active_job_id and self._jobs[self._active_job_id].status in {"queued", "running"}:
                raise RuntimeError("FULL_SCAN_ALREADY_RUNNING")
            job = FullScanJobRecord(
                job_id=uuid4().hex,
                workspace_path=workspace_path,
                max_file_size_bytes=max_file_size_bytes,
                max_traversal_depth=max_traversal_depth,
                max_files_per_run=max_files_per_run,
            )
            job.status = "running"
            job.started_at = _now_iso()
            job.last_event_at = _now_iso()
            self._jobs[job.job_id] = job
            self._active_job_id = job.job_id
            return job

    def get_job(self, job_id: str) -> FullScanJobRecord | None:
        with self._lock:
            return self._jobs.get(job_id)

    def update_job(
        self,
        job_id: str,
        *,
        processed_delta: int = 0,
        indexed_delta: int = 0,
        skip_delta: int = 0,
        error_delta: int = 0,
        skip_reason: str | None = None,
        percent_complete: float | None = None,
    ) -> FullScanJobRecord | None:
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return None
            job.processed_count += processed_delta
            job.indexed_count += indexed_delta
            job.skip_count += skip_delta
            job.error_count += error_delta
            if skip_reason:
                job.skip_breakdown[skip_reason] = job.skip_breakdown.get(skip_reason, 0) + 1
            if percent_complete is not None:
                job.percent_complete = percent_complete
            job.last_event_at = _now_iso()
            return job

    def finish_job(self, job_id: str, result: str) -> FullScanJobRecord | None:
        with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return None
            job.status = result
            job.finished_at = _now_iso()
            job.last_event_at = job.finished_at
            if self._active_job_id == job_id:
                self._active_job_id = None
            return job


STATE = FullScanState()

