# Quickstart: Hybrid Search (BM25 + Vector) for Markdown Collection

## Goal

Проверить, что:
- `POST /v1/search/docs/query` выполняет гибридный поиск (BM25 + vector) по markdown-коллекции;
- гибридный режим не влияет на non-docs поиск;
- пустые/невалидные запросы обрабатываются машиночитаемыми ошибками;
- порядок top-k детерминирован для неизменного индекса.

## Prerequisites

- Репозиторий: `Z:\WORK\ndlss-memory`
- Запущен стек: `docker compose --env-file .env.mcp-dev up -d --build`
- `mcp-server` доступен по `http://localhost:8080`
- В docs-коллекции есть markdown-документы (при необходимости выполнить docs-only индексацию)

## Scenario 1: Run docs-only indexing

```powershell
$body = @{
  workspacePath = "/workspace"
  includeExtensions = @(".md")
} | ConvertTo-Json

$run = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/indexing/docs/jobs" -ContentType "application/json" -Body $body
$run
```

Expected:
- `runId` присутствует;
- `status=running`.

## Scenario 2: Validate indexing summary

```powershell
$summary = Invoke-RestMethod -Method Get -Uri "http://localhost:8080/v1/indexing/docs/jobs/$($run.runId)/summary"
$summary
```

Expected:
- summary содержит `totals` и `skipBreakdown`;
- запуск завершается без критической ошибки;
- при повторном запуске без изменений не появляются дубликаты.

## Scenario 3: Execute hybrid docs search

```powershell
$searchBody = @{
  query = "startup readiness checks"
  limit = 5
} | ConvertTo-Json

$result = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/search/docs/query" -ContentType "application/json" -Body $searchBody
$result
```

Expected:
- ответ содержит `appliedStrategy=bm25_plus_vector_docs_only`;
- каждый элемент результата имеет `sourceType=documentation`;
- каждый элемент содержит `rankingSignals.lexical` и `rankingSignals.semantic`.
- `appliedStrategy` и `rankingSignals` отсутствуют в non-docs endpoint-ах.

## Scenario 4: Validate scope isolation (non-docs unchanged)

```powershell
$semanticBody = @{
  query = "startup readiness checks"
  limit = 5
} | ConvertTo-Json

$semantic = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/search/semantic" -ContentType "application/json" -Body $semanticBody
$semantic
```

Expected:
- non-docs endpoint отвечает в прежнем контракте;
- hybrid-only поля docs endpoint-а не навязываются non-docs endpoint-у.

## Scenario 5: Validate deterministic top-k

```powershell
$first = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/search/docs/query" -ContentType "application/json" -Body $searchBody
$second = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/search/docs/query" -ContentType "application/json" -Body $searchBody

$first.results | Select-Object -First 5
$second.results | Select-Object -First 5
```

Expected:
- для неизменных данных состав и порядок top-5 совпадают (или имеют согласованный стабильный tie-break).

## Scenario 6: Validate invalid input handling

```powershell
$invalid = @{ query = "   " } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/search/docs/query" -ContentType "application/json" -Body $invalid
```

Expected:
- HTTP 400;
- тело ошибки содержит машиночитаемый `errorCode`.
- при временной недоступности docs-коллекции ожидается HTTP 503 с `errorCode=DOCS_COLLECTION_UNAVAILABLE`.

## Scenario 7: MCP tool compatibility

Вызов MCP `tools/call` для `search_docs` с валидным запросом должен вернуть docs-only выдачу в формате, согласованном с API.

Expected:
- инструмент `search_docs` остается совместимым;
- в ответе нет результатов из non-docs коллекций.
