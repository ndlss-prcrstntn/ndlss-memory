from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from system_status_handler import app  # noqa: E402


def test_mcp_initialize_and_ping_flow():
    client = app.test_client()
    session_id = "session-init-ping"

    initialize_response = client.post(
        "/mcp",
        headers={"X-MCP-Session-Id": session_id},
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"clientInfo": {"name": "pytest", "version": "1.0.0"}},
        },
    )
    assert initialize_response.status_code == 200
    initialize_payload = initialize_response.get_json()
    assert initialize_payload["result"]["protocolVersion"]

    initialized_response = client.post(
        "/mcp",
        headers={"X-MCP-Session-Id": session_id},
        json={"jsonrpc": "2.0", "id": 2, "method": "notifications/initialized", "params": {}},
    )
    assert initialized_response.status_code == 200
    assert initialized_response.get_json()["result"]["acknowledged"] is True

    ping_response = client.post(
        "/mcp",
        headers={"X-MCP-Session-Id": session_id},
        json={"jsonrpc": "2.0", "id": 3, "method": "ping", "params": {}},
    )
    assert ping_response.status_code == 200
    assert ping_response.get_json()["result"]["pong"] is True


def test_tools_list_requires_initialized_session():
    client = app.test_client()

    response = client.post(
        "/mcp",
        headers={"X-MCP-Session-Id": "session-tools-without-init"},
        json={"jsonrpc": "2.0", "id": 10, "method": "tools/list", "params": {}},
    )

    assert response.status_code == 409
    payload = response.get_json()
    assert payload["error"]["data"]["errorCode"] == "SESSION_NOT_INITIALIZED"


def test_discovery_and_sse_endpoints_are_available():
    client = app.test_client()

    discovery = client.get("/.well-known/mcp")
    assert discovery.status_code == 200
    discovery_payload = discovery.get_json()
    transport_urls = {item["url"] for item in discovery_payload["transports"]}
    assert any(url.endswith("/mcp") for url in transport_urls)
    assert any(url.endswith("/sse") for url in transport_urls)

    sse = client.get("/sse")
    assert sse.status_code == 200
    assert "text/event-stream" in sse.headers["Content-Type"]
    assert sse.headers.get("X-MCP-Session-Id")


def test_sse_messages_require_existing_session():
    client = app.test_client()

    response = client.post(
        "/messages?sessionId=missing-session",
        json={"jsonrpc": "2.0", "id": 5, "method": "ping", "params": {}},
    )

    assert response.status_code == 404
    payload = response.get_json()
    assert payload["error"]["data"]["errorCode"] == "SESSION_NOT_FOUND"

