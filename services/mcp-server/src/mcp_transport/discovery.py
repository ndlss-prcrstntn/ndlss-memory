from __future__ import annotations

from typing import Any

from mcp_transport.protocol_models import SUPPORTED_METHODS
from mcp_transport.tool_registry import McpToolRegistry
from mcp_transport.versioning import resolve_service_version


def build_discovery_document(*, request, tool_registry: McpToolRegistry) -> dict[str, Any]:
    base_url = request.host_url.rstrip("/")
    return {
        "name": "ndlss-memory-mcp-server",
        "version": resolve_service_version(),
        "transports": [
            {"type": "streamable-http", "url": f"{base_url}/mcp"},
            {"type": "sse", "url": f"{base_url}/sse"},
        ],
        "capabilities": {
            "methods": sorted(SUPPORTED_METHODS),
            "tools": tool_registry.list_tools(),
        },
    }

