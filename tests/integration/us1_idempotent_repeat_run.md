# US1 Integration: Repeat Run Idempotency

## Goal

Verify repeated sync on unchanged files does not create duplicate records.

## Steps

1. Start idempotency run for baseline fixture workspace.
2. Wait for completion and collect summary.
3. Start second idempotency run with the same workspace and no file changes.
4. Compare first and second summaries.

## Expected

- First run reports `updatedChunks > 0`.
- Second run reports `skippedChunks` for unchanged records.
- Second run does not increase unique vector count unexpectedly.
