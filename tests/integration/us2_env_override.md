# US2: environment override scenario

## Goal
Validate env overrides affect runtime config after restart.

## Steps
1. Set custom values in a temp env file:
   - `MCP_PORT=18080`
   - `INDEX_MODE=delta-after-commit`
2. Run compose with that env file.
3. Query `GET /v1/system/config`.

## Expected
- `mcpPort` equals custom port.
- `indexMode` equals `delta-after-commit`.
