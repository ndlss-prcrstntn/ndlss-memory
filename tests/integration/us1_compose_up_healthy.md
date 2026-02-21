# US1: Compose up healthy acceptance

## Pre-conditions
- Docker daemon is running.
- `.env.example` exists.

## Steps
1. Run `pwsh scripts/dev/up.ps1`.
2. Run `docker compose -f infra/docker/docker-compose.yml ps`.
3. Run `pwsh scripts/ops/stack-status.ps1`.

## Expected
- Required services are listed: qdrant, file-indexer, mcp-server.
- Every service status is healthy.
- `/health` endpoint returns `ok`.
