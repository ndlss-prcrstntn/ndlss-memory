from __future__ import annotations

import io
from pathlib import Path
import sys
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

import ingestion_pipeline.vector_upsert_repository as repo_module
from ingestion_pipeline.embedding_models import VectorRecord


class _Response:
    def __init__(self, status: int = 200) -> None:
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def _record() -> VectorRecord:
    return VectorRecord(
        vector_id="chunk-1",
        chunk_id="chunk-1",
        embedding=[0.1] * 16,
        metadata={"path": "docs/readme.md"},
    )


def test_upsert_recreates_collection_after_stale_404(monkeypatch):
    repo = repo_module.VectorUpsertRepository(
        collection_name="workspace_chunks",
        qdrant_url="http://qdrant:6333",
        enable_http_upsert=True,
    )
    repo._collection_initialized = True

    ensure_calls = {"count": 0}

    def fake_ensure_collection_exists() -> None:
        ensure_calls["count"] += 1
        repo._collection_initialized = True

    monkeypatch.setattr(repo, "_ensure_collection_exists", fake_ensure_collection_exists)

    request_calls = {"count": 0}

    def fake_urlopen(req, timeout):
        request_calls["count"] += 1
        if request_calls["count"] == 1:
            raise HTTPError(req.full_url, 404, "Not Found", hdrs=None, fp=io.BytesIO(b"{}"))
        return _Response(status=200)

    monkeypatch.setattr(repo_module.request, "urlopen", fake_urlopen)

    repo.upsert(_record())

    assert request_calls["count"] == 2
    assert ensure_calls["count"] == 2


def test_delete_ignores_missing_collection(monkeypatch):
    repo = repo_module.VectorUpsertRepository(
        collection_name="workspace_chunks",
        qdrant_url="http://qdrant:6333",
        enable_http_upsert=True,
    )
    repo._collection_initialized = True

    monkeypatch.setattr(repo, "_ensure_collection_exists", lambda: None)

    def fake_urlopen(req, timeout):
        raise HTTPError(req.full_url, 404, "Not Found", hdrs=None, fp=io.BytesIO(b"{}"))

    monkeypatch.setattr(repo_module.request, "urlopen", fake_urlopen)

    repo.delete_points({"chunk-1"})

