from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from mcp_transport.protocol_models import (  # noqa: E402
    InvalidParamsError,
    InvalidRequestError,
    JsonRpcRequest,
    build_error_response,
    build_success_response,
)


def test_jsonrpc_request_from_payload_parses_valid_envelope():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "ping",
        "params": {},
    }

    parsed = JsonRpcRequest.from_payload(payload)

    assert parsed.method == "ping"
    assert parsed.request_id == 1
    assert parsed.has_id is True


def test_jsonrpc_request_requires_jsonrpc_version():
    with pytest.raises(InvalidRequestError):
        JsonRpcRequest.from_payload({"method": "ping", "params": {}})


def test_jsonrpc_request_requires_object_params():
    with pytest.raises(InvalidParamsError):
        JsonRpcRequest.from_payload({"jsonrpc": "2.0", "method": "ping", "params": []})


def test_jsonrpc_response_builders_return_expected_shape():
    success = build_success_response(5, {"pong": True})
    error = build_error_response(5, code=-32601, message="unknown", data={"errorCode": "METHOD_NOT_SUPPORTED"})

    assert success["jsonrpc"] == "2.0"
    assert success["id"] == 5
    assert success["result"]["pong"] is True

    assert error["jsonrpc"] == "2.0"
    assert error["id"] == 5
    assert error["error"]["code"] == -32601
    assert error["error"]["data"]["errorCode"] == "METHOD_NOT_SUPPORTED"

