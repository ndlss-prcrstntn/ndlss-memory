# Ingestion Pipeline Contract Smoke

## Goal

Validate that ingestion endpoints are reachable and return contract-compliant
status codes for basic scenarios.

## Preconditions

- Stack is running (`qdrant`, `file-indexer`, `mcp-server` healthy).
- Test workspace is mounted into `/workspace`.

## Scenarios

1. `POST /v1/indexing/ingestion/jobs` returns `202` with `runId`.
2. Repeated `POST` while a run is active returns `409` with
   `errorCode=INGESTION_ALREADY_RUNNING`.
3. `GET /v1/indexing/ingestion/jobs/{runId}` returns `200` and counters.
4. `GET /v1/indexing/ingestion/jobs/{runId}/summary` returns:
   - `409` while run is active
   - `200` after completion with `metadataCoverage`.
5. Unknown `runId` returns `404` with machine-readable `errorCode`.
