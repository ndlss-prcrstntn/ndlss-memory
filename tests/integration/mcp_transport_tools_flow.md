# Integration: MCP Tools Flow

1. Выполнить `initialize` и `notifications/initialized` через `POST /mcp`.
2. Вызвать `tools/list`, проверить наличие 5 обязательных инструментов.
3. Вызвать `tools/call` для `semantic_search`.
4. Если поиск вернул результаты, вызвать:
   - `tools/call` для `get_source_by_id`
   - `tools/call` для `get_metadata_by_id`
5. Вызвать `tools/call` для `start_ingestion`.
6. Вызвать `tools/call` для `get_ingestion_status` с полученным `runId`.
7. Проверить негативный сценарий:
   - `tools/call` с `name=unknown_tool`
   - ожидается JSON-RPC `error` c `code=-32601`.

