from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

import system_status_handler as handler  # noqa: E402
from startup_preflight_models import StartupCheckResult  # noqa: E402
from startup_preflight_state import STATE as STARTUP_PREFLIGHT_STATE  # noqa: E402


class _FailingBootstrapOrchestrator:
    def get_bootstrap_payload(self, _workspace_path: str) -> dict:
        return {
            "trigger": "auto-startup",
            "decision": "retry-failed",
            "status": "failed",
            "workspaceKey": "workspace-key",
            "checkedAt": "2026-02-22T00:00:00+00:00",
            "errorCode": "BOOTSTRAP_COLLECTION_UNAVAILABLE",
            "reason": "Qdrant collection request failed with HTTP 500",
        }

    def get_collection_payload(self) -> dict:
        return {
            "collectionName": "workspace_chunks",
            "exists": False,
            "pointCount": 0,
            "checkedAt": "2026-02-22T00:00:00+00:00",
        }


def test_bootstrap_failure_is_visible_in_readiness(monkeypatch):
    STARTUP_PREFLIGHT_STATE.reset()
    handler.STARTUP_PREFLIGHT_CONTEXT = {
        "workspacePath": "/workspace",
        "indexMode": "full-scan",
        "mcpEndpointPath": "/mcp",
        "collectionName": "workspace_chunks",
    }
    handler.STARTUP_PREFLIGHT_CHECKS = [
        StartupCheckResult(
            check_id="qdrant_reachability",
            status="passed",
            severity="critical",
            message="Qdrant available",
        )
    ]
    monkeypatch.setattr(handler, "BOOTSTRAP_ORCHESTRATOR", _FailingBootstrapOrchestrator())

    handler._update_startup_readiness_with_bootstrap()
    client = handler.app.test_client()
    response = client.get("/v1/system/startup/readiness")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "failed"
    assert payload["bootstrap"]["decision"] == "retry-failed"
    assert payload["bootstrapFailure"]["errorCode"] == "BOOTSTRAP_COLLECTION_UNAVAILABLE"
    assert payload["bootstrapFailure"]["recommendedActions"]
