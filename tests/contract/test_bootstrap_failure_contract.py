from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

import system_status_handler as handler  # noqa: E402
from startup_preflight_state import STATE as STARTUP_PREFLIGHT_STATE  # noqa: E402


def test_startup_readiness_failure_contract_contains_bootstrap_failure_block():
    STARTUP_PREFLIGHT_STATE.reset()
    STARTUP_PREFLIGHT_STATE.mark_ready(
        {
            "status": "failed",
            "workspacePath": "/workspace",
            "indexMode": "full-scan",
            "mcpEndpoint": "/mcp",
            "collectionName": "workspace_chunks",
            "serviceReadiness": {"qdrant": "healthy", "fileIndexer": "healthy", "mcpServer": "healthy"},
            "preflightChecks": [],
            "bootstrap": {
                "trigger": "auto-startup",
                "decision": "retry-failed",
                "status": "failed",
                "workspaceKey": "workspace-key",
                "checkedAt": "2026-02-22T00:00:00+00:00",
                "errorCode": "BOOTSTRAP_COLLECTION_UNAVAILABLE",
                "reason": "collection creation failed",
            },
            "collection": {
                "collectionName": "workspace_chunks",
                "exists": False,
                "pointCount": 0,
                "checkedAt": "2026-02-22T00:00:00+00:00",
            },
            "bootstrapFailure": {
                "errorCode": "BOOTSTRAP_COLLECTION_UNAVAILABLE",
                "message": "collection creation failed",
                "details": {"workspacePath": "/workspace", "collectionName": "workspace_chunks"},
                "recommendedActions": ["retry later"],
            },
            "checkedAt": "2026-02-22T00:00:00+00:00",
        }
    )

    client = handler.app.test_client()
    response = client.get("/v1/system/startup/readiness")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "failed"
    assert "bootstrapFailure" in payload
    assert payload["bootstrapFailure"]["errorCode"] == "BOOTSTRAP_COLLECTION_UNAVAILABLE"
    assert isinstance(payload["bootstrapFailure"]["recommendedActions"], list)
