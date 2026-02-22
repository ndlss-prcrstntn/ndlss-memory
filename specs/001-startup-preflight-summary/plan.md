# План реализации: Предполетные проверки старта и сводка готовности

**Ветка**: `001-startup-preflight-summary` | **Дата**: 2026-02-22 | **Спецификация**: `Z:\WORK\ndlss-memory\specs\001-startup-preflight-summary\spec.md`
**Вход**: Спецификация фичи из `Z:\WORK\ndlss-memory\specs\001-startup-preflight-summary\spec.md`

**Примечание**: Этот файл заполнен командой `/speckit.plan`.

## Summary

Добавить единый startup preflight-слой для `mcp-server` и `file-indexer`, который до перехода в рабочий режим проверяет доступность Qdrant, валидность/читаемость workspace и доступность git для git-зависимых режимов индексации. При провале любой проверки запуск завершается fail-fast со структурированной ошибкой и рекомендацией. При успешном старте выводится единая сводка готовности (service readiness, workspace path, index mode, MCP endpoint, collection name) без изменения существующего API-контракта после успешного старта.

## Technical Context

**Language/Version**: Python 3.12 (`mcp-server`), POSIX shell (`file-indexer` entrypoint/runtime), Docker Compose v2  
**Primary Dependencies**: Flask, PyYAML, встроенные Python-модули (`pathlib`, `subprocess`, `urllib`/HTTP-клиент), Docker Compose runtime env  
**Storage**: Qdrant (`workspace_chunks`), bind mount workspace (`/workspace`), in-memory runtime state для job/status  
**Testing**: pytest (unit/integration), PowerShell smoke/regression scripts, `docker compose up` e2e-проверка  
**Target Platform**: Linux-контейнеры под Docker Engine/Docker Desktop (host: Windows/macOS/Linux)  
**Project Type**: multi-service backend stack (`qdrant`, `file-indexer`, `mcp-server`)  
**Performance Goals**: preflight-проверки завершаются до перехода в ready-состояние; startup summary доступен в логах в течение одного цикла старта (< 60s)  
**Constraints**: обратная совместимость текущих compose preset и REST/MCP API; fail-fast только при критичных startup-зависимостях; UTF-8 для markdown; без добавления новых runtime-сервисов  
**Scale/Scope**: все поддерживаемые compose-файлы (`docker-compose.yml`, `deploy/compose/*.yml`, `deploy/compose-images/*.yml`) и оба режима индексатора (`full-scan`, `delta-after-commit`)

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

**Post-design gate review**: PASS (подтверждено артефактами `research.md`, `data-model.md`, `contracts/startup-preflight-readiness.openapi.yaml`, `quickstart.md`)

## Project Structure

### Documentation (this feature)

```text
Z:\WORK\ndlss-memory\specs\001-startup-preflight-summary\
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- startup-preflight-readiness.openapi.yaml
`-- tasks.md
```

### Source Code (repository root)

```text
Z:\WORK\ndlss-memory\services\mcp-server\src\
Z:\WORK\ndlss-memory\services\file-indexer\scripts\
Z:\WORK\ndlss-memory\services\file-indexer\src\
Z:\WORK\ndlss-memory\deploy\compose\
Z:\WORK\ndlss-memory\deploy\compose-images\
Z:\WORK\ndlss-memory\docs\
Z:\WORK\ndlss-memory\tests\
```

**Structure Decision**: Реализация ограничивается текущими сервисами и entrypoint/runtime-слоем. Новые сервисы, отдельные preflight-контейнеры и внешние оркестраторы не добавляются. Preflight-логика встраивается в существующий startup flow с единым форматом ошибок и ready summary.

## Phase 0: Research Plan

1. Зафиксировать стратегию fail-fast preflight в существующем startup flow (что считается критичным блокером, что диагностическим предупреждением).
2. Выбрать формат структурированных ошибок старта, совместимый с текущим `errorCode`/`message`-подходом API.
3. Определить формат единой startup-ready сводки для операторов (строго обязательные поля + стабильные имена).
4. Проверить best practices для git-зависимых режимов: когда git-check обязателен, а когда должен пропускаться.

## Phase 1: Design Plan

1. Описать data model для startup checks, fail-fast report и readiness summary.
2. Сформировать API/contract-поверхность для наблюдаемости старта (health/status/config/readiness diagnostics) без breaking changes.
3. Подготовить quickstart-сценарии верификации:
   - негативный запуск (Qdrant/workspace/git) с ожидаемым fail-fast;
   - позитивный запуск с готовой summary;
   - проверка неизменности существующих endpoint после успешного старта.
4. Подготовить список test-гейтов для следующего шага implementation (`/speckit.tasks`/`/speckit.implement`).

## Complexity Tracking

Нарушений Constitution Check нет. Исключения не требуются.
