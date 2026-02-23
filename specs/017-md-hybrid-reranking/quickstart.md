# Quickstart: Reranking over Hybrid Docs Search (Markdown Only)

## Goal

Проверить, что:
- docs-search применяет reranking поверх первичного hybrid этапа;
- reranking ограничен markdown docs-коллекцией;
- при деградации reranking работает контролируемый fallback;
- non-docs поиск сохраняет прежнее поведение.

## Prerequisites

- Репозиторий: `Z:\WORK\ndlss-memory`
- Запущен стек: `docker compose --env-file .env.mcp-dev up -d --build`
- `mcp-server` доступен по `http://localhost:8080`
- docs-коллекция проиндексирована (`POST /v1/indexing/docs/jobs`)

## Scenario 1: Prepare docs index

```powershell
$indexBody = @{
  workspacePath = "/workspace"
  includeExtensions = @(".md")
} | ConvertTo-Json

$run = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/indexing/docs/jobs" -ContentType "application/json" -Body $indexBody
$run
```

Expected:
- `runId` получен;
- запуск принят без ошибки.

## Scenario 2: Run docs search with reranking

```powershell
$searchBody = @{
  query = "startup readiness checks"
  limit = 5
} | ConvertTo-Json

$result = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/search/docs/query" -ContentType "application/json" -Body $searchBody
$result
```

Expected:
- `appliedStrategy=bm25_plus_vector_rerank_docs_only`;
- `fallbackApplied=false` при нормальном состоянии reranking;
- каждый результат содержит `rankingSignals.lexical`, `rankingSignals.semantic`, `rankingSignals.rerank`.

## Scenario 3: Validate deterministic output

```powershell
$first = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/search/docs/query" -ContentType "application/json" -Body $searchBody
$second = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/search/docs/query" -ContentType "application/json" -Body $searchBody

$first.results | Select-Object -First 5
$second.results | Select-Object -First 5
```

Expected:
- top-5 порядок стабилен для неизменного индекса;
- tie-break работает предсказуемо.

## Scenario 4: Validate fallback behavior

Смоделировать деградацию reranking этапа через `DOCS_RERANK_FORCE_FAILURE=1` (в тестовом окружении) и повторить docs-запрос.

Expected:
- запрос не падает;
- `fallbackApplied=true`;
- структура ответа остается контрактно валидной.

## Scenario 5: Validate non-docs compatibility

```powershell
$semanticBody = @{
  query = "startup readiness checks"
  limit = 5
} | ConvertTo-Json

$semantic = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/search/semantic" -ContentType "application/json" -Body $semanticBody
$semantic
```

Expected:
- non-docs endpoint возвращает прежний формат;
- reranking-specific поля не появляются в semantic-search ответе.

## Scenario 6: Validate invalid input and availability errors

```powershell
$invalid = @{ query = "   " } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8080/v1/search/docs/query" -ContentType "application/json" -Body $invalid
```

Expected:
- HTTP 400 с `errorCode=SEARCH_QUERY_EMPTY`.

При недоступности docs-коллекции или полного отказа fallback:

Expected:
- HTTP 503 с `errorCode=DOCS_COLLECTION_UNAVAILABLE` или `DOCS_RERANKING_UNAVAILABLE`.

## Scenario 7: MCP docs tool parity

Вызов MCP `tools/call` инструмента `search_docs` с тем же запросом.

Expected:
- структура ответа согласована с docs endpoint;
- scope остается docs-only;
- при fallback поведение и семантика ошибок остаются машиночитаемыми.
