# План реализации: Reranking поверх hybrid только для markdown-коллекции

**Ветка**: `017-md-hybrid-reranking` | **Дата**: 2026-02-23 | **Спецификация**: `Z:\WORK\ndlss-memory\specs\017-md-hybrid-reranking\spec.md`
**Вход**: Спецификация фичи из `Z:\WORK\ndlss-memory\specs\017-md-hybrid-reranking\spec.md`

**Примечание**: Этот файл заполнен командой `/speckit.plan`.

## Summary

Добавить второй этап ранжирования (reranking) поверх существующего hybrid docs-search только для markdown-коллекции. Решение должно улучшить качество top-выдачи, сохранить детерминизм и не менять поведение non-docs поиска.

## Technical Context

**Language/Version**: Python 3.12 (`mcp-server`, `file-indexer`), POSIX shell runtime, PowerShell 7+ для orchestration
**Primary Dependencies**: Flask API, PyYAML, существующие модули `search_repository`/`search_service`, Qdrant HTTP API, Docker Compose v2
**Storage**: Qdrant коллекции `workspace_docs_chunks` (reranking scope) и `workspace_chunks` (без изменений), bind-mounted workspace `/workspace`, in-memory runtime state
**Testing**: pytest (unit/integration/contract), OpenAPI contract checks, compose smoke checks
**Target Platform**: Linux containers под Docker Engine / Docker Desktop
**Project Type**: Multi-service backend stack (`qdrant`, `file-indexer`, `mcp-server`)
**Performance Goals**:
- 95% docs-запросов завершаются менее чем за 3 секунды;
- не менее 90% контрольных docs-запросов имеют релевантный top-3;
- повторные одинаковые запросы к неизменным данным дают стабильный top-k.
**Constraints**:
- состав сервисов неизменен (только `qdrant`, `file-indexer`, `mcp-server`);
- reranking применяется только в markdown docs-search потоке;
- fallback к первичному hybrid этапу обязателен при деградации reranking;
- ошибки должны быть машиночитаемыми и контрактно стабильными;
- `health` и `startup/readiness` валидируются раздельно.
**Scale/Scope**: Репозитории от сотен до десятков тысяч файлов; изменение ограничено docs-search endpoint и MCP docs-search tool без расширения на non-docs поиск.

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

- [x] `research.md` фиксирует решения по reranking-strategy, fallback и scope boundaries.
- [x] `data-model.md` определяет сущности reranking pipeline, правила валидации и state transitions.
- [x] `contracts/md-hybrid-reranking.openapi.yaml` содержит обновленный контракт docs-search с reranking полями и error-кодами.
- [x] `quickstart.md` покрывает позитивные, деградационные, изоляционные и детерминизм-сценарии.

## Project Structure

### Documentation (this feature)

```text
Z:\WORK\ndlss-memory\specs\017-md-hybrid-reranking\
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts\
|   `-- md-hybrid-reranking.openapi.yaml
`-- tasks.md
```

### Source Code (repository root)

```text
Z:\WORK\ndlss-memory\services\file-indexer\
Z:\WORK\ndlss-memory\services\mcp-server\
Z:\WORK\ndlss-memory\infra\docker\
Z:\WORK\ndlss-memory\tests\
```

**Structure Decision**: Переиспользуем существующий docs hybrid search pipeline; reranking добавляется как дополнительный слой ранжирования в текущие `search_repository`/`search_service` и связанные контракты без новых сервисов.

## Phase 0: Outline & Research

1. Best-practice task: выбрать устойчивую reranking strategy поверх hybrid-кандидатов для markdown-корпуса.
2. Integration-pattern task: определить границы применения reranking только для docs endpoint и MCP `search_docs`.
3. Reliability task: определить fallback policy при частичной/полной недоступности reranking этапа.
4. Determinism task: зафиксировать tie-break порядок для равных reranked score.
5. Compatibility task: зафиксировать backward compatibility non-docs endpoint-ов и их контрактов.

**Output**: `Z:\WORK\ndlss-memory\specs\017-md-hybrid-reranking\research.md`

## Phase 1: Design & Contracts

1. Зафиксировать сущности и правила валидации reranking pipeline в `data-model.md`.
2. Подготовить OpenAPI контракт для `POST /v1/search/docs/query` с признаками reranking и fallback/error semantics.
3. Подготовить quickstart-сценарии для:
- reranking positive flow;
- fallback flow при деградации reranking;
- scope isolation относительно non-docs поиска;
- deterministic repeatability.
4. Обновить контекст агента через `.specify/scripts/powershell/update-agent-context.ps1 -AgentType codex`.

**Output**:
- `Z:\WORK\ndlss-memory\specs\017-md-hybrid-reranking\data-model.md`
- `Z:\WORK\ndlss-memory\specs\017-md-hybrid-reranking\contracts\md-hybrid-reranking.openapi.yaml`
- `Z:\WORK\ndlss-memory\specs\017-md-hybrid-reranking\quickstart.md`

## Phase 2: Implementation Planning Boundary

Планирование завершено на уровне дизайна и контрактов; детальная декомпозиция execution-задач выполняется отдельной командой `/speckit.tasks`.

## Complexity Tracking

Нарушений Constitution Check нет. Исключения не требуются.
