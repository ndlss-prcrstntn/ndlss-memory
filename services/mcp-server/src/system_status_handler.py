import fnmatch
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from threading import Thread

import yaml
from flask import Flask, jsonify, request

from command_audit_store import CommandAuditStore
from command_execution_errors import CommandExecutionError, json_error_from_exception as command_json_error_from_exception
from command_execution_models import CommandExecutionRequest
from command_execution_service import CommandExecutionService
from command_execution_state import STATE as COMMAND_EXECUTION_STATE
from command_process_runner import CommandProcessRunner
from command_security_policy import load_command_security_policy
from delta_after_commit_errors import json_error as delta_json_error
from delta_after_commit_state import STATE as DELTA_STATE
from full_scan_errors import json_error as full_scan_json_error
from full_scan_state import STATE as FULL_SCAN_STATE
from idempotency_errors import json_error as idempotency_json_error
from idempotency_state import STATE as IDEMPOTENCY_STATE
from ingestion_errors import classify_pipeline_exception, json_error as ingestion_json_error
from ingestion_state import STATE as INGESTION_STATE
from mcp_transport import register_mcp_transport_routes
from search_errors import SearchApiError, json_error_from_exception as search_json_error_from_exception
from search_models import SemanticSearchRequest
from search_repository import QdrantSearchRepository
from search_service import SearchService
from startup_preflight_checks import run_startup_preflight
from startup_preflight_errors import StartupPreflightError, build_startup_failure_report
from startup_readiness_summary import build_startup_readiness_summary
from startup_preflight_state import STATE as STARTUP_PREFLIGHT_STATE

SERVICE_NAMES = ("qdrant", "file-indexer", "mcp-server")
STATUS_ENV_MAP = {
    "qdrant": "SERVICE_QDRANT_STATUS",
    "file-indexer": "SERVICE_FILE_INDEXER_STATUS",
    "mcp-server": "SERVICE_MCP_SERVER_STATUS",
}

app = Flask(__name__)
SEARCH_SERVICE = SearchService(QdrantSearchRepository.from_env())
COMMAND_EXECUTION_SERVICE: CommandExecutionService | None = None
MCP_DISPATCHER = register_mcp_transport_routes(app)

API_COMMANDS = [
    {
        "category": "system",
        "method": "GET",
        "path": "/health",
        "description": "Service health check",
    },
    {
        "category": "system",
        "method": "GET",
        "path": "/v1/system/status",
        "description": "Overall system and service statuses",
    },
    {
        "category": "system",
        "method": "GET",
        "path": "/v1/system/config",
        "description": "Effective runtime configuration",
    },
    {
        "category": "system",
        "method": "GET",
        "path": "/v1/system/startup/readiness",
        "description": "Startup preflight readiness summary",
    },
    {
        "category": "system",
        "method": "GET",
        "path": "/v1/system/services/{serviceName}",
        "description": "Status for a specific service",
    },
    {
        "category": "mcp",
        "method": "POST",
        "path": "/mcp",
        "description": "MCP streamable HTTP JSON-RPC endpoint",
    },
    {
        "category": "mcp",
        "method": "GET",
        "path": "/sse",
        "description": "MCP legacy SSE endpoint",
    },
    {
        "category": "mcp",
        "method": "POST",
        "path": "/messages",
        "description": "MCP SSE message endpoint",
    },
    {
        "category": "mcp",
        "method": "GET",
        "path": "/.well-known/mcp",
        "description": "MCP discovery endpoint",
    },
    {
        "category": "search",
        "method": "POST",
        "path": "/v1/search/semantic",
        "description": "Run semantic search over indexed chunks",
    },
    {
        "category": "search",
        "method": "GET",
        "path": "/v1/search/results/{resultId}/source",
        "description": "Resolve source text for a search result",
    },
    {
        "category": "search",
        "method": "GET",
        "path": "/v1/search/results/{resultId}/metadata",
        "description": "Resolve metadata for a search result",
    },
    {
        "category": "commands",
        "method": "POST",
        "path": "/v1/commands/execute",
        "description": "Execute an allowed command in workspace",
    },
    {
        "category": "commands",
        "method": "GET",
        "path": "/v1/commands/executions/{requestId}",
        "description": "Get command execution result by request id",
    },
    {
        "category": "commands",
        "method": "GET",
        "path": "/v1/commands/audit",
        "description": "List command audit records",
    },
    {
        "category": "indexing",
        "method": "POST",
        "path": "/v1/indexing/full-scan/jobs",
        "description": "Start full-scan job",
    },
    {
        "category": "indexing",
        "method": "GET",
        "path": "/v1/indexing/full-scan/jobs/{jobId}",
        "description": "Get full-scan job progress",
    },
    {
        "category": "indexing",
        "method": "GET",
        "path": "/v1/indexing/full-scan/jobs/{jobId}/summary",
        "description": "Get full-scan job summary",
    },
    {
        "category": "indexing",
        "method": "POST",
        "path": "/v1/indexing/ingestion/jobs",
        "description": "Start ingestion job",
    },
    {
        "category": "indexing",
        "method": "GET",
        "path": "/v1/indexing/ingestion/jobs/{runId}",
        "description": "Get ingestion job progress",
    },
    {
        "category": "indexing",
        "method": "GET",
        "path": "/v1/indexing/ingestion/jobs/{runId}/summary",
        "description": "Get ingestion job summary",
    },
    {
        "category": "indexing",
        "method": "POST",
        "path": "/v1/indexing/idempotency/jobs",
        "description": "Start idempotency sync job",
    },
    {
        "category": "indexing",
        "method": "GET",
        "path": "/v1/indexing/idempotency/jobs/{runId}",
        "description": "Get idempotency sync progress",
    },
    {
        "category": "indexing",
        "method": "GET",
        "path": "/v1/indexing/idempotency/jobs/{runId}/summary",
        "description": "Get idempotency sync summary",
    },
    {
        "category": "indexing",
        "method": "POST",
        "path": "/v1/indexing/delta-after-commit/jobs",
        "description": "Start delta-after-commit job",
    },
    {
        "category": "indexing",
        "method": "GET",
        "path": "/v1/indexing/delta-after-commit/jobs/{runId}",
        "description": "Get delta-after-commit job progress",
    },
    {
        "category": "indexing",
        "method": "GET",
        "path": "/v1/indexing/delta-after-commit/jobs/{runId}/summary",
        "description": "Get delta-after-commit job summary",
    },
]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _split_csv(value: str) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _parse_int_env(name: str, default: int) -> int:
    value = os.getenv(name, str(default))
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _ensure_file_indexer_src_path() -> None:
    candidates = [
        Path("/workspace/services/file-indexer/src"),
        Path(__file__).resolve().parents[2] / "file-indexer" / "src",
    ]
    explicit = os.getenv("FILE_INDEXER_SRC_PATH", "")
    if explicit:
        candidates.insert(0, Path(explicit))
    for candidate in candidates:
        if candidate.exists():
            as_text = str(candidate)
            if as_text not in sys.path:
                sys.path.insert(0, as_text)
            break


def load_security_policy() -> dict:
    path = "/app/config/security-policy.yaml"
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_command_execution_service() -> CommandExecutionService:
    global COMMAND_EXECUTION_SERVICE
    if COMMAND_EXECUTION_SERVICE is not None:
        return COMMAND_EXECUTION_SERVICE

    security_policy = load_security_policy()
    command_policy = load_command_security_policy(security_policy=security_policy)
    runner = CommandProcessRunner(
        cpu_time_limit_seconds=command_policy.cpu_time_limit_seconds,
        memory_limit_bytes=command_policy.memory_limit_bytes,
    )
    COMMAND_EXECUTION_SERVICE = CommandExecutionService(
        policy=command_policy,
        state=COMMAND_EXECUTION_STATE,
        runner=runner,
        audit_store=CommandAuditStore(
            audit_log_path=command_policy.audit_log_path,
            retention_days=command_policy.audit_retention_days,
        ),
    )
    return COMMAND_EXECUTION_SERVICE


def _is_excluded(path: Path, patterns: list[str]) -> bool:
    path_str = str(path).replace("\\", "/")
    for pattern in patterns:
        normalized = pattern.strip()
        if not normalized:
            continue
        if fnmatch.fnmatch(path_str, normalized) or f"/{normalized}/" in f"/{path_str}/":
            return True
    return False


def _run_full_scan_job(job_id: str) -> None:
    job = FULL_SCAN_STATE.get_job(job_id)
    if not job:
        return

    workspace = Path(job.workspace_path)
    supported_types = {s.lower() for s in _split_csv(os.getenv("INDEX_FILE_TYPES", ".md,.txt,.json,.yml,.yaml"))}
    excluded_patterns = _split_csv(os.getenv("INDEX_EXCLUDE_PATTERNS", ".git,node_modules,dist,build"))
    max_file_size = job.max_file_size_bytes

    if not workspace.exists() or not workspace.is_dir():
        FULL_SCAN_STATE.update_job(job_id, error_delta=1)
        FULL_SCAN_STATE.finish_job(job_id, "failed")
        return

    files = [path for path in workspace.rglob("*") if path.is_file()]
    total = len(files)
    if total == 0:
        FULL_SCAN_STATE.finish_job(job_id, "completed")
        return

    for idx, file_path in enumerate(files, start=1):
        rel_path = file_path.relative_to(workspace)
        ext = file_path.suffix.lower()
        percent = round((idx * 100.0) / total, 2)

        if _is_excluded(rel_path, excluded_patterns):
            FULL_SCAN_STATE.update_job(
                job_id,
                processed_delta=1,
                skip_delta=1,
                skip_reason="EXCLUDED_BY_PATTERN",
                percent_complete=percent,
            )
            continue

        if ext not in supported_types:
            FULL_SCAN_STATE.update_job(job_id, processed_delta=1, skip_delta=1, skip_reason="UNSUPPORTED_TYPE", percent_complete=percent)
            continue

        try:
            size = file_path.stat().st_size
        except OSError:
            FULL_SCAN_STATE.update_job(
                job_id,
                processed_delta=1,
                skip_delta=1,
                error_delta=1,
                skip_reason="READ_ERROR",
                percent_complete=percent,
            )
            continue

        if size == 0:
            FULL_SCAN_STATE.update_job(job_id, processed_delta=1, skip_delta=1, skip_reason="EMPTY_FILE", percent_complete=percent)
            continue

        if size > max_file_size:
            FULL_SCAN_STATE.update_job(job_id, processed_delta=1, skip_delta=1, skip_reason="FILE_TOO_LARGE", percent_complete=percent)
            continue

        try:
            file_path.read_bytes()
            FULL_SCAN_STATE.update_job(job_id, processed_delta=1, indexed_delta=1, percent_complete=percent)
        except OSError:
            FULL_SCAN_STATE.update_job(
                job_id,
                processed_delta=1,
                skip_delta=1,
                error_delta=1,
                skip_reason="READ_ERROR",
                percent_complete=percent,
            )

    FULL_SCAN_STATE.finish_job(job_id, "completed")


def _run_ingestion_job(run_id: str, workspace_path: str, payload: dict) -> None:
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
        _ensure_file_indexer_src_path()
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
        error_code, error_message = classify_pipeline_exception(exc)
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
            "errorCode": error_code,
            "errorMessage": error_message,
        }
        INGESTION_STATE.update_run(run_id, error_code=error_code, error_message=error_message)
        INGESTION_STATE.finish_run(run_id, summary=failure, status="failed")


def _run_idempotency_job(run_id: str, workspace_path: str, payload: dict) -> None:
    run = IDEMPOTENCY_STATE.get_run(run_id)
    if not run:
        return

    def _progress_update(progress: dict[str, int]) -> None:
        IDEMPOTENCY_STATE.update_run(
            run_id,
            total_files=progress.get("totalFiles", run.total_files),
            updated_chunks=progress.get("updatedChunks", run.updated_chunks),
            skipped_chunks=progress.get("skippedChunks", run.skipped_chunks),
            deleted_chunks=progress.get("deletedChunks", run.deleted_chunks),
            failed_chunks=progress.get("failedChunks", run.failed_chunks),
        )

    try:
        _ensure_file_indexer_src_path()
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
        summary = service.run_idempotency_sync(run_id=run_id, workspace_path=workspace_path, progress_callback=_progress_update)
        summary_payload = summary.to_dict()
        IDEMPOTENCY_STATE.finish_run(run_id, summary=summary_payload, status=summary_payload.get("status", "completed"))
    except Exception as exc:
        failure = {
            "runId": run_id,
            "status": "failed",
            "totalFiles": run.total_files,
            "updatedChunks": run.updated_chunks,
            "skippedChunks": run.skipped_chunks,
            "deletedChunks": run.deleted_chunks,
            "failedChunks": run.failed_chunks + 1,
            "startedAt": run.started_at or _now_iso(),
            "finishedAt": _now_iso(),
            "reasonBreakdown": [{"code": "IDEMPOTENCY_PIPELINE_FAILED", "count": 1}],
        }
        IDEMPOTENCY_STATE.update_run(run_id, error_code="IDEMPOTENCY_PIPELINE_FAILED", error_message=str(exc))
        IDEMPOTENCY_STATE.finish_run(run_id, summary=failure, status="failed")


def _run_delta_after_commit_job(run_id: str, workspace_path: str, payload: dict) -> None:
    run = DELTA_STATE.get_run(run_id)
    if not run:
        return

    base_ref = str(payload.get("baseRef") or run.base_ref or os.getenv("DELTA_GIT_BASE_REF", "HEAD~1"))
    target_ref = str(payload.get("targetRef") or run.target_ref or os.getenv("DELTA_GIT_TARGET_REF", "HEAD"))

    def _progress_update(progress: dict[str, int | str | None]) -> None:
        DELTA_STATE.update_run(
            run_id,
            effective_mode=str(progress.get("effectiveMode") or run.effective_mode),
            fallback_reason_code=progress.get("fallbackReasonCode"),
            added_files=int(progress.get("addedFiles") or run.added_files),
            modified_files=int(progress.get("modifiedFiles") or run.modified_files),
            deleted_files=int(progress.get("deletedFiles") or run.deleted_files),
            renamed_files=int(progress.get("renamedFiles") or run.renamed_files),
            indexed_files=int(progress.get("indexedFiles") or run.indexed_files),
            removed_records=int(progress.get("removedRecords") or run.removed_records),
            skipped_files=int(progress.get("skippedFiles") or run.skipped_files),
            failed_files=int(progress.get("failedFiles") or run.failed_files),
        )

    try:
        _ensure_file_indexer_src_path()
        from delta_after_commit.delta_after_commit_service import run_delta_after_commit_pipeline

        summary = run_delta_after_commit_pipeline(
            run_id=run_id,
            workspace_path=workspace_path,
            base_ref=base_ref,
            target_ref=target_ref,
            progress_callback=_progress_update,
        )
        summary_payload = summary.to_dict()
        DELTA_STATE.finish_run(run_id, summary=summary_payload, status=summary_payload.get("status", "completed"))
    except Exception as exc:
        failure = {
            "runId": run_id,
            "status": "failed",
            "requestedMode": "delta-after-commit",
            "effectiveMode": "delta-after-commit",
            "baseRef": base_ref,
            "targetRef": target_ref,
            "addedFiles": run.added_files,
            "modifiedFiles": run.modified_files,
            "deletedFiles": run.deleted_files,
            "renamedFiles": run.renamed_files,
            "indexedFiles": run.indexed_files,
            "removedRecords": run.removed_records,
            "skippedFiles": run.skipped_files,
            "failedFiles": run.failed_files + 1,
            "startedAt": run.started_at or _now_iso(),
            "finishedAt": _now_iso(),
            "reasonBreakdown": [{"code": "DELTA_PIPELINE_FAILED", "count": 1}],
        }
        DELTA_STATE.update_run(run_id, error_code="DELTA_PIPELINE_FAILED", error_message=str(exc))
        DELTA_STATE.finish_run(run_id, summary=failure, status="failed")


def build_runtime_config() -> dict:
    policy = load_security_policy()
    command_policy = load_command_security_policy(security_policy=policy)
    timeout_value = os.getenv("COMMAND_TIMEOUT_SECONDS", str(policy.get("command_timeout_seconds", 20)))
    allowlist_env = os.getenv("COMMAND_ALLOWLIST", "")
    allowlist_cfg = policy.get("command_allowlist", [])
    allowlist = _split_csv(allowlist_env) if allowlist_env else allowlist_cfg
    index_file_types = _split_csv(os.getenv("INDEX_FILE_TYPES", ".md,.txt,.json,.yml,.yaml"))
    index_exclude_patterns = _split_csv(os.getenv("INDEX_EXCLUDE_PATTERNS", ".git,node_modules,dist,build"))
    max_size = _parse_int_env("INDEX_MAX_FILE_SIZE_BYTES", 1048576)
    progress_interval = _parse_int_env("INDEX_PROGRESS_INTERVAL_SECONDS", 15)
    return {
        "projectName": os.getenv("COMPOSE_PROJECT_NAME", "ndlss-memory"),
        "qdrantPort": int(os.getenv("QDRANT_PORT", "6333")),
        "qdrantApiPort": int(os.getenv("QDRANT_API_PORT", "6333")),
        "qdrantHost": os.getenv("QDRANT_HOST", "qdrant"),
        "mcpPort": int(os.getenv("MCP_PORT", "8080")),
        "indexMode": os.getenv("INDEX_MODE", "full-scan"),
        "indexFileTypes": index_file_types,
        "indexExcludePatterns": index_exclude_patterns,
        "indexMaxFileSizeBytes": max_size,
        "indexProgressIntervalSeconds": progress_interval,
        "ingestionChunkSize": _parse_int_env("INGESTION_CHUNK_SIZE", 800),
        "ingestionChunkOverlap": _parse_int_env("INGESTION_CHUNK_OVERLAP", 120),
        "ingestionRetryMaxAttempts": _parse_int_env("INGESTION_RETRY_MAX_ATTEMPTS", 3),
        "ingestionRetryBackoffSeconds": float(os.getenv("INGESTION_RETRY_BACKOFF_SECONDS", "1.0")),
        "ingestionEnableQdrantHttp": os.getenv("INGESTION_ENABLE_QDRANT_HTTP", "1"),
        "ingestionUpsertTimeoutSeconds": float(os.getenv("INGESTION_UPSERT_TIMEOUT_SECONDS", "5")),
        "ingestionEmbeddingVectorSize": _parse_int_env("INGESTION_EMBEDDING_VECTOR_SIZE", 16),
        "deltaGitBaseRef": os.getenv("DELTA_GIT_BASE_REF", "HEAD~1"),
        "deltaGitTargetRef": os.getenv("DELTA_GIT_TARGET_REF", "HEAD"),
        "deltaIncludeRenames": os.getenv("DELTA_INCLUDE_RENAMES", "1"),
        "deltaEnableFallback": os.getenv("DELTA_ENABLE_FALLBACK", "1"),
        "deltaBootstrapOnStart": os.getenv("DELTA_BOOTSTRAP_ON_START", "0"),
        "idempotencyHashAlgorithm": os.getenv("IDEMPOTENCY_HASH_ALGORITHM", "sha256"),
        "idempotencySkipUnchanged": os.getenv("IDEMPOTENCY_SKIP_UNCHANGED", "1"),
        "idempotencyEnableStaleCleanup": os.getenv("IDEMPOTENCY_ENABLE_STALE_CLEANUP", "1"),
        "fullScanFilters": {
            "supportedTypes": index_file_types,
            "excludePatterns": index_exclude_patterns,
            "maxFileSizeBytes": max_size,
        },
        "commandAllowlist": allowlist,
        "commandTimeoutSeconds": int(timeout_value),
        "commandRunAsNonRoot": command_policy.run_as_non_root,
        "commandCpuTimeLimitSeconds": command_policy.cpu_time_limit_seconds,
        "commandMemoryLimitBytes": command_policy.memory_limit_bytes,
        "commandAuditRetentionDays": command_policy.audit_retention_days,
        "startupPreflightEnabled": os.getenv("STARTUP_PREFLIGHT_ENABLED", "1"),
        "startupPreflightTimeoutSeconds": float(os.getenv("STARTUP_PREFLIGHT_TIMEOUT_SECONDS", "3")),
        "startupPreflightRequireGitForDelta": os.getenv("STARTUP_PREFLIGHT_REQUIRE_GIT_FOR_DELTA", "1"),
        "startupReadySummaryLogEnabled": os.getenv("STARTUP_READY_SUMMARY_LOG_ENABLED", "1"),
        "mcpEndpointPath": os.getenv("MCP_ENDPOINT_PATH", "/mcp"),
        "startupReadiness": STARTUP_PREFLIGHT_STATE.get_readiness_summary()
        or {
            "status": "not-ready",
            "failureReport": STARTUP_PREFLIGHT_STATE.get_failure_report(),
        },
    }


def build_ingestion_persistence_diagnostics() -> dict:
    return {
        "qdrantHost": os.getenv("QDRANT_HOST", "qdrant"),
        "qdrantApiPort": int(os.getenv("QDRANT_API_PORT", "6333")),
        "qdrantExternalPort": int(os.getenv("QDRANT_PORT", "6333")),
        "ingestionEnableQdrantHttp": os.getenv("INGESTION_ENABLE_QDRANT_HTTP", "1"),
        "ingestionUpsertTimeoutSeconds": float(os.getenv("INGESTION_UPSERT_TIMEOUT_SECONDS", "5")),
        "ingestionEmbeddingVectorSize": _parse_int_env("INGESTION_EMBEDDING_VECTOR_SIZE", 16),
    }


def build_service_status(name: str) -> dict:
    env_key = STATUS_ENV_MAP[name]
    status = os.getenv(env_key, "healthy")
    return {
        "name": name,
        "status": status,
        "lastCheck": _now_iso(),
        "details": f"Service '{name}' reported by runtime status map",
    }


def build_system_status() -> dict:
    services = [build_service_status(name) for name in SERVICE_NAMES]
    statuses = {item["status"] for item in services}
    if statuses == {"healthy"}:
        overall = "healthy"
        issues = []
    elif "healthy" in statuses:
        overall = "degraded"
        issues = ["One or more services are not healthy"]
    else:
        overall = "down"
        issues = ["No healthy services detected"]
    return {
        "timestamp": _now_iso(),
        "overallStatus": overall,
        "services": services,
        "issues": issues,
    }



def _should_run_startup_preflight() -> bool:
    return os.getenv("STARTUP_PREFLIGHT_ENABLED", "1").strip().lower() in {"1", "true", "yes", "on"}


def _should_log_startup_summary() -> bool:
    return os.getenv("STARTUP_READY_SUMMARY_LOG_ENABLED", "1").strip().lower() in {"1", "true", "yes", "on"}


def _build_startup_service_readiness() -> dict[str, str]:
    payload: dict[str, str] = {}
    for service_name in SERVICE_NAMES:
        current_status = build_service_status(service_name)["status"]
        key = {
            "qdrant": "qdrant",
            "file-indexer": "fileIndexer",
            "mcp-server": "mcpServer",
        }[service_name]
        payload[key] = current_status
    return payload


def _run_startup_preflight_or_exit() -> None:
    STARTUP_PREFLIGHT_STATE.reset()
    if not _should_run_startup_preflight():
        return

    try:
        context, checks = run_startup_preflight()
        summary = build_startup_readiness_summary(
            context=context,
            checks=checks,
            service_readiness=_build_startup_service_readiness(),
        )
        STARTUP_PREFLIGHT_STATE.mark_ready(summary)
        if _should_log_startup_summary():
            print(
                json.dumps(
                    {
                        "event": "startup-ready",
                        "summary": summary,
                    },
                    ensure_ascii=False,
                )
            )
    except StartupPreflightError as exc:
        report = exc.to_failure_report()
        STARTUP_PREFLIGHT_STATE.mark_failed(report)
        print(json.dumps({"event": "startup-preflight-failed", "report": report}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
@app.get("/health")
def get_health():
    return jsonify({"status": "ok", "timestamp": _now_iso()})


@app.get("/")
def get_root_commands():
    return jsonify(
        {
            "service": "ndlss-memory-mcp-server",
            "status": "ok",
            "timestamp": _now_iso(),
            "commands": API_COMMANDS,
        }
    )


@app.get("/v1/system/status")
def get_system_status():
    return jsonify(build_system_status())


@app.get("/v1/system/config")
def get_runtime_config():
    return jsonify(build_runtime_config())


@app.get("/v1/system/startup/readiness")
def get_startup_readiness():
    readiness = STARTUP_PREFLIGHT_STATE.get_readiness_summary()
    if readiness is not None:
        return jsonify(readiness)

    failure_report = STARTUP_PREFLIGHT_STATE.get_failure_report()
    if failure_report is not None:
        return jsonify(failure_report), 503

    payload = build_startup_failure_report(
        error_code="STARTUP_NOT_READY",
        message="Startup preflight is not completed",
        failed_checks=[],
        details={"hint": "Service may still be booting or preflight is disabled"},
    )
    return jsonify(payload), 503


@app.get("/v1/system/services/<service_name>")
def get_service_status(service_name: str):
    if service_name not in SERVICE_NAMES:
        return (
            jsonify(
                {
                    "errorCode": "SERVICE_NOT_FOUND",
                    "message": f"Service '{service_name}' is not registered",
                    "details": "Available services: qdrant, file-indexer, mcp-server",
                }
            ),
            404,
        )
    return jsonify(build_service_status(service_name))


@app.post("/v1/search/semantic")
def semantic_search():
    payload = request.get_json(silent=True) or {}
    try:
        search_request = SemanticSearchRequest.from_payload(payload)
        return jsonify(SEARCH_SERVICE.semantic_search(search_request))
    except SearchApiError as exc:
        return search_json_error_from_exception(exc)


@app.get("/v1/search/results/<result_id>/source")
def get_search_result_source(result_id: str):
    try:
        return jsonify(SEARCH_SERVICE.get_source(result_id))
    except SearchApiError as exc:
        return search_json_error_from_exception(exc)


@app.get("/v1/search/results/<result_id>/metadata")
def get_search_result_metadata(result_id: str):
    try:
        return jsonify(SEARCH_SERVICE.get_metadata(result_id))
    except SearchApiError as exc:
        return search_json_error_from_exception(exc)


@app.post("/v1/commands/execute")
def execute_command():
    payload = request.get_json(silent=True) or {}
    try:
        command_request = CommandExecutionRequest.from_payload(payload)
        result = get_command_execution_service().execute(command_request)
        return jsonify(result.to_response_envelope())
    except CommandExecutionError as exc:
        return command_json_error_from_exception(exc)


@app.get("/v1/commands/executions/<request_id>")
def get_command_execution_result(request_id: str):
    try:
        result = get_command_execution_service().get_result(request_id)
        return jsonify(result.to_response_envelope())
    except CommandExecutionError as exc:
        return command_json_error_from_exception(exc)


@app.get("/v1/commands/audit")
def get_command_audit():
    raw_limit = request.args.get("limit", "50")
    status = request.args.get("status")
    if status:
        status = status.strip()
    try:
        limit = int(raw_limit)
    except (TypeError, ValueError):
        return command_json_error_from_exception(CommandExecutionError("INVALID_REQUEST", "limit must be an integer", 400))
    try:
        response = get_command_execution_service().list_audit(limit=limit, status=status)
        return jsonify(response)
    except CommandExecutionError as exc:
        return command_json_error_from_exception(exc)


@app.post("/v1/indexing/full-scan/jobs")
def start_full_scan_job():
    payload = request.get_json(silent=True) or {}
    workspace_path = payload.get("workspacePath") or os.getenv("WORKSPACE_PATH", "/workspace")
    max_file_size = payload.get("maxFileSizeBytes")
    if max_file_size is None:
        max_file_size = _parse_int_env("INDEX_MAX_FILE_SIZE_BYTES", 1048576)

    try:
        max_file_size = int(max_file_size)
    except (TypeError, ValueError):
        return full_scan_json_error("INVALID_REQUEST", "maxFileSizeBytes must be an integer", 400)

    if max_file_size < 1:
        return full_scan_json_error("INVALID_REQUEST", "maxFileSizeBytes must be >= 1", 400)

    try:
        job = FULL_SCAN_STATE.create_job(workspace_path=workspace_path, max_file_size_bytes=max_file_size)
    except RuntimeError:
        return full_scan_json_error("FULL_SCAN_ALREADY_RUNNING", "Full scan job is already running", 409)

    Thread(target=_run_full_scan_job, args=(job.job_id,), daemon=True).start()
    return jsonify({"jobId": job.job_id, "status": job.status, "acceptedAt": job.accepted_at}), 202


@app.get("/v1/indexing/full-scan/jobs/<job_id>")
def get_full_scan_job_progress(job_id: str):
    job = FULL_SCAN_STATE.get_job(job_id)
    if not job:
        return full_scan_json_error("JOB_NOT_FOUND", f"Full scan job '{job_id}' is not found", 404)
    return jsonify(job.as_progress())


@app.get("/v1/indexing/full-scan/jobs/<job_id>/summary")
def get_full_scan_job_summary(job_id: str):
    job = FULL_SCAN_STATE.get_job(job_id)
    if not job:
        return full_scan_json_error("JOB_NOT_FOUND", f"Full scan job '{job_id}' is not found", 404)
    if job.status in {"queued", "running"}:
        return full_scan_json_error("JOB_NOT_FINISHED", "Full scan job is not finished yet", 409)
    return jsonify(job.as_summary())


@app.post("/v1/indexing/ingestion/jobs")
def start_ingestion_job():
    payload = request.get_json(silent=True) or {}
    workspace_path = payload.get("workspacePath") or os.getenv("WORKSPACE_PATH", "/workspace")
    try:
        run = INGESTION_STATE.create_run(workspace_path=workspace_path)
    except RuntimeError:
        return ingestion_json_error("INGESTION_ALREADY_RUNNING", "Ingestion run is already running", 409)

    Thread(target=_run_ingestion_job, args=(run.run_id, workspace_path, payload), daemon=True).start()
    return jsonify({"runId": run.run_id, "status": run.status, "acceptedAt": run.accepted_at}), 202


@app.get("/v1/indexing/ingestion/jobs/<run_id>")
def get_ingestion_job_status(run_id: str):
    run = INGESTION_STATE.get_run(run_id)
    if not run:
        return ingestion_json_error("RUN_NOT_FOUND", f"Ingestion run '{run_id}' is not found", 404)
    payload = run.as_status()
    payload["persistence"] = build_ingestion_persistence_diagnostics()
    return jsonify(payload)


@app.get("/v1/indexing/ingestion/jobs/<run_id>/summary")
def get_ingestion_job_summary(run_id: str):
    run = INGESTION_STATE.get_run(run_id)
    if not run:
        return ingestion_json_error("RUN_NOT_FOUND", f"Ingestion run '{run_id}' is not found", 404)
    if run.status in {"queued", "running"}:
        return ingestion_json_error("RUN_NOT_FINISHED", "Ingestion run is not finished yet", 409)
    if run.summary is None:
        return ingestion_json_error("RUN_SUMMARY_MISSING", "Run summary is not available", 404)
    payload = dict(run.summary)
    payload["persistence"] = build_ingestion_persistence_diagnostics()
    return jsonify(payload)


@app.post("/v1/indexing/idempotency/jobs")
def start_idempotency_job():
    payload = request.get_json(silent=True) or {}
    workspace_path = payload.get("workspacePath") or os.getenv("WORKSPACE_PATH", "/workspace")
    try:
        run = IDEMPOTENCY_STATE.create_run(workspace_path=workspace_path)
    except RuntimeError:
        return idempotency_json_error("IDEMPOTENCY_ALREADY_RUNNING", "Idempotency sync run is already running", 409)

    Thread(target=_run_idempotency_job, args=(run.run_id, workspace_path, payload), daemon=True).start()
    return jsonify({"runId": run.run_id, "status": run.status, "acceptedAt": run.accepted_at}), 202


@app.get("/v1/indexing/idempotency/jobs/<run_id>")
def get_idempotency_job_status(run_id: str):
    run = IDEMPOTENCY_STATE.get_run(run_id)
    if not run:
        return idempotency_json_error("RUN_NOT_FOUND", f"Idempotency run '{run_id}' is not found", 404)
    return jsonify(run.as_status())


@app.get("/v1/indexing/idempotency/jobs/<run_id>/summary")
def get_idempotency_job_summary(run_id: str):
    run = IDEMPOTENCY_STATE.get_run(run_id)
    if not run:
        return idempotency_json_error("RUN_NOT_FOUND", f"Idempotency run '{run_id}' is not found", 404)
    if run.status in {"queued", "running"}:
        return idempotency_json_error("RUN_NOT_FINISHED", "Idempotency run is not finished yet", 409)
    if run.summary is None:
        return idempotency_json_error("RUN_SUMMARY_MISSING", "Run summary is not available", 404)
    return jsonify(run.summary)


@app.post("/v1/indexing/delta-after-commit/jobs")
def start_delta_after_commit_job():
    payload = request.get_json(silent=True) or {}
    workspace_path = payload.get("workspacePath") or os.getenv("WORKSPACE_PATH", "/workspace")
    base_ref = str(payload.get("baseRef") or os.getenv("DELTA_GIT_BASE_REF", "HEAD~1"))
    target_ref = str(payload.get("targetRef") or os.getenv("DELTA_GIT_TARGET_REF", "HEAD"))

    try:
        run = DELTA_STATE.create_run(workspace_path=workspace_path, base_ref=base_ref, target_ref=target_ref)
    except RuntimeError:
        return delta_json_error("DELTA_ALREADY_RUNNING", "Delta-after-commit run is already running", 409)

    Thread(target=_run_delta_after_commit_job, args=(run.run_id, workspace_path, payload), daemon=True).start()
    return (
        jsonify(
            {
                "runId": run.run_id,
                "status": run.status,
                "acceptedAt": run.accepted_at,
                "requestedMode": run.requested_mode,
            }
        ),
        202,
    )


@app.get("/v1/indexing/delta-after-commit/jobs/<run_id>")
def get_delta_after_commit_job_status(run_id: str):
    run = DELTA_STATE.get_run(run_id)
    if not run:
        return delta_json_error("RUN_NOT_FOUND", f"Delta-after-commit run '{run_id}' is not found", 404)
    return jsonify(run.as_status())


@app.get("/v1/indexing/delta-after-commit/jobs/<run_id>/summary")
def get_delta_after_commit_job_summary(run_id: str):
    run = DELTA_STATE.get_run(run_id)
    if not run:
        return delta_json_error("RUN_NOT_FOUND", f"Delta-after-commit run '{run_id}' is not found", 404)
    if run.status in {"queued", "running"}:
        return delta_json_error("RUN_NOT_FINISHED", "Delta-after-commit run is not finished yet", 409)
    if run.summary is None:
        return delta_json_error("RUN_SUMMARY_MISSING", "Run summary is not available", 404)
    return jsonify(run.summary)


if __name__ == "__main__":
    _run_startup_preflight_or_exit()
    port = int(os.getenv("MCP_PORT", "8080"))
    app.run(host="0.0.0.0", port=port)





