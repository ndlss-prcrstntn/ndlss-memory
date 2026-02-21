# Quickstart: Безопасный запуск команд через MCP

## Цель

Проверить безопасность командного рантайма MCP:

1. allowlist enforcement
2. timeout enforcement
3. workspace isolation
4. structured errors
5. audit logging

## Требования

- Docker Engine / Docker Desktop
- Docker Compose v2
- Запущенный стек `qdrant + file-indexer + mcp-server`
- Настроенная политика `COMMAND_ALLOWLIST` и `COMMAND_TIMEOUT_SECONDS`

## Подготовка

1. Запустите стек:

```bash
docker compose -f Z:\WORK\ndlss-memory\infra\docker\docker-compose.yml --env-file Z:\WORK\ndlss-memory\.env.example up -d --build
```

2. Проверьте здоровье:

```bash
curl http://localhost:8080/health
powershell -File Z:\WORK\ndlss-memory\scripts\ops\stack-status.ps1
```

## Сценарий 1: Разрешенная команда

```bash
curl -X POST http://localhost:8080/v1/commands/execute \
  -H "Content-Type: application/json" \
  -d '{"command":"pwd","args":[],"workingDirectory":"/workspace"}'
```

Ожидание:

- HTTP 200
- `status=ok`
- присутствуют `result` и `meta.requestId`

## Сценарий 2: Блокировка команды вне allowlist

```bash
curl -X POST http://localhost:8080/v1/commands/execute \
  -H "Content-Type: application/json" \
  -d '{"command":"rm","args":["-rf","/"],"workingDirectory":"/workspace"}'
```

Ожидание:

- HTTP 403
- машиночитаемая ошибка `errorCode`
- команда фактически не запускается

## Сценарий 3: Таймаут выполнения

```bash
curl -X POST http://localhost:8080/v1/commands/execute \
  -H "Content-Type: application/json" \
  -d '{"command":"sleep","args":["30"],"workingDirectory":"/workspace","timeoutSeconds":2}'
```

Ожидание:

- HTTP 200
- `status=timeout`
- `result.errorCode=COMMAND_TIMEOUT`

## Сценарий 4: Изоляция рабочей директории

```bash
curl -X POST http://localhost:8080/v1/commands/execute \
  -H "Content-Type: application/json" \
  -d '{"command":"ls","args":[],"workingDirectory":"/etc"}'
```

Ожидание:

- запрос отклоняется
- возвращается ошибка изоляции рабочей директории

## Сценарий 5: Аудит вызовов

```bash
curl "http://localhost:8080/v1/commands/audit?limit=20"
```

Ожидание:

- `status=ok`
- `records[]` содержит успешные и/или отклоненные вызовы
- в каждой записи есть `requestId`, `timestamp`, `command`, `status`

## Troubleshooting

- `400 INVALID_REQUEST`: проверьте формат JSON, command и workingDirectory.
- `403 COMMAND_NOT_ALLOWED`: команда отсутствует в allowlist.
- `408 COMMAND_TIMEOUT`: команда превысила лимит времени.
- `404 REQUEST_NOT_FOUND`: result/audit запрос с неизвестным requestId.
