# Quickstart: MCP Ingestion Reliability (Patch 0.1.7)

## Goal

Validate two critical scenarios after rollout:

1. MCP/REST ingestion creates Qdrant collection and non-empty index.
2. Custom external `QDRANT_PORT` does not break ingestion/search.

## Prerequisites

- Docker Engine + Docker Compose v2
- Internet access for image pull
- Any local project directory with a few text/code files

## Scenario A: Collection creation after ingestion

1. Start stack from project folder:

```powershell
$preset = "generic"
iwr "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose-images/$preset.yml" -OutFile ndlss-compose.yml
$env:NDLSS_WORKSPACE = (Get-Location).Path
$env:NDLSS_IMAGE_TAG = "0.1.7"
$env:MCP_PORT = "8080"
$env:QDRANT_PORT = "6333"
docker compose -p ndlss-quickstart-a -f ndlss-compose.yml up -d
```

2. Check MCP health and transport endpoint:

```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:8080/health"
Invoke-RestMethod -Method Get -Uri "http://localhost:8080/.well-known/mcp"
```

3. Verify collection is absent before ingestion (fresh volume expected):

```powershell
Invoke-WebRequest -Method Get -Uri "http://localhost:6333/collections/workspace_chunks"
```

Expected: `404 Not Found`.

4. Start ingestion:

```powershell
$run = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/indexing/ingestion/jobs" -ContentType "application/json" -Body '{"workspacePath":"/workspace"}'
$runId = $run.runId
```

5. Poll run status until finished:

```powershell
while ($true) {
  $status = Invoke-RestMethod -Method Get -Uri "http://localhost:8080/v1/indexing/ingestion/jobs/$runId"
  $status
  if ($status.status -in @("completed", "failed", "partial")) { break }
  Start-Sleep 1
}
```

6. Validate collection and points:

```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:6333/collections/workspace_chunks"
Invoke-RestMethod -Method Post -Uri "http://localhost:6333/collections/workspace_chunks/points/count" -ContentType "application/json" -Body '{"exact":true}'
```

Expected:

- collection exists (`200`);
- `result.count > 0` for non-empty workspace.

## Scenario B: Non-default external Qdrant port

1. Restart stack with custom host port:

```powershell
docker compose -p ndlss-quickstart-a -f ndlss-compose.yml down
$env:MCP_PORT = "18080"
$env:QDRANT_PORT = "16333"
docker compose -p ndlss-quickstart-b -f ndlss-compose.yml up -d
```

2. Start ingestion and run search:

```powershell
$run = Invoke-RestMethod -Method Post -Uri "http://localhost:18080/v1/indexing/ingestion/jobs" -ContentType "application/json" -Body '{"workspacePath":"/workspace"}'
$runId = $run.runId
while ($true) {
  $status = Invoke-RestMethod -Method Get -Uri "http://localhost:18080/v1/indexing/ingestion/jobs/$runId"
  if ($status.status -in @("completed", "failed", "partial")) { break }
  Start-Sleep 1
}
Invoke-RestMethod -Method Post -Uri "http://localhost:18080/v1/search/semantic" -ContentType "application/json" -Body '{"query":"readme","limit":5}'
```

Expected:

- no connection-refused errors to Qdrant;
- ingestion status is `completed` or `partial` (not transport/backend failure);
- semantic search returns valid envelope (`ok` or `empty`).

## MCP endpoint reminder

- MCP transport endpoint: `POST /mcp`
- Do not use `/` as MCP endpoint; `/` is REST command catalog.

## Cleanup

```powershell
docker compose -p ndlss-quickstart-b -f ndlss-compose.yml down
```
