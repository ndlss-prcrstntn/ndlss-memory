from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from search_repository import QdrantSearchRepository
from search_errors import SearchApiError


def test_docs_repository_search_uses_docs_collection_and_hybrid_signals(monkeypatch):
    repository = QdrantSearchRepository(
        qdrant_url="http://qdrant:6333",
        collection_name="workspace_chunks",
        docs_collection_name="workspace_docs_chunks",
        vector_size=4,
        docs_hybrid_vector_weight=0.6,
        docs_hybrid_bm25_weight=0.4,
        docs_hybrid_max_candidates=30,
        docs_rerank_enabled=True,
        docs_rerank_fail_open=True,
        docs_rerank_max_candidates=20,
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
    payload = repository.docs_search(query="startup readiness", limit=5)
    results = payload["results"]

    assert captured[0][0] == "POST"
    assert captured[0][1] == "/collections/workspace_docs_chunks/points/search"
    assert captured[1][1] == "/collections/workspace_docs_chunks/points/scroll"
    assert payload["appliedStrategy"] == "bm25_plus_vector_rerank_docs_only"
    assert payload["fallbackApplied"] is False
    assert len(results) == 3
    assert {item["documentPath"] for item in results} == {"docs/a.md", "docs/b.md", "docs/c.md"}
    assert results[0]["score"] >= results[1]["score"] >= results[2]["score"]
    assert results[0]["rankingSignals"]["semantic"] >= 0.0
    assert results[0]["rankingSignals"]["lexical"] >= 0.0
    assert results[0]["rankingSignals"]["rerank"] >= 0.0
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
        docs_rerank_enabled=True,
        docs_rerank_fail_open=True,
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
    payload = repository.docs_search(query="same", limit=10)
    results = payload["results"]

    assert [item["documentPath"] for item in results] == ["docs/a.md", "docs/b.md", "docs/b.md"]
    assert [item["chunkIndex"] for item in results] == [0, 0, 1]
    assert payload["fallbackApplied"] is False
    assert all(item["rankingSignals"]["rerank"] >= 0.0 for item in results)
    assert all(item["sourceType"] == "documentation" for item in results)


def test_docs_repository_search_reads_workspace_content_for_lexical_signal(monkeypatch):
    repository = QdrantSearchRepository(
        qdrant_url="http://qdrant:6333",
        collection_name="workspace_chunks",
        docs_collection_name="workspace_docs_chunks",
        vector_size=4,
        docs_hybrid_vector_weight=0.5,
        docs_hybrid_bm25_weight=0.5,
    )

    def fake_request_json(*, method, path, payload):  # noqa: ANN001
        if path == "/collections/workspace_docs_chunks/points/search":
            return {"result": [{"id": "1", "score": 0.7, "payload": {"path": "docs/a.md", "chunkIndex": 0}}]}
        if path == "/collections/workspace_docs_chunks/points/scroll":
            return {"result": {"points": []}}
        raise AssertionError(path)

    monkeypatch.setattr(repository, "_request_json", fake_request_json)
    monkeypatch.setattr(
        repository,
        "_read_source_content",
        lambda source_path, chunk_index: "startup readiness fallback content for lexical ranking",
    )

    payload = repository.docs_search(query="startup readiness", limit=5)
    result = payload["results"][0]

    assert result["snippet"] != ""
    assert result["rankingSignals"]["lexical"] > 0.0
    assert result["rankingSignals"]["rerank"] == 0.0


def test_docs_repository_search_applies_fallback_when_rerank_fails(monkeypatch):
    repository = QdrantSearchRepository(
        qdrant_url="http://qdrant:6333",
        collection_name="workspace_chunks",
        docs_collection_name="workspace_docs_chunks",
        vector_size=4,
        docs_rerank_enabled=True,
        docs_rerank_fail_open=True,
        docs_rerank_force_failure=True,
    )

    def fake_request_json(*, method, path, payload):  # noqa: ANN001
        if path == "/collections/workspace_docs_chunks/points/search":
            return {"result": [{"id": "1", "score": 0.7, "payload": {"path": "docs/a.md", "chunkIndex": 0, "content": "alpha"}}]}
        if path == "/collections/workspace_docs_chunks/points/scroll":
            return {
                "result": {
                    "points": [{"id": "2", "score": 0.0, "payload": {"path": "docs/b.md", "chunkIndex": 0, "content": "beta"}}]
                }
            }
        raise AssertionError(path)

    monkeypatch.setattr(repository, "_request_json", fake_request_json)
    payload = repository.docs_search(query="alpha", limit=5)

    assert payload["fallbackApplied"] is True
    assert payload["appliedStrategy"] == "bm25_plus_vector_rerank_docs_only"
    assert payload["results"][0]["rankingSignals"]["rerank"] == 0.0


def test_docs_repository_search_raises_503_when_rerank_fails_and_fail_open_disabled(monkeypatch):
    repository = QdrantSearchRepository(
        qdrant_url="http://qdrant:6333",
        collection_name="workspace_chunks",
        docs_collection_name="workspace_docs_chunks",
        vector_size=4,
        docs_rerank_enabled=True,
        docs_rerank_fail_open=False,
        docs_rerank_force_failure=True,
    )

    def fake_request_json(*, method, path, payload):  # noqa: ANN001
        if path == "/collections/workspace_docs_chunks/points/search":
            return {"result": [{"id": "1", "score": 0.7, "payload": {"path": "docs/a.md", "chunkIndex": 0, "content": "alpha"}}]}
        if path == "/collections/workspace_docs_chunks/points/scroll":
            return {
                "result": {
                    "points": [{"id": "2", "score": 0.0, "payload": {"path": "docs/b.md", "chunkIndex": 0, "content": "beta"}}]
                }
            }
        raise AssertionError(path)

    monkeypatch.setattr(repository, "_request_json", fake_request_json)
    with pytest.raises(SearchApiError) as exc:
        repository.docs_search(query="alpha", limit=5)

    assert exc.value.code == "DOCS_RERANKING_UNAVAILABLE"
    assert exc.value.status_code == 503
