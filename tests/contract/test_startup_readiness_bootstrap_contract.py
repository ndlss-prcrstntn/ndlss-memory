from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from startup_preflight_state import STATE as STARTUP_PREFLIGHT_STATE  # noqa: E402
from system_status_handler import app  # noqa: E402


def test_startup_readiness_contains_bootstrap_contract_fields():
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
            "bootstrap": {
                "trigger": "auto-startup",
                "decision": "run",
                "status": "running",
                "workspaceKey": "/workspace|key",
                "checkedAt": "2026-02-22T00:00:00+00:00",
            },
            "collection": {
                "collectionName": "workspace_chunks",
                "exists": True,
                "pointCount": 0,
                "checkedAt": "2026-02-22T00:00:00+00:00",
            },
            "checkedAt": "2026-02-22T00:00:00+00:00",
        }
    )
    client = app.test_client()

    response = client.get("/v1/system/startup/readiness")

    assert response.status_code == 200
    payload = response.get_json()
    assert "bootstrap" in payload
    assert "collection" in payload
    assert payload["bootstrap"]["trigger"] in {"auto-startup", "manual"}
    assert payload["bootstrap"]["decision"] in {"run", "skip-already-completed", "retry-failed"}
    assert isinstance(payload["collection"]["pointCount"], int)
