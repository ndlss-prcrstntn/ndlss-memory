# Quickstart (No Clone): 3-5 minutes to first search

This guide starts `ndlss-memory` inside your current project folder with a single command, without cloning this repository.

## Requirements

- Docker Engine
- Docker Compose v2
- Internet access to pull source/images

## 1) Pick a preset and start

### PowerShell

```powershell
$preset = "generic"; iwr "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose-images/$preset.yml" -OutFile ndlss-compose.yml; $env:NDLSS_WORKSPACE=(Get-Location).Path; docker compose -f ndlss-compose.yml up -d
```

### bash

```bash
preset=generic; curl -fsSL "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose-images/${preset}.yml" -o ndlss-compose.yml && NDLSS_WORKSPACE="$PWD" docker compose -f ndlss-compose.yml up -d
```

Optional: pin image tag and namespace (default tag is `latest`):

```bash
NDLSS_DOCKERHUB_NAMESPACE=ndlss NDLSS_IMAGE_TAG=0.1.7 docker compose -f ndlss-compose.yml up -d
```

If a specific tag is not published yet, keep `NDLSS_IMAGE_TAG` unset and use `latest`.

Available presets:

- `generic`
- `python`
- `typescript`
- `javascript`
- `java-kotlin`
- `csharp`
- `go`

Details: `docs/compose-presets.md`.

## Run multiple projects at the same time

Use a unique compose project name (`-p`) and unique host ports for each project.

Project A:

```powershell
$env:MCP_PORT="18080"
$env:QDRANT_PORT="16333"
$env:QDRANT_API_PORT="6333"
docker compose -p ndlss-project-a -f ndlss-compose.yml up -d
```

Project B:

```powershell
$env:MCP_PORT="28080"
$env:QDRANT_PORT="26333"
$env:QDRANT_API_PORT="6333"
docker compose -p ndlss-project-b -f ndlss-compose.yml up -d
```

Stop one stack without affecting another:

```powershell
docker compose -p ndlss-project-a -f ndlss-compose.yml down
```

## 2) Check health

```bash
curl http://localhost:8080/health
```

Expected: HTTP 200.

## 3) Run first semantic search

```bash
curl -X POST http://localhost:8080/v1/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query":"docker compose healthcheck","limit":5}'
```

If the project has not been indexed yet, start ingestion once:

```bash
curl -X POST http://localhost:8080/v1/indexing/ingestion/jobs \
  -H "Content-Type: application/json" \
  -d '{"workspacePath":"/workspace"}'
```

Then repeat the search.

## 4) Optional: connect an MCP client

Verify MCP discovery first:

```bash
curl http://localhost:8080/.well-known/mcp
```

```json
{
  "servers": {
    "ndlss-memory": {
      "transport": "http",
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

Important:

- `http://localhost:8080/` is REST catalog, not MCP JSON-RPC endpoint.
- MCP clients must use `http://localhost:8080/mcp`.
- `QDRANT_PORT` controls host exposure only; internal service traffic uses `QDRANT_API_PORT` (default `6333`).
- Legacy fallback endpoints are `GET /sse` and `POST /messages?sessionId=...`.

## 5) Stop

```bash
docker compose -f ndlss-compose.yml down
```
