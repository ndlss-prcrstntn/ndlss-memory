from __future__ import annotations

import os
from typing import Any

from mcp_transport.protocol_models import SUPPORTED_METHODS
from mcp_transport.tool_registry import McpToolRegistry


def build_discovery_document(*, request, tool_registry: McpToolRegistry) -> dict[str, Any]:
    base_url = request.host_url.rstrip("/")
    return {
        "name": "ndlss-memory-mcp-server",
        "version": os.getenv("NDLSS_VERSION", "0.2.5"),
        "transports": [
            {"type": "streamable-http", "url": f"{base_url}/mcp"},
            {"type": "sse", "url": f"{base_url}/sse"},
        ],
        "capabilities": {
            "methods": sorted(SUPPORTED_METHODS),
            "tools": tool_registry.list_tools(),
        },
    }

