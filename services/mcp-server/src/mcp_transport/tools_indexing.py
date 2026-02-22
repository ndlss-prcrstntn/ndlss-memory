from __future__ import annotations

from typing import Any

from mcp_transport.error_mapper import McpToolExecutionError
from mcp_transport.service_adapter import McpServiceAdapter


class McpIndexingTools:
    def __init__(self, adapter: McpServiceAdapter) -> None:
        self._adapter = adapter

    def call(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if tool_name == "start_ingestion":
            return self._start_ingestion(arguments)
        if tool_name == "get_ingestion_status":
            return self._get_ingestion_status(arguments)
        raise McpToolExecutionError(
            error_code="TOOL_NOT_FOUND",
            message=f"Tool '{tool_name}' is not registered in indexing adapters",
            retryable=False,
            jsonrpc_code=-32601,
            http_status=404,
        )

    def _start_ingestion(self, arguments: dict[str, Any]) -> dict[str, Any]:
        workspace_path = arguments.get("workspacePath")
        payload: dict[str, Any] = {}
        if workspace_path is not None:
            payload["workspacePath"] = workspace_path
        return self._adapter.start_ingestion(payload)

    def _get_ingestion_status(self, arguments: dict[str, Any]) -> dict[str, Any]:
        run_id = str(arguments.get("runId") or "").strip()
        if not run_id:
            raise McpToolExecutionError(
                error_code="INVALID_REQUEST",
                message="get_ingestion_status requires 'runId'",
                retryable=False,
                jsonrpc_code=-32602,
                http_status=400,
            )
        return self._adapter.get_ingestion_status({"runId": run_id})

