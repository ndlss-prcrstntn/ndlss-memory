# Конфигурация окружения

Файл `.env.example` содержит базовые параметры запуска стека.

## Обязательные параметры

- `QDRANT_PORT`: внешний порт Qdrant.
- `MCP_PORT`: внешний порт mcp-server.
- `INDEX_MODE`: `full-scan` или `delta-after-commit`.
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
- `QDRANT_COLLECTION_NAME`: имя коллекции векторных данных.
- `IDEMPOTENCY_HASH_ALGORITHM`: алгоритм fingerprint (должен быть `sha256`).
- `IDEMPOTENCY_SKIP_UNCHANGED`: `1` пропускает неизмененные файлы до upsert.
- `IDEMPOTENCY_ENABLE_STALE_CLEANUP`: `1` удаляет устаревшие чанки после синхронизации.
- `IDEMPOTENCY_MAX_DELETE_BATCH`: максимальный batch удаления устаревших записей.
- `COMMAND_ALLOWLIST`: разрешенные команды через MCP.
- `COMMAND_TIMEOUT_SECONDS`: таймаут выполнения команд.
- `HOST_WORKSPACE_PATH`: путь хоста для bind mount в индексатор.

## Безопасность

- Не добавляйте в allowlist команды с доступом к неограниченному shell.
- Устанавливайте разумный timeout (обычно 10-60 секунд).
- Используйте `HOST_WORKSPACE_PATH` только для необходимых директорий.
- Ограничивайте `INDEX_MAX_FILE_SIZE_BYTES`, чтобы исключить тяжелые файлы.
- Не задавайте `INDEX_PROGRESS_INTERVAL_SECONDS` слишком большим значением
  (рекомендуется 5-60 секунд).
- Держите `INGESTION_CHUNK_OVERLAP` меньше `INGESTION_CHUNK_SIZE`.
- Для `delta-after-commit` задавайте валидные `DELTA_GIT_BASE_REF`/`DELTA_GIT_TARGET_REF`
  относительно mounted workspace.
- Держите `DELTA_ENABLE_FALLBACK=1`, если требуется автоматическое восстановление
  при ошибках Git-диффа.
- Для production включайте `INGESTION_ENABLE_QDRANT_HTTP=1` и задавайте отдельную коллекцию.
- Для идемпотентного режима оставляйте `IDEMPOTENCY_HASH_ALGORITHM=sha256`.
- Используйте `IDEMPOTENCY_ENABLE_STALE_CLEANUP=1`, чтобы индекс не накапливал устаревшие чанки.
