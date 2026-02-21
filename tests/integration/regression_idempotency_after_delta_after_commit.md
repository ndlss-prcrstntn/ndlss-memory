# Regression: Idempotency after Delta-after-commit

## Goal

Ensure idempotency pipeline remains stable after delta implementation.

## Checks

1. Run idempotency repeat-run scenario.
2. Verify `skippedChunks` behavior remains stable.
3. Verify stale cleanup still works.
