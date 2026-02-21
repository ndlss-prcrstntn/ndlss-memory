# ndlss-memory

`ndlss-memory` - локальный MCP-стек на Docker Compose для индексации файлов,
поиска контекста и безопасных tool-вызовов.

## Сервисы

- `qdrant`: хранение векторных данных и метаданных.
- `file-indexer`: сбор и обработка файлов из смонтированной директории.
- `mcp-server`: API/контракт статуса и входная точка для MCP-клиентов.

## Архитектура

```text
Host workspace (bind mount)
        |
        v
  file-indexer -----> qdrant (named volume)
        |
        v
      mcp-server <---- AI clients / IDE / agents
```

## Быстрый старт

```bash
pwsh scripts/dev/up.ps1
```

Проверка:

```bash
docker compose -f infra/docker/docker-compose.yml ps
pwsh scripts/ops/stack-status.ps1
curl http://localhost:8080/health
```

Остановка:

```bash
pwsh scripts/dev/down.ps1
```

## Ключевая конфигурация

Смотрите `.env.example` и `docs/configuration.md`.

- `INDEX_MODE=full-scan|delta-after-commit`
- `INDEX_FILE_TYPES=.md,.txt,...`
- `INDEX_EXCLUDE_PATTERNS=.git,node_modules,...`
- `COMMAND_ALLOWLIST=...`
- `COMMAND_TIMEOUT_SECONDS=...`

## Диагностика и recovery

- Операционный статус: `GET /v1/system/status`
- Конфигурация рантайма: `GET /v1/system/config`
- Статус сервиса: `GET /v1/system/services/{serviceName}`
- Диагностика из CLI: `pwsh scripts/ops/stack-status.ps1`

Если сервис unhealthy:

1. Проверьте `docker compose -f infra/docker/docker-compose.yml logs <service>`
2. Уточните env-параметры в `.env`/`.env.example`
3. Перезапустите стек (`up`/`down` скрипты)

## Документация фичи

- Спецификация: `specs/001-base-docker-compose/spec.md`
- План: `specs/001-base-docker-compose/plan.md`
- Задачи: `specs/001-base-docker-compose/tasks.md`
- Quickstart: `specs/001-base-docker-compose/quickstart.md`
- Контракт: `specs/001-base-docker-compose/contracts/compose-observability.openapi.yaml`

