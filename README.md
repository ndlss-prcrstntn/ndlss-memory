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

## Документация по фичам

- `specs/001-base-docker-compose/`
- `specs/002-full-scan/`
- `specs/003-chunking-embeddings-pipeline/`
- `specs/004-indexing-idempotency/`
- `specs/005-delta-after-commit/`
- `specs/006-mcp-search-tools/`
## Roadmap

### 0. Zero-Friction Setup (DX-first)

- [ ] Возможность запустить стек, просто поместив `docker-compose.yml` в папку проекта
- [x] Автоматический mount текущей директории проекта
- [ ] Минимальная конфигурация через `.env` (только необходимые переменные)
- [ ] Автоматическое создание коллекции в Qdrant при старте
- [ ] Автоматический запуск full-scan при первом запуске
- [x] Понятные логи статуса индексации
- [ ] Документация: "3 минуты до первого запроса"
- [ ] Подключение к MCP-агенту без дополнительной ручной настройки

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

- [ ] Allowlist разрешенных команд
- [ ] Ограничение прав контейнера (non-root)
- [ ] Ограничение CPU/Memory
- [ ] Таймауты выполнения команд
- [ ] Структурированные ошибки
- [ ] Логирование вызовов
- [ ] Изоляция рабочих директорий

### 9. Качество и стабильность

- [ ] Unit-тесты:
  - [ ] чанкинг
  - [x] хеширование
  - [x] фильтрация файлов
- [ ] Integration-тесты:
  - [ ] запись в Qdrant
  - [x] поиск через MCP
- [x] Contract-тесты MCP-инструментов
- [ ] E2E тест:
  - [x] `docker compose up`
  - [ ] full-scan
  - [x] delta-after-commit
  - [ ] проверка поискового запроса
- [x] Проверка идемпотентности повторного запуска

### 10. Open-source упаковка

- [x] Подробный README
- [ ] Quickstart (5-10 минут до первого поиска)
- [x] Примеры `.env`
- [x] Пример docker-compose
- [x] Описание MCP-инструментов
- [x] Архитектурная схема
- [ ] CONTRIBUTING.md
- [x] LICENSE
- [ ] Release checklist:
  - [ ] версия
  - [ ] changelog
  - [ ] теги
  - [ ] проверка Docker image
  - [ ] проверка примеров



