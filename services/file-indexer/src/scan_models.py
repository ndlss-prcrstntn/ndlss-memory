from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ScanJob:
    job_id: str
    mode: str = "full-scan"
    workspace_path: str = "/workspace"
    status: str = "queued"
    started_at: str | None = None
    finished_at: str | None = None
    duration_seconds: float | None = None
    processed_count: int = 0
    indexed_count: int = 0
    skip_count: int = 0
    error_count: int = 0
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return {
            "jobId": self.job_id,
            "mode": self.mode,
            "workspacePath": self.workspace_path,
            "status": self.status,
            "startedAt": self.started_at,
            "finishedAt": self.finished_at,
            "durationSeconds": self.duration_seconds,
            "processedCount": self.processed_count,
            "indexedCount": self.indexed_count,
            "skipCount": self.skip_count,
            "errorCount": self.error_count,
            "createdAt": self.created_at,
        }


@dataclass
class ScanProgress:
    job_id: str
    status: str
    processed_count: int
    indexed_count: int
    skip_count: int
    error_count: int
    last_event_at: str = field(default_factory=now_iso)
    percent_complete: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "jobId": self.job_id,
            "status": self.status,
            "processedCount": self.processed_count,
            "indexedCount": self.indexed_count,
            "skipCount": self.skip_count,
            "errorCount": self.error_count,
            "lastEventAt": self.last_event_at,
            "percentComplete": self.percent_complete,
        }


@dataclass
class ScanSummary:
    job_id: str
    result: str
    duration_seconds: float
    processed_count: int
    indexed_count: int
    skip_count: int
    error_count: int
    applied_limits: dict[str, int | None]
    skip_breakdown: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "jobId": self.job_id,
            "result": self.result,
            "durationSeconds": self.duration_seconds,
            "totals": {
                "processedCount": self.processed_count,
                "indexedCount": self.indexed_count,
                "skipCount": self.skip_count,
                "errorCount": self.error_count,
            },
            "appliedLimits": self.applied_limits,
            "skipBreakdown": self.skip_breakdown,
        }

