from __future__ import annotations

from dataclasses import dataclass
from typing import Any

JSON_RPC_VERSION = "2.0"
JSON_RPC_PARSE_ERROR = -32700
JSON_RPC_INVALID_REQUEST = -32600
JSON_RPC_METHOD_NOT_FOUND = -32601
JSON_RPC_INVALID_PARAMS = -32602
JSON_RPC_INTERNAL_ERROR = -32603

METHOD_INITIALIZE = "initialize"
METHOD_NOTIFICATIONS_INITIALIZED = "notifications/initialized"
METHOD_PING = "ping"
METHOD_TOOLS_LIST = "tools/list"
METHOD_TOOLS_CALL = "tools/call"

SUPPORTED_METHODS = {
    METHOD_INITIALIZE,
    METHOD_NOTIFICATIONS_INITIALIZED,
    METHOD_PING,
    METHOD_TOOLS_LIST,
    METHOD_TOOLS_CALL,
}


class ProtocolError(RuntimeError):
    def __init__(
        self,
        *,
        code: int,
        message: str,
        data: dict[str, Any] | None = None,
        http_status: int = 400,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.data = data or {}
        self.http_status = http_status


class ParseError(ProtocolError):
    def __init__(self, message: str = "Malformed JSON payload") -> None:
        super().__init__(code=JSON_RPC_PARSE_ERROR, message=message, data={"errorCode": "PARSE_ERROR"}, http_status=400)


class InvalidRequestError(ProtocolError):
    def __init__(self, message: str, data: dict[str, Any] | None = None) -> None:
        super().__init__(code=JSON_RPC_INVALID_REQUEST, message=message, data=data, http_status=400)


class MethodNotFoundError(ProtocolError):
    def __init__(self, method: str) -> None:
        super().__init__(
            code=JSON_RPC_METHOD_NOT_FOUND,
            message=f"Method '{method}' is not supported",
            data={"method": method, "errorCode": "METHOD_NOT_SUPPORTED"},
            http_status=404,
        )


class InvalidParamsError(ProtocolError):
    def __init__(self, message: str, data: dict[str, Any] | None = None) -> None:
        super().__init__(code=JSON_RPC_INVALID_PARAMS, message=message, data=data, http_status=400)


@dataclass(frozen=True)
class JsonRpcRequest:
    method: str
    params: dict[str, Any]
    request_id: str | int | None
    has_id: bool

    @classmethod
    def from_payload(cls, payload: Any) -> "JsonRpcRequest":
        if not isinstance(payload, dict):
            raise InvalidRequestError("JSON-RPC request must be an object")

        jsonrpc = payload.get("jsonrpc")
        if jsonrpc != JSON_RPC_VERSION:
            raise InvalidRequestError("jsonrpc must equal '2.0'")

        method = payload.get("method")
        if not isinstance(method, str) or not method.strip():
            raise InvalidRequestError("method must be a non-empty string")

        params = payload.get("params", {})
        if params is None:
            params = {}
        if not isinstance(params, dict):
            raise InvalidParamsError("params must be an object")

        has_id = "id" in payload
        request_id = payload.get("id")
        if has_id and request_id is not None and not isinstance(request_id, (str, int)):
            raise InvalidRequestError("id must be string, integer or null")

        return cls(
            method=method.strip(),
            params=params,
            request_id=request_id if has_id else None,
            has_id=has_id,
        )


def build_success_response(request_id: str | int | None, result: dict[str, Any]) -> dict[str, Any]:
    return {
        "jsonrpc": JSON_RPC_VERSION,
        "id": request_id,
        "result": result,
    }


def build_error_response(
    request_id: str | int | None,
    *,
    code: int,
    message: str,
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "jsonrpc": JSON_RPC_VERSION,
        "id": request_id,
        "error": {
            "code": code,
            "message": message,
        },
    }
    if data:
        payload["error"]["data"] = data
    return payload
