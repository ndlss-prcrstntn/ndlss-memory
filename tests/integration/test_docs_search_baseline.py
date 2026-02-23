from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

import system_status_handler as handler  # noqa: E402


class _DocsSearchServiceStub:
    def docs_search(self, request):  # noqa: ANN001
        if request.query == "missing":
            return {
                "query": request.query,
                "total": 0,
                "appliedStrategy": "bm25_plus_vector_rerank_docs_only",
                "fallbackApplied": False,
                "results": [],
            }
        return {
            "query": request.query,
            "total": 1,
            "appliedStrategy": "bm25_plus_vector_rerank_docs_only",
            "fallbackApplied": False,
            "results": [
                {
                    "documentPath": "docs/guide.md",
                    "chunkIndex": 0,
                    "snippet": "startup readiness summary",
                    "score": 0.91,
                    "sourceType": "documentation",
                    "rankingSignals": {"lexical": 0.5, "semantic": 0.9, "rerank": 0.92},
                }
            ],
        }


def test_docs_search_baseline_positive_and_empty(monkeypatch):
    monkeypatch.setattr(handler, "SEARCH_SERVICE", _DocsSearchServiceStub())
    client = handler.app.test_client()

    positive = client.post("/v1/search/docs/query", json={"query": "startup readiness", "limit": 5})
    assert positive.status_code == 200
    positive_payload = positive.get_json()
    assert positive_payload["query"] == "startup readiness"
    assert positive_payload["total"] == 1
    assert positive_payload["results"][0]["sourceType"] == "documentation"

    empty = client.post("/v1/search/docs/query", json={"query": "missing"})
    assert empty.status_code == 200
    empty_payload = empty.get_json()
    assert empty_payload["total"] == 0
    assert empty_payload["results"] == []
