from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from search_models import SemanticSearchRequest
from search_service import SearchService


class _RepositoryStub:
    def __init__(self, results):
        self._results = results
        self.last_query = None
        self.last_limit = None
        self.last_filters = None

    def semantic_search(self, *, query, limit, filters):
        self.last_query = query
        self.last_limit = limit
        self.last_filters = filters
        return list(self._results)


def test_semantic_search_response_is_structured_and_honors_limit_input():
    repo = _RepositoryStub(
        [
            {
                "resultId": "chunk:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "score": 0.91,
                "snippet": "snippet-1",
                "sourcePath": "docs/one.md",
                "fileType": ".md",
                "metadataRef": "chunk:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            }
        ]
    )
    service = SearchService(repo)
    request = SemanticSearchRequest.from_payload({"query": "docker compose", "limit": 5})

    response = service.semantic_search(request)

    assert response["status"] == "ok"
    assert response["meta"]["count"] == 1
    assert response["meta"]["limit"] == 5
    assert len(response["results"]) == 1
    assert response["results"][0]["resultId"].startswith("chunk:")
    assert repo.last_query == "docker compose"
    assert repo.last_limit == 5


def test_semantic_search_returns_empty_status_on_no_matches():
    repo = _RepositoryStub([])
    service = SearchService(repo)
    request = SemanticSearchRequest.from_payload({"query": "no-match"})

    response = service.semantic_search(request)

    assert response["status"] == "empty"
    assert response["results"] == []
    assert response["meta"]["count"] == 0
