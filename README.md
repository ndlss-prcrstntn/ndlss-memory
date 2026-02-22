# ndlss-memory

`ndlss-memory` - локальный memory-слой для MCP-агентов.
Проект индексирует файлы workspace, хранит векторы/метаданные в Qdrant и предоставляет HTTP API через `mcp-server`.

## Что реализовано сейчас

- Docker Compose стек из трех сервисов: `qdrant`, `file-indexer`, `mcp-server`.
- Режимы индексации: `full-scan` и `delta-after-commit`.
- Пайплайн чанкинга и эмбеддингов с retry.
- Идемпотентная синхронизация индекса (без дублей, cleanup устаревших чанков).
- MCP search tools:
  - `semantic search`
  - получение источника по `resultId`
  - получение метаданных по `resultId`
  - фильтрация по `path` / `folder` / `fileType`
  - структурированные ответы и машиночитаемые ошибки
- MCP secure command runtime:
  - allowlist команд
  - timeout/ресурсные ограничения
  - изоляция рабочей директории
  - аудит вызовов и structured errors

## Сервисы

- `qdrant`: векторное хранилище и payload-метаданные.
- `file-indexer`: full-scan, ingestion, idempotency, delta-after-commit.
- `mcp-server`: REST API статуса, управления индексацией и MCP search tools.

## Структура репозитория

```text
infra/docker/                 # docker compose стек
services/file-indexer/        # логика индексатора
services/mcp-server/          # API и контракты MCP-сервера
scripts/dev/                  # запуск/остановка стека
scripts/ops/                  # операционные проверки
scripts/tests/                # compose/regression сценарии
tests/                        # unit/integration/contract артефакты
specs/                        # feature-спеки, планы и задачи
```

## Быстрый старт

Требования:

- Docker Engine + Docker Compose v2
- Windows PowerShell (или PowerShell 7+)

Запуск стека:

```powershell
powershell -File scripts/dev/up.ps1
```

Проверка состояния:

```powershell
docker compose -f infra/docker/docker-compose.yml ps
powershell -File scripts/ops/stack-status.ps1
curl http://localhost:8080/health
```

Остановка:

```powershell
powershell -File scripts/dev/down.ps1
```

Полный сценарий "5-10 минут до первого поиска": `docs/quickstart.md`.

## Первый поисковый запрос

```bash
curl -X POST http://localhost:8080/v1/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query":"docker compose healthcheck","limit":5}'
```

Далее можно использовать `resultId`:

- `GET /v1/search/results/{resultId}/source`
- `GET /v1/search/results/{resultId}/metadata`

## Конфигурация

Базовая конфигурация задается через `.env` (пример: `.env.example`).

Ключевые группы параметров:

- Индексация: `INDEX_MODE`, `INDEX_FILE_TYPES`, `INDEX_EXCLUDE_PATTERNS`, `INDEX_MAX_FILE_SIZE_BYTES`.
- Чанкинг/эмбеддинги: `INGESTION_CHUNK_SIZE`, `INGESTION_CHUNK_OVERLAP`, `INGESTION_RETRY_*`.
- Delta-after-commit: `DELTA_GIT_BASE_REF`, `DELTA_GIT_TARGET_REF`, `DELTA_INCLUDE_RENAMES`, `DELTA_ENABLE_FALLBACK`.
- Идемпотентность: `IDEMPOTENCY_HASH_ALGORITHM`, `IDEMPOTENCY_SKIP_UNCHANGED`, `IDEMPOTENCY_ENABLE_STALE_CLEANUP`.
- Безопасность команд: `COMMAND_ALLOWLIST`, `COMMAND_TIMEOUT_SECONDS`.

Подробно: `docs/configuration.md`.

## API

Системные:

- `GET /health`
- `GET /v1/system/status`
- `GET /v1/system/config`
- `GET /v1/system/services/{serviceName}`

Индексация:

- `POST /v1/indexing/full-scan/jobs`
- `GET /v1/indexing/full-scan/jobs/{jobId}`
- `GET /v1/indexing/full-scan/jobs/{jobId}/summary`
- `POST /v1/indexing/ingestion/jobs`
- `GET /v1/indexing/ingestion/jobs/{runId}`
- `GET /v1/indexing/ingestion/jobs/{runId}/summary`
- `POST /v1/indexing/idempotency/jobs`
- `GET /v1/indexing/idempotency/jobs/{runId}`
- `GET /v1/indexing/idempotency/jobs/{runId}/summary`
- `POST /v1/indexing/delta-after-commit/jobs`
- `GET /v1/indexing/delta-after-commit/jobs/{runId}`
- `GET /v1/indexing/delta-after-commit/jobs/{runId}/summary`

MCP search tools:

- `POST /v1/search/semantic`
- `GET /v1/search/results/{resultId}/source`
- `GET /v1/search/results/{resultId}/metadata`

MCP command security:

- `POST /v1/commands/execute`
- `GET /v1/commands/executions/{requestId}`
- `GET /v1/commands/audit`

## Тестирование

Unit:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/unit/file_indexer
.\.venv\Scripts\python.exe -m pytest tests/unit/mcp_server
```

Compose regression:

```powershell
powershell -File scripts/tests/full_scan_compose_regression.ps1
powershell -File scripts/tests/ingestion_compose_regression.ps1
powershell -File scripts/tests/idempotency_compose_regression.ps1
powershell -File scripts/tests/delta_after_commit_compose_regression.ps1
```

Quality stability suite:

```powershell
powershell -File scripts/tests/run_quality_stability_suite.ps1
powershell -File scripts/tests/contract_quality_stability.ps1
powershell -File scripts/tests/quality_stability_e2e.ps1
powershell -File scripts/tests/validate_markdown_encoding.ps1
```

## Документация по фичам

- `specs/001-base-docker-compose/`
- `specs/002-full-scan/`
- `specs/003-chunking-embeddings-pipeline/`
- `specs/004-indexing-idempotency/`
- `specs/005-delta-after-commit/`
- `specs/006-mcp-search-tools/`
- `specs/007-secure-mcp-commands/`
- `specs/008-quality-stability-tests/`

## Contribution

- `CONTRIBUTING.md` - правила contribution и PR-процесса.
- `docs/release-checklist.md` - проверка перед публикацией релиза.
## Roadmap

### 0. Zero-Friction Setup (DX-first)

- [x] Возможность запустить стек, просто поместив `docker-compose.yml` в папку проекта
- [x] Автоматический mount текущей директории проекта
- [x] Минимальная конфигурация через `.env` (только необходимые переменные)
- [x] Автоматическое создание коллекции в Qdrant при старте
- [x] Автоматический запуск full-scan при первом запуске
- [x] Понятные логи статуса индексации
- [x] Документация: "3 минуты до первого запроса"
- [x] Подключение к MCP-агенту без дополнительной ручной настройки

### 1. Базовая инфраструктура

- [x] Подготовить базовый Docker Compose стек
  - [x] Qdrant
  - [x] file-indexer
  - [x] mcp-server
  - [x] Настроить healthcheck для всех сервисов
  - [x] Настроить общую docker-сеть
  - [x] Добавить volume для хранения данных Qdrant
  - [x] Добавить volume для индексируемых файлов

### 2. Конфигурация индексатора

- [x] Добавить `.env` / config-файл
- [x] Настроить `INDEX_FILE_TYPES`
- [x] Настроить `INDEX_EXCLUDE_PATTERNS`
- [x] Настроить пути для индексации
- [x] Настроить лимиты (размер файла, глубина обхода, количество файлов)
- [x] Поддержать конфигурацию через переменные окружения

### 3. Режим Full Scan

- [x] Реализовать полный обход папки
- [x] Фильтрация по поддерживаемым типам
- [x] Исключение файлов по паттернам
- [x] Логирование прогресса индексации
- [x] Обработка ошибок чтения файлов
- [x] Защита от слишком больших файлов

### 4. Пайплайн чанкинга и эмбеддингов

- [x] Реализовать разбивку файлов на чанки
- [x] Настроить размер чанка и overlap
- [x] Интегрировать генерацию эмбеддингов
- [x] Добавить retry-механику для эмбеддингов
- [x] Запись в Qdrant (upsert)
- [x] Сохранение метаданных:
  - [x] путь
  - [x] имя файла
  - [x] тип файла
  - [x] hash контента
  - [x] timestamp

### 5. Идемпотентность индексации

- [x] Генерация hash контента (SHA256)
- [x] Проверка существования хеша перед upsert
- [x] Использование deterministic ID для чанков
- [x] Обновление записи при изменении файла
- [x] Удаление устаревших чанков

### 6. Режим Delta-after-commit

- [x] Интеграция с Git
- [x] Использование `git diff` для получения измененных файлов
- [x] Индексация только:
  - [x] добавленных файлов
  - [x] измененных файлов
  - [x] удаление удаленных файлов из Qdrant
- [x] Обработка rename файлов
- [x] Фоллбек на full-scan при ошибке

### 7. MCP-инструменты поиска

- [x] Tool: semantic search
- [x] Tool: получить источник по ID
- [x] Tool: получить метаданные документа
- [x] Поддержка фильтрации по:
  - [x] пути
  - [x] папке
  - [x] типу файла
- [x] Возврат структурированного ответа
- [x] Обработка пустых результатов

### 8. Безопасный запуск команд через MCP

- [x] Allowlist разрешенных команд
- [x] Ограничение прав контейнера (non-root)
- [x] Ограничение CPU/Memory
- [x] Таймауты выполнения команд
- [x] Структурированные ошибки
- [x] Логирование вызовов
- [x] Изоляция рабочих директорий

### 9. Качество и стабильность

- [x] Unit-тесты:
  - [x] чанкинг
  - [x] хеширование
  - [x] фильтрация файлов
- [x] Integration-тесты:
  - [x] запись в Qdrant
  - [x] поиск через MCP
- [x] Contract-тесты MCP-инструментов
- [x] E2E тест:
  - [x] `docker compose up`
  - [x] full-scan
  - [x] delta-after-commit
  - [x] проверка поискового запроса
- [x] Проверка идемпотентности повторного запуска

### 10. Open-source упаковка

- [x] Подробный README
- [x] Quickstart (5-10 минут до первого поиска)
- [x] Примеры `.env`
- [x] Пример docker-compose
- [x] Описание MCP-инструментов
- [x] Архитектурная схема
- [x] CONTRIBUTING.md
- [x] LICENSE
- [x] Release checklist:
  - [x] версия
  - [x] changelog
  - [x] теги
  - [x] проверка Docker image
  - [x] проверка примеров



