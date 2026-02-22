from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

import system_status_handler as handler  # noqa: E402


def test_full_scan_mode_keeps_watch_endpoints_disabled(monkeypatch):
    monkeypatch.setenv("INDEX_MODE", "full-scan")
    client = handler.app.test_client()

    watch_status = client.get("/v1/indexing/watch/status")
    runtime_config = client.get("/v1/system/config")

    assert watch_status.status_code == 503
    assert runtime_config.status_code == 200
    assert runtime_config.get_json()["indexMode"] == "full-scan"


def test_delta_mode_keeps_watch_endpoints_disabled(monkeypatch):
    monkeypatch.setenv("INDEX_MODE", "delta-after-commit")
    client = handler.app.test_client()

    watch_summary = client.get("/v1/indexing/watch/summary")
    runtime_config = client.get("/v1/system/config")

    assert watch_summary.status_code == 503
    assert runtime_config.status_code == 200
    assert runtime_config.get_json()["indexMode"] == "delta-after-commit"
