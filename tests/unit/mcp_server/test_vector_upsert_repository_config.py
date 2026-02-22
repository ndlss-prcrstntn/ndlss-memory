from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

import ingestion_pipeline.vector_upsert_repository as repo_module


def test_repository_from_env_prefers_qdrant_api_port(monkeypatch):
    monkeypatch.setenv("QDRANT_HOST", "qdrant")
    monkeypatch.setenv("QDRANT_PORT", "16333")
    monkeypatch.setenv("QDRANT_API_PORT", "6333")
    monkeypatch.setenv("QDRANT_COLLECTION_NAME", "workspace_chunks")
    monkeypatch.setenv("INGESTION_ENABLE_QDRANT_HTTP", "1")
    repo_module._REPOSITORY_CACHE.clear()

    repo = repo_module.repository_from_env()

    assert repo.qdrant_url == "http://qdrant:6333"
    assert repo.enable_http_upsert is True


def test_repository_from_env_enables_http_upsert_when_enabled(monkeypatch):
    monkeypatch.setenv("QDRANT_HOST", "qdrant")
    monkeypatch.setenv("QDRANT_PORT", "6333")
    monkeypatch.delenv("QDRANT_API_PORT", raising=False)
    monkeypatch.setenv("INGESTION_ENABLE_QDRANT_HTTP", "1")
    repo_module._REPOSITORY_CACHE.clear()

    repo = repo_module.repository_from_env()

    assert repo.enable_http_upsert is True
