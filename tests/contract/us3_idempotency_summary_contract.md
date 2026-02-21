# Contract Test: Idempotency Summary Endpoint

## Endpoint

`GET /v1/indexing/idempotency/jobs/{runId}/summary`

## Success Response (`200`)

- Required fields:
  - `runId`
  - `status`
  - `totalFiles`
  - `updatedChunks`
  - `skippedChunks`
  - `deletedChunks`
  - `failedChunks`
  - `startedAt`
  - `finishedAt`
  - `reasonBreakdown[]`

## Error Responses

- `404` for unknown run ID.
- `409` when run is not finished.
- Error payload includes `errorCode` and `message`.
