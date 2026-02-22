from __future__ import annotations

from typing import Any

from mcp_transport.protocol_models import (
    JSON_RPC_INTERNAL_ERROR,
    ProtocolError,
    build_error_response,
)
from search_errors import SearchApiError


class McpToolExecutionError(RuntimeError):
    def __init__(
        self,
        *,
        error_code: str,
        message: str,
        details: str | None = None,
        retryable: bool = False,
        jsonrpc_code: int = -32000,
        http_status: int = 400,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.details = details
        self.retryable = retryable
        self.jsonrpc_code = jsonrpc_code
        self.http_status = http_status


def _merge_data(base: dict[str, Any] | None, extra: dict[str, Any]) -> dict[str, Any]:
    payload = dict(base or {})
    payload.update({key: value for key, value in extra.items() if value is not None})
    return payload


def map_exception(exc: Exception) -> tuple[int, str, dict[str, Any], int]:
    if isinstance(exc, ProtocolError):
        return exc.code, exc.message, exc.data, exc.http_status

    if isinstance(exc, McpToolExecutionError):
        return (
            exc.jsonrpc_code,
            exc.message,
            _merge_data(
                None,
                {
                    "errorCode": exc.error_code,
                    "details": exc.details,
                    "retryable": exc.retryable,
                },
            ),
            exc.http_status,
        )

    if isinstance(exc, SearchApiError):
        return (
            -32010,
            exc.message,
            _merge_data(
                None,
                {
                    "errorCode": exc.code,
                    "details": exc.details,
                    "retryable": exc.status_code >= 500,
                },
            ),
            exc.status_code,
        )

    return (
        JSON_RPC_INTERNAL_ERROR,
        "Internal server error",
        {"errorCode": "INTERNAL_SERVER_ERROR", "retryable": False},
        500,
    )


def build_jsonrpc_error(request_id: str | int | None, exc: Exception) -> tuple[dict[str, Any], int]:
    code, message, data, http_status = map_exception(exc)
    return build_error_response(request_id, code=code, message=message, data=data), http_status

