# Integration: Filters And Empty Result

## Цель

Проверить фильтры и обработку пустых результатов без internal errors.

## Шаги

1. Запрос с фильтрами:
   - `POST /v1/search/semantic`
   - body: `{"query":"healthcheck","filters":{"folder":"docs","fileType":".md"}}`
2. Проверить, что каждый результат удовлетворяет фильтрам.
3. Запрос без совпадений:
   - `POST /v1/search/semantic`
   - body: `{"query":"definitely-no-match-phrase-123456"}`
4. Проверить:
   - HTTP 200
   - `status=empty`
   - `results=[]`
   - присутствует `meta`
