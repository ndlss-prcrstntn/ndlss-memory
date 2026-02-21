# Quickstart: Режим Full Scan

## Цель

Запустить задачу полной индексации (`full-scan`), отслеживать прогресс и получить
итоговый отчет с причинами пропусков.

## Требования

- Docker Engine / Docker Desktop
- Docker Compose v2
- Доступный workspace с файлами для индексации

## Подготовка

1. Убедитесь, что стек запущен:

```bash
docker compose -f Z:\WORK\ndlss-memory\infra\docker\docker-compose.yml --env-file Z:\WORK\ndlss-memory\.env.example up -d --build
```

2. Проверьте, что `INDEX_MODE=full-scan` и настроены:
- `INDEX_FILE_TYPES`
- `INDEX_EXCLUDE_PATTERNS`
- `HOST_WORKSPACE_PATH`
- `INDEX_MAX_FILE_SIZE_BYTES`
- `INDEX_PROGRESS_INTERVAL_SECONDS`

## Запуск Full Scan

```bash
curl -X POST http://localhost:8080/v1/indexing/full-scan/jobs
```

Ожидаемый ответ содержит `jobId`.

## Проверка прогресса

```bash
curl http://localhost:8080/v1/indexing/full-scan/jobs/<jobId>
```

Проверяйте, что обновляются поля:
- `processedCount`
- `indexedCount`
- `skipCount`
- `errorCount`
- `status`

## Получение итогового отчета

После завершения задачи:

```bash
curl http://localhost:8080/v1/indexing/full-scan/jobs/<jobId>/summary
```

Проверьте:
- итоговый статус
- длительность
- статистику обработанных/пропущенных файлов
- разбиение причин пропуска (`skipBreakdown`)

## Базовая валидация результата

- Все файлы поддерживаемых типов обработаны.
- Исключенные паттернами файлы не попали в индекс.
- Файлы больше лимита отражены как `FILE_TOO_LARGE`.
- Ошибки чтения не остановили задачу целиком.

## Проверка правил фильтрации

1. Убедитесь, что `INDEX_FILE_TYPES` включает только нужные расширения.
2. Проверьте `INDEX_EXCLUDE_PATTERNS` (например: `.git,node_modules,dist`).
3. Запросите summary и проверьте `skipBreakdown`:
- `UNSUPPORTED_TYPE` для неподдерживаемых расширений.
- `EXCLUDED_BY_PATTERN` для исключенных путей.

## Troubleshooting

- `404 job not found`: проверьте корректность `jobId`.
- `409 full scan already running`: дождитесь завершения текущей задачи.
- Прогресс не меняется: проверьте логи `file-indexer` и mount `HOST_WORKSPACE_PATH`.
- Слишком много пропусков: проверьте `INDEX_FILE_TYPES` и `INDEX_EXCLUDE_PATTERNS`.
