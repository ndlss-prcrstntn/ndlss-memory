# План реализации: Hybrid search (BM25 + vector) только для md коллекции

**Ветка**: `016-md-hybrid-search` | **Дата**: 2026-02-23 | **Спецификация**: `Z:\WORK\ndlss-memory\specs\016-md-hybrid-search\spec.md`
**Вход**: Спецификация фичи из `Z:\WORK\ndlss-memory\specs\016-md-hybrid-search\spec.md`

**Примечание**: Этот файл заполнен командой `/speckit.plan`.

## Summary

Добавить гибридный поиск (BM25 + vector) для markdown-коллекции документации, сохранив неизменным текущее поведение остальных поисковых сценариев. Результат должен быть детерминированным, машиночитаемым по ошибкам и обратно совместимым по публичным контрактам вне docs-search.

## Technical Context

**Language/Version**: Python 3.12 (`mcp-server`, `file-indexer`), POSIX shell runtime, PowerShell 7+ для orchestration
**Primary Dependencies**: Flask API, PyYAML, существующие модули `search_service`/`search_repository`, Qdrant HTTP API, Docker Compose v2
**Storage**: Qdrant коллекции `workspace_docs_chunks` (гибридный поиск), `workspace_chunks` (без изменений), bind-mounted workspace `/workspace`, in-memory runtime state
**Testing**: pytest (unit/integration/contract), OpenAPI contract checks, compose smoke checks
**Target Platform**: Linux containers под Docker Engine / Docker Desktop
**Project Type**: Multi-service backend stack (`qdrant`, `file-indexer`, `mcp-server`)
**Performance Goals**:
- 95% docs-запросов получают ответ менее чем за 2 секунды;
- не менее 85% контрольных markdown-запросов возвращают релевантный результат в top-3;
- одинаковый запрос к неизменному индексу дает детерминированный top-k порядок.
**Constraints**:
- состав сервисов неизменен (только `qdrant`, `file-indexer`, `mcp-server`);
- гибридный режим применяется только для markdown-коллекции;
- `full-scan` и `delta-after-commit` остаются рабочими и без регрессий;
- ошибки API/MCP сохраняют машиночитаемый формат;
- `health` и `startup/readiness` проверяются отдельно в валидационных сценариях.
**Scale/Scope**: Поиск по markdown-документации в репозиториях от сотен до десятков тысяч файлов; изменение ограничено docs-search потоком и связанными контрактами.

## Constitution Check

*GATE: Должен пройти до Phase 0 research. Повторно проверить после Phase 1 design.*

**Pre-design gate review**: PASS

- [x] Состав сервисов не нарушает конституцию: только `qdrant`, `file-indexer`, `mcp-server`.
- [x] Предусмотрены оба режима индексатора: `full-scan` и `delta-after-commit`.
- [x] В плане есть проверка идемпотентности индексации (без дубликатов при повторном запуске).
- [x] MCP-инструменты имеют формализованные контракты ввода/вывода и машиночитаемые ошибки.
- [x] Для запуска команд описаны ограничения безопасности: allowlist, таймауты, изоляция.
- [x] Для локальной разработки предусмотрены уникальные порты и явный env-профиль MCP.
- [x] Явно разделены семантики `health` и `startup/readiness` в сценариях валидации.
- [x] Для multi-module задач описан MCP-контекстный проход и последующая file-level верификация.
- [x] Включены обязательные проверки: тесты, `docker compose up`, MCP-контракты, регрессия индексатора в обоих режимах.
- [x] Запланировано обновление `README.md` и quickstart в том же изменении.

**Post-design gate review**: PASS

- [x] `research.md` фиксирует решения по fusion-стратегии, детерминизму выдачи и границам scope.
- [x] `data-model.md` описывает сущности hybrid docs-search, правила валидации и переходы состояний.
- [x] `contracts/md-hybrid-search.openapi.yaml` определяет формальный контракт docs-search с машиночитаемыми ошибками.
- [x] `quickstart.md` покрывает позитивные, негативные, изоляционные и детерминизм-сценарии.

## Project Structure

### Documentation (this feature)

```text
Z:\WORK\ndlss-memory\specs\016-md-hybrid-search\
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts\
|   `-- md-hybrid-search.openapi.yaml
`-- tasks.md
```

### Source Code (repository root)

```text
Z:\WORK\ndlss-memory\services\file-indexer\
Z:\WORK\ndlss-memory\services\mcp-server\
Z:\WORK\ndlss-memory\infra\docker\
Z:\WORK\ndlss-memory\tests\
```

**Structure Decision**: Используем существующие сервисы и search-слои. Гибридная логика добавляется в docs-search pipeline и конфигурацию ранжирования без добавления новых сервисов/хранилищ.

## Phase 0: Outline & Research

1. Best-practice task: определить устойчивую fusion-стратегию BM25 + vector для markdown-корпуса.
2. Integration-pattern task: зафиксировать границу применения гибридного режима только для docs-коллекции.
3. Integration-pattern task: выбрать детерминированный tie-break и правило стабильного ранжирования top-k.
4. Dependency task: определить требования к наблюдаемости качества (метрики релевантности, latency, empty/error rate).
5. Compatibility task: обеспечить backward compatibility для `/v1/search/semantic` и остальных не-docs сценариев.

**Output**: `Z:\WORK\ndlss-memory\specs\016-md-hybrid-search\research.md`

## Phase 1: Design & Contracts

1. Зафиксировать сущности, поля, валидации и переходы состояний для hybrid docs-search в `data-model.md`.
2. Подготовить OpenAPI контракт для `POST /v1/search/docs/query` с гибридным ранжированием и машиночитаемыми ошибками.
3. Подготовить quickstart-сценарии для:
- запуска docs-индексации;
- проверки гибридного docs-search;
- проверки изоляции (без изменений для non-docs search);
- проверки детерминизма и негативных кейсов.
4. Обновить контекст агента через `.specify/scripts/powershell/update-agent-context.ps1 -AgentType codex`.

**Output**:
- `Z:\WORK\ndlss-memory\specs\016-md-hybrid-search\data-model.md`
- `Z:\WORK\ndlss-memory\specs\016-md-hybrid-search\contracts\md-hybrid-search.openapi.yaml`
- `Z:\WORK\ndlss-memory\specs\016-md-hybrid-search\quickstart.md`

## Phase 2: Implementation Planning Boundary

На этом этапе артефакты планирования готовы; детализация по шагам реализации и порядок выполнения задач формируются отдельно командой `/speckit.tasks`.

## Complexity Tracking

Нарушений Constitution Check нет. Исключения не требуются.
