from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from search_errors import SearchApiError
from search_models import SearchFilters, SemanticSearchRequest


def test_filters_are_normalized_and_file_type_gets_dot_prefix():
    filters = SearchFilters.from_payload({"path": " docs\\a.md ", "folder": " docs/sub ", "fileType": "md"})

    assert filters.path == "docs/a.md"
    assert filters.folder == "docs/sub"
    assert filters.file_type == ".md"


def test_semantic_search_request_validates_query_and_limit():
    request = SemanticSearchRequest.from_payload({"query": "healthcheck", "limit": 7})

    assert request.query == "healthcheck"
    assert request.limit == 7

    with pytest.raises(SearchApiError) as empty_query_exc:
        SemanticSearchRequest.from_payload({"query": "   "})
    assert empty_query_exc.value.code == "INVALID_REQUEST"

    with pytest.raises(SearchApiError) as bad_limit_exc:
        SemanticSearchRequest.from_payload({"query": "ok", "limit": 0})
    assert bad_limit_exc.value.code == "INVALID_REQUEST"
