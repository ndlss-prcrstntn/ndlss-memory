from __future__ import annotations

from typing import Any

from mcp_transport.error_mapper import McpToolExecutionError
from mcp_transport.service_adapter import McpServiceAdapter
from search_errors import SearchApiError


class McpSearchTools:
    def __init__(self, adapter: McpServiceAdapter) -> None:
        self._adapter = adapter

    def call(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if tool_name == "semantic_search":
            return self._semantic_search(arguments)
        if tool_name == "get_source_by_id":
            return self._get_source(arguments)
        if tool_name == "get_metadata_by_id":
            return self._get_metadata(arguments)
        raise McpToolExecutionError(
            error_code="TOOL_NOT_FOUND",
            message=f"Tool '{tool_name}' is not registered in search adapters",
            retryable=False,
            jsonrpc_code=-32601,
            http_status=404,
        )

    def _semantic_search(self, arguments: dict[str, Any]) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "query": arguments.get("query"),
            "limit": arguments.get("limit", 10),
            "filters": arguments.get("filters", {}),
        }
        query = str(payload.get("query") or "").strip()
        if not query:
            raise McpToolExecutionError(
                error_code="INVALID_REQUEST",
                message="semantic_search requires non-empty 'query'",
                retryable=False,
                jsonrpc_code=-32602,
                http_status=400,
            )
        try:
            return self._adapter.semantic_search(payload)
        except SearchApiError as exc:
            # Fresh workspace may not have collection yet; return a valid empty result.
            if exc.code == "SEARCH_COLLECTION_NOT_FOUND":
                return {
                    "status": "empty",
                    "results": [],
                    "meta": {"count": 0, "limit": int(payload.get("limit") or 10)},
                }
            raise

    def _get_source(self, arguments: dict[str, Any]) -> dict[str, Any]:
        result_id = str(arguments.get("resultId") or "").strip()
        if not result_id:
            raise McpToolExecutionError(
                error_code="INVALID_REQUEST",
                message="get_source_by_id requires 'resultId'",
                retryable=False,
                jsonrpc_code=-32602,
                http_status=400,
            )
        return self._adapter.get_source(result_id)

    def _get_metadata(self, arguments: dict[str, Any]) -> dict[str, Any]:
        result_id = str(arguments.get("resultId") or "").strip()
        if not result_id:
            raise McpToolExecutionError(
                error_code="INVALID_REQUEST",
                message="get_metadata_by_id requires 'resultId'",
                retryable=False,
                jsonrpc_code=-32602,
                http_status=400,
            )
        return self._adapter.get_metadata(result_id)
