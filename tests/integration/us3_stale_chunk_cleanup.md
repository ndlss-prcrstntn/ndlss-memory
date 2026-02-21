# US3 Integration: Stale Chunk Cleanup

## Goal

Ensure stale chunks are removed when source files are deleted or shortened.

## Steps

1. Run idempotency sync with full fixture set.
2. Remove one previously indexed file and truncate another file.
3. Run idempotency sync again.
4. Inspect summary and reason breakdown.

## Expected

- `deletedChunks` is greater than zero after cleanup.
- Summary contains stale cleanup reason codes.
- Search/index view no longer references removed chunk IDs.
