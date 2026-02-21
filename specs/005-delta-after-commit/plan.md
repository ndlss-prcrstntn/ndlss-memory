# План реализации: Delta-after-commit режим

**Ветка**: `005-delta-after-commit` | **Дата**: 2026-02-21 | **Спецификация**: `Z:\WORK\ndlss-memory\specs\005-delta-after-commit\spec.md`
**Вход**: Спецификация фичи из `Z:\WORK\ndlss-memory\specs\005-delta-after-commit\spec.md`

**Примечание**: Этот файл заполнен командой `/speckit.plan`.

## Summary

Реализовать режим `delta-after-commit`, который вычисляет изменения через Git,
индексирует только добавленные/измененные файлы, удаляет из индекса удаленные
или переименованные исходные пути и автоматически выполняет `full-scan` при
ошибках получения diff. Результат: сокращение объема обработки и устойчивый
механизм восстановления без ручного вмешательства.

## Technical Context

**Language/Version**: Python 3.12 (`mcp-server`), POSIX shell (`file-indexer` workers), Docker Compose v2
**Primary Dependencies**: Git CLI (`git diff --name-status --find-renames`), Flask, PyYAML, Qdrant HTTP API
**Storage**: Qdrant коллекция `workspace_chunks`, in-memory runtime state для job status, workspace bind mount
**Testing**: pytest unit tests, integration сценарии в `scripts/tests/*.ps1`, contract validation OpenAPI, compose regression
**Target Platform**: Linux containers under Docker Engine / Docker Desktop
**Project Type**: multi-service backend (`qdrant`, `file-indexer`, `mcp-server`)
**Performance Goals**: delta-run для <=200 измененных файлов выполняется быстрее full-scan на том же workspace; fallback стартует в рамках того же run без ручного рестарта
**Constraints**: состав сервисов фиксирован, обязательна поддержка `full-scan` и `delta-after-commit`, машиночитаемые ошибки, markdown-файлы только UTF-8
**Scale/Scope**: один mounted workspace на стек, один активный delta run, обработка типовых Git-изменений (`A`, `M`, `D`, `R`)

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

**Post-design gate review**: PASS (подтверждено артефактами `research.md`, `data-model.md`, `contracts/delta-after-commit-indexing.openapi.yaml`, `quickstart.md`)

## Project Structure

### Documentation (this feature)

```text
Z:\WORK\ndlss-memory\specs\005-delta-after-commit\
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- delta-after-commit-indexing.openapi.yaml
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
|-- contract/
|-- integration/
`-- unit/
```

**Structure Decision**: Логику расчета Git-изменений и маршрутизации действий
по файлам размещать в `services/file-indexer/src`, оркестрацию запуска/статуса и
контракт API держать в `services/mcp-server/src` и `services/mcp-server/openapi`.
Документы планирования и валидации фичи хранить в
`Z:\WORK\ndlss-memory\specs\005-delta-after-commit`.

## Complexity Tracking

Нарушений Constitution Check нет. Исключения не требуются.
