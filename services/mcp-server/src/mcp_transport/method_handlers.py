from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from mcp_transport.error_mapper import McpToolExecutionError
from mcp_transport.protocol_models import (
    InvalidParamsError,
    JsonRpcRequest,
    MethodNotFoundError,
    METHOD_INITIALIZE,
    METHOD_NOTIFICATIONS_INITIALIZED,
    METHOD_PING,
    METHOD_TOOLS_CALL,
    METHOD_TOOLS_LIST,
)
from mcp_transport.session_state import McpSessionStore
from mcp_transport.tool_registry import McpToolRegistry
from mcp_transport.tools_indexing import McpIndexingTools
from mcp_transport.tools_search import McpSearchTools


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class McpMethodHandlers:
    def __init__(
        self,
        *,
        session_store: McpSessionStore,
        tool_registry: McpToolRegistry,
        search_tools: McpSearchTools,
        indexing_tools: McpIndexingTools,
    ) -> None:
        self._sessions = session_store
        self._tools = tool_registry
        self._search_tools = search_tools
        self._indexing_tools = indexing_tools

    def handle(self, request: JsonRpcRequest, *, session_id: str, transport: str) -> dict[str, Any]:
        self._sessions.ensure_session(session_id, transport=transport)
        method = request.method

        if method == METHOD_INITIALIZE:
            return self._handle_initialize(session_id=session_id, params=request.params)
        if method == METHOD_NOTIFICATIONS_INITIALIZED:
            return self._handle_initialized(session_id=session_id, params=request.params)
        if method == METHOD_PING:
            return self._handle_ping()
        if method == METHOD_TOOLS_LIST:
            self._assert_initialized(session_id)
            return self._handle_tools_list()
        if method == METHOD_TOOLS_CALL:
            self._assert_initialized(session_id)
            return self._handle_tools_call(request.params)
        raise MethodNotFoundError(method)

    def _handle_initialize(self, *, session_id: str, params: dict[str, Any]) -> dict[str, Any]:
        client_info = params.get("clientInfo")
        if client_info is not None and not isinstance(client_info, dict):
            raise InvalidParamsError("clientInfo must be an object when provided")

        self._sessions.mark_initialized(session_id, client_info=client_info)
        return {
            "protocolVersion": "2025-06-18",
            "serverInfo": {
                "name": "ndlss-memory-mcp-server",
                "version": os.getenv("NDLSS_VERSION", "0.2.5"),
            },
            "capabilities": {
                "tools": {"listChanged": False},
            },
        }

    def _handle_initialized(self, *, session_id: str, params: dict[str, Any]) -> dict[str, Any]:
        if params and not isinstance(params, dict):
            raise InvalidParamsError("params must be an object")
        session = self._sessions.mark_initialized(session_id)
        if session is None:
            raise McpToolExecutionError(
                error_code="SESSION_NOT_FOUND",
                message=f"Session '{session_id}' is not found",
                retryable=False,
                jsonrpc_code=-32004,
                http_status=404,
            )
        return {"acknowledged": True}

    @staticmethod
    def _handle_ping() -> dict[str, Any]:
        return {"pong": True, "timestamp": _now_iso()}

    def _handle_tools_list(self) -> dict[str, Any]:
        return {"tools": self._tools.list_tools()}

    def _handle_tools_call(self, params: dict[str, Any]) -> dict[str, Any]:
        name = params.get("name")
        if not isinstance(name, str) or not name.strip():
            raise InvalidParamsError("tools/call requires non-empty string field 'name'")

        arguments = params.get("arguments", {})
        if arguments is None:
            arguments = {}
        if not isinstance(arguments, dict):
            raise InvalidParamsError("tools/call arguments must be an object")

        tool_name = name.strip()
        if not self._tools.has_tool(tool_name):
            raise McpToolExecutionError(
                error_code="TOOL_NOT_FOUND",
                message=f"Tool '{tool_name}' is not supported",
                retryable=False,
                jsonrpc_code=-32601,
                http_status=404,
            )

        if tool_name in {"semantic_search", "search_docs", "get_source_by_id", "get_metadata_by_id"}:
            payload = self._search_tools.call(tool_name, arguments)
        else:
            payload = self._indexing_tools.call(tool_name, arguments)

        return {
            "toolName": tool_name,
            "payload": payload,
        }

    def _assert_initialized(self, session_id: str) -> None:
        session = self._sessions.get_session(session_id)
        if session is None or not session.initialized:
            raise McpToolExecutionError(
                error_code="SESSION_NOT_INITIALIZED",
                message="MCP session is not initialized",
                retryable=True,
                jsonrpc_code=-32002,
                http_status=409,
            )

