from __future__ import annotations

import subprocess
from pathlib import Path

from delta_after_commit.change_models import GitChangeSet


class GitDiffError(RuntimeError):
    def __init__(self, reason_code: str, message: str) -> None:
        super().__init__(message)
        self.reason_code = reason_code


def _normalize(path: str) -> str:
    return str(Path(path)).replace("\\", "/")


def read_git_change_set(
    *,
    workspace_path: str,
    base_ref: str,
    target_ref: str,
    include_renames: bool = True,
) -> list[GitChangeSet]:
    command = ["git", "-C", workspace_path, "diff", "--name-status"]
    if include_renames:
        command.append("--find-renames")
    command.extend([base_ref, target_ref])

    try:
        proc = subprocess.run(command, check=False, text=True, capture_output=True)
    except OSError as exc:
        raise GitDiffError("GIT_NOT_AVAILABLE", f"git command failed to execute: {exc}") from exc

    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip()
        reason = "BASE_REF_NOT_FOUND" if "ambiguous argument" in stderr.lower() else "GIT_DIFF_FAILED"
        raise GitDiffError(reason, stderr or "git diff failed")

    change_set: list[GitChangeSet] = []
    for index, line in enumerate((proc.stdout or "").splitlines()):
        raw = line.strip()
        if not raw:
            continue
        parts = raw.split("\t")
        status_raw = parts[0]
        status_key = status_raw[:1].upper()

        if status_key == "A" and len(parts) >= 2:
            change_set.append(
                GitChangeSet(change_id=f"{index}:A:{parts[1]}", change_type="added", path=_normalize(parts[1]), raw_status=status_raw)
            )
            continue

        if status_key == "M" and len(parts) >= 2:
            change_set.append(
                GitChangeSet(
                    change_id=f"{index}:M:{parts[1]}",
                    change_type="modified",
                    path=_normalize(parts[1]),
                    raw_status=status_raw,
                )
            )
            continue

        if status_key == "D" and len(parts) >= 2:
            change_set.append(
                GitChangeSet(
                    change_id=f"{index}:D:{parts[1]}",
                    change_type="deleted",
                    path=_normalize(parts[1]),
                    raw_status=status_raw,
                )
            )
            continue

        if status_key == "R" and len(parts) >= 3:
            change_set.append(
                GitChangeSet(
                    change_id=f"{index}:R:{parts[1]}->{parts[2]}",
                    change_type="renamed",
                    path=_normalize(parts[2]),
                    old_path=_normalize(parts[1]),
                    raw_status=status_raw,
                )
            )
            continue

        # Conservative fallback for other statuses: treat as modified if path is present.
        if len(parts) >= 2:
            change_set.append(
                GitChangeSet(
                    change_id=f"{index}:X:{parts[1]}",
                    change_type="modified",
                    path=_normalize(parts[1]),
                    raw_status=status_raw,
                )
            )

    return change_set
