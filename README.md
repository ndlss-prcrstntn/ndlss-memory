# ndlss-memory

`ndlss-memory` - локальный MCP-стек на Docker Compose для индексации файлов,
поиска контекста и безопасных tool-вызовов.

## Сервисы

- `qdrant`: хранение векторных данных и метаданных.
- `file-indexer`: сбор и обработка файлов из смонтированной директории.
- `mcp-server`: API/контракт статуса и входная точка для MCP-клиентов.

## Архитектура

```text
Host workspace (bind mount)
        |
        v
  file-indexer -----> qdrant (named volume)
        |
        v
      mcp-server <---- AI clients / IDE / agents
```

## Быстрый старт

```bash
pwsh scripts/dev/up.ps1
```

Проверка:

```bash
docker compose -f infra/docker/docker-compose.yml ps
pwsh scripts/ops/stack-status.ps1
curl http://localhost:8080/health
```

Остановка:

```bash
pwsh scripts/dev/down.ps1
```

## Ключевая конфигурация

Смотрите `.env.example` и `docs/configuration.md`.

- `INDEX_MODE=full-scan|delta-after-commit`
- `INDEX_FILE_TYPES=.md,.txt,...`
- `INDEX_EXCLUDE_PATTERNS=.git,node_modules,...`
- `INDEX_MAX_FILE_SIZE_BYTES=...`
- `INDEX_PROGRESS_INTERVAL_SECONDS=...`
- `COMMAND_ALLOWLIST=...`
- `COMMAND_TIMEOUT_SECONDS=...`

## Диагностика и recovery

- Операционный статус: `GET /v1/system/status`
- Конфигурация рантайма: `GET /v1/system/config`
- Статус сервиса: `GET /v1/system/services/{serviceName}`
- Диагностика из CLI: `pwsh scripts/ops/stack-status.ps1`

Если сервис unhealthy:

1. Проверьте `docker compose -f infra/docker/docker-compose.yml logs <service>`
2. Уточните env-параметры в `.env`/`.env.example`
3. Перезапустите стек (`up`/`down` скрипты)

### Full Scan troubleshooting

- `FULL_SCAN_ALREADY_RUNNING`: дождитесь завершения активной задачи или
  проверьте статус через `GET /v1/indexing/full-scan/jobs/{jobId}`.
- `JOB_NOT_FINISHED` при запросе summary: дождитесь финального статуса
  (`completed|failed|cancelled`) и повторите запрос.
- Большой `skipCount`: проверьте `INDEX_FILE_TYPES`,
  `INDEX_EXCLUDE_PATTERNS` и `INDEX_MAX_FILE_SIZE_BYTES`.
- Нулевой прогресс: проверьте `WORKSPACE_PATH` и наличие файлов в
  смонтированной директории.

### Ingestion troubleshooting

- `INGESTION_ALREADY_RUNNING`: дождитесь завершения активного ingestion run.
- `RUN_NOT_FINISHED`: дождитесь терминального статуса перед запросом summary.
- Высокий `retryCount`: проверьте стабильность embedding provider.
- Высокий `failedChunks`: проверьте `INGESTION_RETRY_MAX_ATTEMPTS` и
  `INGESTION_RETRY_BACKOFF_SECONDS`.
- Низкий `metadataCoverage`: проверьте `workspacePath` и маппинг обязательных
  полей (`path`, `fileName`, `fileType`, `contentHash`, `timestamp`).

## Документация фичи

- Спецификация: `specs/001-base-docker-compose/spec.md`
- План: `specs/001-base-docker-compose/plan.md`
- Задачи: `specs/001-base-docker-compose/tasks.md`
- Quickstart: `specs/001-base-docker-compose/quickstart.md`
- Контракт: `specs/001-base-docker-compose/contracts/compose-observability.openapi.yaml`

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

- [ ] Генерация hash контента (SHA256)
- [ ] Проверка существования хеша перед upsert
- [ ] Использование deterministic ID для чанков
- [ ] Обновление записи при изменении файла
- [ ] Удаление устаревших чанков

### 6. Режим Delta-after-commit

- [ ] Интеграция с Git
- [ ] Использование `git diff` для получения измененных файлов
- [ ] Индексация только:
  - [ ] добавленных файлов
  - [ ] измененных файлов
  - [ ] удаление удаленных файлов из Qdrant
- [ ] Обработка rename файлов
- [ ] Фоллбек на full-scan при ошибке

### 7. MCP-инструменты поиска

- [ ] Tool: semantic search
- [ ] Tool: получить источник по ID
- [ ] Tool: получить метаданные документа
- [ ] Поддержка фильтрации по:
  - [ ] пути
  - [ ] папке
  - [ ] типу файла
- [ ] Возврат структурированного ответа
- [ ] Обработка пустых результатов

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
  - [ ] хеширование
  - [x] фильтрация файлов
- [ ] Integration-тесты:
  - [ ] запись в Qdrant
  - [ ] поиск через MCP
- [ ] Contract-тесты MCP-инструментов
- [ ] E2E тест:
  - [ ] `docker compose up`
  - [ ] full-scan
  - [ ] delta-after-commit
  - [ ] проверка поискового запроса
- [ ] Проверка идемпотентности повторного запуска

### 10. Open-source упаковка

- [x] Подробный README
- [ ] Quickstart (5-10 минут до первого поиска)
- [x] Примеры `.env`
- [x] Пример docker-compose
- [ ] Описание MCP-инструментов
- [x] Архитектурная схема
- [ ] CONTRIBUTING.md
- [x] LICENSE
- [ ] Release checklist:
  - [ ] версия
  - [ ] changelog
  - [ ] теги
  - [ ] проверка Docker image
  - [ ] проверка примеров

