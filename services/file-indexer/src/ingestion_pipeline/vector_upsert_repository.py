from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any
from urllib import error, request

from ingestion_pipeline.embedding_models import VectorRecord


class UpsertError(RuntimeError):
    pass


@dataclass
class VectorUpsertRepository:
    collection_name: str
    qdrant_url: str
    request_timeout_seconds: float = 5.0
    enable_http_upsert: bool = False
    _points: dict[str, dict[str, Any]] = field(default_factory=dict)

    def upsert(self, record: VectorRecord) -> None:
        point = record.to_qdrant_point()
        self._points[record.vector_id] = point
        if self.enable_http_upsert:
            self._upsert_via_http(point)

    def get_point(self, vector_id: str) -> dict[str, Any] | None:
        return self._points.get(vector_id)

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


def repository_from_env() -> VectorUpsertRepository:
    host = os.getenv("QDRANT_HOST", "qdrant")
    port = os.getenv("QDRANT_PORT", "6333")
    return VectorUpsertRepository(
        collection_name=os.getenv("QDRANT_COLLECTION_NAME", "workspace_chunks"),
        qdrant_url=f"http://{host}:{port}",
        request_timeout_seconds=float(os.getenv("INGESTION_UPSERT_TIMEOUT_SECONDS", "5")),
        enable_http_upsert=os.getenv("INGESTION_ENABLE_QDRANT_HTTP", "0") == "1",
    )

