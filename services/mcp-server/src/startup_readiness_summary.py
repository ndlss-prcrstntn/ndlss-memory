from __future__ import annotations

from startup_preflight_models import StartupCheckResult, StartupReadinessSummary


def build_startup_readiness_summary(
    *,
    context: dict,
    checks: list[StartupCheckResult],
    service_readiness: dict[str, str],
    status: str = "ready",
    collection: dict | None = None,
    bootstrap: dict | None = None,
    bootstrap_failure: dict | None = None,
) -> dict:
    summary = StartupReadinessSummary(
        service_readiness=service_readiness,
        workspace_path=context["workspacePath"],
        index_mode=context["indexMode"],
        mcp_endpoint=context["mcpEndpointPath"],
        collection_name=context["collectionName"],
        preflight_checks=checks,
        status=status,
        collection=collection,
        bootstrap=bootstrap,
        bootstrap_failure=bootstrap_failure,
    )
    return summary.to_dict()

