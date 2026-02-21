# Quickstart: Пайплайн чанкинга и эмбеддингов

## Цель

Запустить ingestion pipeline для chunking + embedding + upsert и проверить,
что записи сохраняются с обязательными метаданными.

## Требования

- Docker Engine / Docker Desktop
- Docker Compose v2
- Доступный workspace с текстовыми файлами

## Подготовка

1. Поднимите стек:

```bash
docker compose -f Z:\WORK\ndlss-memory\infra\docker\docker-compose.yml --env-file Z:\WORK\ndlss-memory\.env.example up -d --build
```

2. Проверьте параметры запуска пайплайна в env:
- размер чанка
- overlap
- retry лимит эмбеддингов

## Запуск ingestion job

```bash
curl -X POST http://localhost:8080/v1/indexing/ingestion/jobs
```

Ожидаемый ответ содержит `runId`.

## Мониторинг прогресса

```bash
curl http://localhost:8080/v1/indexing/ingestion/jobs/<runId>
```

Проверяйте поля:
- `totalFiles`
- `totalChunks`
- `embeddedChunks`
- `failedChunks`
- `retryCount`
- `errorCode` / `errorMessage` (если run завершился с ошибкой)

## Получение итоговой сводки

```bash
curl http://localhost:8080/v1/indexing/ingestion/jobs/<runId>/summary
```

Проверьте:
- финальный статус (`completed|failed|partial`)
- количество успешно обработанных чанков
- количество ошибок и retry
- покрытие обязательных метаданных
- `metadataCoverage.path`
- `metadataCoverage.fileName`
- `metadataCoverage.fileType`
- `metadataCoverage.contentHash`
- `metadataCoverage.timestamp`

## Базовая проверка качества

- Чанки формируются с ожидаемым overlap.
- Эмбеддинги создаются для большинства чанков.
- Ошибки эмбеддингов отражаются в статистике и не теряются.
- В summary видны метаданные: path, fileName, fileType, contentHash, timestamp.

## Troubleshooting

- `409` при запуске: уже выполняется другая ingestion job.
- Высокий `failedChunks`: проверьте доступность embedding provider.
- Низкий `metadataCoverage`: проверьте маппинг источников перед upsert.
- `404` по runId: проверьте корректность идентификатора запуска.
