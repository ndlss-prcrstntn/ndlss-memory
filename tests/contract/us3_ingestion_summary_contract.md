# Contract Test: Ingestion Summary Endpoint

## Endpoint

`GET /v1/indexing/ingestion/jobs/{runId}/summary`

## Positive Case

- Status code: `200`
- Response includes:
  - `runId`, `status`, `totalFiles`, `totalChunks`
  - `embeddedChunks`, `failedChunks`, `retryCount`
  - `startedAt`, `finishedAt`
  - `metadataCoverage.path`
  - `metadataCoverage.fileName`
  - `metadataCoverage.fileType`
  - `metadataCoverage.contentHash`
  - `metadataCoverage.timestamp`

## Error Cases

- Unknown `runId` returns `404` with `errorCode`.
- Active run returns `409` with `errorCode=RUN_NOT_FINISHED`.
