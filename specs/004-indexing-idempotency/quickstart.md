# Quickstart: Идемпотентность индексации

## Цель

Проверить, что повторная индексация неизмененных данных не создает дубликатов,
измененные файлы обновляются, а устаревшие чанки удаляются.

## Требования

- Docker Engine / Docker Desktop
- Docker Compose v2
- Рабочая директория с тестовыми файлами

## Подготовка

1. Поднимите стек:

```bash
docker compose -f Z:\WORK\ndlss-memory\infra\docker\docker-compose.yml --env-file Z:\WORK\ndlss-memory\.env.example up -d --build
```

2. Убедитесь, что сервис `mcp-server` отвечает:

```bash
curl http://localhost:8080/health
```

## Сценарий 1: Базовый запуск

```bash
curl -X POST http://localhost:8080/v1/indexing/idempotency/jobs
```

Сохраните `runId`, дождитесь завершения и получите summary:

```bash
curl http://localhost:8080/v1/indexing/idempotency/jobs/<runId>/summary
```

Проверьте поля:

- `updatedChunks`
- `skippedChunks`
- `deletedChunks`
- `failedChunks`
- `reasonBreakdown`

## Сценарий 2: Повторный запуск без изменений

1. Повторите `POST /v1/indexing/idempotency/jobs` без изменения файлов.
2. Сравните summary первого и второго запуска.

Ожидание:

- `skippedChunks` растет или остается доминирующим.
- Количество уникальных записей не растет сверх допустимого отклонения.

## Сценарий 3: Изменение и удаление

1. Измените содержимое одного файла.
2. Удалите один ранее индексированный файл.
3. Запустите синхронизацию повторно.

Ожидание:

- `updatedChunks` отражает изменения контента.
- `deletedChunks` отражает удаленные/устаревшие чанки.
- `failedChunks` равен 0 в штатном сценарии.
- `reasonBreakdown` содержит коды `DELETED_STALE` и/или `DELETED_SOURCE_REMOVED`.

## Troubleshooting

- `409` при старте run: уже выполняется другой idempotency run.
- `RUN_NOT_FINISHED` для summary: дождитесь терминального статуса.
- Высокий `failedChunks`: проверьте логи `mcp-server` и `file-indexer`.
- Отсутствует `deletedChunks` после удаления файла: проверьте, что файл
  ранее был проиндексирован и что cleanup включен в текущем запуске.
