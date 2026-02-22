# Конфигурация окружения

Файл `.env.example` содержит базовые параметры запуска стека.

## Обязательные параметры

- `QDRANT_PORT`: внешний host-порт Qdrant (только публикация на localhost).
- `QDRANT_API_PORT`: внутренний порт Qdrant для связи сервисов внутри docker-сети (`mcp-server`/`file-indexer` -> `qdrant`).
- `MCP_PORT`: внешний порт mcp-server.
- `INDEX_MODE`: `full-scan`, `delta-after-commit` или `watch`.
- `INDEX_FILE_TYPES`: расширения индексируемых файлов через запятую.
- `INDEX_EXCLUDE_PATTERNS`: исключаемые каталоги/паттерны.
- `INDEX_MAX_FILE_SIZE_BYTES`: лимит размера файла для Full Scan.
- `INDEX_PROGRESS_INTERVAL_SECONDS`: интервал обновления прогресса сканирования в секундах.
- `INGESTION_CHUNK_SIZE`: размер чанка для ingestion pipeline.
- `INGESTION_CHUNK_OVERLAP`: overlap между соседними чанками.
- `INGESTION_RETRY_MAX_ATTEMPTS`: лимит retry при ошибках эмбеддингов.
- `INGESTION_RETRY_BACKOFF_SECONDS`: пауза между retry эмбеддингов.
- `INGESTION_MAX_CHUNKS_PER_FILE`: максимальное число чанков на файл (опционально).
- `INGESTION_EMBEDDING_VECTOR_SIZE`: размерность тестового embedding adapter.
- `INGESTION_ENABLE_QDRANT_HTTP`: `1` включает HTTP upsert в Qdrant, `0` оставляет in-memory upsert.
- `INGESTION_UPSERT_TIMEOUT_SECONDS`: таймаут upsert-запроса в Qdrant.
- `INGESTION_BOOTSTRAP_ON_START`: `1` запускает ingestion при старте индексатора.
- `DELTA_GIT_BASE_REF`: базовая Git-ревизия для расчета изменений в режиме `delta-after-commit`.
- `DELTA_GIT_TARGET_REF`: целевая Git-ревизия для расчета изменений.
- `DELTA_INCLUDE_RENAMES`: `1` включает обработку rename как remove old + index new.
- `DELTA_ENABLE_FALLBACK`: `1` включает автоматический фоллбек на full-scan при ошибке git diff.
- `DELTA_BOOTSTRAP_ON_START`: `1` выполняет bootstrap delta-run при старте контейнера в режиме `delta-after-commit`.
- `WATCH_POLL_INTERVAL_SECONDS`: частота polling-цикла watcher.
- `WATCH_COALESCE_WINDOW_SECONDS`: окно коалесценции burst-событий.
- `WATCH_RECONCILE_INTERVAL_SECONDS`: период fallback reconcile-сверки индекса с workspace.
- `WATCH_RETRY_MAX_ATTEMPTS`: максимум retry при ошибках watcher loop.
- `WATCH_RETRY_BASE_DELAY_SECONDS`: базовый backoff для retry.
- `WATCH_RETRY_MAX_DELAY_SECONDS`: верхняя граница backoff.
- `WATCH_HEARTBEAT_INTERVAL_SECONDS`: интервал heartbeat в статусе watch-runtime.
- `WATCH_MAX_EVENTS_PER_CYCLE`: лимит событий в одном цикле обработки.
- `QDRANT_COLLECTION_NAME`: имя коллекции векторных данных.
- `IDEMPOTENCY_HASH_ALGORITHM`: алгоритм fingerprint (должен быть `sha256`).
- `IDEMPOTENCY_SKIP_UNCHANGED`: `1` пропускает неизмененные файлы до upsert.
- `IDEMPOTENCY_ENABLE_STALE_CLEANUP`: `1` удаляет устаревшие чанки после синхронизации.
- `IDEMPOTENCY_MAX_DELETE_BATCH`: максимальный batch удаления устаревших записей.
- `COMMAND_ALLOWLIST`: разрешенные команды через MCP.
- `COMMAND_TIMEOUT_SECONDS`: таймаут выполнения команд.
- `COMMAND_CPU_TIME_LIMIT_SECONDS`: лимит CPU-time на выполнение команды.
- `COMMAND_MEMORY_LIMIT_BYTES`: лимит памяти на выполнение команды (в байтах).
- `COMMAND_RUN_AS_NON_ROOT`: запуск command runtime без root (`1`/`0`).
- `COMMAND_AUDIT_LOG_PATH`: путь к файлу аудита вызовов команд.
- `COMMAND_AUDIT_RETENTION_DAYS`: срок хранения записей аудита (в днях).
- `STARTUP_PREFLIGHT_ENABLED`: включает startup preflight (`1`/`0`).
- `STARTUP_PREFLIGHT_TIMEOUT_SECONDS`: таймаут preflight-проверок зависимостей.
- `STARTUP_PREFLIGHT_REQUIRE_GIT_FOR_DELTA`: требовать git для `INDEX_MODE=delta-after-commit`.
- `STARTUP_READY_SUMMARY_LOG_ENABLED`: печатать единый startup-ready summary в лог.
- `BOOTSTRAP_AUTO_INGEST_ON_START`: автоматически запускать bootstrap ingestion при старте (`1`/`0`).
- `BOOTSTRAP_RETRY_FAILED_ON_START`: автоматически повторять failed-bootstrap при старте (`1`/`0`).
- `BOOTSTRAP_STATE_COLLECTION`: служебная коллекция маркеров bootstrap-состояния workspace.
- `MCP_ENDPOINT_PATH`: MCP endpoint path для startup summary (по умолчанию `/mcp`).
- `HOST_WORKSPACE_PATH`: путь хоста для bind mount в индексатор.

## Безопасность

- Не добавляйте в allowlist команды с доступом к неограниченному shell.
- Устанавливайте разумный timeout (обычно 10-60 секунд).
- Устанавливайте разумные лимиты `COMMAND_CPU_TIME_LIMIT_SECONDS` и
  `COMMAND_MEMORY_LIMIT_BYTES` для предотвращения деградации сервиса.
- Используйте `HOST_WORKSPACE_PATH` только для необходимых директорий.
- Ограничивайте `INDEX_MAX_FILE_SIZE_BYTES`, чтобы исключить тяжелые файлы.
- Не задавайте `INDEX_PROGRESS_INTERVAL_SECONDS` слишком большим значением
  (рекомендуется 5-60 секунд).
- Держите `INGESTION_CHUNK_OVERLAP` меньше `INGESTION_CHUNK_SIZE`.
- Для `delta-after-commit` задавайте валидные `DELTA_GIT_BASE_REF`/`DELTA_GIT_TARGET_REF`
  относительно mounted workspace.
- Для `watch` держите `WATCH_RECONCILE_INTERVAL_SECONDS` включенным (>= 30) для автоматической
  компенсации пропущенных FS-событий.
- Держите `DELTA_ENABLE_FALLBACK=1`, если требуется автоматическое восстановление
  при ошибках Git-диффа.
- Для реальной индексации через MCP обязательно держите `INGESTION_ENABLE_QDRANT_HTTP=1`.
- Для production задавайте отдельную коллекцию и не переиспользуйте общий индекс между проектами.
- Не подменяйте внутренний порт Qdrant через `QDRANT_PORT`: для сервис-сервис трафика используйте `QDRANT_API_PORT` (по умолчанию `6333`).
- Для идемпотентного режима оставляйте `IDEMPOTENCY_HASH_ALGORITHM=sha256`.
- Используйте `IDEMPOTENCY_ENABLE_STALE_CLEANUP=1`, чтобы индекс не накапливал устаревшие чанки.
- Держите `COMMAND_RUN_AS_NON_ROOT=1` и не ослабляйте контейнерные security-параметры
  без отдельного обоснования.
- Храните аудит минимум `COMMAND_AUDIT_RETENTION_DAYS=7`, чтобы покрывать
  операционные расследования.
- Не отключайте `STARTUP_PREFLIGHT_ENABLED` в production без отдельной проверки
  качества запуска.
- Для медленных сред увеличьте `STARTUP_PREFLIGHT_TIMEOUT_SECONDS` вместо
  отключения preflight.
- Для `INDEX_MODE=delta-after-commit` оставляйте
  `STARTUP_PREFLIGHT_REQUIRE_GIT_FOR_DELTA=1`.
- Для zero-friction bootstrap держите `BOOTSTRAP_AUTO_INGEST_ON_START=1`.
- Для production оставляйте `BOOTSTRAP_RETRY_FAILED_ON_START=1`, чтобы
  failed-bootstrap автоматически восстанавливался после кратковременных сбоев.
- Не переиспользуйте `BOOTSTRAP_STATE_COLLECTION` между изолированными окружениями.

## Bootstrap observability

- `GET /v1/system/startup/readiness` возвращает:
  - `bootstrap` (`trigger`, `decision`, `status`, `workspaceKey`, `runId?`, `errorCode?`, `reason?`);
  - `collection` (`collectionName`, `exists`, `pointCount`, `checkedAt`);
  - `bootstrapFailure` при статусе `failed` (структурированная actionable-диагностика).
- `GET /v1/indexing/ingestion/jobs/{runId}` и `/summary` включают:
  - `bootstrap` контекст запуска;
  - `collection` snapshot для верификации готовности индекса.
- `GET /v1/indexing/watch/status` возвращает:
  - текущее состояние (`starting/running/recovering/failed/stopped`);
  - глубину очереди, счетчики обработанных/ошибочных событий;
  - последнюю ошибку и backoff.
- `GET /v1/indexing/watch/summary` возвращает:
  - итоги последнего окна обработки (`indexedFiles/deletedRecords/skippedFiles/failedFiles`);
  - затронутые файлы и reason breakdown.

## MCP transport troubleshooting

- Если MCP-клиент получает `404` или `405`, проверьте endpoint:
  - корректно: `http://localhost:8080/mcp`
  - некорректно: `http://localhost:8080/` (это REST catalog, не MCP JSON-RPC)
- Проверьте discovery:
  - `GET http://localhost:8080/.well-known/mcp`
- Для legacy fallback:
  - `GET /sse` (получить `sessionId`)
  - `POST /messages?sessionId=...`
- Если `tools/list` возвращает `SESSION_NOT_INITIALIZED`, сначала выполните:
  - `initialize`
  - `notifications/initialized`
- Если `semantic_search` возвращает пустой результат в новом workspace:
  - это допустимо до первой индексации;
  - запустите `start_ingestion` и затем повторите поиск.
