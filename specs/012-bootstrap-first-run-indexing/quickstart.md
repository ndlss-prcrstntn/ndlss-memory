# Quickstart: First-Run Bootstrap Indexing

Этот сценарий проверяет, что после первого запуска стека индексация становится пригодной к поиску без ручного триггера ingestion.

## Предусловия

- Docker Engine + Docker Compose v2
- PowerShell 7+
- Рабочая директория проекта: `Z:\WORK\ndlss-memory`

## 1. Подготовить «чистый» workspace

```powershell
Set-Location 'Z:\WORK\ndlss-memory'
$workspace = 'Z:\WORK\tmp\bootstrap-smoke'
Remove-Item $workspace -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $workspace | Out-Null
Set-Content -Path (Join-Path $workspace 'hello.md') -Value 'first-run bootstrap searchable text'
```

## 2. Запустить стек без ручного ingestion-триггера

```powershell
$env:ROOT_HOST_WORKSPACE_PATH = $workspace
$env:NDLSS_WORKSPACE = $workspace
docker compose up -d
```

Ожидается:
- сервисы `qdrant`, `file-indexer`, `mcp-server` переходят в healthy;
- в логах `mcp-server` есть structured-событие bootstrap (`run` или `skip-already-completed`).

## 3. Проверить startup readiness и bootstrap-контекст

```powershell
$readiness = Invoke-RestMethod -Method Get -Uri 'http://localhost:8080/v1/system/startup/readiness'
$readiness | ConvertTo-Json -Depth 8
```

Ожидается:
- заполнен блок `bootstrap`;
- `collection.collectionName = workspace_chunks` (или заданное имя);
- `collection.exists = true`.

## 4. Проверить, что коллекция создана и содержит точки

```powershell
Invoke-RestMethod -Method Post -Uri 'http://localhost:6333/collections/workspace_chunks/points/count' -ContentType 'application/json' -Body '{"exact":false}'
```

Ожидается:
- запрос успешен;
- `result.count > 0` для непустого workspace.

## 5. Проверить, что restart не дублирует дорогой bootstrap

```powershell
$before = (Invoke-RestMethod -Method Post -Uri 'http://localhost:6333/collections/workspace_chunks/points/count' -ContentType 'application/json' -Body '{"exact":false}').result.count

docker compose restart mcp-server file-indexer
Start-Sleep -Seconds 8

$after = (Invoke-RestMethod -Method Post -Uri 'http://localhost:6333/collections/workspace_chunks/points/count' -ContentType 'application/json' -Body '{"exact":false}').result.count
"before=$before after=$after"
$postRestartReadiness = Invoke-RestMethod -Method Get -Uri 'http://localhost:8080/v1/system/startup/readiness'
$postRestartReadiness.bootstrap | ConvertTo-Json -Depth 8
```

Ожидается:
- в readiness/logs отражается `bootstrap.decision = skip-already-completed`;
- `after` не растет из-за дублирующего полного bootstrap.

## 6. Проверить доступность ручного ingestion endpoint

```powershell
Invoke-RestMethod -Method Post -Uri 'http://localhost:8080/v1/indexing/ingestion/jobs' -ContentType 'application/json' -Body (@{ workspacePath = '/workspace' } | ConvertTo-Json)
```

Ожидается:
- endpoint отвечает `202` и возвращает `runId`;
- ручной режим остается рабочим и обратно совместимым.

## 7. Очистка

```powershell
docker compose down
Remove-Item Env:ROOT_HOST_WORKSPACE_PATH -ErrorAction SilentlyContinue
Remove-Item Env:NDLSS_WORKSPACE -ErrorAction SilentlyContinue
```

## Последний smoke run (2026-02-22)

- Сценарий: `scripts/tests/startup_bootstrap_smoke.ps1`
- Статус: `passed`
- Порты: `MCP_PORT=18080`, `QDRANT_PORT=16333`, `QDRANT_API_PORT=6333`
- Коллекция: `workspace_chunks`
- Количество точек после bootstrap: `7`
- Артефакт: `tests/artifacts/quality-stability/startup-bootstrap-smoke.json`

