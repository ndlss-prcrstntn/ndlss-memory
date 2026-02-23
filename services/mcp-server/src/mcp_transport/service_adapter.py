from __future__ import annotations

import os
from datetime import datetime, timezone
from threading import Thread
from typing import Any

from ingestion_state import STATE as INGESTION_STATE
from mcp_transport.error_mapper import McpToolExecutionError
from search_errors import SearchApiError
from search_models import DocsSearchRequest, SemanticSearchRequest
from search_repository import QdrantSearchRepository
from search_service import SearchService


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class McpServiceAdapter:
    def __init__(self, search_service: SearchService | None = None) -> None:
        self._search_service = search_service or SearchService(QdrantSearchRepository.from_env())

    def semantic_search(self, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            request = SemanticSearchRequest.from_payload(payload)
            return self._search_service.semantic_search(request)
        except SearchApiError:
            raise
        except Exception as exc:
            raise McpToolExecutionError(
                error_code="INVALID_REQUEST",
                message="Invalid semantic search request",
                details=str(exc),
                retryable=False,
                jsonrpc_code=-32602,
                http_status=400,
            ) from exc

    def docs_search(self, payload: dict[str, Any]) -> dict[str, Any]:
        try:
            normalized_payload: dict[str, Any] = {
                "query": payload.get("query"),
                "limit": payload.get("limit", 10),
            }
            if payload.get("workspacePath") is not None:
                normalized_payload["workspacePath"] = payload.get("workspacePath")
            request = DocsSearchRequest.from_payload(normalized_payload)
            return self._search_service.docs_search(request)
        except SearchApiError:
            raise
        except Exception as exc:
            raise McpToolExecutionError(
                error_code="INVALID_REQUEST",
                message="Invalid docs search request",
                details=str(exc),
                retryable=False,
                jsonrpc_code=-32602,
                http_status=400,
            ) from exc

    def get_source(self, result_id: str) -> dict[str, Any]:
        if not result_id.strip():
            raise McpToolExecutionError(
                error_code="INVALID_REQUEST",
                message="resultId must not be empty",
                retryable=False,
                jsonrpc_code=-32602,
                http_status=400,
            )
        return self._search_service.get_source(result_id.strip())

    def get_metadata(self, result_id: str) -> dict[str, Any]:
        if not result_id.strip():
            raise McpToolExecutionError(
                error_code="INVALID_REQUEST",
                message="resultId must not be empty",
                retryable=False,
                jsonrpc_code=-32602,
                http_status=400,
            )
        return self._search_service.get_metadata(result_id.strip())

    def start_ingestion(self, payload: dict[str, Any]) -> dict[str, Any]:
        workspace_path = str(payload.get("workspacePath") or os.getenv("WORKSPACE_PATH", "/workspace"))
        try:
            run = INGESTION_STATE.create_run(workspace_path=workspace_path)
        except RuntimeError as exc:
            raise McpToolExecutionError(
                error_code="INGESTION_ALREADY_RUNNING",
                message="Ingestion run is already running",
                retryable=True,
                jsonrpc_code=-32009,
                http_status=409,
            ) from exc

        Thread(target=self._run_ingestion_job, args=(run.run_id, workspace_path, payload), daemon=True).start()
        return {"runId": run.run_id, "status": run.status, "acceptedAt": run.accepted_at}

    def get_ingestion_status(self, payload: dict[str, Any]) -> dict[str, Any]:
        run_id = str(payload.get("runId") or "").strip()
        if not run_id:
            raise McpToolExecutionError(
                error_code="INVALID_REQUEST",
                message="runId is required",
                retryable=False,
                jsonrpc_code=-32602,
                http_status=400,
            )
        run = INGESTION_STATE.get_run(run_id)
        if run is None:
            raise McpToolExecutionError(
                error_code="RUN_NOT_FOUND",
                message=f"Ingestion run '{run_id}' is not found",
                retryable=False,
                jsonrpc_code=-32004,
                http_status=404,
            )
        return run.as_status()

    def _run_ingestion_job(self, run_id: str, workspace_path: str, payload: dict[str, Any]) -> None:
        run = INGESTION_STATE.get_run(run_id)
        if not run:
            return

        def _progress_update(progress: dict[str, int]) -> None:
            INGESTION_STATE.update_run(
                run_id,
                total_files=progress.get("totalFiles", run.total_files),
                total_chunks=progress.get("totalChunks", run.total_chunks),
                embedded_chunks=progress.get("embeddedChunks", run.embedded_chunks),
                failed_chunks=progress.get("failedChunks", run.failed_chunks),
                retry_count=progress.get("retryCount", run.retry_count),
            )

        try:
            from ingestion_pipeline.chunk_models import ChunkingConfig
            from ingestion_pipeline.ingestion_service import IngestionService

            effective_chunk_size = int(payload.get("chunkSize") or os.getenv("INGESTION_CHUNK_SIZE", "800"))
            effective_overlap = int(payload.get("chunkOverlap") or os.getenv("INGESTION_CHUNK_OVERLAP", "120"))
            effective_attempts = int(payload.get("retryMaxAttempts") or os.getenv("INGESTION_RETRY_MAX_ATTEMPTS", "3"))
            effective_backoff = float(os.getenv("INGESTION_RETRY_BACKOFF_SECONDS", "1.0"))

            config = ChunkingConfig(
                chunk_size=effective_chunk_size,
                chunk_overlap=effective_overlap,
                retry_max_attempts=effective_attempts,
                retry_backoff_seconds=effective_backoff,
            )
            config.validate()
            service = IngestionService(config=config)
            summary = service.run(run_id=run_id, workspace_path=workspace_path, progress_callback=_progress_update)
            summary_payload = summary.to_dict()
            INGESTION_STATE.finish_run(run_id, summary=summary_payload, status=summary_payload.get("status", "completed"))
        except Exception as exc:
            failure = {
                "runId": run_id,
                "status": "failed",
                "totalFiles": run.total_files,
                "totalChunks": run.total_chunks,
                "embeddedChunks": run.embedded_chunks,
                "failedChunks": run.failed_chunks + 1,
                "retryCount": run.retry_count,
                "startedAt": run.started_at or _now_iso(),
                "finishedAt": _now_iso(),
                "metadataCoverage": {
                    "path": 0,
                    "fileName": 0,
                    "fileType": 0,
                    "contentHash": 0,
                    "timestamp": 0,
                },
            }
            INGESTION_STATE.update_run(run_id, error_code="INGESTION_PIPELINE_FAILED", error_message=str(exc))
            INGESTION_STATE.finish_run(run_id, summary=failure, status="failed")

