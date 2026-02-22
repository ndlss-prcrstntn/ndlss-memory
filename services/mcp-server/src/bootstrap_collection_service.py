from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib import error, request


class BootstrapCollectionServiceError(RuntimeError):
    pass


@dataclass
class BootstrapCollectionSnapshot:
    collection_name: str
    exists: bool
    point_count: int
    checked_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "collectionName": self.collection_name,
            "exists": self.exists,
            "pointCount": self.point_count,
            "checkedAt": self.checked_at,
        }


@dataclass
class BootstrapCollectionService:
    qdrant_url: str
    collection_name: str
    vector_size: int = 16
    request_timeout_seconds: float = 5.0

    @classmethod
    def from_env(cls) -> "BootstrapCollectionService":
        host = os.getenv("QDRANT_HOST", "qdrant")
        port = os.getenv("QDRANT_API_PORT") or os.getenv("QDRANT_PORT", "6333")
        return cls(
            qdrant_url=f"http://{host}:{port}",
            collection_name=os.getenv("QDRANT_COLLECTION_NAME", "workspace_chunks"),
            vector_size=int(os.getenv("INGESTION_EMBEDDING_VECTOR_SIZE", "16")),
            request_timeout_seconds=float(os.getenv("INGESTION_UPSERT_TIMEOUT_SECONDS", "5")),
        )

    def ensure_collection_exists(self) -> bool:
        endpoint = f"/collections/{self.collection_name}"
        try:
            self._request_json(method="GET", path=endpoint, payload=None)
            return False
        except BootstrapCollectionServiceError as exc:
            if "HTTP 404" not in str(exc):
                raise
        self._request_json(
            method="PUT",
            path=endpoint,
            payload={"vectors": {"size": self.vector_size, "distance": "Cosine"}},
        )
        return True

    def point_count(self) -> int:
        response = self._request_json(
            method="POST",
            path=f"/collections/{self.collection_name}/points/count",
            payload={"exact": False},
        )
        result = response.get("result", {})
        return int(result.get("count", 0))

    def exists(self) -> bool:
        try:
            self._request_json(method="GET", path=f"/collections/{self.collection_name}", payload=None)
            return True
        except BootstrapCollectionServiceError as exc:
            if "HTTP 404" in str(exc):
                return False
            raise

    def snapshot(self, checked_at: str) -> BootstrapCollectionSnapshot:
        exists = self.exists()
        count = self.point_count() if exists else 0
        return BootstrapCollectionSnapshot(
            collection_name=self.collection_name,
            exists=exists,
            point_count=count,
            checked_at=checked_at,
        )

    def _request_json(self, *, method: str, path: str, payload: dict[str, Any] | None) -> dict[str, Any]:
        endpoint = f"{self.qdrant_url.rstrip('/')}{path}"
        body: bytes | None = None
        headers: dict[str, str] = {}
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = request.Request(endpoint, method=method, data=body, headers=headers)
        try:
            with request.urlopen(req, timeout=self.request_timeout_seconds) as response:
                raw = response.read().decode("utf-8")
                if not raw:
                    return {}
                return json.loads(raw)
        except error.HTTPError as exc:
            raise BootstrapCollectionServiceError(f"Qdrant collection request failed with HTTP {exc.code}") from exc
        except error.URLError as exc:
            raise BootstrapCollectionServiceError(f"Qdrant collection connection error: {exc.reason}") from exc
        except json.JSONDecodeError as exc:
            raise BootstrapCollectionServiceError("Qdrant collection response is not valid JSON") from exc
