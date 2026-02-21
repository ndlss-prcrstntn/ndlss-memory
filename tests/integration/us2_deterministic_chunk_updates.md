# US2 Integration: Deterministic Chunk Updates

## Goal

Validate that deterministic chunk IDs allow updating only affected chunks after
partial file modifications.

## Steps

1. Run idempotency sync on baseline fixture set.
2. Modify a subset of text in one file while keeping the rest unchanged.
3. Run idempotency sync again.
4. Compare updated/skipped counters and reason breakdown.

## Expected

- `updatedChunks` reflects only changed chunks.
- `skippedChunks` includes unchanged chunks.
- No duplicate records are created for unchanged content.
