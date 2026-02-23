from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

import system_status_handler as handler  # noqa: E402
from search_errors import SearchApiError  # noqa: E402


class _DocsSearchServiceStub:
    def docs_search(self, request):  # noqa: ANN001
        return {
            "query": request.query,
            "total": 1,
            "appliedStrategy": "bm25_plus_vector_rerank_docs_only",
            "fallbackApplied": False,
            "results": [
                {
                    "documentPath": "docs/readme.md",
                    "chunkIndex": 0,
                    "snippet": "overview",
                    "score": 0.7,
                    "sourceType": "documentation",
                    "rankingSignals": {"lexical": 0.4, "semantic": 0.9, "rerank": 0.75},
                }
            ],
        }


def test_docs_search_endpoint_contract_success(monkeypatch):
    monkeypatch.setattr(handler, "SEARCH_SERVICE", _DocsSearchServiceStub())
    client = handler.app.test_client()

    response = client.post("/v1/search/docs/query", json={"query": "overview", "limit": 3})
    assert response.status_code == 200
    payload = response.get_json()

    assert payload["query"] == "overview"
    assert isinstance(payload["total"], int)
    assert payload["appliedStrategy"] == "bm25_plus_vector_rerank_docs_only"
    assert payload["fallbackApplied"] is False
    assert isinstance(payload["results"], list)
    assert payload["results"][0]["documentPath"] == "docs/readme.md"
    assert payload["results"][0]["sourceType"] == "documentation"
    assert "rankingSignals" in payload["results"][0]
    assert "rerank" in payload["results"][0]["rankingSignals"]


def test_docs_search_endpoint_contract_error_payload():
    client = handler.app.test_client()

    response = client.post("/v1/search/docs/query", json={"query": "   "})
    assert response.status_code == 400
    payload = response.get_json()
    assert payload["errorCode"] == "SEARCH_QUERY_EMPTY"
    assert "message" in payload


class _DocsSearchUnavailableStub:
    def docs_search(self, request):  # noqa: ANN001
        raise SearchApiError(
            "DOCS_COLLECTION_UNAVAILABLE",
            "Docs collection is temporarily unavailable",
            503,
        )


def test_docs_search_endpoint_contract_unavailable_payload(monkeypatch):
    monkeypatch.setattr(handler, "SEARCH_SERVICE", _DocsSearchUnavailableStub())
    client = handler.app.test_client()

    response = client.post("/v1/search/docs/query", json={"query": "overview"})
    assert response.status_code == 503
    payload = response.get_json()
    assert payload["errorCode"] == "DOCS_COLLECTION_UNAVAILABLE"
    assert "message" in payload


class _DocsRerankingUnavailableStub:
    def docs_search(self, request):  # noqa: ANN001
        raise SearchApiError(
            "DOCS_RERANKING_UNAVAILABLE",
            "Docs reranking stage is temporarily unavailable",
            503,
        )


def test_docs_search_endpoint_contract_reranking_unavailable_payload(monkeypatch):
    monkeypatch.setattr(handler, "SEARCH_SERVICE", _DocsRerankingUnavailableStub())
    client = handler.app.test_client()

    response = client.post("/v1/search/docs/query", json={"query": "overview"})
    assert response.status_code == 503
    payload = response.get_json()
    assert payload["errorCode"] == "DOCS_RERANKING_UNAVAILABLE"
    assert "message" in payload
