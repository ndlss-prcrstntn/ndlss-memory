from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from search_repository import QdrantSearchRepository


def test_docs_repository_search_uses_docs_collection_and_is_deterministic(monkeypatch):
    repository = QdrantSearchRepository(
        qdrant_url="http://qdrant:6333",
        collection_name="workspace_chunks",
        docs_collection_name="workspace_docs_chunks",
        vector_size=4,
    )
    captured = {}

    def fake_request_json(*, method, path, payload):
        captured["method"] = method
        captured["path"] = path
        captured["payload"] = payload
        return {
            "result": [
                {"id": "3", "score": 0.8, "payload": {"path": "docs/b.md", "chunkIndex": 1, "content": "bbb"}},
                {"id": "2", "score": 0.9, "payload": {"path": "docs/c.md", "chunkIndex": 0, "content": "ccc"}},
                {"id": "1", "score": 0.8, "payload": {"path": "docs/a.md", "chunkIndex": 0, "content": "aaa"}},
            ]
        }

    monkeypatch.setattr(repository, "_request_json", fake_request_json)
    results = repository.docs_search(query="docs", limit=10)

    assert captured["method"] == "POST"
    assert captured["path"] == "/collections/workspace_docs_chunks/points/search"
    assert [item["documentPath"] for item in results] == ["docs/c.md", "docs/a.md", "docs/b.md"]
    assert all(item["sourceType"] == "documentation" for item in results)
