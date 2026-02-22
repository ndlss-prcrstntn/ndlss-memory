from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass
from typing import Any
from urllib import error, request

from bootstrap_state import BootstrapStateRecord

_BOOTSTRAP_POINT_NAMESPACE = uuid.UUID("f6ccddf1-7d61-4f88-93f4-36def53c1a0d")


class BootstrapStateRepositoryError(RuntimeError):
    pass


@dataclass
class BootstrapStateRepository:
    qdrant_url: str
    state_collection_name: str
    request_timeout_seconds: float = 5.0
    _collection_initialized: bool = False

    @classmethod
    def from_env(cls) -> "BootstrapStateRepository":
        host = os.getenv("QDRANT_HOST", "qdrant")
        port = os.getenv("QDRANT_API_PORT") or os.getenv("QDRANT_PORT", "6333")
        return cls(
            qdrant_url=f"http://{host}:{port}",
            state_collection_name=os.getenv("BOOTSTRAP_STATE_COLLECTION", "workspace_bootstrap_state"),
            request_timeout_seconds=float(os.getenv("INGESTION_UPSERT_TIMEOUT_SECONDS", "5")),
        )

    def get(self, workspace_key: str) -> BootstrapStateRecord | None:
        self.ensure_collection_exists()
        point_id = self._point_id(workspace_key)
        response = self._request_json(
            method="POST",
            path=f"/collections/{self.state_collection_name}/points",
            payload={"ids": [point_id], "with_payload": True, "with_vector": False},
        )
        points = response.get("result", [])
        if not isinstance(points, list) or not points:
            return None
        payload = points[0].get("payload", {})
        if not isinstance(payload, dict):
            return None
        return BootstrapStateRecord.from_payload(payload)

    def upsert(self, record: BootstrapStateRecord) -> None:
        self.ensure_collection_exists()
        point = {
            "id": self._point_id(record.workspace_key),
            "vector": [1.0],
            "payload": record.to_payload(),
        }
        self._request_json(
            method="PUT",
            path=f"/collections/{self.state_collection_name}/points?wait=true",
            payload={"points": [point]},
        )

    def ensure_collection_exists(self) -> bool:
        if self._collection_initialized:
            return False
        created = False
        path = f"/collections/{self.state_collection_name}"
        try:
            self._request_json(method="GET", path=path, payload=None)
        except BootstrapStateRepositoryError as exc:
            if "HTTP 404" not in str(exc):
                raise
            self._request_json(
                method="PUT",
                path=path,
                payload={"vectors": {"size": 1, "distance": "Cosine"}},
            )
            created = True
        self._collection_initialized = True
        return created

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
            raise BootstrapStateRepositoryError(f"Qdrant bootstrap state request failed with HTTP {exc.code}") from exc
        except error.URLError as exc:
            raise BootstrapStateRepositoryError(f"Qdrant bootstrap state connection error: {exc.reason}") from exc
        except json.JSONDecodeError as exc:
            raise BootstrapStateRepositoryError("Qdrant bootstrap state response is not valid JSON") from exc

    @staticmethod
    def _point_id(workspace_key: str) -> str:
        return str(uuid.uuid5(_BOOTSTRAP_POINT_NAMESPACE, workspace_key))
