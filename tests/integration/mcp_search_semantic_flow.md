# Integration: Semantic Search Flow

## Цель

Проверить базовый сценарий semantic search и ограничение `limit`.

## Шаги

1. Отправить `POST /v1/search/semantic` с телом:
   - `{"query":"docker compose","limit":3}`
2. Проверить, что:
   - HTTP 200
   - `status` равен `ok` или `empty`
   - `meta.limit` равен `3`
   - `len(results) <= 3`
3. При `status=ok` убедиться, что каждый элемент содержит:
   - `resultId`, `score`, `snippet`, `sourcePath`, `fileType`
