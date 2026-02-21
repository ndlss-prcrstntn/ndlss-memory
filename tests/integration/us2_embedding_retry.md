# US2 Integration: Embedding Retry and Upsert

## Goal

Validate retry behavior for transient embedding errors and successful upsert
after retries.

## Preconditions

- Ingestion test env prepared.
- Fixture contains `[[EMBEDDING_TRANSIENT]]` token.

## Steps

1. Start ingestion run with `retryMaxAttempts >= 2`.
2. Monitor run status.
3. Request run summary.

## Expected Results

- `retryCount` is greater than zero for transient fixture files.
- `embeddedChunks` increases after retry path.
- `failedChunks` includes only truly fatal cases.
