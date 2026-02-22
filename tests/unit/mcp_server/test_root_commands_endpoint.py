from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from system_status_handler import app


def test_root_endpoint_returns_commands_catalog():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["service"] == "ndlss-memory-mcp-server"
    assert payload["status"] == "ok"
    assert isinstance(payload.get("commands"), list)
    assert payload["commands"]


def test_root_endpoint_catalog_contains_core_paths():
    client = app.test_client()

    response = client.get("/")
    payload = response.get_json()
    paths = {item["path"] for item in payload["commands"]}

    assert "/health" in paths
    assert "/v1/search/semantic" in paths
    assert "/v1/indexing/ingestion/jobs" in paths
    assert "/v1/commands/execute" in paths
