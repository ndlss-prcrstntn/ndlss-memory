# Regression: Delta-after-commit After Idempotency

## Goal

Ensure `delta-after-commit` mode and runtime observability are not regressed by
idempotency changes.

## Checks

1. Stack starts with `INDEX_MODE=delta-after-commit`.
2. Runtime config endpoint reports delta mode correctly.
3. Idempotency sync endpoints remain reachable and return valid payloads.
