from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


class IndexingRunLimitValidationError(ValueError):
    def __init__(self, field_name: str, message: str) -> None:
        super().__init__(message)
        self.field_name = field_name
        self.error_code = "INVALID_LIMIT_VALUE"


@dataclass(frozen=True)
class IndexingRunLimitPolicy:
    max_traversal_depth: int | None = None
    max_files_per_run: int | None = None

    def to_applied_limits(self) -> dict[str, int | None]:
        return {
            "maxTraversalDepth": self.max_traversal_depth,
            "maxFilesPerRun": self.max_files_per_run,
        }

    @property
    def is_default_behavior(self) -> bool:
        return self.max_traversal_depth is None and self.max_files_per_run is None


def _parse_optional_int(
    raw: Any,
    *,
    field_name: str,
    minimum: int,
) -> int | None:
    if raw is None:
        return None
    if isinstance(raw, str) and raw.strip() == "":
        return None

    if isinstance(raw, bool):
        raise IndexingRunLimitValidationError(field_name, f"{field_name} must be an integer >= {minimum}")

    try:
        value = int(raw)
    except (TypeError, ValueError) as exc:
        raise IndexingRunLimitValidationError(field_name, f"{field_name} must be an integer >= {minimum}") from exc

    if value < minimum:
        raise IndexingRunLimitValidationError(field_name, f"{field_name} must be >= {minimum}")
    return value


def resolve_indexing_run_limits(payload: Mapping[str, Any], *, env: Mapping[str, str] | None = None) -> IndexingRunLimitPolicy:
    env_payload = env or {}
    max_depth_raw = payload.get("maxTraversalDepth")
    max_files_raw = payload.get("maxFilesPerRun")

    if max_depth_raw is None:
        max_depth_raw = env_payload.get("INDEX_MAX_TRAVERSAL_DEPTH")
    if max_files_raw is None:
        max_files_raw = env_payload.get("INDEX_MAX_FILES_PER_RUN")

    return IndexingRunLimitPolicy(
        max_traversal_depth=_parse_optional_int(max_depth_raw, field_name="maxTraversalDepth", minimum=0),
        max_files_per_run=_parse_optional_int(max_files_raw, field_name="maxFilesPerRun", minimum=1),
    )
