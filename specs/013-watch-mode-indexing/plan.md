# План реализации: Непрерывный Watch Mode

**Ветка**: `013-watch-mode-indexing` | **Дата**: 2026-02-22 | **Спецификация**: `Z:\WORK\ndlss-memory\specs\013-watch-mode-indexing\spec.md`  
**Вход**: Спецификация фичи из `Z:\WORK\ndlss-memory\specs\013-watch-mode-indexing\spec.md`

**Примечание**: Этот файл заполнен командой `/speckit.plan`.

## Summary

Добавить непрерывный режим `INDEX_MODE=watch`, который автоматически отслеживает изменения файлов в workspace и запускает инкрементальную переиндексацию только затронутых файлов (create/update/delete) без ручного API-триггера. Решение должно быть устойчивым к burst-нагрузке и временным ошибкам наблюдателя, публиковать прозрачный статус watch-активности через логи и status/summary endpoint, и не менять поведение режимов `full-scan` и `delta-after-commit`.

## Technical Context

**Language/Version**: Python 3.12 (`mcp-server` и ingestion runtime), POSIX shell runtime в контейнере (`file-indexer`)  
**Primary Dependencies**: Flask, PyYAML, существующие модули `ingestion_pipeline/*`, `idempotency_state`, `ingestion_state`, файловый watcher-адаптер в Python runtime  
**Storage**: Qdrant (`workspace_chunks`, служебные коллекции состояния), bind-mounted workspace (`/workspace`), in-memory состояние watch-run и очереди событий  
**Testing**: pytest (unit/integration/contract), PowerShell smoke/compose сценарии, quality suite (`scripts/tests/run_quality_stability_suite.ps1`)  
**Target Platform**: Linux containers (Docker Engine / Docker Desktop на Windows/macOS/Linux)  
**Project Type**: Multi-service backend stack (`qdrant`, `file-indexer`, `mcp-server`)  
**Performance Goals**: отражение изменений файла в поиске <= 60 секунд (SC-001); устойчивость при burst >= 100 событий/60 секунд (SC-002); восстановление watch после временной ошибки <= 2 минуты (SC-003)  
**Constraints**: сохранить обратную совместимость API; не нарушить `full-scan` и `delta-after-commit`; fail-safe retry/backoff без остановки watch-loop; обновить docs/quickstart в том же изменении  
**Scale/Scope**: изменения в `Z:\WORK\ndlss-memory\services\mcp-server\src`, `Z:\WORK\ndlss-memory\services\file-indexer\src` (при необходимости), `Z:\WORK\ndlss-memory\docker-compose.yml`, `Z:\WORK\ndlss-memory\deploy\compose-images\*.yml`, `Z:\WORK\ndlss-memory\tests\*`, `Z:\WORK\ndlss-memory\docs\*`

## Constitution Check

*GATE: Должен пройти до Phase 0 research. Повторно проверить после Phase 1 design.*

**Pre-design gate review**: PASS

- [x] Состав сервисов не нарушает конституцию: только `qdrant`, `file-indexer`, `mcp-server`.
- [x] Предусмотрены оба режима индексатора: `full-scan` и `delta-after-commit` (без регрессий).
- [x] В плане есть проверка идемпотентности индексации (без дубликатов при повторной обработке событий).
- [x] MCP-инструменты/endpoint имеют формализованные контракты ввода/вывода и машиночитаемые ошибки.
- [x] Для запуска команд описаны ограничения безопасности: allowlist, таймауты, изоляция.
- [x] Включены обязательные проверки: тесты, `docker compose up`, MCP/REST контракты, регрессия индексатора в обоих режимах.
- [x] Запланировано обновление `README.md` и quickstart в том же изменении.

**Post-design gate review**: PASS (подтверждено артефактами `research.md`, `data-model.md`, `contracts/watch-mode-indexing.openapi.yaml`, `quickstart.md`)

## Project Structure

### Documentation (this feature)

```text
Z:\WORK\ndlss-memory\specs\013-watch-mode-indexing\
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts\
|   `-- watch-mode-indexing.openapi.yaml
`-- tasks.md
```

### Source Code (repository root)

```text
Z:\WORK\ndlss-memory\services\mcp-server\src\
Z:\WORK\ndlss-memory\services\file-indexer\src\
Z:\WORK\ndlss-memory\services\mcp-server\openapi\
Z:\WORK\ndlss-memory\docker-compose.yml
Z:\WORK\ndlss-memory\deploy\compose-images\
Z:\WORK\ndlss-memory\tests\
Z:\WORK\ndlss-memory\docs\
```

**Structure Decision**: watch-координатор и state-management реализуются в `mcp-server` как единый runtime orchestration слой поверх существующего ingestion/idempotency pipeline, чтобы переиспользовать текущую бизнес-логику индексации и публичные endpoint. `file-indexer` сохраняет совместимость runtime-режимов и конфигурации compose.

## Phase 0: Research Plan

1. Выбрать и обосновать стратегию detection изменений в Docker-mounted workspace для режима `watch` с фокусом на стабильность при burst.
2. Определить стратегию коалесценции/дедупликации событий (create/update/delete/rename) и правила запуска инкрементальной обработки.
3. Выбрать retry/backoff политику для ошибок watcher-loop и ошибок инкрементальной индексации.
4. Определить схему публикации watch-активности в логах и status/summary API без breaking change.
5. Определить минимальный regression-набор для гарантии, что `full-scan`/`delta-after-commit` не деградируют.

## Phase 1: Design Plan

1. Описать data model для watch-событий, состояния watcher и результатов инкрементальной обработки.
2. Подготовить контракт API наблюдаемости watch (`/v1/indexing/watch/status`, `/summary`, и расширения existing status endpoint).
3. Подготовить quickstart-сценарии:
   - запуск `INDEX_MODE=watch`;
   - проверка create/update/delete без ручного trigger;
   - проверка retry/recovery после искусственной ошибки.
4. Обновить агентный контекст через `.specify/scripts/powershell/update-agent-context.ps1 -AgentType codex`.

## Complexity Tracking

Нарушений Constitution Check нет. Исключения не требуются.
