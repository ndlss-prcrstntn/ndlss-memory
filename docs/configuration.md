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
- `QDRANT_COLLECTION_NAME`: имя коллекции векторных данных.
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
- Для production включайте `INGESTION_ENABLE_QDRANT_HTTP=1` и задавайте отдельную коллекцию.
