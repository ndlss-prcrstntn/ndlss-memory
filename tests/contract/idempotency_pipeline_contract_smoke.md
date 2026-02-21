# Idempotency Pipeline Contract Smoke

## Goal

Validate baseline contract behavior of idempotency endpoints.

## Preconditions

- Stack is up and healthy.
- Workspace is mounted to `/workspace`.

## Scenarios

1. `POST /v1/indexing/idempotency/jobs` returns `202` and `runId`.
2. Repeated `POST` while run is active returns `409` with
   `errorCode=IDEMPOTENCY_ALREADY_RUNNING`.
3. `GET /v1/indexing/idempotency/jobs/{runId}` returns `200` with counters:
   `updatedChunks`, `skippedChunks`, `deletedChunks`, `failedChunks`.
4. `GET /v1/indexing/idempotency/jobs/{runId}/summary` returns:
   - `409` while run is active
   - `200` after completion with `reasonBreakdown`.
5. Unknown `runId` returns `404` with machine-readable `errorCode`.
