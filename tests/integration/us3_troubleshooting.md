# US3: troubleshooting scenario

## Scenario
One service is unhealthy and user restores the stack.

## Steps
1. Start stack with `pwsh scripts/dev/up.ps1`.
2. Force one service status override:
   - `SERVICE_FILE_INDEXER_STATUS=unhealthy`
3. Run `pwsh scripts/ops/stack-status.ps1`.
4. Follow troubleshooting steps in quickstart.
5. Restore healthy status and restart stack.

## Expected
- Diagnostics script reports degraded state.
- User can identify affected service.
- After restart, system becomes healthy.
