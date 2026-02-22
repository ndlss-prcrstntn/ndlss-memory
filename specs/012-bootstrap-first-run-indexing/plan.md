# План реализации: Bootstrap первого запуска индексации

**Ветка**: `012-bootstrap-first-run-indexing` | **Дата**: 2026-02-22 | **Спецификация**: `Z:\WORK\ndlss-memory\specs\012-bootstrap-first-run-indexing\spec.md`
**Вход**: Спецификация фичи из `Z:\WORK\ndlss-memory\specs\012-bootstrap-first-run-indexing\spec.md`

**Примечание**: Этот файл заполнен командой `/speckit.plan`.

## Summary

Добавить автоматический bootstrap индексации для первого запуска workspace: при старте стека система автоматически проверяет/создает коллекцию в Qdrant, запускает первичную индексацию без ручного API-триггера и публикует явный статус bootstrap в логах и статусных endpoint. Повторные рестарты не должны заново выполнять дорогой полный bootstrap, а ручные endpoint индексации должны оставаться доступными и обратно совместимыми.

## Technical Context

**Language/Version**: Python 3.12 (`mcp-server`), POSIX shell (`file-indexer` runtime), Docker Compose v2  
**Primary Dependencies**: Flask, PyYAML, Qdrant HTTP API, внутренние модули `ingestion_pipeline/*`, `ingestion_state.py`, `startup_*`  
**Storage**: Qdrant (коллекция `workspace_chunks` + служебное состояние bootstrap), bind-mounted workspace (`/workspace`, read-only), in-memory runtime state для job/status  
**Testing**: pytest (unit/integration/contract), PowerShell smoke/e2e scripts, `docker compose up` regression  
**Target Platform**: Linux containers under Docker Engine / Docker Desktop (host: Windows/macOS/Linux)  
**Project Type**: multi-service backend stack (`qdrant`, `file-indexer`, `mcp-server`)  
**Performance Goals**: автоматический bootstrap доводит новый workspace до searchable-состояния в рамках SC-метрики (<10 минут для типового малого/среднего проекта); повторный restart не выполняет полный bootstrap повторно  
**Constraints**: без добавления новых сервисов; сохранить существующие ручные endpoint и MCP/REST совместимость; fail-fast при критических сбоях bootstrap; markdown в UTF-8  
**Scale/Scope**: `docker-compose.yml`, `deploy/compose/*.yml`, `deploy/compose-images/*.yml`, runtime логика в `services/mcp-server/src` и наблюдаемость через существующие summary endpoint

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

**Post-design gate review**: PASS (подтверждено артефактами `research.md`, `data-model.md`, `contracts/first-run-bootstrap.openapi.yaml`, `quickstart.md`)

## Project Structure

### Documentation (this feature)

```text
Z:\WORK\ndlss-memory\specs\012-bootstrap-first-run-indexing\
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- first-run-bootstrap.openapi.yaml
`-- tasks.md
```

### Source Code (repository root)

```text
Z:\WORK\ndlss-memory\services\mcp-server\src\
Z:\WORK\ndlss-memory\services\mcp-server\openapi\
Z:\WORK\ndlss-memory\services\file-indexer\scripts\
Z:\WORK\ndlss-memory\deploy\compose\
Z:\WORK\ndlss-memory\deploy\compose-images\
Z:\WORK\ndlss-memory\docs\
Z:\WORK\ndlss-memory\tests\
```

**Structure Decision**: Реализация встраивается в существующую startup/ingestion архитектуру `mcp-server` с минимальными изменениями контрактов: расширяем текущие endpoint и сводки статусом bootstrap, не добавляя отдельный сервис и не ломая ручные операции.

## Phase 0: Research Plan

1. Определить стратегию хранения признака «bootstrap уже выполнен» для workspace, которая переживает рестарт контейнеров.
2. Выбрать способ безопасного авто-создания коллекции Qdrant при первом запуске без конфликтов с ручным ingestion.
3. Определить правила запуска авто-bootstrap и блокировок, чтобы не запускать дорогую индексацию повторно при каждом restart.
4. Зафиксировать формат публикации bootstrap-статуса в логах и summary endpoint без breaking changes.

## Phase 1: Design Plan

1. Описать data model для состояния bootstrap, готовности коллекции и итоговой сводки первого запуска.
2. Подготовить OpenAPI-контракт наблюдаемости bootstrap и совместимости ручных endpoint (`/v1/indexing/ingestion/jobs*`, `/v1/system/startup/readiness`).
3. Подготовить quickstart-сценарии:
   - первый запуск на пустом/новом workspace;
   - проверка, что restart не дублирует bootstrap;
   - проверка, что ручной запуск ingestion остается доступным.
4. Подготовить тестовые гейты для следующей фазы implementation (`/speckit.tasks`, `/speckit.implement`).

## Complexity Tracking

Нарушений Constitution Check нет. Исключения не требуются.

