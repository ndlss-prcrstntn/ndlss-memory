from __future__ import annotations

from typing import Any

from startup_preflight_models import StartupCheckResult, now_iso


class StartupPreflightError(RuntimeError):
    def __init__(
        self,
        *,
        error_code: str,
        message: str,
        failed_checks: list[StartupCheckResult],
        details: dict[str, Any] | None = None,
        recommended_actions: list[str] | None = None,
        http_status: int = 503,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.failed_checks = failed_checks
        self.details = details or {}
        self.recommended_actions = recommended_actions or []
        self.http_status = http_status

    def to_failure_report(self) -> dict[str, Any]:
        return build_startup_failure_report(
            error_code=self.error_code,
            message=self.message,
            failed_checks=self.failed_checks,
            details=self.details,
            recommended_actions=self.recommended_actions,
        )


def build_startup_failure_report(
    *,
    error_code: str,
    message: str,
    failed_checks: list[StartupCheckResult],
    details: dict[str, Any] | None = None,
    recommended_actions: list[str] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "errorCode": error_code,
        "message": message,
        "failedChecks": [check.to_dict() for check in failed_checks],
        "generatedAt": now_iso(),
    }
    if details:
        payload["details"] = details
    if recommended_actions:
        payload["recommendedActions"] = recommended_actions
    return payload


def build_bootstrap_failure_report(
    *,
    workspace_path: str,
    collection_name: str,
    error_code: str,
    message: str,
) -> dict[str, Any]:
    return {
        "errorCode": error_code,
        "message": message,
        "details": {
            "workspacePath": workspace_path,
            "collectionName": collection_name,
        },
        "recommendedActions": [
            "Проверьте доступность Qdrant и сетевое соединение между сервисами",
            "Проверьте readiness endpoint и повторите запуск после устранения причины",
            "При необходимости запустите ручной ingestion через POST /v1/indexing/ingestion/jobs",
        ],
    }

