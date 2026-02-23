from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

import system_status_handler as handler  # noqa: E402


class _DocsSearchServiceStub:
    def docs_search(self, request):  # noqa: ANN001
        return {
            "query": request.query,
            "total": 1,
            "results": [
                {
                    "documentPath": "docs/readme.md",
                    "chunkIndex": 0,
                    "snippet": "overview",
                    "score": 0.7,
                    "sourceType": "documentation",
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
    assert isinstance(payload["results"], list)
    assert payload["results"][0]["documentPath"] == "docs/readme.md"
    assert payload["results"][0]["sourceType"] == "documentation"


def test_docs_search_endpoint_contract_error_payload():
    client = handler.app.test_client()

    response = client.post("/v1/search/docs/query", json={"query": "   "})
    assert response.status_code == 400
    payload = response.get_json()
    assert payload["errorCode"] == "SEARCH_QUERY_EMPTY"
    assert "message" in payload
