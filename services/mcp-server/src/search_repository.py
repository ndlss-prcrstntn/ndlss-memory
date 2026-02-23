from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, request

from search_errors import SearchApiError, backend_error, collection_not_found, docs_collection_unavailable
from search_hybrid import blend_scores, bm25_scores
from search_models import SearchFilters
from search_result_ref import build_result_id, parse_result_id


def _normalize_path(value: str) -> str:
    return value.replace("\\", "/")


@dataclass
class QdrantSearchRepository:
    qdrant_url: str
    collection_name: str
    docs_collection_name: str = "workspace_docs_chunks"
    request_timeout_seconds: float = 5.0
    vector_size: int = 16
    workspace_path: str = "/workspace"
    docs_hybrid_vector_weight: float = 0.65
    docs_hybrid_bm25_weight: float = 0.35
    docs_hybrid_max_candidates: int = 200

    @classmethod
    def from_env(cls) -> "QdrantSearchRepository":
        host = os.getenv("QDRANT_HOST", "qdrant")
        port = os.getenv("QDRANT_API_PORT") or os.getenv("QDRANT_PORT", "6333")
        collection_name = os.getenv("QDRANT_COLLECTION_NAME", "workspace_chunks")
        docs_collection_name = os.getenv("QDRANT_DOCS_COLLECTION_NAME", "workspace_docs_chunks")
        return cls(
            qdrant_url=f"http://{host}:{port}",
            collection_name=collection_name,
            docs_collection_name=docs_collection_name,
            request_timeout_seconds=float(os.getenv("INGESTION_UPSERT_TIMEOUT_SECONDS", "5")),
            vector_size=int(os.getenv("INGESTION_EMBEDDING_VECTOR_SIZE", "16")),
            workspace_path=os.getenv("WORKSPACE_PATH", "/workspace"),
            docs_hybrid_vector_weight=float(os.getenv("DOCS_HYBRID_VECTOR_WEIGHT", "0.65")),
            docs_hybrid_bm25_weight=float(os.getenv("DOCS_HYBRID_BM25_WEIGHT", "0.35")),
            docs_hybrid_max_candidates=int(os.getenv("DOCS_HYBRID_MAX_CANDIDATES", "200")),
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

        try:
            response = self._request_json(
                method="POST",
                path=f"/collections/{self.collection_name}/points/search",
                payload=payload,
            )
        except SearchApiError as exc:
            # Fresh workspace without ingestion should behave as "no matches", not as backend failure.
            if exc.code == "SEARCH_COLLECTION_NOT_FOUND":
                return []
            raise
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

    def docs_search(self, *, query: str, limit: int) -> list[dict[str, Any]]:
        vector_limit = min(max(limit * 4, 20), max(self.docs_hybrid_max_candidates, limit))
        payload: dict[str, Any] = {"vector": self._build_query_embedding(query), "limit": vector_limit, "with_payload": True}
        try:
            response = self._request_json(
                method="POST",
                path=f"/collections/{self.docs_collection_name}/points/search",
                payload=payload,
            )
        except SearchApiError as exc:
            if exc.code == "SEARCH_COLLECTION_NOT_FOUND":
                return []
            if exc.code == "SEARCH_BACKEND_ERROR":
                raise docs_collection_unavailable(exc.details or exc.message) from exc
            raise

        vector_points = response.get("result", [])
        if not isinstance(vector_points, list):
            vector_points = []

        lexical_points = self._scroll_docs_points(limit=max(self.docs_hybrid_max_candidates, limit))
        candidate_points = list(vector_points)
        candidate_points.extend(lexical_points)

        candidates: dict[str, dict[str, Any]] = {}
        vector_scores: dict[str, float] = {}
        lexical_documents: dict[str, str] = {}

        for point in candidate_points:
            mapped_item = self._map_point_to_docs_result(point)
            if not mapped_item:
                continue
            candidate_id = self._candidate_id(
                document_path=str(mapped_item["documentPath"]),
                chunk_index=int(mapped_item["chunkIndex"]),
            )
            existing = candidates.get(candidate_id)
            if existing is None:
                candidates[candidate_id] = mapped_item
            elif len(str(mapped_item.get("snippet", ""))) > len(str(existing.get("snippet", ""))):
                candidates[candidate_id] = mapped_item

            lexical_documents[candidate_id] = str(mapped_item.get("_lexicalText", ""))
            vector_scores.setdefault(candidate_id, 0.0)

        for point in vector_points:
            mapped_item = self._map_point_to_docs_result(point)
            if not mapped_item:
                continue
            candidate_id = self._candidate_id(
                document_path=str(mapped_item["documentPath"]),
                chunk_index=int(mapped_item["chunkIndex"]),
            )
            vector_scores[candidate_id] = max(vector_scores.get(candidate_id, 0.0), float(point.get("score", 0.0)))

        lexical_scores = bm25_scores(query=query, documents=lexical_documents)
        blended, normalized_vector, normalized_lexical = blend_scores(
            vector_scores=vector_scores,
            lexical_scores=lexical_scores,
            vector_weight=self.docs_hybrid_vector_weight,
            lexical_weight=self.docs_hybrid_bm25_weight,
        )

        ranked: list[dict[str, Any]] = []
        for candidate_id, score in blended.items():
            candidate = candidates.get(candidate_id)
            if not candidate:
                continue
            ranked.append(
                {
                    "documentPath": candidate["documentPath"],
                    "chunkIndex": candidate["chunkIndex"],
                    "snippet": candidate["snippet"],
                    "score": float(score),
                    "sourceType": "documentation",
                    "rankingSignals": {
                        "lexical": float(normalized_lexical.get(candidate_id, 0.0)),
                        "semantic": float(normalized_vector.get(candidate_id, 0.0)),
                    },
                }
            )

        ranked.sort(
            key=lambda item: (
                -float(item["score"]),
                str(item["documentPath"]),
                int(item["chunkIndex"]),
            )
        )
        return ranked[:limit]

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
        try:
            response = self._request_json(
                method="POST",
                path=f"/collections/{self.collection_name}/points",
                payload={"ids": [point_id], "with_payload": True, "with_vector": False},
            )
        except SearchApiError as exc:
            if exc.code == "SEARCH_COLLECTION_NOT_FOUND":
                return None
            raise
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

    def _map_point_to_docs_result(self, point: dict[str, Any]) -> dict[str, Any] | None:
        payload = point.get("payload", {})
        source_path = _normalize_path(str(payload.get("path", "")))
        if not source_path:
            return None
        raw_chunk_index = payload.get("chunkIndex", 0)
        if isinstance(raw_chunk_index, str) and raw_chunk_index.isdigit():
            chunk_index = int(raw_chunk_index)
        elif isinstance(raw_chunk_index, int):
            chunk_index = raw_chunk_index
        else:
            chunk_index = 0
        snippet = str(payload.get("snippet", "")).strip()
        content = str(payload.get("content", "")).strip()
        if not snippet:
            snippet = content[:280]
        lexical_text = content or snippet
        return {
            "documentPath": source_path,
            "chunkIndex": chunk_index,
            "snippet": snippet,
            "score": float(point.get("score", 0.0)),
            "sourceType": "documentation",
            "_lexicalText": lexical_text,
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
            response_text = self._read_http_error_body(exc)
            if exc.code == 404 and self._is_missing_collection_error(path=path, response_text=response_text):
                collection_name = self.docs_collection_name if f"/collections/{self.docs_collection_name}/" in path else self.collection_name
                raise collection_not_found(collection_name) from exc
            raise backend_error(
                f"Qdrant request failed with HTTP {exc.code}",
                details=response_text.strip() or None,
            ) from exc
        except error.URLError as exc:
            raise backend_error(f"Qdrant connection error: {exc.reason}") from exc
        except json.JSONDecodeError as exc:
            raise backend_error("Qdrant response is not valid JSON") from exc

    @staticmethod
    def _read_http_error_body(exc: error.HTTPError) -> str:
        try:
            return exc.read().decode("utf-8", errors="replace")
        except Exception:
            return ""

    def _is_missing_collection_error(self, *, path: str, response_text: str) -> bool:
        normalized = response_text.lower()
        collection_markers = {self.collection_name.lower(), self.docs_collection_name.lower()}
        # Qdrant returns 404 with body like:
        # {"status":{"error":"Not found: Collection `workspace_chunks` doesn't exist!"}, ...}
        if "collection" in normalized and ("doesn't exist" in normalized or "not found" in normalized):
            if any(marker in normalized for marker in collection_markers):
                return True
        # Fallback: the request is scoped to the configured collection path.
        return (
            f"/collections/{self.collection_name}/" in path
            or f"/collections/{self.docs_collection_name}/" in path
        )

    def _scroll_docs_points(self, *, limit: int) -> list[dict[str, Any]]:
        try:
            response = self._request_json(
                method="POST",
                path=f"/collections/{self.docs_collection_name}/points/scroll",
                payload={"limit": max(limit, 1), "with_payload": True, "with_vector": False},
            )
        except SearchApiError as exc:
            if exc.code == "SEARCH_COLLECTION_NOT_FOUND":
                return []
            if exc.code == "SEARCH_BACKEND_ERROR":
                raise docs_collection_unavailable(exc.details or exc.message) from exc
            raise

        result = response.get("result", {})
        if isinstance(result, list):
            return result
        if isinstance(result, dict):
            points = result.get("points", [])
            if isinstance(points, list):
                return points
        return []

    @staticmethod
    def _candidate_id(*, document_path: str, chunk_index: int) -> str:
        return f"{document_path}::{chunk_index}"

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

