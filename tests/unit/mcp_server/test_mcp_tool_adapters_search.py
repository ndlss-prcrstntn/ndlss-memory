from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from mcp_transport.error_mapper import McpToolExecutionError  # noqa: E402
from mcp_transport.tools_search import McpSearchTools  # noqa: E402
from search_errors import SearchApiError  # noqa: E402


class _AdapterSuccess:
    def semantic_search(self, payload):  # noqa: ANN001
        return {"status": "ok", "results": [{"resultId": "chunk:1"}], "meta": {"count": 1, "limit": payload["limit"]}}

    def get_source(self, result_id):  # noqa: ANN001
        return {"status": "ok", "source": {"resultId": result_id}}

    def get_metadata(self, result_id):  # noqa: ANN001
        return {"status": "ok", "metadata": {"resultId": result_id}}


class _AdapterMissingCollection:
    def semantic_search(self, payload):  # noqa: ANN001
        raise SearchApiError("SEARCH_COLLECTION_NOT_FOUND", "missing collection", 404)


def test_semantic_search_adapter_requires_query():
    tools = McpSearchTools(_AdapterSuccess())

    with pytest.raises(McpToolExecutionError) as exc:
        tools.call("semantic_search", {"limit": 5})

    assert exc.value.error_code == "INVALID_REQUEST"


def test_semantic_search_returns_empty_on_missing_collection():
    tools = McpSearchTools(_AdapterMissingCollection())

    response = tools.call("semantic_search", {"query": "hello", "limit": 3})

    assert response["status"] == "empty"
    assert response["results"] == []


def test_source_and_metadata_calls_use_result_id():
    tools = McpSearchTools(_AdapterSuccess())

    source = tools.call("get_source_by_id", {"resultId": "chunk:abc"})
    metadata = tools.call("get_metadata_by_id", {"resultId": "chunk:abc"})

    assert source["source"]["resultId"] == "chunk:abc"
    assert metadata["metadata"]["resultId"] == "chunk:abc"

