from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

WatchEventType = Literal["created", "updated", "deleted", "renamed"]
WatchEventStatus = Literal["queued", "processing", "completed", "failed", "skipped"]
WatchRunStatus = Literal["starting", "running", "recovering", "failed", "stopped"]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class WatchEvent:
    event_type: WatchEventType
    path: str
    old_path: str | None = None
    event_id: str = field(default_factory=lambda: uuid4().hex)
    detected_at: str = field(default_factory=now_iso)
    coalesced_at: str | None = None
    status: WatchEventStatus = "queued"
    error_code: str | None = None
    error_message: str | None = None

    def to_payload(self) -> dict[str, Any]:
        payload = {
            "eventId": self.event_id,
            "eventType": self.event_type,
            "path": self.path,
            "detectedAt": self.detected_at,
            "coalescedAt": self.coalesced_at,
            "status": self.status,
        }
        if self.old_path:
            payload["oldPath"] = self.old_path
        if self.error_code:
            payload["errorCode"] = self.error_code
        if self.error_message:
            payload["errorMessage"] = self.error_message
        return payload


@dataclass
class WatchRunStateSnapshot:
    mode: str = "watch"
    state: WatchRunStatus = "starting"
    workspace_path: str = "/workspace"
    started_at: str = field(default_factory=now_iso)
    last_heartbeat_at: str = field(default_factory=now_iso)
    last_event_at: str | None = None
    queue_depth: int = 0
    processed_events: int = 0
    failed_events: int = 0
    retry_count: int = 0
    last_error_code: str | None = None
    last_error_message: str | None = None
    backoff_seconds: float = 0.0

    def to_payload(self) -> dict[str, Any]:
        payload = {
            "mode": self.mode,
            "state": self.state,
            "workspacePath": self.workspace_path,
            "startedAt": self.started_at,
            "lastHeartbeatAt": self.last_heartbeat_at,
            "queueDepth": self.queue_depth,
            "processedEvents": self.processed_events,
            "failedEvents": self.failed_events,
            "retryCount": self.retry_count,
            "backoffSeconds": self.backoff_seconds,
        }
        if self.last_event_at:
            payload["lastEventAt"] = self.last_event_at
        if self.last_error_code:
            payload["lastErrorCode"] = self.last_error_code
        if self.last_error_message:
            payload["lastErrorMessage"] = self.last_error_message
        return payload


@dataclass
class IncrementalIndexResult:
    affected_files: list[str]
    indexed_files: int
    deleted_records: int
    skipped_files: int
    failed_files: int
    reason_breakdown: dict[str, int] = field(default_factory=dict)
    status: Literal["completed", "partial", "failed"] = "completed"
    summary_id: str = field(default_factory=lambda: uuid4().hex)
    window_started_at: str = field(default_factory=now_iso)
    window_finished_at: str | None = None

    def finalize(self) -> None:
        if self.window_finished_at is None:
            self.window_finished_at = now_iso()
        if self.failed_files > 0 and self.indexed_files == 0 and self.deleted_records == 0:
            self.status = "failed"
        elif self.failed_files > 0:
            self.status = "partial"
        else:
            self.status = "completed"

    def to_payload(self) -> dict[str, Any]:
        self.finalize()
        payload = {
            "summaryId": self.summary_id,
            "status": self.status,
            "windowStartedAt": self.window_started_at,
            "windowFinishedAt": self.window_finished_at,
            "affectedFiles": list(self.affected_files),
            "indexedFiles": self.indexed_files,
            "deletedRecords": self.deleted_records,
            "skippedFiles": self.skipped_files,
            "failedFiles": self.failed_files,
            "generatedAt": now_iso(),
        }
        if self.reason_breakdown:
            payload["reasonBreakdown"] = [
                {"code": code, "count": count}
                for code, count in sorted(self.reason_breakdown.items())
                if count > 0
            ]
        return payload
