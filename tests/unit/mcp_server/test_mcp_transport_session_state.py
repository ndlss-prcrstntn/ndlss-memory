from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from mcp_transport.session_state import McpSessionStore  # noqa: E402


def test_session_store_create_and_mark_initialized():
    store = McpSessionStore()

    created = store.create_session(transport="sse")
    assert created.initialized is False
    assert store.get_session(created.session_id) is not None

    updated = store.mark_initialized(created.session_id, client_info={"name": "client"})
    assert updated is not None
    assert updated.initialized is True
    assert updated.client_info == {"name": "client"}


def test_session_store_ensure_and_enqueue_response():
    store = McpSessionStore()

    session = store.ensure_session("shared-session", transport="streamable-http")
    assert session.session_id == "shared-session"
    assert session.transport == "streamable-http"

    store.enqueue_response("shared-session", {"jsonrpc": "2.0", "id": 1, "result": {"ok": True}})
    current = store.get_session("shared-session")
    assert current is not None
    assert len(current.queued_responses) == 1

