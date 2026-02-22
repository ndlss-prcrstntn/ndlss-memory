from __future__ import annotations

import os
import shutil
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from startup_preflight_errors import StartupPreflightError
from startup_preflight_models import StartupCheckResult
from startup_readiness_summary import build_startup_readiness_summary


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def build_runtime_context() -> dict[str, Any]:
    index_mode = os.getenv("INDEX_MODE", "full-scan")
    git_required = _env_bool("STARTUP_PREFLIGHT_REQUIRE_GIT_FOR_DELTA", True) and index_mode == "delta-after-commit"
    return {
        "qdrantHost": os.getenv("QDRANT_HOST", "qdrant"),
        "qdrantApiPort": int(os.getenv("QDRANT_API_PORT", "6333")),
        "workspacePath": os.getenv("WORKSPACE_PATH", "/workspace"),
        "indexMode": index_mode,
        "gitRequired": git_required,
        "collectionName": os.getenv("QDRANT_COLLECTION_NAME", "workspace_chunks"),
        "mcpEndpointPath": os.getenv("MCP_ENDPOINT_PATH", "/mcp"),
        "timeoutSeconds": float(os.getenv("STARTUP_PREFLIGHT_TIMEOUT_SECONDS", "3")),
    }


def _qdrant_check(context: dict[str, Any]) -> StartupCheckResult:
    host = context["qdrantHost"]
    port = context["qdrantApiPort"]
    timeout_seconds = context["timeoutSeconds"]
    url = f"http://{host}:{port}/collections"
    try:
        with urllib.request.urlopen(url, timeout=timeout_seconds) as response:
            status = int(response.status)
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return StartupCheckResult(
            check_id="qdrant_reachability",
            status="failed",
            severity="critical",
            message="Qdrant недоступен из mcp-server",
            error_code="PREFLIGHT_QDRANT_UNREACHABLE",
            details={"url": url, "reason": str(exc)},
            action="Проверьте контейнер qdrant, сеть compose и QDRANT_API_PORT",
        )

    if status >= 400:
        return StartupCheckResult(
            check_id="qdrant_reachability",
            status="failed",
            severity="critical",
            message="Qdrant вернул неуспешный HTTP-статус",
            error_code="PREFLIGHT_QDRANT_HTTP_ERROR",
            details={"url": url, "status": status},
            action="Проверьте состояние qdrant и повторите запуск",
        )

    return StartupCheckResult(
        check_id="qdrant_reachability",
        status="passed",
        severity="critical",
        message="Qdrant доступен",
        details={"url": url, "status": status},
    )


def _workspace_check(context: dict[str, Any]) -> StartupCheckResult:
    workspace_path = Path(context["workspacePath"])
    if not workspace_path.exists():
        return StartupCheckResult(
            check_id="workspace_readable",
            status="failed",
            severity="critical",
            message="Рабочая директория не существует",
            error_code="PREFLIGHT_WORKSPACE_NOT_FOUND",
            details={"workspacePath": str(workspace_path)},
            action="Проверьте bind mount и переменную WORKSPACE_PATH",
        )
    if not workspace_path.is_dir():
        return StartupCheckResult(
            check_id="workspace_readable",
            status="failed",
            severity="critical",
            message="WORKSPACE_PATH должен указывать на директорию",
            error_code="PREFLIGHT_WORKSPACE_NOT_DIRECTORY",
            details={"workspacePath": str(workspace_path)},
            action="Укажите директорию проекта в WORKSPACE_PATH",
        )
    if not os.access(workspace_path, os.R_OK):
        return StartupCheckResult(
            check_id="workspace_readable",
            status="failed",
            severity="critical",
            message="Рабочая директория недоступна для чтения",
            error_code="PREFLIGHT_WORKSPACE_NOT_READABLE",
            details={"workspacePath": str(workspace_path)},
            action="Проверьте права доступа на директорию проекта",
        )
    return StartupCheckResult(
        check_id="workspace_readable",
        status="passed",
        severity="critical",
        message="Рабочая директория доступна для чтения",
        details={"workspacePath": str(workspace_path)},
    )


def _git_check(context: dict[str, Any]) -> StartupCheckResult:
    if not context["gitRequired"]:
        return StartupCheckResult(
            check_id="git_available",
            status="skipped",
            severity="info",
            message="Проверка git пропущена для текущего index mode",
            details={"indexMode": context["indexMode"]},
        )

    git_bin = shutil.which("git")
    if git_bin is None:
        return StartupCheckResult(
            check_id="git_available",
            status="failed",
            severity="critical",
            message="git недоступен в окружении запуска",
            error_code="PREFLIGHT_GIT_NOT_AVAILABLE",
            details={"indexMode": context["indexMode"]},
            action="Установите git в контейнер/окружение mcp-server",
        )

    workspace = context["workspacePath"]
    try:
        completed = subprocess.run(
            [git_bin, "-C", workspace, "rev-parse", "--is-inside-work-tree"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
    except OSError as exc:
        return StartupCheckResult(
            check_id="git_available",
            status="failed",
            severity="critical",
            message="Не удалось выполнить git-проверку",
            error_code="PREFLIGHT_GIT_EXECUTION_FAILED",
            details={"workspacePath": workspace, "reason": str(exc)},
            action="Проверьте доступность git и путь WORKSPACE_PATH",
        )

    if completed.returncode != 0:
        return StartupCheckResult(
            check_id="git_available",
            status="failed",
            severity="critical",
            message="Текущий workspace не является git-репозиторием",
            error_code="PREFLIGHT_GIT_REPOSITORY_REQUIRED",
            details={"workspacePath": workspace, "stderr": completed.stderr.strip()},
            action="Используйте git-репозиторий или переключите INDEX_MODE на full-scan",
        )

    return StartupCheckResult(
        check_id="git_available",
        status="passed",
        severity="critical",
        message="git доступен и workspace является репозиторием",
        details={"workspacePath": workspace},
    )


def run_startup_preflight() -> tuple[dict[str, Any], list[StartupCheckResult]]:
    context = build_runtime_context()
    checks = [_qdrant_check(context), _workspace_check(context), _git_check(context)]
    failed_critical = [check for check in checks if check.status == "failed" and check.severity == "critical"]
    if failed_critical:
        raise StartupPreflightError(
            error_code="STARTUP_PREFLIGHT_FAILED",
            message="Startup preflight checks failed",
            failed_checks=failed_critical,
            details={"indexMode": context["indexMode"], "workspacePath": context["workspacePath"]},
            recommended_actions=[check.action for check in failed_critical if check.action],
        )
    return context, checks


def build_readiness_summary(
    *,
    context: dict[str, Any],
    checks: list[StartupCheckResult],
    service_readiness: dict[str, str],
) -> dict[str, Any]:
    return build_startup_readiness_summary(context=context, checks=checks, service_readiness=service_readiness)
