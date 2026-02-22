from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

import system_status_handler as handler  # noqa: E402
from watch_mode_models import IncrementalIndexResult  # noqa: E402


def test_watch_summary_contract_fields(monkeypatch):
    monkeypatch.setenv("INDEX_MODE", "watch")
    handler.WATCH_STATE.start("/workspace")
    handler.WATCH_STATE.set_state("running")
    summary = IncrementalIndexResult(
        affected_files=["docs/a.md"],
        indexed_files=1,
        deleted_records=0,
        skipped_files=0,
        failed_files=0,
    )
    handler.WATCH_STATE.set_last_summary(summary)

    client = handler.app.test_client()
    response = client.get("/v1/indexing/watch/summary")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] in {"completed", "partial", "failed"}
    assert isinstance(payload["affectedFiles"], list)
    assert isinstance(payload["indexedFiles"], int)
    assert isinstance(payload["deletedRecords"], int)
    assert isinstance(payload["skippedFiles"], int)
    assert isinstance(payload["failedFiles"], int)
