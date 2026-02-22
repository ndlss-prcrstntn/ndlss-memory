from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

import system_status_handler as handler  # noqa: E402


def test_watch_status_contract_fields(monkeypatch):
    monkeypatch.setenv("INDEX_MODE", "watch")
    handler.WATCH_STATE.start("/workspace")
    handler.WATCH_STATE.set_state("running")
    handler.WATCH_STATE.heartbeat()

    client = handler.app.test_client()
    response = client.get("/v1/indexing/watch/status")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["mode"] == "watch"
    assert payload["state"] in {"starting", "running", "recovering", "failed", "stopped"}
    assert isinstance(payload["queueDepth"], int)
    assert isinstance(payload["processedEvents"], int)
    assert isinstance(payload["failedEvents"], int)
    assert isinstance(payload["retryCount"], int)
