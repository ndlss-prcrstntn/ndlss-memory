from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class StartupCheckResult:
    check_id: str
    status: str
    severity: str
    message: str
    error_code: str | None = None
    details: dict[str, Any] = field(default_factory=dict)
    action: str | None = None
    checked_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "checkId": self.check_id,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "checkedAt": self.checked_at,
        }
        if self.error_code:
            payload["errorCode"] = self.error_code
        if self.details:
            payload["details"] = self.details
        if self.action:
            payload["action"] = self.action
        return payload


@dataclass
class StartupReadinessSummary:
    service_readiness: dict[str, str]
    workspace_path: str
    index_mode: str
    mcp_endpoint: str
    collection_name: str
    preflight_checks: list[StartupCheckResult]
    status: str = "ready"
    collection: dict[str, Any] | None = None
    bootstrap: dict[str, Any] | None = None
    bootstrap_failure: dict[str, Any] | None = None
    checked_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "status": self.status,
            "serviceReadiness": self.service_readiness,
            "workspacePath": self.workspace_path,
            "indexMode": self.index_mode,
            "mcpEndpoint": self.mcp_endpoint,
            "collectionName": self.collection_name,
            "preflightChecks": [check.to_dict() for check in self.preflight_checks],
            "checkedAt": self.checked_at,
        }
        if self.collection is not None:
            payload["collection"] = self.collection
        if self.bootstrap is not None:
            payload["bootstrap"] = self.bootstrap
        if self.bootstrap_failure is not None:
            payload["bootstrapFailure"] = self.bootstrap_failure
        return payload

