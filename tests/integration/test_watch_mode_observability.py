from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

import system_status_handler as handler  # noqa: E402
from watch_mode_models import IncrementalIndexResult  # noqa: E402


def test_watch_observability_endpoints_return_status_and_summary(monkeypatch):
    monkeypatch.setenv("INDEX_MODE", "watch")
    handler.WATCH_STATE.start("/workspace")
    handler.WATCH_STATE.set_state("recovering")
    handler.WATCH_STATE.record_retry(error_code="WATCH_RUNTIME_ERROR", error_message="temporary", recoverable=True)
    handler.WATCH_STATE.mark_processed(processed=3, failed=1)
    handler.WATCH_STATE.set_last_summary(
        IncrementalIndexResult(
            affected_files=["docs/a.md", "docs/b.md"],
            indexed_files=2,
            deleted_records=1,
            skipped_files=0,
            failed_files=0,
        )
    )

    client = handler.app.test_client()
    status_response = client.get("/v1/indexing/watch/status")
    summary_response = client.get("/v1/indexing/watch/summary")

    assert status_response.status_code == 200
    status_payload = status_response.get_json()
    assert status_payload["state"] in {"recovering", "running"}
    assert status_payload["processedEvents"] >= 3
    assert status_payload["failedEvents"] >= 1

    assert summary_response.status_code == 200
    summary_payload = summary_response.get_json()
    assert summary_payload["indexedFiles"] == 2
    assert summary_payload["deletedRecords"] == 1
