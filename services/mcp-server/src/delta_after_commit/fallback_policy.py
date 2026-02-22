from __future__ import annotations

import os
from dataclasses import dataclass

from delta_after_commit.git_diff_reader import GitDiffError


@dataclass(frozen=True)
class FallbackDecision:
    should_fallback: bool
    reason_code: str | None = None


class FallbackPolicy:
    def __init__(self, enabled: bool | None = None) -> None:
        if enabled is None:
            enabled = os.getenv("DELTA_ENABLE_FALLBACK", "1").strip() in {"1", "true", "yes", "on"}
        self.enabled = enabled

    def for_exception(self, exc: Exception) -> FallbackDecision:
        if not self.enabled:
            return FallbackDecision(False)
        if isinstance(exc, GitDiffError):
            return FallbackDecision(True, exc.reason_code)
        return FallbackDecision(True, "DELTA_FALLBACK_UNEXPECTED_ERROR")
