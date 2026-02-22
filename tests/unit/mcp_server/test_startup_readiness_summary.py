from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from startup_preflight_models import StartupCheckResult  # noqa: E402
from startup_readiness_summary import build_startup_readiness_summary  # noqa: E402


def test_build_startup_readiness_summary_contains_required_fields():
    context = {
        "workspacePath": "/workspace",
        "indexMode": "full-scan",
        "mcpEndpointPath": "/mcp",
        "collectionName": "workspace_chunks",
    }
    checks = [
        StartupCheckResult(
            check_id="qdrant_reachability",
            status="passed",
            severity="critical",
            message="Qdrant available",
        ),
        StartupCheckResult(
            check_id="workspace_readable",
            status="passed",
            severity="critical",
            message="Workspace readable",
        ),
    ]

    payload = build_startup_readiness_summary(
        context=context,
        checks=checks,
        service_readiness={"qdrant": "healthy", "fileIndexer": "healthy", "mcpServer": "healthy"},
    )

    assert payload["status"] == "ready"
    assert payload["workspacePath"] == "/workspace"
    assert payload["indexMode"] == "full-scan"
    assert payload["mcpEndpoint"] == "/mcp"
    assert payload["collectionName"] == "workspace_chunks"
    assert len(payload["preflightChecks"]) == 2

