from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_workspace_key(workspace_path: str) -> str:
    normalized = str(Path(workspace_path).as_posix()).strip().lower()
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]
    return f"{normalized}|{digest}"


@dataclass
class BootstrapStateRecord:
    workspace_key: str
    collection_name: str
    status: str
    trigger: str = "auto-startup"
    attempt: int = 1
    last_run_id: str | None = None
    started_at: str | None = None
    finished_at: str | None = None
    error_code: str | None = None
    error_message: str | None = None
    created_collection: bool = False
    point_count_after_run: int = 0
    updated_at: str = field(default_factory=now_iso)

    def to_payload(self) -> dict[str, Any]:
        return {
            "workspaceKey": self.workspace_key,
            "collectionName": self.collection_name,
            "status": self.status,
            "trigger": self.trigger,
            "attempt": self.attempt,
            "lastRunId": self.last_run_id,
            "startedAt": self.started_at,
            "finishedAt": self.finished_at,
            "errorCode": self.error_code,
            "errorMessage": self.error_message,
            "createdCollection": self.created_collection,
            "pointCountAfterRun": self.point_count_after_run,
            "updatedAt": self.updated_at,
        }

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "BootstrapStateRecord":
        return cls(
            workspace_key=str(payload.get("workspaceKey") or ""),
            collection_name=str(payload.get("collectionName") or "workspace_chunks"),
            status=str(payload.get("status") or "pending"),
            trigger=str(payload.get("trigger") or "auto-startup"),
            attempt=int(payload.get("attempt") or 1),
            last_run_id=payload.get("lastRunId"),
            started_at=payload.get("startedAt"),
            finished_at=payload.get("finishedAt"),
            error_code=payload.get("errorCode"),
            error_message=payload.get("errorMessage"),
            created_collection=bool(payload.get("createdCollection") or False),
            point_count_after_run=int(payload.get("pointCountAfterRun") or 0),
            updated_at=str(payload.get("updatedAt") or now_iso()),
        )


@dataclass
class BootstrapRuntimeSnapshot:
    workspace_key: str
    trigger: str
    decision: str
    status: str
    reason: str | None = None
    error_code: str | None = None
    run_id: str | None = None
    collection_name: str = "workspace_chunks"
    checked_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "trigger": self.trigger,
            "decision": self.decision,
            "status": self.status,
            "workspaceKey": self.workspace_key,
            "collectionName": self.collection_name,
            "checkedAt": self.checked_at,
        }
        if self.run_id:
            payload["runId"] = self.run_id
        if self.reason:
            payload["reason"] = self.reason
        if self.error_code:
            payload["errorCode"] = self.error_code
        return payload


class BootstrapRuntimeState:
    def __init__(self) -> None:
        self._lock = Lock()
        self._workspace_snapshot: dict[str, BootstrapRuntimeSnapshot] = {}
        self._run_workspace_map: dict[str, str] = {}

    def set_snapshot(self, snapshot: BootstrapRuntimeSnapshot) -> None:
        with self._lock:
            self._workspace_snapshot[snapshot.workspace_key] = snapshot
            if snapshot.run_id:
                self._run_workspace_map[snapshot.run_id] = snapshot.workspace_key

    def get_snapshot(self, workspace_key: str) -> BootstrapRuntimeSnapshot | None:
        with self._lock:
            return self._workspace_snapshot.get(workspace_key)

    def bind_run(self, run_id: str, workspace_key: str) -> None:
        with self._lock:
            self._run_workspace_map[run_id] = workspace_key

    def workspace_for_run(self, run_id: str) -> str | None:
        with self._lock:
            return self._run_workspace_map.get(run_id)

    def reset(self) -> None:
        with self._lock:
            self._workspace_snapshot = {}
            self._run_workspace_map = {}


RUNTIME_STATE = BootstrapRuntimeState()
