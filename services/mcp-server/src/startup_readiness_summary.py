from __future__ import annotations

from startup_preflight_models import StartupCheckResult, StartupReadinessSummary


def build_startup_readiness_summary(
    *,
    context: dict,
    checks: list[StartupCheckResult],
    service_readiness: dict[str, str],
) -> dict:
    summary = StartupReadinessSummary(
        service_readiness=service_readiness,
        workspace_path=context["workspacePath"],
        index_mode=context["indexMode"],
        mcp_endpoint=context["mcpEndpointPath"],
        collection_name=context["collectionName"],
        preflight_checks=checks,
    )
    return summary.to_dict()

