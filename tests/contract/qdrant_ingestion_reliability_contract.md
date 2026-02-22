# Qdrant Ingestion Reliability Contract

## Scope

- `POST /v1/indexing/ingestion/jobs`
- `GET /v1/indexing/ingestion/jobs/{runId}`
- `GET /v1/indexing/ingestion/jobs/{runId}/summary`
- `GET /v1/system/config`
- `GET /collections/workspace_chunks`
- `POST /collections/workspace_chunks/points/count`

## Assertions

1. Starting ingestion returns `202` with `runId`, `status`, and `acceptedAt`.
2. Ingestion status response includes:
   - progress fields (`totalFiles`, `totalChunks`, `embeddedChunks`, `failedChunks`)
   - `errorCode`/`errorMessage` when failed
   - `persistence.qdrantApiPort`
   - `persistence.ingestionEnableQdrantHttp`
3. Ingestion summary is available only after run completion.
4. Successful ingestion on non-empty workspace guarantees:
   - `workspace_chunks` collection exists
   - `points/count` returns `count > 0`
5. Persistence failures must surface as `errorCode=INGESTION_PERSISTENCE_FAILED`.

## Compatibility Notes

- External Qdrant host mapping uses `QDRANT_PORT`.
- Internal service-to-service Qdrant access uses `QDRANT_API_PORT`.
- MCP transport endpoint remains `POST /mcp`.
