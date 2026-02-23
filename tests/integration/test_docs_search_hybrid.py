from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

import system_status_handler as handler  # noqa: E402


class _HybridDocsSearchServiceStub:
    def docs_search(self, request):  # noqa: ANN001
        if request.query == "missing":
            return {
                "query": request.query,
                "total": 0,
                "appliedStrategy": "bm25_plus_vector_rerank_docs_only",
                "fallbackApplied": False,
                "results": [],
            }
        if request.query == "fallback":
            return {
                "query": request.query,
                "total": 1,
                "appliedStrategy": "bm25_plus_vector_rerank_docs_only",
                "fallbackApplied": True,
                "results": [
                    {
                        "documentPath": "docs/fallback.md",
                        "chunkIndex": 0,
                        "snippet": "fallback path",
                        "score": 0.5,
                        "sourceType": "documentation",
                        "rankingSignals": {"lexical": 0.4, "semantic": 0.7, "rerank": 0.0},
                    }
                ],
            }
        return {
            "query": request.query,
            "total": 2,
            "appliedStrategy": "bm25_plus_vector_rerank_docs_only",
            "fallbackApplied": False,
            "results": [
                {
                    "documentPath": "docs/a.md",
                    "chunkIndex": 0,
                    "snippet": "startup readiness A",
                    "score": 0.9,
                    "sourceType": "documentation",
                    "rankingSignals": {"lexical": 0.6, "semantic": 0.9, "rerank": 0.95},
                },
                {
                    "documentPath": "docs/b.md",
                    "chunkIndex": 1,
                    "snippet": "startup readiness B",
                    "score": 0.8,
                    "sourceType": "documentation",
                    "rankingSignals": {"lexical": 0.5, "semantic": 0.7, "rerank": 0.85},
                },
            ],
        }

    def semantic_search(self, request):  # noqa: ANN001
        return {
            "status": "ok",
            "results": [{"resultId": "chunk:123", "score": 0.5, "snippet": "code", "sourcePath": "src/app.py", "fileType": ".py"}],
            "meta": {"count": 1, "limit": request.limit},
        }


def test_docs_hybrid_search_positive_and_non_docs_compatibility(monkeypatch):
    monkeypatch.setattr(handler, "SEARCH_SERVICE", _HybridDocsSearchServiceStub())
    client = handler.app.test_client()

    docs_response = client.post("/v1/search/docs/query", json={"query": "startup readiness", "limit": 5})
    assert docs_response.status_code == 200
    docs_payload = docs_response.get_json()
    assert docs_payload["appliedStrategy"] == "bm25_plus_vector_rerank_docs_only"
    assert docs_payload["fallbackApplied"] is False
    assert docs_payload["results"][0]["rankingSignals"]["semantic"] == 0.9
    assert docs_payload["results"][0]["rankingSignals"]["rerank"] == 0.95

    semantic_response = client.post("/v1/search/semantic", json={"query": "startup readiness", "limit": 3})
    assert semantic_response.status_code == 200
    semantic_payload = semantic_response.get_json()
    assert semantic_payload["status"] == "ok"
    assert "appliedStrategy" not in semantic_payload


def test_docs_hybrid_search_repeatable_top_k(monkeypatch):
    monkeypatch.setattr(handler, "SEARCH_SERVICE", _HybridDocsSearchServiceStub())
    client = handler.app.test_client()

    first = client.post("/v1/search/docs/query", json={"query": "startup readiness", "limit": 5})
    second = client.post("/v1/search/docs/query", json={"query": "startup readiness", "limit": 5})

    assert first.status_code == 200
    assert second.status_code == 200
    first_docs = first.get_json()["results"]
    second_docs = second.get_json()["results"]
    assert [item["documentPath"] for item in first_docs] == [item["documentPath"] for item in second_docs]
    assert [item["chunkIndex"] for item in first_docs] == [item["chunkIndex"] for item in second_docs]


def test_docs_hybrid_search_empty_result(monkeypatch):
    monkeypatch.setattr(handler, "SEARCH_SERVICE", _HybridDocsSearchServiceStub())
    client = handler.app.test_client()

    response = client.post("/v1/search/docs/query", json={"query": "missing"})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["total"] == 0
    assert payload["results"] == []


def test_docs_hybrid_search_fallback_response(monkeypatch):
    monkeypatch.setattr(handler, "SEARCH_SERVICE", _HybridDocsSearchServiceStub())
    client = handler.app.test_client()

    response = client.post("/v1/search/docs/query", json={"query": "fallback", "limit": 5})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["fallbackApplied"] is True
    assert payload["results"][0]["rankingSignals"]["rerank"] == 0.0
