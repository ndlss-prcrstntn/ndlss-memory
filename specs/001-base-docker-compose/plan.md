# План реализации: Базовый Docker Compose стек

**Ветка**: `001-base-docker-compose` | **Дата**: 2026-02-21 | **Спецификация**: `specs/001-base-docker-compose/spec.md`
**Вход**: Спецификация фичи из `/specs/001-base-docker-compose/spec.md`

**Примечание**: Этот файл заполнен командой `/speckit.plan`.

## Summary

Реализовать базовый воспроизводимый запуск стека из трех сервисов (`qdrant`,
`file-indexer`, `mcp-server`) одной командой, с healthcheck, персистентным
хранилищем Qdrant, bind mount рабочей директории и документацией first-run.
Подход: сначала фиксируем операционные решения (compose, конфиг, статусы),
затем формализуем модель данных runtime-конфигурации и контракт операционного
статуса для диагностики.

## Technical Context

**Language/Version**: Docker Compose Specification (CLI v2), YAML 1.2
**Primary Dependencies**: Docker Engine, Docker Compose CLI, контейнерные образы `qdrant`, `file-indexer`, `mcp-server`
**Storage**: Named volume для Qdrant + bind mount рабочей директории для индексатора
**Testing**: Smoke/integration проверки `docker compose up`, healthcheck, статус сервисов, сценарии перезапуска
**Target Platform**: Linux/macOS/Windows с Docker Desktop или Docker Engine
**Project Type**: multi-service backend orchestration
**Performance Goals**: стек переходит в `healthy` за <= 300 секунд на типовой машине разработки
**Constraints**: ровно 3 обязательных сервиса, конфигурация через env, безопасность запуска команд через allowlist/timeout/isolation
**Scale/Scope**: локальный запуск одного workspace, базовая операционная готовность без глубокой бизнес-логики сервисов

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

**Post-design gate review**: PASS (подтверждено артефактами `research.md`, `data-model.md`, `contracts/`, `quickstart.md`)

## Project Structure

### Documentation (this feature)

```text
specs/001-base-docker-compose/
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- compose-observability.openapi.yaml
`-- tasks.md
```

### Source Code (repository root)

```text
infra/
`-- docker/
    `-- docker-compose.yml

services/
|-- file-indexer/
|   `-- Dockerfile
|-- mcp-server/
|   `-- Dockerfile
`-- shared/

tests/
|-- contract/
|   `-- compose_observability_contract_test.md
|-- integration/
|   `-- compose_startup_smoke_test.md
`-- unit/
```

**Structure Decision**: Используем явное разделение `infra/` и `services/`, чтобы
инфраструктурные артефакты не смешивались с кодом сервисов. Контракт статуса
сервиса и quickstart лежат рядом со спецификацией фичи для трассируемости.

## Complexity Tracking

Нарушений Constitution Check нет. Дополнительные исключения не требуются.
