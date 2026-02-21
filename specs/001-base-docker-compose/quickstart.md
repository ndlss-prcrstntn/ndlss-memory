# Quickstart: Базовый Docker Compose стек

## Цель

Поднять базовый стек (`qdrant`, `file-indexer`, `mcp-server`), проверить
готовность сервисов и выполнить базовую диагностику.

## Требования

- Docker Engine / Docker Desktop
- Docker Compose v2
- PowerShell 7+ (для скриптов из `scripts/`)

## Подготовка

1. Скопируйте `.env.example` в `.env` при необходимости локальных изменений.
2. Проверьте значения в `.env.example` или `.env`.

## Запуск

```bash
pwsh scripts/dev/up.ps1
```

Либо напрямую:

```bash
docker compose -f infra/docker/docker-compose.yml --env-file .env.example up -d --build
```

## Проверка состояния

```bash
docker compose -f infra/docker/docker-compose.yml ps
pwsh scripts/ops/stack-status.ps1
```

Проверка health endpoint:

```bash
curl http://localhost:8080/health
```

## Остановка

```bash
pwsh scripts/dev/down.ps1
```

Полная очистка с volume:

```bash
pwsh scripts/dev/down.ps1 -RemoveVolumes
```

## Проверка режимов индексатора

1. Установите `INDEX_MODE=full-scan` и перезапустите стек.
2. Установите `INDEX_MODE=delta-after-commit` и перезапустите стек.
3. Убедитесь, что статус `file-indexer` остается healthy.

## Troubleshooting

- Порт занят: измените `QDRANT_PORT` или `MCP_PORT` в env-файле.
- `file-indexer` unhealthy: проверьте `INDEX_MODE` и `INDEX_FILE_TYPES`.
- `mcp-server` unhealthy: проверьте логи и доступность порта MCP.
- Ошибка mount: проверьте `HOST_WORKSPACE_PATH` и права доступа.

## Критерии готовности

- Все три сервиса в состоянии healthy.
- `/v1/system/status` возвращает агрегированный статус.
- Перезапуск не теряет данные Qdrant в стандартном цикле.
