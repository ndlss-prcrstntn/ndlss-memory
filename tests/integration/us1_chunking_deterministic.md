# US1 Integration: Deterministic Chunking

## Goal

Validate that chunking is deterministic and always respects `chunkSize` and
`chunkOverlap`.

## Test Data

- Workspace: `tests/fixtures/chunking-embeddings`
- File type set: `.md,.txt`
- Chunk settings: `chunkSize=120`, `chunkOverlap=24`

## Steps

1. Prepare env via `scripts/tests/ingestion_test_env.ps1`.
2. Start ingestion run: `POST /v1/indexing/ingestion/jobs`.
3. Poll `GET /v1/indexing/ingestion/jobs/{runId}` until final status.
4. Read run summary from `GET /v1/indexing/ingestion/jobs/{runId}/summary`.

## Expected Results

- `status` is `completed` or `partial`.
- `totalChunks` is stable across repeated runs over the same dataset.
- Neighbor chunk boundaries reflect configured overlap.
