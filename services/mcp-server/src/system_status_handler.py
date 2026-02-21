import fnmatch
import os
from datetime import datetime, timezone
from pathlib import Path
from threading import Thread

import yaml
from flask import Flask, jsonify, request

from full_scan_errors import json_error
from full_scan_state import STATE

SERVICE_NAMES = ("qdrant", "file-indexer", "mcp-server")
STATUS_ENV_MAP = {
    "qdrant": "SERVICE_QDRANT_STATUS",
    "file-indexer": "SERVICE_FILE_INDEXER_STATUS",
    "mcp-server": "SERVICE_MCP_SERVER_STATUS",
}

app = Flask(__name__)


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


def load_security_policy() -> dict:
    path = "/app/config/security-policy.yaml"
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


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
    job = STATE.get_job(job_id)
    if not job:
        return

    workspace = Path(job.workspace_path)
    supported_types = {s.lower() for s in _split_csv(os.getenv("INDEX_FILE_TYPES", ".md,.txt,.json,.yml,.yaml"))}
    excluded_patterns = _split_csv(os.getenv("INDEX_EXCLUDE_PATTERNS", ".git,node_modules,dist,build"))
    max_file_size = job.max_file_size_bytes

    if not workspace.exists() or not workspace.is_dir():
        STATE.update_job(job_id, error_delta=1)
        STATE.finish_job(job_id, "failed")
        return

    files = [path for path in workspace.rglob("*") if path.is_file()]
    total = len(files)
    if total == 0:
        STATE.finish_job(job_id, "completed")
        return

    for idx, file_path in enumerate(files, start=1):
        rel_path = file_path.relative_to(workspace)
        ext = file_path.suffix.lower()
        percent = round((idx * 100.0) / total, 2)

        if _is_excluded(rel_path, excluded_patterns):
            STATE.update_job(job_id, processed_delta=1, skip_delta=1, skip_reason="EXCLUDED_BY_PATTERN", percent_complete=percent)
            continue

        if ext not in supported_types:
            STATE.update_job(job_id, processed_delta=1, skip_delta=1, skip_reason="UNSUPPORTED_TYPE", percent_complete=percent)
            continue

        try:
            size = file_path.stat().st_size
        except OSError:
            STATE.update_job(job_id, processed_delta=1, skip_delta=1, error_delta=1, skip_reason="READ_ERROR", percent_complete=percent)
            continue

        if size == 0:
            STATE.update_job(job_id, processed_delta=1, skip_delta=1, skip_reason="EMPTY_FILE", percent_complete=percent)
            continue

        if size > max_file_size:
            STATE.update_job(job_id, processed_delta=1, skip_delta=1, skip_reason="FILE_TOO_LARGE", percent_complete=percent)
            continue

        try:
            file_path.read_bytes()
            STATE.update_job(job_id, processed_delta=1, indexed_delta=1, percent_complete=percent)
        except OSError:
            STATE.update_job(job_id, processed_delta=1, skip_delta=1, error_delta=1, skip_reason="READ_ERROR", percent_complete=percent)

    STATE.finish_job(job_id, "completed")


def build_runtime_config() -> dict:
    policy = load_security_policy()
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
        "mcpPort": int(os.getenv("MCP_PORT", "8080")),
        "indexMode": os.getenv("INDEX_MODE", "full-scan"),
        "indexFileTypes": index_file_types,
        "indexExcludePatterns": index_exclude_patterns,
        "indexMaxFileSizeBytes": max_size,
        "indexProgressIntervalSeconds": progress_interval,
        "fullScanFilters": {
            "supportedTypes": index_file_types,
            "excludePatterns": index_exclude_patterns,
            "maxFileSizeBytes": max_size,
        },
        "commandAllowlist": allowlist,
        "commandTimeoutSeconds": int(timeout_value),
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


@app.get("/health")
def get_health():
    return jsonify({"status": "ok", "timestamp": _now_iso()})


@app.get("/v1/system/status")
def get_system_status():
    return jsonify(build_system_status())


@app.get("/v1/system/config")
def get_runtime_config():
    return jsonify(build_runtime_config())


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
        return json_error("INVALID_REQUEST", "maxFileSizeBytes must be an integer", 400)

    if max_file_size < 1:
        return json_error("INVALID_REQUEST", "maxFileSizeBytes must be >= 1", 400)

    try:
        job = STATE.create_job(workspace_path=workspace_path, max_file_size_bytes=max_file_size)
    except RuntimeError:
        return json_error("FULL_SCAN_ALREADY_RUNNING", "Full scan job is already running", 409)

    Thread(target=_run_full_scan_job, args=(job.job_id,), daemon=True).start()
    return jsonify({"jobId": job.job_id, "status": job.status, "acceptedAt": job.accepted_at}), 202


@app.get("/v1/indexing/full-scan/jobs/<job_id>")
def get_full_scan_job_progress(job_id: str):
    job = STATE.get_job(job_id)
    if not job:
        return json_error("JOB_NOT_FOUND", f"Full scan job '{job_id}' is not found", 404)
    return jsonify(job.as_progress())


@app.get("/v1/indexing/full-scan/jobs/<job_id>/summary")
def get_full_scan_job_summary(job_id: str):
    job = STATE.get_job(job_id)
    if not job:
        return json_error("JOB_NOT_FOUND", f"Full scan job '{job_id}' is not found", 404)
    if job.status in {"queued", "running"}:
        return json_error("JOB_NOT_FINISHED", "Full scan job is not finished yet", 409)
    return jsonify(job.as_summary())


if __name__ == "__main__":
    port = int(os.getenv("MCP_PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
