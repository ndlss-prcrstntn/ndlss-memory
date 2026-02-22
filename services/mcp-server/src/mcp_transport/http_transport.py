from __future__ import annotations

from flask import jsonify

from mcp_transport.dispatcher import McpDispatcher
from mcp_transport.error_mapper import build_jsonrpc_error
from mcp_transport.protocol_models import InvalidRequestError, ParseError


def _resolve_session_id(request) -> str:
    header_value = request.headers.get("X-MCP-Session-Id", "").strip()
    query_value = request.args.get("sessionId", "").strip()
    return header_value or query_value or "http-default"


def handle_mcp_http(*, request, dispatcher: McpDispatcher):
    if not request.is_json:
        payload, status = build_jsonrpc_error(None, ParseError())
        return jsonify(payload), status

    payload = request.get_json(silent=True)
    if payload is None:
        response, status = build_jsonrpc_error(None, ParseError())
        return jsonify(response), status

    session_id = _resolve_session_id(request)
    if not session_id:
        response, status = build_jsonrpc_error(None, InvalidRequestError("sessionId must not be empty"))
        return jsonify(response), status

    response, status = dispatcher.dispatch(payload=payload, session_id=session_id, transport="streamable-http")
    return jsonify(response), status

