from __future__ import annotations

from pathlib import Path

from delta_after_commit.change_models import DeltaCandidateFile, GitChangeSet
from file_size_guard import is_file_too_large
from file_type_filter import is_supported_file
from path_exclude_filter import is_excluded_path


def classify_changes(
    *,
    run_id: str,
    root: Path,
    change_set: list[GitChangeSet],
    supported_types: set[str],
    exclude_patterns: list[str],
    max_file_size_bytes: int,
    include_renames: bool,
) -> list[DeltaCandidateFile]:
    result: list[DeltaCandidateFile] = []

    for change in change_set:
        if change.change_type == "deleted":
            result.append(
                DeltaCandidateFile(
                    run_id=run_id,
                    path=change.path,
                    source_change_type=change.change_type,
                    decision="delete",
                    decision_reason_code="SOURCE_DELETED",
                )
            )
            continue

        if change.change_type == "renamed":
            if change.old_path:
                result.append(
                    DeltaCandidateFile(
                        run_id=run_id,
                        path=change.old_path,
                        old_path=change.path,
                        source_change_type=change.change_type,
                        decision="delete",
                        decision_reason_code="RENAMED_SOURCE_REMOVED",
                    )
                )
            if not include_renames:
                result.append(
                    DeltaCandidateFile(
                        run_id=run_id,
                        path=change.path,
                        old_path=change.old_path,
                        source_change_type=change.change_type,
                        decision="skip",
                        decision_reason_code="RENAMED_INDEX_DISABLED",
                        filtered_out=True,
                    )
                )
                continue

        if change.change_type not in {"added", "modified", "renamed"}:
            continue

        candidate = root / change.path
        rel_path = Path(change.path)

        if is_excluded_path(rel_path, exclude_patterns):
            result.append(
                DeltaCandidateFile(
                    run_id=run_id,
                    path=change.path,
                    old_path=change.old_path,
                    source_change_type=change.change_type,
                    decision="skip",
                    decision_reason_code="EXCLUDED_BY_PATTERN",
                    filtered_out=True,
                )
            )
            continue

        if not candidate.exists() or not candidate.is_file():
            result.append(
                DeltaCandidateFile(
                    run_id=run_id,
                    path=change.path,
                    old_path=change.old_path,
                    source_change_type=change.change_type,
                    decision="skip",
                    decision_reason_code="SOURCE_MISSING",
                    filtered_out=True,
                )
            )
            continue

        if not is_supported_file(candidate, supported_types):
            result.append(
                DeltaCandidateFile(
                    run_id=run_id,
                    path=change.path,
                    old_path=change.old_path,
                    source_change_type=change.change_type,
                    decision="skip",
                    decision_reason_code="UNSUPPORTED_TYPE",
                    filtered_out=True,
                )
            )
            continue

        too_large, size = is_file_too_large(candidate, max_file_size_bytes)
        if size < 0:
            result.append(
                DeltaCandidateFile(
                    run_id=run_id,
                    path=change.path,
                    old_path=change.old_path,
                    source_change_type=change.change_type,
                    decision="skip",
                    decision_reason_code="READ_ERROR",
                    filtered_out=True,
                )
            )
            continue

        if size == 0:
            result.append(
                DeltaCandidateFile(
                    run_id=run_id,
                    path=change.path,
                    old_path=change.old_path,
                    source_change_type=change.change_type,
                    decision="skip",
                    decision_reason_code="EMPTY_FILE",
                    filtered_out=True,
                )
            )
            continue

        if too_large:
            result.append(
                DeltaCandidateFile(
                    run_id=run_id,
                    path=change.path,
                    old_path=change.old_path,
                    source_change_type=change.change_type,
                    decision="skip",
                    decision_reason_code="FILE_TOO_LARGE",
                    filtered_out=True,
                )
            )
            continue

        result.append(
            DeltaCandidateFile(
                run_id=run_id,
                path=change.path,
                old_path=change.old_path,
                source_change_type=change.change_type,
                decision="index",
                decision_reason_code="CHANGED_INPUT",
            )
        )

    return result
