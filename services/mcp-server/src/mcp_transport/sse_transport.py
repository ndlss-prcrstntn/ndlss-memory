from __future__ import annotations

import json

from flask import Response, jsonify

from mcp_transport.dispatcher import McpDispatcher
from mcp_transport.error_mapper import build_jsonrpc_error
from mcp_transport.protocol_models import InvalidRequestError, ParseError


def handle_sse_connect(*, dispatcher: McpDispatcher):
    session = dispatcher.session_store.create_session(transport="sse")
    bootstrap = {
        "sessionId": session.session_id,
        "messageUrl": f"/messages?sessionId={session.session_id}",
    }
    body = f"event: endpoint\ndata: {json.dumps(bootstrap)}\n\n"
    response = Response(body, mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-MCP-Session-Id"] = session.session_id
    return response


def handle_sse_message(*, request, dispatcher: McpDispatcher):
    session_id = str(request.args.get("sessionId") or "").strip()
    if not session_id:
        payload, status = build_jsonrpc_error(None, InvalidRequestError("sessionId query parameter is required"))
        return jsonify(payload), status

    if dispatcher.session_store.get_session(session_id) is None:
        payload, status = build_jsonrpc_error(
            None,
            InvalidRequestError("sessionId is not found", data={"errorCode": "SESSION_NOT_FOUND"}),
        )
        return jsonify(payload), 404

    if not request.is_json:
        payload, status = build_jsonrpc_error(None, ParseError())
        return jsonify(payload), status

    body = request.get_json(silent=True)
    if body is None:
        payload, status = build_jsonrpc_error(None, ParseError())
        return jsonify(payload), status

    response, status = dispatcher.dispatch(payload=body, session_id=session_id, transport="sse")
    if status >= 400:
        return jsonify(response), status

    dispatcher.session_store.enqueue_response(session_id, response)
    return jsonify({"status": "accepted", "sessionId": session_id}), 202

