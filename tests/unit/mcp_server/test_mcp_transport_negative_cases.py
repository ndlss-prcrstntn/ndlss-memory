from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from system_status_handler import app  # noqa: E402


def test_mcp_rejects_non_json_payload():
    client = app.test_client()

    response = client.post("/mcp", data="not json", content_type="text/plain")

    assert response.status_code == 400
    payload = response.get_json()
    assert payload["error"]["code"] == -32700


def test_mcp_returns_method_not_found_for_unknown_method():
    client = app.test_client()

    response = client.post(
        "/mcp",
        headers={"X-MCP-Session-Id": "session-unknown-method"},
        json={"jsonrpc": "2.0", "id": 99, "method": "unknown/method", "params": {}},
    )

    assert response.status_code == 404
    payload = response.get_json()
    assert payload["error"]["code"] == -32601


def test_mcp_rejects_malformed_envelope():
    client = app.test_client()

    response = client.post("/mcp", json={"id": 1, "method": "ping"})

    assert response.status_code == 400
    payload = response.get_json()
    assert payload["error"]["code"] == -32600

