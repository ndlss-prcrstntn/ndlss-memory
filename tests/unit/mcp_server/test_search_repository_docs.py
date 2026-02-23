from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from search_repository import QdrantSearchRepository


def test_docs_repository_search_uses_docs_collection_and_hybrid_signals(monkeypatch):
    repository = QdrantSearchRepository(
        qdrant_url="http://qdrant:6333",
        collection_name="workspace_chunks",
        docs_collection_name="workspace_docs_chunks",
        vector_size=4,
        docs_hybrid_vector_weight=0.6,
        docs_hybrid_bm25_weight=0.4,
        docs_hybrid_max_candidates=30,
    )
    captured = []

    def fake_request_json(*, method, path, payload):
        captured.append((method, path, payload))
        if path == "/collections/workspace_docs_chunks/points/search":
            return {
                "result": [
                    {
                        "id": "1",
                        "score": 0.82,
                        "payload": {"path": "docs/a.md", "chunkIndex": 0, "content": "startup checklist"},
                    },
                    {
                        "id": "2",
                        "score": 0.9,
                        "payload": {"path": "docs/c.md", "chunkIndex": 0, "content": "readiness bootstrap steps"},
                    },
                ]
            }
        if path == "/collections/workspace_docs_chunks/points/scroll":
            return {
                "result": {
                    "points": [
                        {
                            "id": "3",
                            "score": 0.0,
                            "payload": {"path": "docs/b.md", "chunkIndex": 0, "content": "startup readiness checks"},
                        }
                    ]
                }
            }
        raise AssertionError(path)

    monkeypatch.setattr(repository, "_request_json", fake_request_json)
    results = repository.docs_search(query="startup readiness", limit=5)

    assert captured[0][0] == "POST"
    assert captured[0][1] == "/collections/workspace_docs_chunks/points/search"
    assert captured[1][1] == "/collections/workspace_docs_chunks/points/scroll"
    assert len(results) == 3
    assert {item["documentPath"] for item in results} == {"docs/a.md", "docs/b.md", "docs/c.md"}
    assert results[0]["score"] >= results[1]["score"] >= results[2]["score"]
    assert results[0]["rankingSignals"]["semantic"] >= 0.0
    assert results[0]["rankingSignals"]["lexical"] >= 0.0
    assert all("rankingSignals" in item for item in results)
    assert all(item["sourceType"] == "documentation" for item in results)


def test_docs_repository_search_uses_deterministic_tie_breaker(monkeypatch):
    repository = QdrantSearchRepository(
        qdrant_url="http://qdrant:6333",
        collection_name="workspace_chunks",
        docs_collection_name="workspace_docs_chunks",
        vector_size=4,
        docs_hybrid_vector_weight=1.0,
        docs_hybrid_bm25_weight=0.0,
    )

    def fake_request_json(*, method, path, payload):
        if path == "/collections/workspace_docs_chunks/points/search":
            return {
                "result": [
                    {
                        "id": "3",
                        "score": 0.8,
                        "payload": {"path": "docs/b.md", "chunkIndex": 1, "content": "same"},
                    },
                    {
                        "id": "1",
                        "score": 0.8,
                        "payload": {"path": "docs/a.md", "chunkIndex": 0, "content": "same"},
                    },
                    {
                        "id": "2",
                        "score": 0.8,
                        "payload": {"path": "docs/b.md", "chunkIndex": 0, "content": "same"},
                    },
                ]
            }
        if path == "/collections/workspace_docs_chunks/points/scroll":
            return {"result": {"points": []}}
        raise AssertionError(path)

    monkeypatch.setattr(repository, "_request_json", fake_request_json)
    results = repository.docs_search(query="same", limit=10)

    assert [item["documentPath"] for item in results] == ["docs/a.md", "docs/b.md", "docs/b.md"]
    assert [item["chunkIndex"] for item in results] == [0, 0, 1]
    assert all(item["sourceType"] == "documentation" for item in results)
