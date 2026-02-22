# Contract: MCP Discovery & Client Config

## Preconditions

- `mcp-server` доступен на `http://localhost:8080`

## Discovery document

- [ ] `GET /.well-known/mcp` возвращает HTTP 200
- [ ] в ответе есть `name`, `version`, `transports`, `capabilities`
- [ ] `transports` содержит `streamable-http` URL, оканчивающийся на `/mcp`
- [ ] `transports` содержит `sse` URL, оканчивающийся на `/sse`
- [ ] `capabilities.methods` включает `initialize`, `tools/list`, `tools/call`

## Client configuration expectations

- [ ] пример VS Code/Claude/Cline указывает endpoint `http://localhost:8080/mcp`
- [ ] в документации есть troubleshooting для 404/405 при ошибочном endpoint

