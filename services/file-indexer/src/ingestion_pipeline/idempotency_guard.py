from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IdempotencyDecision:
    should_upsert: bool
    reason_code: str


def should_upsert(*, current_hash: str, previous_hash: str | None, skip_unchanged: bool) -> IdempotencyDecision:
    if previous_hash is None:
        return IdempotencyDecision(should_upsert=True, reason_code="NEW_FILE")
    if previous_hash == current_hash and skip_unchanged:
        return IdempotencyDecision(should_upsert=False, reason_code="SKIPPED_UNCHANGED")
    if previous_hash == current_hash:
        return IdempotencyDecision(should_upsert=True, reason_code="FORCED_REINDEX")
    return IdempotencyDecision(should_upsert=True, reason_code="CONTENT_CHANGED")


def stale_chunk_ids(previous_ids: set[str], current_ids: set[str]) -> set[str]:
    return previous_ids - current_ids

