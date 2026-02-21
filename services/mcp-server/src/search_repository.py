from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, request

from search_errors import backend_error
from search_models import SearchFilters
from search_result_ref import build_result_id, parse_result_id


def _normalize_path(value: str) -> str:
    return value.replace("\\", "/")


@dataclass
class QdrantSearchRepository:
    qdrant_url: str
    collection_name: str
    request_timeout_seconds: float = 5.0
    vector_size: int = 16
    workspace_path: str = "/workspace"

    @classmethod
    def from_env(cls) -> "QdrantSearchRepository":
        host = os.getenv("QDRANT_HOST", "qdrant")
        port = os.getenv("QDRANT_PORT", "6333")
        collection_name = os.getenv("QDRANT_COLLECTION_NAME", "workspace_chunks")
        return cls(
            qdrant_url=f"http://{host}:{port}",
            collection_name=collection_name,
            request_timeout_seconds=float(os.getenv("INGESTION_UPSERT_TIMEOUT_SECONDS", "5")),
            vector_size=int(os.getenv("INGESTION_EMBEDDING_VECTOR_SIZE", "16")),
            workspace_path=os.getenv("WORKSPACE_PATH", "/workspace"),
        )

    def semantic_search(self, *, query: str, limit: int, filters: SearchFilters) -> list[dict[str, Any]]:
        payload: dict[str, Any] = {
            "vector": self._build_query_embedding(query),
            "limit": limit,
            "with_payload": True,
        }
        qdrant_filter = self._build_qdrant_filter(filters)
        if qdrant_filter:
            payload["filter"] = qdrant_filter

        response = self._request_json(
            method="POST",
            path=f"/collections/{self.collection_name}/points/search",
            payload=payload,
        )
        points = response.get("result", [])
        if not isinstance(points, list):
            return []

        mapped: list[dict[str, Any]] = []
        for point in points:
            mapped_item = self._map_point_to_result(point)
            if mapped_item:
                mapped.append(mapped_item)

        if filters.folder:
            folder = filters.folder.strip("/")
            mapped = [item for item in mapped if item["sourcePath"].startswith(folder + "/") or item["sourcePath"] == folder]

        return mapped

    def get_source_by_result_id(self, result_id: str) -> dict[str, Any] | None:
        point = self._get_point(result_id)
        if not point:
            return None

        payload = point.get("payload", {})
        source_path = _normalize_path(str(payload.get("path", "")))
        chunk_index = payload.get("chunkIndex")
        if isinstance(chunk_index, str) and chunk_index.isdigit():
            chunk_index = int(chunk_index)
        if not isinstance(chunk_index, int):
            chunk_index = None

        content = str(payload.get("content", "")).strip()
        if not content and source_path:
            content = self._read_source_content(source_path=source_path, chunk_index=chunk_index)

        return {
            "resultId": build_result_id(str(point.get("id", ""))),
            "content": content,
            "sourcePath": source_path,
            "chunkIndex": chunk_index,
        }

    def get_metadata_by_result_id(self, result_id: str) -> dict[str, Any] | None:
        point = self._get_point(result_id)
        if not point:
            return None

        payload = point.get("payload", {})
        source_path = _normalize_path(str(payload.get("path", "")))
        file_name = str(payload.get("fileName", "")) or Path(source_path).name
        file_type = str(payload.get("fileType", ""))
        if not file_type and file_name:
            file_type = Path(file_name).suffix
        return {
            "resultId": build_result_id(str(point.get("id", ""))),
            "fileName": file_name,
            "fileType": file_type,
            "sourcePath": source_path,
            "contentHash": payload.get("contentHash"),
            "indexedAt": payload.get("timestamp"),
        }

    def _get_point(self, result_id: str) -> dict[str, Any] | None:
        point_id = parse_result_id(result_id)
        response = self._request_json(
            method="POST",
            path=f"/collections/{self.collection_name}/points",
            payload={"ids": [point_id], "with_payload": True, "with_vector": False},
        )
        points = response.get("result", [])
        if not isinstance(points, list) or not points:
            return None
        return points[0]

    def _map_point_to_result(self, point: dict[str, Any]) -> dict[str, Any] | None:
        point_id = str(point.get("id", "")).strip()
        if not point_id:
            return None

        payload = point.get("payload", {})
        source_path = _normalize_path(str(payload.get("path", "")))
        content = str(payload.get("content", ""))
        snippet = str(payload.get("snippet", "")).strip()
        if not snippet and content:
            snippet = content[:280]
        if not snippet and source_path:
            snippet = self._read_source_content(source_path=source_path, chunk_index=None)[:280]

        file_type = str(payload.get("fileType", ""))
        if not file_type and source_path:
            file_type = Path(source_path).suffix

        return {
            "resultId": build_result_id(point_id),
            "score": float(point.get("score", 0.0)),
            "snippet": snippet,
            "sourcePath": source_path,
            "fileType": file_type,
            "metadataRef": build_result_id(point_id),
        }

    def _request_json(self, *, method: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        endpoint = f"{self.qdrant_url.rstrip('/')}{path}"
        body = json.dumps(payload).encode("utf-8")
        req = request.Request(
            endpoint,
            method=method,
            data=body,
            headers={"Content-Type": "application/json"},
        )
        try:
            with request.urlopen(req, timeout=self.request_timeout_seconds) as response:
                raw = response.read().decode("utf-8")
                if not raw:
                    return {}
                return json.loads(raw)
        except error.HTTPError as exc:
            raise backend_error(f"Qdrant request failed with HTTP {exc.code}") from exc
        except error.URLError as exc:
            raise backend_error(f"Qdrant connection error: {exc.reason}") from exc
        except json.JSONDecodeError as exc:
            raise backend_error("Qdrant response is not valid JSON") from exc

    def _build_query_embedding(self, query: str) -> list[float]:
        digest = hashlib.sha256(query.encode("utf-8")).hexdigest()
        vector: list[float] = []
        for index in range(self.vector_size):
            offset = (index * 4) % len(digest)
            sample = digest[offset : offset + 4]
            vector.append(int(sample, 16) / 65535.0)
        return vector

    @staticmethod
    def _build_qdrant_filter(filters: SearchFilters) -> dict[str, Any] | None:
        must: list[dict[str, Any]] = []
        if filters.path:
            must.append({"key": "path", "match": {"value": filters.path}})
        if filters.file_type:
            must.append({"key": "fileType", "match": {"value": filters.file_type}})
        if not must:
            return None
        return {"must": must}

    def _read_source_content(self, *, source_path: str, chunk_index: int | None) -> str:
        try:
            root = Path(self.workspace_path)
            target = (root / source_path).resolve()
            if not target.exists() or not target.is_file():
                return ""
            # Safety: avoid path traversal outside workspace mount.
            if root.resolve() not in target.parents and target != root.resolve():
                return ""
            content = target.read_text(encoding="utf-8", errors="replace")
            if chunk_index is None:
                return content

            chunk_size = int(os.getenv("INGESTION_CHUNK_SIZE", "800"))
            overlap = int(os.getenv("INGESTION_CHUNK_OVERLAP", "120"))
            if overlap >= chunk_size:
                overlap = max(chunk_size - 1, 0)
            step = max(chunk_size - overlap, 1)
            start = chunk_index * step
            return content[start : start + chunk_size]
        except OSError:
            return ""

