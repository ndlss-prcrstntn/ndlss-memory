from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from search_errors import invalid_request, search_query_empty

DEFAULT_LIMIT = 10
MAX_LIMIT = 100
DOCS_DEFAULT_LIMIT = 10
DOCS_MAX_LIMIT = 50


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_optional_text(value: Any) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    if not normalized:
        return None
    return normalized.replace("\\", "/")


@dataclass(frozen=True)
class SearchFilters:
    path: str | None = None
    folder: str | None = None
    file_type: str | None = None

    @classmethod
    def from_payload(cls, payload: Any) -> "SearchFilters":
        if payload is None:
            return cls()
        if not isinstance(payload, dict):
            raise invalid_request("filters must be an object")
        path = _normalize_optional_text(payload.get("path"))
        folder = _normalize_optional_text(payload.get("folder"))
        file_type = _normalize_optional_text(payload.get("fileType"))
        if file_type and not file_type.startswith("."):
            file_type = f".{file_type}"
        if folder:
            folder = folder.strip("/")
        return cls(path=path, folder=folder, file_type=file_type)

    def as_dict(self) -> dict[str, str]:
        data: dict[str, str] = {}
        if self.path:
            data["path"] = self.path
        if self.folder:
            data["folder"] = self.folder
        if self.file_type:
            data["fileType"] = self.file_type
        return data


@dataclass(frozen=True)
class SemanticSearchRequest:
    query: str
    limit: int = DEFAULT_LIMIT
    filters: SearchFilters = SearchFilters()

    @classmethod
    def from_payload(cls, payload: Any) -> "SemanticSearchRequest":
        if not isinstance(payload, dict):
            raise invalid_request("Request body must be a JSON object")
        query = str(payload.get("query", "")).strip()
        if not query:
            raise invalid_request("query must not be empty")

        raw_limit = payload.get("limit", DEFAULT_LIMIT)
        try:
            limit = int(raw_limit)
        except (TypeError, ValueError) as exc:
            raise invalid_request("limit must be an integer") from exc
        if limit < 1 or limit > MAX_LIMIT:
            raise invalid_request(f"limit must be in range [1, {MAX_LIMIT}]")

        filters = SearchFilters.from_payload(payload.get("filters"))
        return cls(query=query, limit=limit, filters=filters)


@dataclass(frozen=True)
class DocsSearchRequest:
    query: str
    limit: int = DOCS_DEFAULT_LIMIT
    workspace_path: str | None = None

    @classmethod
    def from_payload(cls, payload: Any) -> "DocsSearchRequest":
        if not isinstance(payload, dict):
            raise invalid_request("Request body must be a JSON object")
        query = str(payload.get("query", "")).strip()
        if not query:
            raise search_query_empty()

        raw_limit = payload.get("limit", DOCS_DEFAULT_LIMIT)
        try:
            limit = int(raw_limit)
        except (TypeError, ValueError) as exc:
            raise invalid_request("limit must be an integer") from exc
        if limit < 1 or limit > DOCS_MAX_LIMIT:
            raise invalid_request(f"limit must be in range [1, {DOCS_MAX_LIMIT}]")

        workspace_path = _normalize_optional_text(payload.get("workspacePath"))
        return cls(query=query, limit=limit, workspace_path=workspace_path)


@dataclass(frozen=True)
class SearchResult:
    result_id: str
    score: float
    snippet: str
    source_path: str
    file_type: str
    metadata_ref: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "resultId": self.result_id,
            "score": self.score,
            "snippet": self.snippet,
            "sourcePath": self.source_path,
            "fileType": self.file_type,
            "metadataRef": self.metadata_ref,
        }


@dataclass(frozen=True)
class DocumentSource:
    result_id: str
    content: str
    source_path: str
    chunk_index: int | None

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "resultId": self.result_id,
            "content": self.content,
            "sourcePath": self.source_path,
        }
        if self.chunk_index is not None:
            payload["chunkIndex"] = self.chunk_index
        return payload


@dataclass(frozen=True)
class DocumentMetadata:
    result_id: str
    file_name: str
    file_type: str
    source_path: str
    content_hash: str | None
    indexed_at: str | None

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "resultId": self.result_id,
            "fileName": self.file_name,
            "fileType": self.file_type,
            "sourcePath": self.source_path,
        }
        if self.content_hash:
            payload["contentHash"] = self.content_hash
        if self.indexed_at:
            payload["indexedAt"] = self.indexed_at
        return payload


def build_results_envelope(results: list[SearchResult], *, limit: int) -> dict[str, Any]:
    status = "ok" if results else "empty"
    return {
        "status": status,
        "results": [item.as_dict() for item in results],
        "meta": {
            "count": len(results),
            "limit": limit,
            "requestedAt": _now_iso(),
        },
    }


def build_source_envelope(source: DocumentSource) -> dict[str, Any]:
    return {"status": "ok", "source": source.as_dict(), "meta": {"requestedAt": _now_iso()}}


def build_metadata_envelope(metadata: DocumentMetadata) -> dict[str, Any]:
    return {"status": "ok", "metadata": metadata.as_dict(), "meta": {"requestedAt": _now_iso()}}


@dataclass(frozen=True)
class DocsSearchResultItem:
    document_path: str
    chunk_index: int
    snippet: str
    score: float
    source_type: str = "documentation"
    ranking_signals: dict[str, float] | None = None

    def as_dict(self) -> dict[str, Any]:
        ranking = self.ranking_signals or {"lexical": 0.0, "semantic": 0.0}
        return {
            "documentPath": self.document_path,
            "chunkIndex": self.chunk_index,
            "snippet": self.snippet,
            "score": self.score,
            "sourceType": self.source_type,
            "rankingSignals": {
                "lexical": float(ranking.get("lexical", 0.0)),
                "semantic": float(ranking.get("semantic", 0.0)),
            },
        }


def build_docs_results_envelope(*, query: str, results: list[DocsSearchResultItem]) -> dict[str, Any]:
    return {
        "query": query,
        "total": len(results),
        "appliedStrategy": "bm25_plus_vector_docs_only",
        "results": [item.as_dict() for item in results],
    }
