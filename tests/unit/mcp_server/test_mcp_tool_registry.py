from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from mcp_transport.tool_registry import McpToolRegistry  # noqa: E402


def test_default_tool_registry_contains_required_tools():
    registry = McpToolRegistry.default()

    names = {item["name"] for item in registry.list_tools()}
    assert names == {
        "semantic_search",
        "search_docs",
        "get_source_by_id",
        "get_metadata_by_id",
        "start_ingestion",
        "get_ingestion_status",
    }


def test_get_tool_returns_descriptor():
    registry = McpToolRegistry.default()
    tool = registry.get_tool("semantic_search")

    assert tool is not None
    assert tool.name == "semantic_search"
    assert "query" in tool.input_schema["properties"]

