# Quickstart: Watch Mode Incremental Indexing

Этот сценарий проверяет, что `INDEX_MODE=watch` автоматически обновляет индекс при изменении файлов без ручного запуска ingestion job.

## Предусловия

- Docker Engine + Docker Compose v2
- PowerShell 7+
- Репозиторий: `Z:\WORK\ndlss-memory`

## 1. Подготовить рабочую директорию

```powershell
Set-Location 'Z:\WORK\ndlss-memory'
$workspace = 'Z:\WORK\tmp\watch-mode-smoke'
Remove-Item $workspace -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $workspace | Out-Null
Set-Content -Path (Join-Path $workspace 'notes.md') -Value 'watch mode initial content'
```

## 2. Запустить стек в режиме watch

```powershell
$env:ROOT_HOST_WORKSPACE_PATH = $workspace
$env:INDEX_MODE = 'watch'
$env:WATCH_POLL_INTERVAL_SECONDS = '3'
$env:WATCH_COALESCE_WINDOW_SECONDS = '2'
$env:WATCH_RECONCILE_INTERVAL_SECONDS = '30'
docker compose up -d
```

Ожидается:
- сервисы переходят в healthy;
- в логах есть события запуска watch-loop (`starting -> running`).

## 3. Проверить статус watch

```powershell
Invoke-RestMethod -Method Get -Uri 'http://localhost:8080/v1/indexing/watch/status' | ConvertTo-Json -Depth 8
```

Ожидается:
- `mode = watch`;
- `state = running`;
- `queueDepth` и счетчики событий присутствуют.

## 4. Проверить create/update/delete без ручного триггера

### 4.1 Create

```powershell
Set-Content -Path (Join-Path $workspace 'feature.md') -Value 'watch create event searchable text'
Start-Sleep -Seconds 5
Invoke-RestMethod -Method Post -Uri 'http://localhost:8080/v1/search/semantic' -ContentType 'application/json' -Body '{"query":"create event searchable text","limit":5}' | ConvertTo-Json -Depth 8
```

### 4.2 Update

```powershell
Set-Content -Path (Join-Path $workspace 'feature.md') -Value 'watch updated content searchable text'
Start-Sleep -Seconds 5
Invoke-RestMethod -Method Post -Uri 'http://localhost:8080/v1/search/semantic' -ContentType 'application/json' -Body '{"query":"updated content searchable text","limit":5}' | ConvertTo-Json -Depth 8
```

### 4.3 Delete

```powershell
Remove-Item (Join-Path $workspace 'feature.md') -Force
Start-Sleep -Seconds 5
Invoke-RestMethod -Method Post -Uri 'http://localhost:8080/v1/search/semantic' -ContentType 'application/json' -Body '{"query":"updated content searchable text","limit":5}' | ConvertTo-Json -Depth 8
```

Ожидается:
- после create/update поиск отражает изменения;
- после delete данные файла не возвращаются как актуальные.

## 5. Burst-проверка устойчивости

```powershell
1..120 | ForEach-Object {
  Set-Content -Path (Join-Path $workspace ("burst-$_.md")) -Value ("burst file $_")
}
Start-Sleep -Seconds 10
Invoke-RestMethod -Method Get -Uri 'http://localhost:8080/v1/indexing/watch/status' | ConvertTo-Json -Depth 8
Invoke-RestMethod -Method Get -Uri 'http://localhost:8080/v1/indexing/watch/summary' | ConvertTo-Json -Depth 8
```

Ожидается:
- watcher остается в `running` или кратковременно `recovering` с возвратом в `running`;
- summary содержит агрегированные счетчики обработанных/ошибочных событий.

## 6. Проверка восстановления после ошибки

```powershell
# Вариант: временно остановить зависимость, затем вернуть
# docker stop ndlss-memory-qdrant
# Start-Sleep -Seconds 10
# docker start ndlss-memory-qdrant
# Start-Sleep -Seconds 20
Invoke-RestMethod -Method Get -Uri 'http://localhost:8080/v1/indexing/watch/status' | ConvertTo-Json -Depth 8
```

Ожидается:
- фиксируется ошибка и retry/backoff;
- watch-loop не останавливается навсегда и возвращается в рабочее состояние.

## 7. Очистка

```powershell
docker compose down
Remove-Item Env:ROOT_HOST_WORKSPACE_PATH -ErrorAction SilentlyContinue
Remove-Item Env:INDEX_MODE -ErrorAction SilentlyContinue
```

