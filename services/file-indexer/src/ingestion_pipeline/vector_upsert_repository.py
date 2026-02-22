from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, field
from typing import Any
from urllib import error, request

from ingestion_pipeline.embedding_models import VectorRecord


class UpsertError(RuntimeError):
    pass


_REPOSITORY_CACHE: dict[str, "VectorUpsertRepository"] = {}
_QDRANT_POINT_NAMESPACE = uuid.UUID("c6a7f5f3-2f2d-4f4a-92c2-8f313f2fd63c")


@dataclass
class VectorUpsertRepository:
    collection_name: str
    qdrant_url: str
    request_timeout_seconds: float = 5.0
    enable_http_upsert: bool = False
    _points: dict[str, dict[str, Any]] = field(default_factory=dict)
    _file_hash_index: dict[str, str] = field(default_factory=dict)
    _file_chunk_index: dict[str, set[str]] = field(default_factory=dict)

    def upsert(self, record: VectorRecord) -> None:
        point = record.to_qdrant_point()
        point["id"] = self._qdrant_point_id(record.vector_id)
        self._points[record.vector_id] = point
        if self.enable_http_upsert:
            self._upsert_via_http(point)

    def get_point(self, vector_id: str) -> dict[str, Any] | None:
        return self._points.get(vector_id)

    def get_file_hash(self, file_path: str) -> str | None:
        return self._file_hash_index.get(file_path)

    def get_file_chunk_ids(self, file_path: str) -> set[str]:
        return set(self._file_chunk_index.get(file_path, set()))

    def list_indexed_files(self) -> set[str]:
        return set(self._file_hash_index.keys())

    def set_file_index(self, *, file_path: str, file_hash: str, chunk_ids: set[str]) -> None:
        self._file_hash_index[file_path] = file_hash
        self._file_chunk_index[file_path] = set(chunk_ids)

    def remove_file(self, file_path: str) -> None:
        self._file_hash_index.pop(file_path, None)
        self._file_chunk_index.pop(file_path, None)

    def delete_file_records(self, file_path: str) -> int:
        point_ids = self.get_file_chunk_ids(file_path)
        deleted = self.delete_points(point_ids)
        self.remove_file(file_path)
        return deleted

    def delete_points(self, point_ids: set[str]) -> int:
        if not point_ids:
            return 0
        deleted = 0
        for point_id in point_ids:
            if point_id in self._points:
                deleted += 1
                del self._points[point_id]
        if self.enable_http_upsert:
            self._delete_via_http(point_ids)
        return deleted

    def _upsert_via_http(self, point: dict[str, Any]) -> None:
        payload = json.dumps({"points": [point]}).encode("utf-8")
        endpoint = f"{self.qdrant_url.rstrip('/')}/collections/{self.collection_name}/points?wait=true"
        req = request.Request(endpoint, method="PUT", data=payload, headers={"Content-Type": "application/json"})
        try:
            with request.urlopen(req, timeout=self.request_timeout_seconds) as resp:
                if resp.status >= 300:
                    raise UpsertError(f"Qdrant upsert failed with HTTP {resp.status}")
        except error.HTTPError as exc:
            raise UpsertError(f"Qdrant upsert failed with HTTP {exc.code}") from exc
        except error.URLError as exc:
            raise UpsertError(f"Qdrant upsert connection error: {exc.reason}") from exc

    def _delete_via_http(self, point_ids: set[str]) -> None:
        payload = json.dumps({"points": [self._qdrant_point_id(point_id) for point_id in point_ids]}).encode("utf-8")
        endpoint = f"{self.qdrant_url.rstrip('/')}/collections/{self.collection_name}/points/delete?wait=true"
        req = request.Request(endpoint, method="POST", data=payload, headers={"Content-Type": "application/json"})
        try:
            with request.urlopen(req, timeout=self.request_timeout_seconds) as resp:
                if resp.status >= 300:
                    raise UpsertError(f"Qdrant delete failed with HTTP {resp.status}")
        except error.HTTPError as exc:
            raise UpsertError(f"Qdrant delete failed with HTTP {exc.code}") from exc
        except error.URLError as exc:
            raise UpsertError(f"Qdrant delete connection error: {exc.reason}") from exc

    @staticmethod
    def _qdrant_point_id(point_id: str) -> str:
        try:
            return str(uuid.UUID(point_id))
        except (ValueError, TypeError, AttributeError):
            return str(uuid.uuid5(_QDRANT_POINT_NAMESPACE, str(point_id)))


def repository_from_env() -> VectorUpsertRepository:
    host = os.getenv("QDRANT_HOST", "qdrant")
    port = os.getenv("QDRANT_PORT", "6333")
    collection_name = os.getenv("QDRANT_COLLECTION_NAME", "workspace_chunks")
    qdrant_url = f"http://{host}:{port}"
    cache_key = f"{qdrant_url}|{collection_name}"
    if cache_key not in _REPOSITORY_CACHE:
        _REPOSITORY_CACHE[cache_key] = VectorUpsertRepository(
            collection_name=collection_name,
            qdrant_url=qdrant_url,
            request_timeout_seconds=float(os.getenv("INGESTION_UPSERT_TIMEOUT_SECONDS", "5")),
            enable_http_upsert=os.getenv("INGESTION_ENABLE_QDRANT_HTTP", "0") == "1",
        )
    return _REPOSITORY_CACHE[cache_key]

