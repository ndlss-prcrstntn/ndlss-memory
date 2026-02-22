from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

from search_errors import SearchApiError, backend_error, collection_not_found
from search_models import SearchFilters
from search_repository import QdrantSearchRepository


def test_from_env_prefers_qdrant_api_port(monkeypatch):
    monkeypatch.setenv("QDRANT_HOST", "qdrant")
    monkeypatch.setenv("QDRANT_PORT", "16333")
    monkeypatch.setenv("QDRANT_API_PORT", "6333")

    repo = QdrantSearchRepository.from_env()

    assert repo.qdrant_url == "http://qdrant:6333"


def test_from_env_falls_back_to_qdrant_port(monkeypatch):
    monkeypatch.setenv("QDRANT_HOST", "qdrant")
    monkeypatch.setenv("QDRANT_PORT", "16333")
    monkeypatch.delenv("QDRANT_API_PORT", raising=False)

    repo = QdrantSearchRepository.from_env()

    assert repo.qdrant_url == "http://qdrant:16333"


class _MissingCollectionRepo(QdrantSearchRepository):
    def _request_json(self, *, method, path, payload):  # noqa: ANN001
        raise collection_not_found(self.collection_name)


class _BackendFailureRepo(QdrantSearchRepository):
    def _request_json(self, *, method, path, payload):  # noqa: ANN001
        raise backend_error("Qdrant unavailable")


def _repo(repo_cls) -> QdrantSearchRepository:  # noqa: ANN001
    return repo_cls(
        qdrant_url="http://qdrant:6333",
        collection_name="workspace_chunks",
        request_timeout_seconds=5.0,
        vector_size=16,
        workspace_path="/workspace",
    )


def test_semantic_search_returns_empty_when_collection_is_missing():
    repo = _repo(_MissingCollectionRepo)

    response = repo.semantic_search(query="healthcheck", limit=5, filters=SearchFilters())

    assert response == []


def test_get_source_and_metadata_return_none_when_collection_is_missing():
    repo = _repo(_MissingCollectionRepo)
    result_id = "chunk:1111111111111111111111111111111111111111111111111111111111111111"

    source = repo.get_source_by_result_id(result_id)
    metadata = repo.get_metadata_by_result_id(result_id)

    assert source is None
    assert metadata is None


def test_semantic_search_still_raises_on_real_backend_error():
    repo = _repo(_BackendFailureRepo)

    with pytest.raises(SearchApiError) as exc:
        repo.semantic_search(query="healthcheck", limit=5, filters=SearchFilters())

    assert exc.value.code == "SEARCH_BACKEND_ERROR"
