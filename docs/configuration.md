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
