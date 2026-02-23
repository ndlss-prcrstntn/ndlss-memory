import fnmatch
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from threading import Thread

import yaml
from flask import Flask, jsonify, request

from bootstrap_orchestrator import BootstrapOrchestrator
from bootstrap_state import build_workspace_key
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
from full_scan_state import LIMIT_DEPTH_EXCEEDED, LIMIT_MAX_FILES_REACHED, STATE as FULL_SCAN_STATE
from idempotency_errors import json_error as idempotency_json_error
from idempotency_state import STATE as IDEMPOTENCY_STATE
from indexing_run_limits import IndexingRunLimitValidationError, resolve_indexing_run_limits
from ingestion_errors import INVALID_LIMIT_VALUE as INGESTION_INVALID_LIMIT_VALUE
from ingestion_errors import classify_pipeline_exception, json_error as ingestion_json_error
from ingestion_state import STATE as INGESTION_STATE
from mcp_transport import register_mcp_transport_routes
from search_errors import SearchApiError, json_error_from_exception as search_json_error_from_exception
from search_models import DocsSearchRequest, SemanticSearchRequest
from search_repository import QdrantSearchRepository
from search_service import SearchService
from startup_preflight_checks import run_startup_preflight
from startup_preflight_errors import (
    StartupPreflightError,
    build_bootstrap_failure_report,
    build_startup_failure_report,
)
from startup_readiness_summary import build_startup_readiness_summary
from startup_preflight_state import STATE as STARTUP_PREFLIGHT_STATE
from watch_mode_orchestrator import WatchModeOrchestrator
from watch_mode_state import STATE as WATCH_STATE

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
BOOTSTRAP_ORCHESTRATOR = BootstrapOrchestrator()
STARTUP_PREFLIGHT_CONTEXT: dict | None = None
STARTUP_PREFLIGHT_CHECKS: list = []
WATCH_ORCHESTRATOR: WatchModeOrchestrator | None = None

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
        "method": "POST",
        "path": "/v1/search/docs/query",
        "description": "Run hybrid (BM25 + vector) docs-only search over documentation collection",
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
        "path": "/v1/indexing/docs/jobs",
        "description": "Start docs-only indexing job",
    },
    {
        "category": "indexing",
        "method": "GET",
        "path": "/v1/indexing/docs/jobs/{runId}/summary",
        "description": "Get docs-only indexing summary",
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
    {
        "category": "indexing",
        "method": "GET",
        "path": "/v1/indexing/watch/status",
        "description": "Get watch mode runtime status",
    },
    {
        "category": "indexing",
        "method": "GET",
        "path": "/v1/indexing/watch/summary",
        "description": "Get watch mode last batch summary",
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


def _parse_optional_int_env(name: str, minimum: int) -> int | None:
    raw = os.getenv(name, "")
    if raw is None or str(raw).strip() == "":
        return None
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return None
    if value < minimum:
        return None
    return value


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
            _evict_if_shadowed("ingestion_pipeline", candidate)
            _evict_if_shadowed("delta_after_commit", candidate)
            break


def _evict_if_shadowed(namespace: str, expected_root: Path) -> None:
    module = sys.modules.get(namespace)
    if module is None:
        return
    module_file = getattr(module, "__file__", None)
    if not module_file:
        return
    expected = str(expected_root.resolve())
    actual = str(Path(module_file).resolve())
    if os.path.normcase(actual).startswith(os.path.normcase(expected)):
        return
    prefix = f"{namespace}."
    for name in list(sys.modules.keys()):
        if name == namespace or name.startswith(prefix):
            del sys.modules[name]


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


def _is_watch_mode_enabled() -> bool:
    return os.getenv("INDEX_MODE", "full-scan") == "watch"


def get_watch_orchestrator() -> WatchModeOrchestrator:
    global WATCH_ORCHESTRATOR
    if WATCH_ORCHESTRATOR is None:
        WATCH_ORCHESTRATOR = WatchModeOrchestrator(
            workspace_path=os.getenv("WORKSPACE_PATH", "/workspace"),
            state=WATCH_STATE,
        )
    return WATCH_ORCHESTRATOR


def _start_watch_mode_if_needed() -> None:
    if not _is_watch_mode_enabled():
        return
    orchestrator = get_watch_orchestrator()
    started = orchestrator.start()
    if started:
        print(json.dumps({"event": "watch-loop-started", "workspacePath": os.getenv("WORKSPACE_PATH", "/workspace")}, ensure_ascii=False))


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

    files = sorted(
        (path for path in workspace.rglob("*") if path.is_file()),
        key=lambda path: str(path.relative_to(workspace)).replace("\\", "/"),
    )
    total = len(files)
    if total == 0:
        FULL_SCAN_STATE.finish_job(job_id, "completed")
        return

    selected_files = 0
    for idx, file_path in enumerate(files, start=1):
        rel_path = file_path.relative_to(workspace)
        ext = file_path.suffix.lower()
        percent = round((idx * 100.0) / total, 2)
        depth = max(len(rel_path.parts) - 1, 0)

        if job.max_traversal_depth is not None and depth > job.max_traversal_depth:
            FULL_SCAN_STATE.update_job(
                job_id,
                processed_delta=1,
                skip_delta=1,
                skip_reason=LIMIT_DEPTH_EXCEEDED,
                percent_complete=percent,
            )
            continue

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

        if job.max_files_per_run is not None and selected_files >= job.max_files_per_run:
            FULL_SCAN_STATE.update_job(
                job_id,
                processed_delta=1,
                skip_delta=1,
                skip_reason=LIMIT_MAX_FILES_REACHED,
                percent_complete=percent,
            )
            continue

        try:
            file_path.read_bytes()
            FULL_SCAN_STATE.update_job(job_id, processed_delta=1, indexed_delta=1, percent_complete=percent)
            selected_files += 1
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
        service = IngestionService(
            config=config,
            max_traversal_depth=run.max_traversal_depth,
            max_files_per_run=run.max_files_per_run,
        )
        summary = service.run(run_id=run_id, workspace_path=workspace_path, progress_callback=_progress_update)
        summary_payload = summary.to_dict()
        INGESTION_STATE.finish_run(run_id, summary=summary_payload, status=summary_payload.get("status", "completed"))
        finished = INGESTION_STATE.get_run(run_id)
        if finished and finished.bootstrap and finished.bootstrap.get("trigger") == "auto-startup":
            BOOTSTRAP_ORCHESTRATOR.on_ingestion_finished(
                run_id=run_id,
                workspace_path=workspace_path,
                status=summary_payload.get("status", "completed"),
                error_code=summary_payload.get("errorCode"),
                error_message=summary_payload.get("errorMessage"),
            )
            _update_startup_readiness_with_bootstrap()
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
            "appliedLimits": {
                "maxTraversalDepth": run.max_traversal_depth,
                "maxFilesPerRun": run.max_files_per_run,
            },
            "skipBreakdown": [],
            "errorCode": error_code,
            "errorMessage": error_message,
        }
        INGESTION_STATE.update_run(run_id, error_code=error_code, error_message=error_message)
        INGESTION_STATE.finish_run(run_id, summary=failure, status="failed")
        finished = INGESTION_STATE.get_run(run_id)
        if finished and finished.bootstrap and finished.bootstrap.get("trigger") == "auto-startup":
            BOOTSTRAP_ORCHESTRATOR.on_ingestion_finished(
                run_id=run_id,
                workspace_path=workspace_path,
                status="failed",
                error_code=error_code,
                error_message=error_message,
            )
            _update_startup_readiness_with_bootstrap()


def _run_docs_ingestion_job(run_id: str, workspace_path: str, payload: dict) -> None:
    run = INGESTION_STATE.get_run(run_id)
    if not run:
        return

    def _progress_update(progress: dict[str, int]) -> None:
        indexed = int(progress.get("indexedDocuments", 0))
        updated = int(progress.get("updatedDocuments", 0))
        deleted = int(progress.get("deletedDocuments", 0))
        INGESTION_STATE.update_run(
            run_id,
            total_files=int(progress.get("processedDocuments", run.total_files)),
            total_chunks=indexed + updated + deleted,
            embedded_chunks=indexed + updated,
            failed_chunks=int(progress.get("skippedDocuments", run.failed_chunks)),
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
        service = IngestionService(
            config=config,
            max_traversal_depth=run.max_traversal_depth,
            max_files_per_run=run.max_files_per_run,
        )
        include_extensions = payload.get("includeExtensions")
        if not isinstance(include_extensions, list):
            include_extensions = None
        summary = service.run_docs_index(
            run_id=run_id,
            workspace_path=workspace_path,
            include_extensions=include_extensions,
            progress_callback=_progress_update,
        )
        summary_payload = summary.to_dict()
        INGESTION_STATE.finish_run(run_id, summary=summary_payload, status=summary_payload.get("status", "completed"))
    except Exception as exc:
        error_code, error_message = classify_pipeline_exception(exc)
        failure = {
            "runId": run_id,
            "status": "failed",
            "totals": {
                "processedDocuments": run.total_files,
                "indexedDocuments": 0,
                "updatedDocuments": 0,
                "skippedDocuments": run.failed_chunks + 1,
                "deletedDocuments": 0,
            },
            "skipBreakdown": [{"code": "DOCS_INDEXING_FAILED", "count": 1}],
            "appliedLimits": {
                "maxTraversalDepth": run.max_traversal_depth,
                "maxFilesPerRun": run.max_files_per_run,
            },
            "startedAt": run.started_at or _now_iso(),
            "finishedAt": _now_iso(),
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


def _resolve_ready_status(bootstrap_status: str) -> str:
    if bootstrap_status == "running":
        return "running"
    if bootstrap_status in {"failed", "blocked"}:
        return "failed"
    return "ready"


def _update_startup_readiness_with_bootstrap() -> None:
    if STARTUP_PREFLIGHT_CONTEXT is None or not STARTUP_PREFLIGHT_CHECKS:
        return
    workspace_path = STARTUP_PREFLIGHT_CONTEXT.get("workspacePath", os.getenv("WORKSPACE_PATH", "/workspace"))
    bootstrap_payload = BOOTSTRAP_ORCHESTRATOR.get_bootstrap_payload(workspace_path)
    collection_payload = BOOTSTRAP_ORCHESTRATOR.get_collection_payload()
    bootstrap_error_code = str(bootstrap_payload.get("errorCode") or "BOOTSTRAP_RUNTIME_FAILED")
    bootstrap_reason = str(bootstrap_payload.get("reason") or "Bootstrap failed")
    bootstrap_failure = None
    if str(bootstrap_payload.get("status") or "").lower() == "failed":
        bootstrap_failure = build_bootstrap_failure_report(
            workspace_path=workspace_path,
            collection_name=str(collection_payload.get("collectionName") or STARTUP_PREFLIGHT_CONTEXT.get("collectionName", "workspace_chunks")),
            error_code=bootstrap_error_code,
            message=bootstrap_reason,
        )
    summary = build_startup_readiness_summary(
        context=STARTUP_PREFLIGHT_CONTEXT,
        checks=STARTUP_PREFLIGHT_CHECKS,
        service_readiness=_build_startup_service_readiness(),
        status=_resolve_ready_status(str(bootstrap_payload.get("status") or "ready")),
        bootstrap=bootstrap_payload,
        collection=collection_payload,
        bootstrap_failure=bootstrap_failure,
    )
    STARTUP_PREFLIGHT_STATE.mark_ready(summary)


def _start_ingestion_run(
    *,
    workspace_path: str,
    payload: dict,
    run_kind: str = "ingestion",
    runner=None,
    max_traversal_depth: int | None = None,
    max_files_per_run: int | None = None,
    bootstrap_context: dict | None = None,
):
    run = INGESTION_STATE.create_run(
        workspace_path=workspace_path,
        run_kind=run_kind,
        max_traversal_depth=max_traversal_depth,
        max_files_per_run=max_files_per_run,
        bootstrap=bootstrap_context,
    )
    if _is_watch_mode_enabled():
        INGESTION_STATE.update_run(run.run_id, watch_activity=WATCH_STATE.get_status())
    target = runner or _run_ingestion_job
    Thread(target=target, args=(run.run_id, workspace_path, payload), daemon=True).start()
    return run


def build_runtime_config() -> dict:
    policy = load_security_policy()
    command_policy = load_command_security_policy(security_policy=policy)
    timeout_value = os.getenv("COMMAND_TIMEOUT_SECONDS", str(policy.get("command_timeout_seconds", 20)))
    allowlist_env = os.getenv("COMMAND_ALLOWLIST", "")
    allowlist_cfg = policy.get("command_allowlist", [])
    allowlist = _split_csv(allowlist_env) if allowlist_env else allowlist_cfg
    index_file_types = _split_csv(os.getenv("INDEX_FILE_TYPES", ".md,.txt,.json,.yml,.yaml"))
    index_exclude_patterns = _split_csv(os.getenv("INDEX_EXCLUDE_PATTERNS", ".git,node_modules,dist,build"))
    docs_index_file_types = _split_csv(os.getenv("DOCS_INDEX_FILE_TYPES", ".md"))
    docs_index_exclude_patterns = _split_csv(os.getenv("DOCS_INDEX_EXCLUDE_PATTERNS", ".git,node_modules,dist,build"))
    max_size = _parse_int_env("INDEX_MAX_FILE_SIZE_BYTES", 1048576)
    max_traversal_depth = _parse_optional_int_env("INDEX_MAX_TRAVERSAL_DEPTH", 0)
    max_files_per_run = _parse_optional_int_env("INDEX_MAX_FILES_PER_RUN", 1)
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
        "docsIndexFileTypes": docs_index_file_types,
        "docsIndexExcludePatterns": docs_index_exclude_patterns,
        "indexMaxFileSizeBytes": max_size,
        "indexMaxTraversalDepth": max_traversal_depth,
        "indexMaxFilesPerRun": max_files_per_run,
        "indexProgressIntervalSeconds": progress_interval,
        "ingestionChunkSize": _parse_int_env("INGESTION_CHUNK_SIZE", 800),
        "ingestionChunkOverlap": _parse_int_env("INGESTION_CHUNK_OVERLAP", 120),
        "ingestionRetryMaxAttempts": _parse_int_env("INGESTION_RETRY_MAX_ATTEMPTS", 3),
        "ingestionRetryBackoffSeconds": float(os.getenv("INGESTION_RETRY_BACKOFF_SECONDS", "1.0")),
        "ingestionEnableQdrantHttp": os.getenv("INGESTION_ENABLE_QDRANT_HTTP", "1"),
        "ingestionUpsertTimeoutSeconds": float(os.getenv("INGESTION_UPSERT_TIMEOUT_SECONDS", "5")),
        "ingestionEmbeddingVectorSize": _parse_int_env("INGESTION_EMBEDDING_VECTOR_SIZE", 16),
        "qdrantCollectionName": os.getenv("QDRANT_COLLECTION_NAME", "workspace_chunks"),
        "qdrantDocsCollectionName": os.getenv("QDRANT_DOCS_COLLECTION_NAME", "workspace_docs_chunks"),
        "deltaGitBaseRef": os.getenv("DELTA_GIT_BASE_REF", "HEAD~1"),
        "deltaGitTargetRef": os.getenv("DELTA_GIT_TARGET_REF", "HEAD"),
        "deltaIncludeRenames": os.getenv("DELTA_INCLUDE_RENAMES", "1"),
        "deltaEnableFallback": os.getenv("DELTA_ENABLE_FALLBACK", "1"),
        "deltaBootstrapOnStart": os.getenv("DELTA_BOOTSTRAP_ON_START", "0"),
        "watchPollIntervalSeconds": _parse_int_env("WATCH_POLL_INTERVAL_SECONDS", 5),
        "watchCoalesceWindowSeconds": _parse_int_env("WATCH_COALESCE_WINDOW_SECONDS", 2),
        "watchReconcileIntervalSeconds": _parse_int_env("WATCH_RECONCILE_INTERVAL_SECONDS", 60),
        "watchRetryMaxAttempts": _parse_int_env("WATCH_RETRY_MAX_ATTEMPTS", 5),
        "watchRetryBaseDelaySeconds": float(os.getenv("WATCH_RETRY_BASE_DELAY_SECONDS", "1")),
        "watchRetryMaxDelaySeconds": float(os.getenv("WATCH_RETRY_MAX_DELAY_SECONDS", "30")),
        "watchHeartbeatIntervalSeconds": _parse_int_env("WATCH_HEARTBEAT_INTERVAL_SECONDS", 30),
        "watchMaxEventsPerCycle": _parse_int_env("WATCH_MAX_EVENTS_PER_CYCLE", 200),
        "watchStatus": WATCH_STATE.get_status(),
        "watchSummary": WATCH_STATE.get_last_summary(),
        "idempotencyHashAlgorithm": os.getenv("IDEMPOTENCY_HASH_ALGORITHM", "sha256"),
        "idempotencySkipUnchanged": os.getenv("IDEMPOTENCY_SKIP_UNCHANGED", "1"),
        "idempotencyEnableStaleCleanup": os.getenv("IDEMPOTENCY_ENABLE_STALE_CLEANUP", "1"),
        "fullScanFilters": {
            "supportedTypes": index_file_types,
            "excludePatterns": index_exclude_patterns,
            "maxFileSizeBytes": max_size,
            "maxTraversalDepth": max_traversal_depth,
            "maxFilesPerRun": max_files_per_run,
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
        "bootstrapAutoIngestOnStart": os.getenv("BOOTSTRAP_AUTO_INGEST_ON_START", "1"),
        "bootstrapRetryFailedOnStart": os.getenv("BOOTSTRAP_RETRY_FAILED_ON_START", "1"),
        "bootstrapStateCollection": os.getenv("BOOTSTRAP_STATE_COLLECTION", "workspace_bootstrap_state"),
        "mcpEndpointPath": os.getenv("MCP_ENDPOINT_PATH", "/mcp"),
        "bootstrap": BOOTSTRAP_ORCHESTRATOR.get_bootstrap_payload(os.getenv("WORKSPACE_PATH", "/workspace")),
        "collection": BOOTSTRAP_ORCHESTRATOR.get_collection_payload(),
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
    global STARTUP_PREFLIGHT_CONTEXT, STARTUP_PREFLIGHT_CHECKS
    STARTUP_PREFLIGHT_STATE.reset()
    STARTUP_PREFLIGHT_CONTEXT = None
    STARTUP_PREFLIGHT_CHECKS = []
    if not _should_run_startup_preflight():
        return

    try:
        context, checks = run_startup_preflight()
        STARTUP_PREFLIGHT_CONTEXT = context
        STARTUP_PREFLIGHT_CHECKS = checks
        summary = build_startup_readiness_summary(context=context, checks=checks, service_readiness=_build_startup_service_readiness())
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
        decision = BOOTSTRAP_ORCHESTRATOR.evaluate_startup(
            workspace_path=context["workspacePath"],
            start_ingestion_run=lambda workspace: _start_ingestion_run(
                workspace_path=workspace,
                payload={"workspacePath": workspace},
                max_traversal_depth=None,
                max_files_per_run=None,
                bootstrap_context={
                    "trigger": "auto-startup",
                    "decision": "run",
                    "status": "running",
                    "workspaceKey": build_workspace_key(workspace),
                },
            ).run_id,
        )
        if _should_log_startup_summary():
            print(json.dumps({"event": "startup-bootstrap", "bootstrap": decision.to_dict()}, ensure_ascii=False))
        _update_startup_readiness_with_bootstrap()
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


@app.post("/v1/search/docs/query")
def docs_search():
    payload = request.get_json(silent=True) or {}
    try:
        search_request = DocsSearchRequest.from_payload(payload)
        return jsonify(SEARCH_SERVICE.docs_search(search_request))
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
    try:
        run_limits = resolve_indexing_run_limits(payload, env=os.environ)
    except IndexingRunLimitValidationError as exc:
        return full_scan_json_error(exc.error_code, str(exc), 400)
    if max_file_size is None:
        max_file_size = _parse_int_env("INDEX_MAX_FILE_SIZE_BYTES", 1048576)

    try:
        max_file_size = int(max_file_size)
    except (TypeError, ValueError):
        return full_scan_json_error("INVALID_REQUEST", "maxFileSizeBytes must be an integer", 400)

    if max_file_size < 1:
        return full_scan_json_error("INVALID_REQUEST", "maxFileSizeBytes must be >= 1", 400)

    try:
        job = FULL_SCAN_STATE.create_job(
            workspace_path=workspace_path,
            max_file_size_bytes=max_file_size,
            max_traversal_depth=run_limits.max_traversal_depth,
            max_files_per_run=run_limits.max_files_per_run,
        )
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
        run_limits = resolve_indexing_run_limits(payload, env=os.environ)
    except IndexingRunLimitValidationError as exc:
        return ingestion_json_error(INGESTION_INVALID_LIMIT_VALUE, str(exc), 400)
    try:
        run = _start_ingestion_run(
            workspace_path=workspace_path,
            payload=payload,
            max_traversal_depth=run_limits.max_traversal_depth,
            max_files_per_run=run_limits.max_files_per_run,
            bootstrap_context={
                "trigger": "manual",
                "decision": "run",
                "status": "running",
                "workspaceKey": build_workspace_key(workspace_path),
            },
        )
    except RuntimeError:
        return ingestion_json_error("INGESTION_ALREADY_RUNNING", "Ingestion run is already running", 409)
    return jsonify({"runId": run.run_id, "status": run.status, "acceptedAt": run.accepted_at}), 202


@app.post("/v1/indexing/docs/jobs")
def start_docs_ingestion_job():
    payload = request.get_json(silent=True) or {}
    workspace_path = payload.get("workspacePath") or os.getenv("WORKSPACE_PATH", "/workspace")
    try:
        run_limits = resolve_indexing_run_limits(payload, env=os.environ)
    except IndexingRunLimitValidationError as exc:
        return ingestion_json_error(INGESTION_INVALID_LIMIT_VALUE, str(exc), 400)
    try:
        run = _start_ingestion_run(
            workspace_path=workspace_path,
            payload=payload,
            run_kind="docs",
            runner=_run_docs_ingestion_job,
            max_traversal_depth=run_limits.max_traversal_depth,
            max_files_per_run=run_limits.max_files_per_run,
            bootstrap_context={
                "trigger": "manual",
                "decision": "run",
                "status": "running",
                "workspaceKey": build_workspace_key(workspace_path),
            },
        )
    except RuntimeError:
        return ingestion_json_error("INGESTION_ALREADY_RUNNING", "Ingestion run is already running", 409)
    return jsonify({"runId": run.run_id, "status": run.status, "acceptedAt": run.accepted_at}), 202


@app.get("/v1/indexing/ingestion/jobs/<run_id>")
def get_ingestion_job_status(run_id: str):
    run = INGESTION_STATE.get_run(run_id)
    if not run:
        return ingestion_json_error("RUN_NOT_FOUND", f"Ingestion run '{run_id}' is not found", 404)
    payload = run.as_status()
    payload["persistence"] = build_ingestion_persistence_diagnostics()
    if "bootstrap" not in payload:
        payload["bootstrap"] = BOOTSTRAP_ORCHESTRATOR.get_bootstrap_payload(run.workspace_path)
    if _is_watch_mode_enabled():
        payload.setdefault("watch", WATCH_STATE.get_status())
    payload["collection"] = BOOTSTRAP_ORCHESTRATOR.get_collection_payload()
    return jsonify(payload)


@app.get("/v1/indexing/docs/jobs/<run_id>/summary")
def get_docs_job_summary(run_id: str):
    run = INGESTION_STATE.get_run(run_id)
    if not run or run.run_kind != "docs":
        return ingestion_json_error("RUN_NOT_FOUND", f"Docs indexing run '{run_id}' is not found", 404)
    if run.status in {"queued", "running"}:
        return ingestion_json_error("RUN_NOT_FINISHED", "Docs indexing run is not finished yet", 409)
    if run.summary is None:
        return ingestion_json_error("RUN_SUMMARY_MISSING", "Run summary is not available", 404)
    payload = dict(run.summary)
    collection = BOOTSTRAP_ORCHESTRATOR.get_collection_payload()
    payload["collection"] = collection.get("docsCollection") or {
        "collectionName": os.getenv("QDRANT_DOCS_COLLECTION_NAME", "workspace_docs_chunks"),
        "exists": False,
        "pointCount": 0,
    }
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
    payload.setdefault("bootstrap", run.bootstrap or BOOTSTRAP_ORCHESTRATOR.get_bootstrap_payload(run.workspace_path))
    if _is_watch_mode_enabled():
        payload.setdefault("watch", WATCH_STATE.get_status())
    payload["collection"] = BOOTSTRAP_ORCHESTRATOR.get_collection_payload()
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


@app.get("/v1/indexing/watch/status")
def get_watch_mode_status():
    if not _is_watch_mode_enabled():
        return (
            jsonify(
                {
                    "errorCode": "WATCH_MODE_DISABLED",
                    "message": "Watch mode is available only when INDEX_MODE=watch",
                }
            ),
            503,
        )

    payload = WATCH_STATE.get_status()
    if payload.get("state") == "stopped" and not get_watch_orchestrator().is_running:
        return (
            jsonify(
                {
                    "errorCode": "WATCH_NOT_RUNNING",
                    "message": "Watch loop is not running",
                    "details": payload,
                }
            ),
            503,
        )
    return jsonify(payload)


@app.get("/v1/indexing/watch/summary")
def get_watch_mode_summary():
    if not _is_watch_mode_enabled():
        return (
            jsonify(
                {
                    "errorCode": "WATCH_MODE_DISABLED",
                    "message": "Watch mode is available only when INDEX_MODE=watch",
                }
            ),
            503,
        )
    summary = WATCH_STATE.get_last_summary()
    if summary is None:
        return (
            jsonify(
                {
                    "errorCode": "WATCH_SUMMARY_NOT_FOUND",
                    "message": "Watch summary is not available yet",
                }
            ),
            404,
        )
    return jsonify(summary)


if __name__ == "__main__":
    _run_startup_preflight_or_exit()
    _start_watch_mode_if_needed()
    port = int(os.getenv("MCP_PORT", "8080"))
    app.run(host="0.0.0.0", port=port)





