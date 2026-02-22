from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from mcp_transport.error_mapper import McpToolExecutionError, build_jsonrpc_error  # noqa: E402
from mcp_transport.protocol_models import MethodNotFoundError  # noqa: E402
from search_errors import SearchApiError  # noqa: E402


def test_build_jsonrpc_error_from_protocol_error():
    payload, status = build_jsonrpc_error(1, MethodNotFoundError("unknown/method"))

    assert status == 404
    assert payload["error"]["code"] == -32601
    assert payload["error"]["data"]["errorCode"] == "METHOD_NOT_SUPPORTED"


def test_build_jsonrpc_error_from_tool_execution_error():
    payload, status = build_jsonrpc_error(
        2,
        McpToolExecutionError(
            error_code="RUN_NOT_FOUND",
            message="run not found",
            details="no run",
            retryable=False,
            jsonrpc_code=-32004,
            http_status=404,
        ),
    )

    assert status == 404
    assert payload["error"]["code"] == -32004
    assert payload["error"]["data"]["errorCode"] == "RUN_NOT_FOUND"


def test_build_jsonrpc_error_from_search_error():
    payload, status = build_jsonrpc_error(
        3,
        SearchApiError("SEARCH_BACKEND_ERROR", "backend unavailable", 502, "qdrant timeout"),
    )

    assert status == 502
    assert payload["error"]["code"] == -32010
    assert payload["error"]["data"]["errorCode"] == "SEARCH_BACKEND_ERROR"

