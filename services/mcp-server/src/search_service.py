from __future__ import annotations

from typing import Any

from search_errors import result_not_found
from search_models import (
    DocsSearchRequest,
    DocsSearchResultItem,
    DocumentMetadata,
    DocumentSource,
    SearchResult,
    SemanticSearchRequest,
    build_docs_results_envelope,
    build_metadata_envelope,
    build_results_envelope,
    build_source_envelope,
)
from search_repository import QdrantSearchRepository


class SearchService:
    def __init__(self, repository: QdrantSearchRepository) -> None:
        self._repository = repository

    def semantic_search(self, search_request: SemanticSearchRequest) -> dict[str, Any]:
        raw_results = self._repository.semantic_search(
            query=search_request.query,
            limit=search_request.limit,
            filters=search_request.filters,
        )
        results = [
            SearchResult(
                result_id=str(item["resultId"]),
                score=float(item["score"]),
                snippet=str(item.get("snippet", "")),
                source_path=str(item.get("sourcePath", "")),
                file_type=str(item.get("fileType", "")),
                metadata_ref=str(item.get("metadataRef", item["resultId"])),
            )
            for item in raw_results
        ]
        return build_results_envelope(results, limit=search_request.limit)

    def docs_search(self, search_request: DocsSearchRequest) -> dict[str, Any]:
        repository_payload = self._repository.docs_search(
            query=search_request.query,
            limit=search_request.limit,
        )
        if isinstance(repository_payload, dict):
            raw_results = repository_payload.get("results", [])
            applied_strategy = str(repository_payload.get("appliedStrategy", "bm25_plus_vector_rerank_docs_only"))
            fallback_applied = bool(repository_payload.get("fallbackApplied", False))
        else:
            raw_results = repository_payload
            applied_strategy = "bm25_plus_vector_rerank_docs_only"
            fallback_applied = False
        results = [
            DocsSearchResultItem(
                document_path=str(item.get("documentPath", "")),
                chunk_index=int(item.get("chunkIndex", 0)),
                snippet=str(item.get("snippet", "")),
                score=float(item.get("score", 0.0)),
                source_type=str(item.get("sourceType", "documentation")),
                ranking_signals=item.get("rankingSignals"),
            )
            for item in raw_results
        ]
        return build_docs_results_envelope(
            query=search_request.query,
            results=results,
            applied_strategy=applied_strategy,
            fallback_applied=fallback_applied,
        )

    def get_source(self, result_id: str) -> dict[str, Any]:
        payload = self._repository.get_source_by_result_id(result_id)
        if payload is None:
            raise result_not_found(result_id)
        source = DocumentSource(
            result_id=str(payload["resultId"]),
            content=str(payload.get("content", "")),
            source_path=str(payload.get("sourcePath", "")),
            chunk_index=payload.get("chunkIndex"),
        )
        return build_source_envelope(source)

    def get_metadata(self, result_id: str) -> dict[str, Any]:
        payload = self._repository.get_metadata_by_result_id(result_id)
        if payload is None:
            raise result_not_found(result_id)
        metadata = DocumentMetadata(
            result_id=str(payload["resultId"]),
            file_name=str(payload.get("fileName", "")),
            file_type=str(payload.get("fileType", "")),
            source_path=str(payload.get("sourcePath", "")),
            content_hash=str(payload.get("contentHash")) if payload.get("contentHash") is not None else None,
            indexed_at=str(payload.get("indexedAt")) if payload.get("indexedAt") is not None else None,
        )
        return build_metadata_envelope(metadata)

