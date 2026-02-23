from __future__ import annotations

import io
import json
from pathlib import Path
import sys
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[3]
SRC_PATH = ROOT / "services" / "mcp-server" / "src"
sys.path.insert(0, str(SRC_PATH))

import bootstrap_collection_service as module  # noqa: E402


class _Response:
    def __init__(self, *, status: int = 200, payload: dict | None = None) -> None:
        self.status = status
        self._payload = payload or {}

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_ensure_collection_creates_when_missing(monkeypatch):
    service = module.BootstrapCollectionService(
        qdrant_url="http://qdrant:6333",
        collection_name="workspace_chunks",
        vector_size=16,
    )
    calls = {"count": 0}

    def fake_urlopen(req, timeout):
        calls["count"] += 1
        if calls["count"] == 1:
            raise HTTPError(req.full_url, 404, "Not Found", hdrs=None, fp=io.BytesIO(b"{}"))
        return _Response(status=200, payload={"result": "ok"})

    monkeypatch.setattr(module.request, "urlopen", fake_urlopen)
    created = service.ensure_collection_exists()
    assert created is True
    assert calls["count"] == 2


def test_point_count_reads_qdrant_response(monkeypatch):
    service = module.BootstrapCollectionService(
        qdrant_url="http://qdrant:6333",
        collection_name="workspace_chunks",
    )

    def fake_urlopen(req, timeout):
        return _Response(status=200, payload={"result": {"count": 7}})

    monkeypatch.setattr(module.request, "urlopen", fake_urlopen)
    assert service.point_count() == 7


def test_ensure_docs_collection_creates_when_missing(monkeypatch):
    service = module.BootstrapCollectionService(
        qdrant_url="http://qdrant:6333",
        collection_name="workspace_chunks",
        docs_collection_name="workspace_docs_chunks",
        vector_size=16,
    )
    calls = {"count": 0}

    def fake_urlopen(req, timeout):
        calls["count"] += 1
        if calls["count"] == 1:
            raise HTTPError(req.full_url, 404, "Not Found", hdrs=None, fp=io.BytesIO(b"{}"))
        return _Response(status=200, payload={"result": "ok"})

    monkeypatch.setattr(module.request, "urlopen", fake_urlopen)
    created = service.ensure_docs_collection_exists()
    assert created is True
