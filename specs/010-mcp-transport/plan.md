# План реализации: Надежность MCP Индексации

**Ветка**: `010-mcp-transport` | **Дата**: 2026-02-22 | **Спецификация**: `Z:\WORK\ndlss-memory\specs\010-mcp-transport\spec.md`  
**Вход**: Спецификация фичи из `Z:\WORK\ndlss-memory\specs\010-mcp-transport\spec.md`

**Примечание**: Этот файл заполнен командой `/speckit.plan`.

## Summary

Исправить reliability-разрыв между успешным запуском индексации через MCP и фактическим созданием данных в Qdrant. Для этого фича разделяет внутренний и внешний порты Qdrant, включает HTTP upsert для MCP-инициируемой индексации, обновляет compose-пресеты/документацию и добавляет автоматические регрессии на создание коллекции и запуск с нестандартным внешним портом.

## Technical Context

**Language/Version**: Python 3.12 (runtime и тестовые скрипты), PowerShell 7+ (orchestration/регрессии), Docker Compose Specification v2  
**Primary Dependencies**: Flask, PyYAML, встроенные Python urllib/json/hashlib, Docker Compose CLI, Qdrant HTTP API  
**Storage**: Qdrant коллекция `workspace_chunks`, локальные workspace файлы через bind mount, in-memory runtime state для job tracking  
**Testing**: pytest (unit), PowerShell regression/smoke scripts, docker compose integration checks, contract markdown artifacts  
**Target Platform**: Linux containers под Docker Engine/Docker Desktop, локальный запуск с Windows/macOS/Linux host  
**Project Type**: multi-service backend stack (`qdrant`, `file-indexer`, `mcp-server`)  
**Performance Goals**: p95 MCP handshake < 5s; p95 MCP semantic search < 3s; создание коллекции и первая запись в пределах одного ingestion run  
**Constraints**: сохраняется текущий состав сервисов; обратная совместимость текущих REST/MCP endpoint; обязательный UTF-8 для markdown; внешние порты должны быть независимы от внутреннего service-to-service трафика  
**Scale/Scope**: все публичные compose presets (`deploy/compose-images/*.yml`, `deploy/compose/*.yml`), документация запуска, quality regression pipeline и patch-release 0.1.7

## Constitution Check

*GATE: Должен пройти до Phase 0 research. Повторно проверить после Phase 1 design.*

**Pre-design gate review**: PASS

- [x] Состав сервисов не нарушает конституцию: только `qdrant`, `file-indexer`, `mcp-server`.
- [x] Предусмотрены оба режима индексатора: `full-scan` и `delta-after-commit`.
- [x] В плане есть проверка идемпотентности индексации (без дубликатов при повторном запуске).
- [x] MCP-инструменты имеют формализованные контракты ввода/вывода и машиночитаемые ошибки.
- [x] Для запуска команд описаны ограничения безопасности: allowlist, таймауты, изоляция.
- [x] Включены обязательные проверки: тесты, `docker compose up`, MCP-контракты, регрессия индексатора в обоих режимах.
- [x] Запланировано обновление `README.md` и quickstart в том же изменении.

**Post-design gate review**: PASS (подтверждено артефактами `research.md`, `data-model.md`, `contracts/qdrant-ingestion-reliability.openapi.yaml`, `quickstart.md`)

## Project Structure

### Documentation (this feature)

```text
Z:\WORK\ndlss-memory\specs\010-mcp-transport\
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- qdrant-ingestion-reliability.openapi.yaml
`-- tasks.md
```

### Source Code (repository root)

```text
Z:\WORK\ndlss-memory\deploy\
|-- compose/
`-- compose-images/

Z:\WORK\ndlss-memory\services\
|-- file-indexer/
`-- mcp-server/

Z:\WORK\ndlss-memory\scripts\tests\

Z:\WORK\ndlss-memory\docs\
```

**Structure Decision**: Все изменения ограничиваются существующими сервисами и инфраструктурными YAML/скриптами. Новые runtime-сервисы не добавляются. Ключевой design-фокус: консистентная env-модель (`QDRANT_PORT` как host port, `QDRANT_API_PORT` как internal service port) и гарантированный HTTP upsert для MCP-инициируемой индексации.

## Phase 0: Research Plan

1. Проверить best-practice разделения internal/external портов для Docker Compose multi-project запуска.
2. Уточнить минимальный безопасный набор env-переменных для гарантированного создания коллекции в ingestion pipeline.
3. Зафиксировать тестовый паттерн для регрессий:
   - коллекция отсутствует до run;
   - создается после run;
   - points/count > 0;
   - сценарий с нестандартным внешним `QDRANT_PORT`.

## Phase 1: Design Plan

1. Описать сущности состояния (ingestion outcome, collection state, runtime port config, regression result).
2. Спроектировать контракты проверки для:
   - запуска ingestion и статуса;
   - проверки коллекции/количества точек;
   - системного runtime config snapshot.
3. Подготовить quickstart-последовательность для пользователя:
   - корректный MCP endpoint (`/mcp`);
   - семантика портов (`QDRANT_PORT` внешний, `QDRANT_API_PORT` внутренний);
   - проверка индекса после ingestion.

## Complexity Tracking

Нарушений Constitution Check нет. Исключения не требуются.
