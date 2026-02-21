# Quickstart: MCP-инструменты поиска

## Цель

Проверить работу трех MCP-инструментов поиска:

1. semantic search
2. получение источника по `resultId`
3. получение метаданных документа по `resultId`

включая фильтрацию и обработку пустых результатов.

## Требования

- Docker Engine / Docker Desktop
- Docker Compose v2
- Запущенный стек `qdrant + file-indexer + mcp-server`
- Предварительно проиндексированный workspace

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

3. Убедитесь, что в индексе есть данные (full-scan/ingestion/idempotency уже выполнялись).

## Сценарий 1: Semantic Search

```bash
curl -X POST http://localhost:8080/v1/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query":"docker compose healthcheck","limit":5}'
```

Ожидание:

- `status=ok` или `status=empty`
- при `ok`: `results` содержит объекты с `resultId`, `score`, `snippet`, `sourcePath`
- `meta.count` соответствует размеру выдачи

## Сценарий 2: Получение источника по ID

1. Возьмите `resultId` из ответа semantic search.
2. Запросите источник:

```bash
curl http://localhost:8080/v1/search/results/<resultId>/source
```

Ожидание:

- `status=ok`
- в `source` присутствуют `resultId`, `content`, `sourcePath`
- для неизвестного ID: `404 RESULT_NOT_FOUND`

## Сценарий 3: Получение метаданных по ID

```bash
curl http://localhost:8080/v1/search/results/<resultId>/metadata
```

Ожидание:

- `status=ok`
- в `metadata` присутствуют `fileName`, `fileType`, `sourcePath`
- для неизвестного ID: `404 RESULT_NOT_FOUND`

## Сценарий 4: Фильтрация и пустой результат

Запрос с фильтрами:

```bash
curl -X POST http://localhost:8080/v1/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query":"healthcheck","filters":{"folder":"docs","fileType":".md"}}'
```

Запрос с пустой выдачей:

```bash
curl -X POST http://localhost:8080/v1/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query":"definitely-no-match-phrase-123456"}'
```

Ожидание:

- Фильтры применяются совместно (логическое И)
- Для пустой выдачи: `status=empty`, `results=[]`, без internal error

## Troubleshooting

- `400 INVALID_REQUEST`: проверьте `query` и формат `filters`.
- `404 RESULT_NOT_FOUND`: проверьте корректность `resultId`.
- Пустая выдача при ожидаемых совпадениях: проверьте, что индекс актуален и
  фильтры не слишком узкие.
- Низкая релевантность: проверьте полноту индексированных данных и качество
  входного запроса.
