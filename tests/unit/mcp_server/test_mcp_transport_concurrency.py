from pathlib import Path
import sys
import threading

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from mcp_transport.session_state import McpSessionStore  # noqa: E402


def test_session_store_handles_parallel_updates():
    store = McpSessionStore()
    failures: list[str] = []

    def worker(index: int) -> None:
        try:
            session_id = f"session-{index}"
            store.ensure_session(session_id, transport="streamable-http")
            store.mark_initialized(session_id, client_info={"worker": index})
            store.enqueue_response(session_id, {"jsonrpc": "2.0", "id": index, "result": {"ok": True}})
        except Exception as exc:  # pragma: no cover
            failures.append(str(exc))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(20)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert failures == []
    for i in range(20):
        session = store.get_session(f"session-{i}")
        assert session is not None
        assert session.initialized is True
        assert len(session.queued_responses) == 1

