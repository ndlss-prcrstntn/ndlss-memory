# Quickstart: MCP Transport Compatibility

## Цель

Проверить, что `ndlss-memory` доступен как MCP transport (а не только REST API):
`POST /mcp`, `GET /sse` + `POST /messages`, `GET /.well-known/mcp`,
а также базовые MCP методы и инструменты.

## Prerequisites

- Docker Engine + Docker Compose v2
- Доступ к репозиторию `Z:\WORK\ndlss-memory`
- Любой HTTP-клиент (PowerShell/curl) и MCP-клиент (VS Code/Claude/Cline)

## 1. Поднять стек

```powershell
Set-Location Z:\WORK\ndlss-memory
docker compose up -d
```

Проверить health:

```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:8080/health"
```

Ожидаемый результат: `status=ok`.

## 2. Проверить discovery и transport endpoint-ы

```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:8080/.well-known/mcp"
Invoke-WebRequest -Method Post -Uri "http://localhost:8080/mcp" -ContentType "application/json" -Body '{"jsonrpc":"2.0","id":1,"method":"ping"}'
Invoke-WebRequest -Method Get -Uri "http://localhost:8080/sse"
```

Ожидаемый результат:
- discovery возвращает JSON с transport/capabilities;
- `/mcp` возвращает JSON-RPC envelope;
- `/sse` доступен как event-stream endpoint.

## 3. Выполнить MCP handshake через `/mcp`

```powershell
$init = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"clientInfo":{"name":"manual-check","version":"1.0.0"}}}'
Invoke-RestMethod -Method Post -Uri "http://localhost:8080/mcp" -ContentType "application/json" -Body $init

$initialized = '{"jsonrpc":"2.0","id":null,"method":"notifications/initialized","params":{}}'
Invoke-RestMethod -Method Post -Uri "http://localhost:8080/mcp" -ContentType "application/json" -Body $initialized

$ping = '{"jsonrpc":"2.0","id":2,"method":"ping","params":{}}'
Invoke-RestMethod -Method Post -Uri "http://localhost:8080/mcp" -ContentType "application/json" -Body $ping
```

Ожидаемый результат: все три вызова завершаются без protocol error.

## 4. Проверить `tools/list` и `tools/call`

```powershell
$toolsList = '{"jsonrpc":"2.0","id":3,"method":"tools/list","params":{}}'
Invoke-RestMethod -Method Post -Uri "http://localhost:8080/mcp" -ContentType "application/json" -Body $toolsList

$toolCall = '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"semantic_search","arguments":{"query":"docker compose healthcheck","limit":5}}}'
Invoke-RestMethod -Method Post -Uri "http://localhost:8080/mcp" -ContentType "application/json" -Body $toolCall
```

Ожидаемый результат:
- `tools/list` содержит минимум 5 заявленных инструментов;
- `tools/call` возвращает структурированный `result` (или валидную JSON-RPC `error`).

## 5. Проверить сценарий отсутствующей коллекции

Если индексация еще не запускалась, вызов поиска не должен падать backend 5xx.

```powershell
$toolCall = '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"semantic_search","arguments":{"query":"first run","limit":5}}}'
Invoke-RestMethod -Method Post -Uri "http://localhost:8080/mcp" -ContentType "application/json" -Body $toolCall
```

Ожидаемый результат: корректный пустой результат поиска (empty), а не transport/backend fatal.

## 6. Подключить MCP-клиент

Используйте runtime-конфигурацию клиента с endpoint-ом transport, указанным в discovery.
Минимальный пример (если клиент поддерживает streamable HTTP):

```json
{
  "servers": {
    "ndlss-memory": {
      "transport": "http",
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

## 7. Прогнать contract/integration проверки

```powershell
python -m pytest tests/unit/mcp_server
powershell -File scripts/tests/contract_quality_stability.ps1
```

Ожидаемый результат: MCP transport и tool контракты проходят без регрессий.

## 8. Остановка стека

```powershell
docker compose down
```
