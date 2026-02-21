from __future__ import annotations

from pathlib import Path

from command_execution_errors import workspace_isolation_violation


def resolve_workspace_directory(*, workspace_root: str, requested_working_directory: str) -> Path:
    root = Path(workspace_root).resolve()
    requested = Path(requested_working_directory)
    if requested.is_absolute():
        target = requested.resolve()
    else:
        target = (root / requested).resolve()

    if target != root and root not in target.parents:
        raise workspace_isolation_violation(str(target))
    return target

