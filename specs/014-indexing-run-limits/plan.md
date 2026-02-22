# План реализации: Ограничение глубины и объема индексации

**Ветка**: `014-indexing-run-limits` | **Дата**: 2026-02-22 | **Спецификация**: `Z:\WORK\ndlss-memory\specs\014-indexing-run-limits\spec.md`
**Вход**: Спецификация фичи из `Z:\WORK\ndlss-memory\specs\014-indexing-run-limits\spec.md`

**Примечание**: Этот файл заполнен командой `/speckit.plan`.

## Summary

Добавить в запуски индексации два ограничителя blast radius: максимальную глубину обхода директорий и максимальное количество файлов на запуск. Ограничения должны работать детерминированно, применяться единообразно в `full-scan` и релевантных ingestion-путях, а также отражаться в summary с причинами пропуска файлов. При отключенных лимитах поведение должно оставаться полностью обратносуместимым.

## Technical Context

**Language/Version**: Python 3.12 (`mcp-server`), POSIX shell (`file-indexer` runtime), PowerShell 7+ (test orchestration)
**Primary Dependencies**: Flask API, PyYAML, существующие модули индексации (`full-scan`, `ingestion`), Docker Compose v2, Qdrant HTTP API
**Storage**: Qdrant коллекции (`workspace_chunks`), bind-mounted workspace (`/workspace`), runtime summary/state в памяти сервиса
**Testing**: pytest (unit/integration/contract), PowerShell smoke/regression scripts, `scripts/tests/run_quality_stability_suite.ps1`
**Target Platform**: Linux containers under Docker Engine / Docker Desktop
**Project Type**: Multi-service backend stack (`qdrant`, `file-indexer`, `mcp-server`)
**Performance Goals**:
- число обработанных файлов в запуске никогда не превышает `max-files` лимит;
- файлы глубже `max-depth` никогда не попадают в обработку;
- повторные запуски на неизменных данных с теми же лимитами дают тот же набор отобранных файлов.
**Constraints**:
- defaults должны сохранять текущее поведение без лимитов;
- ограничения применяются одинаково во всех релевантных путях обхода файлов;
- summary обязан объяснять пропуски по лимитам отдельными причинами;
- не допускается регрессия режимов `full-scan` и `delta-after-commit`.
**Scale/Scope**: Репозитории большого размера (десятки тысяч файлов), изменения в конфигурации запуска, pipeline отбора файлов и summary контрактах.

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

- [x] `research.md` зафиксировал детерминированные правила применения лимитов и fallback-поведение без нарушения существующих режимов.
- [x] `data-model.md` и contracts описывают лимиты и причины пропуска без изменения состава сервисов.
- [x] `quickstart.md` включает проверки для `full-scan` и ingestion путей и обратной совместимости дефолтов.

## Project Structure

### Documentation (this feature)

```text
Z:\WORK\ndlss-memory\specs\014-indexing-run-limits\
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts\
|   `-- indexing-run-limits.openapi.yaml
`-- tasks.md
```

### Source Code (repository root)

```text
Z:\WORK\ndlss-memory\services\file-indexer\
Z:\WORK\ndlss-memory\services\mcp-server\
Z:\WORK\ndlss-memory\infra\docker\
Z:\WORK\ndlss-memory\tests\
```

**Structure Decision**: Логику лимитов внедряем в существующий слой отбора файлов и формирования summary для full-scan/ingestion, без добавления новых сервисов. Контракты фиксируем в отдельном feature-артефакте `contracts/indexing-run-limits.openapi.yaml`.

## Phase 0: Outline & Research

1. Research task: правила вычисления `traversal depth` относительно корня workspace и поведение для граничных значений (`0`, unset).
2. Best-practice task: детерминированный отбор файлов при ограничении `max-files` (стабильный порядок обхода).
3. Integration-pattern task: единое применение лимитов в full-scan и релевантных ingestion-путях.
4. Integration-pattern task: модель summary с отдельными skip-reason кодами для depth/file-limit.
5. Compatibility task: стратегия дефолтов и валидации конфигурации без breaking behavior.

**Output**: `Z:\WORK\ndlss-memory\specs\014-indexing-run-limits\research.md`

## Phase 1: Design & Contracts

1. Описать сущности, поля, валидации и переходы состояний в `data-model.md`.
2. Подготовить OpenAPI контракт для запуска и summary full-scan/ingestion с полями лимитов и причин пропуска.
3. Подготовить quickstart сценарии для:
- применения `max-depth`;
- применения `max-files`;
- проверки обратной совместимости при отключенных лимитах.
4. Обновить контекст агента через `.specify/scripts/powershell/update-agent-context.ps1 -AgentType codex`.

**Output**:
- `Z:\WORK\ndlss-memory\specs\014-indexing-run-limits\data-model.md`
- `Z:\WORK\ndlss-memory\specs\014-indexing-run-limits\contracts\indexing-run-limits.openapi.yaml`
- `Z:\WORK\ndlss-memory\specs\014-indexing-run-limits\quickstart.md`

## Complexity Tracking

Нарушений Constitution Check нет. Исключения не требуются.
