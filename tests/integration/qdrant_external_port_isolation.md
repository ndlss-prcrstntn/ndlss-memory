# Integration: Qdrant External Port Isolation

## Objective

Ensure non-default external `QDRANT_PORT` does not impact internal Qdrant
connectivity for `file-indexer` and `mcp-server`.

## Scenario

1. Start compose stack with:
   - `QDRANT_PORT=16333`
   - `QDRANT_API_PORT=6333`
2. Wait for `/health` response from `mcp-server`.
3. Trigger ingestion.
4. Execute semantic search.
5. Validate no internal connection-refused errors and successful response envelopes.

## Artifacts

- `tests/artifacts/quality-stability/us2-custom-port-summary.json`
