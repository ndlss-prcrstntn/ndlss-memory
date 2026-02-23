# План реализации: Docs collection indexing + baseline docs search

**Ветка**: `015-docs-index-baseline` | **Дата**: 2026-02-22 | **Спецификация**: `Z:\WORK\ndlss-memory\specs\015-docs-index-baseline\spec.md`
**Вход**: Спецификация фичи из `Z:\WORK\ndlss-memory\specs\015-docs-index-baseline\spec.md`

**Примечание**: Этот файл заполнен командой `/speckit.plan`.

## Summary

Добавить отдельную индексную область для markdown-документации и отдельный baseline-поиск только по docs без hybrid/rerank. Поведение должно быть детерминированным, идемпотентным и обратно совместимым с существующим поиском по коду.

## Technical Context

**Language/Version**: Python 3.12 (`mcp-server`, `file-indexer`), POSIX shell runtime, PowerShell 7+ для e2e/quality orchestration
**Primary Dependencies**: Flask API, PyYAML, существующие модули `ingestion_pipeline/*`, runtime bootstrap services, Docker Compose v2, Qdrant HTTP API
**Storage**: Qdrant коллекции (`workspace_chunks` + новая docs-коллекция), bind-mounted workspace (`/workspace`), in-memory run state/summaries
**Testing**: pytest (unit/integration/contract), PowerShell smoke scripts, compose-based regression checks
**Target Platform**: Linux containers under Docker Engine / Docker Desktop
**Project Type**: Multi-service backend stack (`qdrant`, `file-indexer`, `mcp-server`)
**Performance Goals**:
- docs-поиск возвращает результаты только из docs-коллекции;
- повторные одинаковые запросы по неизменным данным дают идентичный top-k порядок;
- повторная индексация без изменений не увеличивает количество записей docs-коллекции.
**Constraints**:
- состав сервисов неизменен (только `qdrant`, `file-indexer`, `mcp-server`);
- оба режима индексатора (`full-scan`, `delta-after-commit`) должны оставаться рабочими;
- docs-коллекция должна создаваться на старте и самовосстанавливаться при `404` во время записи/удаления;
- markdown-артефакты сохраняются в UTF-8.
**Scale/Scope**: Репозитории от сотен до десятков тысяч файлов; baseline docs-поиск для пользовательских и системных markdown-документов.

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

**Post-design gate review**: PASS

- [x] `research.md` закрывает спорные решения по уникальности, созданию коллекции и обратной совместимости.
- [x] `data-model.md` фиксирует сущности docs-индекса и детерминированные правила идентификации.
- [x] `contracts/docs-index-baseline.openapi.yaml` описывает контракт запуска docs-индексации и docs-поиска с машиночитаемыми ошибками.
- [x] `quickstart.md` включает позитивные, негативные и backward-compat сценарии.

## Project Structure

### Documentation (this feature)

```text
Z:\WORK\ndlss-memory\specs\015-docs-index-baseline\
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts\
|   `-- docs-index-baseline.openapi.yaml
`-- tasks.md
```

### Source Code (repository root)

```text
Z:\WORK\ndlss-memory\services\file-indexer\
Z:\WORK\ndlss-memory\services\mcp-server\
Z:\WORK\ndlss-memory\infra\docker\
Z:\WORK\ndlss-memory\tests\
```

**Structure Decision**: Используем существующие сервисы и pipeline-модули: docs-индексация и docs-поиск реализуются как расширение текущих слоев индексации/поиска, без добавления новых сервисов.

## Phase 0: Outline & Research

1. Research task: правило уникальности docs-документов и docs-чанков для идемпотентности.
2. Best-practice task: стратегия создания коллекции (startup + lazy self-heal) без race-condition.
3. Integration-pattern task: единое применение отбора markdown-файлов в `full-scan` и `delta-after-commit`.
4. Integration-pattern task: формат summary для docs-индексации и коды причин пропуска.
5. Compatibility task: изоляция docs-поиска от существующего code-search поведения.

**Output**: `Z:\WORK\ndlss-memory\specs\015-docs-index-baseline\research.md`

## Phase 1: Design & Contracts

1. Зафиксировать сущности, поля, валидации и переходы состояний в `data-model.md`.
2. Подготовить OpenAPI контракт для:
- запуска docs-индексации;
- получения docs-индексационного summary;
- выполнения baseline docs-поиска.
3. Подготовить quickstart сценарии для:
- чистой docs-индексации;
- docs-поиска по контрольным запросам;
- backward compatibility для существующего поиска по коду.
4. Обновить контекст агента через `.specify/scripts/powershell/update-agent-context.ps1 -AgentType codex`.

**Output**:
- `Z:\WORK\ndlss-memory\specs\015-docs-index-baseline\data-model.md`
- `Z:\WORK\ndlss-memory\specs\015-docs-index-baseline\contracts\docs-index-baseline.openapi.yaml`
- `Z:\WORK\ndlss-memory\specs\015-docs-index-baseline\quickstart.md`

## Complexity Tracking

Нарушений Constitution Check нет. Исключения не требуются.
