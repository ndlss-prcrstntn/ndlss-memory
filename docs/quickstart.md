# Quickstart (No Clone): 3-5 minutes to first search

This guide starts `ndlss-memory` inside your current project folder with a single command, without cloning this repository.

## Requirements

- Docker Engine
- Docker Compose v2
- Internet access to pull source/images

## 1) Pick a preset and start

### PowerShell

```powershell
$preset = "generic"; iwr "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose/$preset.yml" -OutFile ndlss-compose.yml; $env:NDLSS_WORKSPACE=(Get-Location).Path; docker compose -f ndlss-compose.yml up -d --build
```

### bash

```bash
preset=generic; curl -fsSL "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose/${preset}.yml" -o ndlss-compose.yml && NDLSS_WORKSPACE="$PWD" docker compose -f ndlss-compose.yml up -d --build
```

Optional: pin service source to a release tag or commit:

```bash
NDLSS_GIT_REF=v1.0.0 docker compose -f ndlss-compose.yml up -d --build
```

Available presets:

- `generic`
- `python`
- `typescript`
- `javascript`
- `java-kotlin`
- `csharp`
- `go`

Details: `docs/compose-presets.md`.

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

```json
{
  "servers": {
    "ndlss-memory": {
      "transport": "http",
      "url": "http://localhost:8080"
    }
  }
}
```

## 5) Stop

```bash
docker compose -f ndlss-compose.yml down
```
