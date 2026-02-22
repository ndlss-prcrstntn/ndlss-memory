# Quickstart: Traversal Depth + Max Files Limits

## Цель

Проверить, что запуски индексации поддерживают два ограничителя:
- `maxTraversalDepth`
- `maxFilesPerRun`

и что summary показывает примененные лимиты и причины пропуска файлов.

## Prerequisites

- Репозиторий: `Z:\WORK\ndlss-memory`
- Запущен стек: `docker compose up -d --build`
- Сервис `mcp-server` доступен по `http://localhost:8080` (или по переопределенному `MCP_PORT`)
- Опциональные дефолты лимитов через окружение:
  - `INDEX_MAX_TRAVERSAL_DEPTH`
  - `INDEX_MAX_FILES_PER_RUN`

## Scenario 1: Full-scan с ограничением глубины и количества файлов

1. Запустите full-scan с лимитами:

```powershell
$body = @{
  workspacePath = "/workspace"
  maxTraversalDepth = 2
  maxFilesPerRun = 100
} | ConvertTo-Json

$job = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/indexing/full-scan/jobs" -ContentType "application/json" -Body $body
$job
```

2. Дождитесь завершения и получите summary:

```powershell
$summary = Invoke-RestMethod -Method Get -Uri "http://localhost:8080/v1/indexing/full-scan/jobs/$($job.jobId)/summary"
$summary
```

3. Проверьте в ответе:
- `appliedLimits.maxTraversalDepth == 2`
- `appliedLimits.maxFilesPerRun == 100`
- при превышении лимитов есть `skipBreakdown` с кодами:
  - `LIMIT_DEPTH_EXCEEDED`
  - `LIMIT_MAX_FILES_REACHED`

## Scenario 2: Ingestion path с теми же лимитами

1. Запустите ingestion с лимитами:

```powershell
$body = @{
  workspacePath = "/workspace"
  maxTraversalDepth = 1
  maxFilesPerRun = 50
} | ConvertTo-Json

$run = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/indexing/ingestion/jobs" -ContentType "application/json" -Body $body
$run
```

2. Получите summary:

```powershell
$summary = Invoke-RestMethod -Method Get -Uri "http://localhost:8080/v1/indexing/ingestion/jobs/$($run.runId)/summary"
$summary
```

3. Проверьте, что лимиты и skip reasons отражены аналогично full-scan сценарию.

## Scenario 3: Backward compatibility (лимиты не заданы)

1. Запустите full-scan без лимитов:

```powershell
$body = @{ workspacePath = "/workspace" } | ConvertTo-Json
$job = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/indexing/full-scan/jobs" -ContentType "application/json" -Body $body
$job
```

2. Получите summary и проверьте:
- `appliedLimits.maxTraversalDepth == null`
- `appliedLimits.maxFilesPerRun == null`
- пропуски по кодам `LIMIT_DEPTH_EXCEEDED` / `LIMIT_MAX_FILES_REACHED` отсутствуют.

## Negative scenario: невалидные значения лимитов

```powershell
$body = @{
  workspacePath = "/workspace"
  maxTraversalDepth = -1
  maxFilesPerRun = 0
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/indexing/full-scan/jobs" -ContentType "application/json" -Body $body
```

Ожидание: запрос отклоняется с ошибкой валидации лимитов.
