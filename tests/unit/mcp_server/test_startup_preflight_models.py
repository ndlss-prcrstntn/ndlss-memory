from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from startup_preflight_models import StartupCheckResult, StartupReadinessSummary  # noqa: E402
from startup_preflight_state import StartupPreflightState  # noqa: E402


def test_startup_check_result_to_dict_includes_optional_fields():
    check = StartupCheckResult(
        check_id="qdrant_reachability",
        status="failed",
        severity="critical",
        message="Qdrant is unreachable",
        error_code="PREFLIGHT_QDRANT_UNREACHABLE",
        details={"url": "http://qdrant:6333/collections"},
        action="Check Qdrant container",
    )

    payload = check.to_dict()

    assert payload["checkId"] == "qdrant_reachability"
    assert payload["status"] == "failed"
    assert payload["severity"] == "critical"
    assert payload["errorCode"] == "PREFLIGHT_QDRANT_UNREACHABLE"
    assert payload["details"]["url"].endswith("/collections")
    assert payload["action"] == "Check Qdrant container"


def test_readiness_summary_to_dict_contains_required_keys():
    summary = StartupReadinessSummary(
        service_readiness={"qdrant": "healthy", "fileIndexer": "healthy", "mcpServer": "healthy"},
        workspace_path="/workspace",
        index_mode="full-scan",
        mcp_endpoint="/mcp",
        collection_name="workspace_chunks",
        preflight_checks=[
            StartupCheckResult(
                check_id="workspace_readable",
                status="passed",
                severity="critical",
                message="workspace is readable",
            )
        ],
    )

    payload = summary.to_dict()

    assert payload["status"] == "ready"
    assert payload["workspacePath"] == "/workspace"
    assert payload["indexMode"] == "full-scan"
    assert payload["mcpEndpoint"] == "/mcp"
    assert payload["collectionName"] == "workspace_chunks"
    assert len(payload["preflightChecks"]) == 1


def test_startup_preflight_state_roundtrip():
    state = StartupPreflightState()
    ready_payload = {"status": "ready", "workspacePath": "/workspace"}
    failure_payload = {"errorCode": "STARTUP_PREFLIGHT_FAILED", "message": "failed"}

    state.mark_ready(ready_payload)
    assert state.get_readiness_summary() == ready_payload
    assert state.get_failure_report() is None

    state.mark_failed(failure_payload)
    assert state.get_failure_report() == failure_payload
    assert state.get_readiness_summary() is None

    state.reset()
    assert state.get_failure_report() is None
    assert state.get_readiness_summary() is None

