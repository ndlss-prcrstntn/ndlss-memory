from __future__ import annotations

from typing import Any

from mcp_transport.error_mapper import build_jsonrpc_error
from mcp_transport.method_handlers import McpMethodHandlers
from mcp_transport.protocol_models import JsonRpcRequest, ParseError
from mcp_transport.session_state import McpSessionStore


class McpDispatcher:
    def __init__(self, *, handlers: McpMethodHandlers, session_store: McpSessionStore) -> None:
        self._handlers = handlers
        self.session_store = session_store

    def dispatch(self, *, payload: Any, session_id: str, transport: str) -> tuple[dict[str, Any], int]:
        try:
            if payload is None:
                raise ParseError()
            request = JsonRpcRequest.from_payload(payload)
        except Exception as exc:
            return build_jsonrpc_error(None, exc)

        try:
            result = self._handlers.handle(request, session_id=session_id, transport=transport)
            if request.has_id:
                return {"jsonrpc": "2.0", "id": request.request_id, "result": result}, 200

            payload = {
                "jsonrpc": "2.0",
                "id": None,
                "result": {"accepted": True},
            }
            return payload, 202
        except Exception as exc:
            response, status = build_jsonrpc_error(request.request_id if request.has_id else None, exc)
            if transport == "sse":
                self.session_store.enqueue_response(session_id, response)
            return response, status

