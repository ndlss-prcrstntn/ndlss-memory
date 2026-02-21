# Regression: Full Scan After Idempotency

## Goal

Verify full-scan behavior remains stable after idempotency sync features are
added.

## Checks

1. Full-scan job starts and completes through existing endpoints.
2. Full-scan progress/summary payloads remain contract-compatible.
3. Idempotency API remains available after full-scan run.
