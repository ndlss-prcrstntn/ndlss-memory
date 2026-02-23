# Quickstart: Docs Collection Indexing + Baseline Docs Search

## Цель

Проверить, что:
- markdown-документы индексируются в отдельную docs-коллекцию;
- docs-поиск использует только docs-коллекцию;
- существующий поиск по коду остается совместимым.

## Prerequisites

- Репозиторий: `Z:\WORK\ndlss-memory`
- Запущен стек: `docker compose up -d --build`
- Сервис `mcp-server` доступен по `http://localhost:8080`

## Scenario 1: Запуск docs-индексации

```powershell
$body = @{
  workspacePath = "/workspace"
  includeExtensions = @(".md")
} | ConvertTo-Json

$run = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/indexing/docs/jobs" -ContentType "application/json" -Body $body
$run
```

Ожидание:
- возвращается `runId` и `status=running`.

## Scenario 2: Получение summary docs-индексации

```powershell
$summary = Invoke-RestMethod -Method Get -Uri "http://localhost:8080/v1/indexing/docs/jobs/$($run.runId)/summary"
$summary
```

Ожидание:
- есть `totals.processedDocuments`, `totals.indexedDocuments`, `totals.skippedDocuments`;
- присутствует `skipBreakdown` с машиночитаемыми кодами;
- при отсутствии markdown-документов запуск завершается без падения.

## Scenario 3: Baseline docs-поиск

```powershell
$searchBody = @{
  query = "startup readiness"
  limit = 5
} | ConvertTo-Json

$result = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/search/docs/query" -ContentType "application/json" -Body $searchBody
$result
```

Ожидание:
- выдача содержит только элементы с `sourceType=documentation`;
- каждый элемент содержит `documentPath`, `chunkIndex`, `snippet`, `score`;
- для неизменных данных повтор запроса возвращает стабильный top-k порядок.

## Scenario 4: Empty result

```powershell
$searchBody = @{ query = "nonexistent_docs_term_12345" } | ConvertTo-Json
$result = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/search/docs/query" -ContentType "application/json" -Body $searchBody
$result
```

Ожидание:
- `total=0`, `results=[]`, статус запроса успешный.

## Scenario 5: Backward compatibility для code search

1. Выполнить существующий запрос к основному поиску по коду.
2. Убедиться, что формат ответа и поведение не изменились после добавления docs-коллекции.

Ожидание:
- docs-функциональность не ломает текущий сценарий code-search.

## Scenario 6: MCP docs-search tool

Вызов MCP `tools/call` для инструмента `search_docs` с аргументами:

```json
{
  "name": "search_docs",
  "arguments": {
    "query": "startup readiness",
    "limit": 5
  }
}
```

Ожидание:
- возвращается `query`, `total`, `results`;
- каждый элемент `results` имеет `sourceType=documentation`.
