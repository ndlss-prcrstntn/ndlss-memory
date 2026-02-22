from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from startup_preflight_state import STATE as STARTUP_PREFLIGHT_STATE  # noqa: E402
from system_status_handler import app  # noqa: E402


def test_readiness_endpoint_returns_not_ready_when_state_is_empty():
    STARTUP_PREFLIGHT_STATE.reset()
    client = app.test_client()

    response = client.get("/v1/system/startup/readiness")

    assert response.status_code == 503
    payload = response.get_json()
    assert payload["errorCode"] == "STARTUP_NOT_READY"
    assert isinstance(payload["failedChecks"], list)


def test_readiness_endpoint_returns_ready_payload_when_state_is_ready():
    STARTUP_PREFLIGHT_STATE.reset()
    STARTUP_PREFLIGHT_STATE.mark_ready(
        {
            "status": "ready",
            "workspacePath": "/workspace",
            "indexMode": "full-scan",
            "mcpEndpoint": "/mcp",
            "collectionName": "workspace_chunks",
            "serviceReadiness": {"qdrant": "healthy", "fileIndexer": "healthy", "mcpServer": "healthy"},
            "preflightChecks": [],
            "checkedAt": "2026-02-22T00:00:00+00:00",
        }
    )
    client = app.test_client()

    response = client.get("/v1/system/startup/readiness")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ready"

