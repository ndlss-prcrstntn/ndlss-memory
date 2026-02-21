# Compose startup smoke test

## Goal
Verify that docker compose starts all required services and all healthchecks pass.

## Steps
1. Run `docker compose -f infra/docker/docker-compose.yml --env-file .env.example up -d --build`.
2. Run `docker compose -f infra/docker/docker-compose.yml ps`.
3. Confirm `qdrant`, `file-indexer`, `mcp-server` show `Up (healthy)`.
4. Call `GET /health` on mcp-server.

## Expected
- No container exits unexpectedly.
- All required services are healthy.
