# Contract Test: Full Scan Jobs API (Base)

## Goal

Проверить базовый контракт API задач полной индексации.

## Preconditions

- Compose-стек запущен.
- `mcp-server` доступен на `http://localhost:8080`.

## Checks

1. `POST /v1/indexing/full-scan/jobs` возвращает `202` и `jobId`.
2. `GET /v1/indexing/full-scan/jobs/{jobId}` возвращает `200` со статусом задачи.
3. `GET /v1/indexing/full-scan/jobs/unknown` возвращает `404` с машиночитаемой ошибкой.
4. `GET /v1/indexing/full-scan/jobs/{jobId}/summary` до завершения возвращает `409`.

## Expected Error Shape

```json
{
  "errorCode": "STRING_CODE",
  "message": "Human readable message",
  "details": "Optional details"
}
```

