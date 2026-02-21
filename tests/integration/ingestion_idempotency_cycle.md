# Integration: Ingestion Idempotency Cycle

## Goal

Validate repeated ingestion runs over unchanged input do not inflate unique
vector record count.

## Steps

1. Run ingestion once and capture summary totals.
2. Run ingestion again on unchanged fixture set.
3. Compare `totalChunks` and `embeddedChunks` deltas.

## Expected Results

- Repeated run remains stable (no uncontrolled growth).
- Summary counters are consistent within configured tolerance.
