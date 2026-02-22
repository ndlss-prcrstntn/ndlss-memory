# Integration: Qdrant Ingestion Reliability

## Objective

Validate that MCP-triggered ingestion persists vectors in Qdrant and exposes
diagnostics required for troubleshooting.

## Scenario

1. Start compose stack with clean volume.
2. Verify `workspace_chunks` does not exist before ingestion.
3. Trigger ingestion via `POST /v1/indexing/ingestion/jobs`.
4. Poll status until terminal state.
5. Validate:
   - `status` is `completed` on healthy run
   - `errorCode` is empty
   - `persistence.qdrantApiPort` is present
6. Query Qdrant:
   - collection exists
   - points count is greater than zero

## Artifacts

- `tests/artifacts/quality-stability/us1-ingestion-collection-summary.json`
