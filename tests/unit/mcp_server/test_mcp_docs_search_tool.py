from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from mcp_transport.error_mapper import McpToolExecutionError  # noqa: E402
from mcp_transport.tool_registry import McpToolRegistry  # noqa: E402
from mcp_transport.tools_search import McpSearchTools  # noqa: E402


class _Adapter:
    def docs_search(self, payload):  # noqa: ANN001
        return {
            "query": payload["query"],
            "total": 1,
            "results": [
                {
                    "documentPath": "docs/guide.md",
                    "chunkIndex": 0,
                    "snippet": "docs",
                    "score": 0.9,
                    "sourceType": "documentation",
                }
            ],
        }


def test_mcp_registry_contains_search_docs_tool():
    registry = McpToolRegistry.default()
    descriptor = registry.get_tool("search_docs")
    assert descriptor is not None
    assert descriptor.name == "search_docs"
    assert descriptor.input_schema["required"] == ["query"]


def test_mcp_docs_search_tool_calls_adapter():
    tools = McpSearchTools(_Adapter())

    payload = tools.call("search_docs", {"query": "readiness", "limit": 5})

    assert payload["query"] == "readiness"
    assert payload["results"][0]["sourceType"] == "documentation"


def test_mcp_docs_search_tool_rejects_empty_query():
    tools = McpSearchTools(_Adapter())

    with pytest.raises(McpToolExecutionError) as exc:
        tools.call("search_docs", {"query": " "})

    assert exc.value.error_code == "SEARCH_QUERY_EMPTY"
