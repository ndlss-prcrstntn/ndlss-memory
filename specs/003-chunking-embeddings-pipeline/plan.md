# План реализации: Пайплайн чанкинга и эмбеддингов

**Ветка**: `003-chunking-embeddings-pipeline` | **Дата**: 2026-02-21 | **Спецификация**: `Z:\WORK\ndlss-memory\specs\003-chunking-embeddings-pipeline\spec.md`
**Вход**: Спецификация фичи из `Z:\WORK\ndlss-memory\specs\003-chunking-embeddings-pipeline\spec.md`

**Примечание**: Этот файл заполнен командой `/speckit.plan`.

## Summary

Реализовать пайплайн подготовки контента для векторного поиска: разбивка файлов
на чанки с настраиваемыми размером и overlap, генерация эмбеддингов с retry,
upsert-запись в Qdrant и сохранение трассируемых метаданных для каждой записи.
Ожидаемый результат: повторяемый ingestion-поток с наблюдаемой статистикой,
пригодный для последующего semantic search.

## Technical Context

**Language/Version**: Python 3.12 for service runtime, Docker Compose v2 for orchestration
**Primary Dependencies**: Flask API service, Qdrant HTTP API, embedding provider adapter, file-indexing pipeline modules
**Storage**: Qdrant vector collections, workspace file mount, ingestion run state in service memory with summary persistence
**Testing**: unit tests for chunking and metadata mapping, integration tests for ingestion jobs, contract tests for chunk/embedding API
**Target Platform**: Linux containers in Docker Engine / Docker Desktop
**Project Type**: multi-service backend (`qdrant`, `file-indexer`, `mcp-server`)
**Performance Goals**: process >= 1000 documents within 30 minutes; keep successful embedding ratio >= 99% in normal runs
**Constraints**: no extra services beyond constitution set; config via env/runtime params; deterministic updates and no duplicate vector records
**Scale/Scope**: single workspace per stack; one active ingestion job per runtime; chunking+embedding+upsert only (search UI out of scope)

## Constitution Check

*GATE: Должен пройти до Phase 0 research. Повторно проверить после Phase 1 design.*

**Pre-design gate review**: PASS

- [x] Состав сервисов не нарушает конституцию: только `qdrant`, `file-indexer`, `mcp-server`.
- [x] Предусмотрены оба режима индексатора: `full-scan` и `delta-after-commit`.
- [x] В плане есть проверка идемпотентности индексации (без дубликатов при повторном запуске).
- [x] MCP-инструменты имеют формализованные контракты ввода/вывода и машиночитаемые ошибки.
- [x] Для запуска команд описаны ограничения безопасности: allowlist, таймауты, изоляция.
- [x] Включены обязательные проверки: тесты, `docker compose up`, MCP-контракты,
      регрессия индексатора в обоих режимах.
- [x] Запланировано обновление `README.md` и quickstart в том же изменении.

**Post-design gate review**: PASS (подтверждено артефактами `research.md`, `data-model.md`, `contracts/chunking-embeddings.openapi.yaml`, `quickstart.md`)

## Project Structure

### Documentation (this feature)

```text
Z:\WORK\ndlss-memory\specs\003-chunking-embeddings-pipeline\
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- chunking-embeddings.openapi.yaml
`-- tasks.md
```

### Source Code (repository root)

```text
Z:\WORK\ndlss-memory\services\
|-- file-indexer/
|   |-- src/
|   |-- scripts/
|   `-- config/
|-- mcp-server/
|   |-- src/
|   `-- openapi/
`-- shared/

Z:\WORK\ndlss-memory\infra\docker\
`-- docker-compose.yml

Z:\WORK\ndlss-memory\tests\
|-- unit/
|-- integration/
`-- contract/
```

**Structure Decision**: Реализацию пайплайна концентрируем в `services/file-indexer/src`,
а внешний контракт управления ingestion-задачами и статусами размещаем в
`services/mcp-server/src` и OpenAPI-файлах. Документы фичи храним в каталоге
`specs/003-chunking-embeddings-pipeline`.

## Complexity Tracking

Нарушений Constitution Check нет. Дополнительные исключения не требуются.
