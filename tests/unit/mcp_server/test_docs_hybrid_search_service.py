from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from search_models import DocsSearchRequest
from search_service import SearchService


class _HybridRepositoryStub:
    def docs_search(self, *, query, limit):  # noqa: ANN001
        return [
            {
                "documentPath": "docs/guide.md",
                "chunkIndex": 0,
                "snippet": "startup readiness summary",
                "score": 0.88,
                "sourceType": "documentation",
                "rankingSignals": {"lexical": 0.5, "semantic": 0.8},
            }
        ][:limit]


def test_docs_search_service_returns_hybrid_envelope():
    service = SearchService(_HybridRepositoryStub())
    request = DocsSearchRequest.from_payload({"query": "startup readiness", "limit": 5})

    response = service.docs_search(request)

    assert response["query"] == "startup readiness"
    assert response["appliedStrategy"] == "bm25_plus_vector_docs_only"
    assert response["total"] == 1
    assert response["results"][0]["sourceType"] == "documentation"
    assert response["results"][0]["rankingSignals"]["lexical"] == 0.5
    assert response["results"][0]["rankingSignals"]["semantic"] == 0.8
