# Integration Smoke: MCP Handshake Endpoints

1. Запустить стек:
   - `pwsh scripts/dev/up.ps1`
2. Проверить discovery:
   - `GET http://localhost:8080/.well-known/mcp`
3. Проверить streamable HTTP:
   - `POST http://localhost:8080/mcp` с `initialize`
4. Проверить legacy SSE connect:
   - `GET http://localhost:8080/sse`
   - убедиться, что присутствует `X-MCP-Session-Id`
5. Проверить ping:
   - `POST /mcp` с `ping` и тем же `X-MCP-Session-Id`
6. Проверить отрицательный сценарий:
   - `POST /mcp` с неизвестным `method`
   - ожидается JSON-RPC error `-32601`

