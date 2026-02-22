from __future__ import annotations

from flask import Flask, jsonify, request

from mcp_transport.dispatcher import McpDispatcher
from mcp_transport.discovery import build_discovery_document
from mcp_transport.http_transport import handle_mcp_http
from mcp_transport.method_handlers import McpMethodHandlers
from mcp_transport.service_adapter import McpServiceAdapter
from mcp_transport.session_state import McpSessionStore
from mcp_transport.sse_transport import handle_sse_connect, handle_sse_message
from mcp_transport.tool_registry import McpToolRegistry
from mcp_transport.tools_indexing import McpIndexingTools
from mcp_transport.tools_search import McpSearchTools


def register_mcp_transport_routes(app: Flask) -> McpDispatcher:
    session_store = McpSessionStore()
    tool_registry = McpToolRegistry.default()
    adapter = McpServiceAdapter()
    handlers = McpMethodHandlers(
        session_store=session_store,
        tool_registry=tool_registry,
        search_tools=McpSearchTools(adapter),
        indexing_tools=McpIndexingTools(adapter),
    )
    dispatcher = McpDispatcher(handlers=handlers, session_store=session_store)

    @app.post("/mcp")
    def mcp_http_endpoint():
        return handle_mcp_http(request=request, dispatcher=dispatcher)

    @app.get("/sse")
    def mcp_sse_endpoint():
        return handle_sse_connect(dispatcher=dispatcher)

    @app.post("/messages")
    def mcp_sse_messages_endpoint():
        return handle_sse_message(request=request, dispatcher=dispatcher)

    @app.get("/.well-known/mcp")
    def mcp_discovery_endpoint():
        return jsonify(build_discovery_document(request=request, tool_registry=tool_registry))

    return dispatcher

