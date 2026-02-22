# Contract: MCP Tools List/Call

## Preconditions

- MCP handshake успешно завершен
- доступен endpoint `POST /mcp`

## tools/list

- [ ] `tools/list` возвращает массив `tools`
- [ ] каталог содержит `semantic_search`
- [ ] каталог содержит `get_source_by_id`
- [ ] каталог содержит `get_metadata_by_id`
- [ ] каталог содержит `start_ingestion`
- [ ] каталог содержит `get_ingestion_status`

## tools/call

- [ ] `tools/call` с `semantic_search` возвращает JSON-RPC `result`
- [ ] `tools/call` с невалидными аргументами возвращает JSON-RPC `error`
- [ ] `error.data` содержит `errorCode`, `retryable` и при наличии `details`
- [ ] для несуществующего инструмента возвращается `code=-32601`

