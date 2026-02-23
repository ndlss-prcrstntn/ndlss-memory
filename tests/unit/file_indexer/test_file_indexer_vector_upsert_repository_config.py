from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "file-indexer" / "src"
sys.path.insert(0, str(SRC_PATH))

import ingestion_pipeline.vector_upsert_repository as repo_module


def test_repository_from_env_prefers_qdrant_api_port(monkeypatch):
    monkeypatch.setenv("QDRANT_HOST", "qdrant")
    monkeypatch.setenv("QDRANT_PORT", "16333")
    monkeypatch.setenv("QDRANT_API_PORT", "6333")
    monkeypatch.setenv("QDRANT_COLLECTION_NAME", "workspace_chunks")
    repo_module._REPOSITORY_CACHE.clear()

    repo = repo_module.repository_from_env()

    assert repo.qdrant_url == "http://qdrant:6333"


def test_repository_from_env_falls_back_to_qdrant_port(monkeypatch):
    monkeypatch.setenv("QDRANT_HOST", "qdrant")
    monkeypatch.setenv("QDRANT_PORT", "16333")
    monkeypatch.delenv("QDRANT_API_PORT", raising=False)
    repo_module._REPOSITORY_CACHE.clear()

    repo = repo_module.repository_from_env()

    assert repo.qdrant_url == "http://qdrant:16333"


def test_repository_from_env_uses_docs_collection_for_docs_scope(monkeypatch):
    monkeypatch.setenv("QDRANT_HOST", "qdrant")
    monkeypatch.setenv("QDRANT_PORT", "6333")
    monkeypatch.setenv("QDRANT_DOCS_COLLECTION_NAME", "workspace_docs_chunks")
    repo_module._REPOSITORY_CACHE.clear()

    repo = repo_module.repository_from_env(index_scope="docs")

    assert repo.collection_name == "workspace_docs_chunks"
