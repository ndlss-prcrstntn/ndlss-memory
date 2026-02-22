# Contract: MCP Transport Handshake

## Preconditions

- `mcp-server` доступен на `http://localhost:8080`
- endpoint-ы `/mcp`, `/sse`, `/messages`, `/.well-known/mcp` зарегистрированы

## Handshake Envelope

- [ ] `POST /mcp` с `initialize` возвращает JSON-RPC envelope (`jsonrpc`, `id`, `result`)
- [ ] `result.protocolVersion` присутствует и не пустой
- [ ] `result.capabilities.tools` присутствует
- [ ] `notifications/initialized` возвращает `result.acknowledged=true`
- [ ] `ping` возвращает `result.pong=true`

## Transport Errors

- [ ] malformed JSON на `/mcp` возвращает JSON-RPC error с `code=-32700`
- [ ] unsupported method возвращает JSON-RPC error с `code=-32601`
- [ ] ошибка содержит машиночитаемый `error.data.errorCode`

