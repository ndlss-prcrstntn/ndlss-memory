# План реализации: MCP Transport Compatibility

**Ветка**: `009-mcp-transport` | **Дата**: 2026-02-22 | **Спецификация**: `Z:\WORK\ndlss-memory\specs\009-mcp-transport\spec.md`
**Вход**: Спецификация фичи из `Z:\WORK\ndlss-memory\specs\009-mcp-transport\spec.md`

**Примечание**: Этот файл заполнен командой `/speckit.plan`.

## Summary

Добавить полноценную MCP-транспортную совместимость для клиентов VS Code/Claude/Cline: стандартный JSON-RPC transport endpoint, SSE fallback endpoint, discovery endpoint, обязательные MCP методы (`initialize`, `notifications/initialized`, `ping`, `tools/list`, `tools/call`), унифицированные JSON-RPC ошибки и контрактные проверки. Подход: расширить `mcp-server` как MCP transport facade поверх существующей доменной логики поиска/индексации, сохранить обратную совместимость текущих REST endpoint-ов, добавить клиентские конфиги и smoke/contract тесты совместимости.

## Technical Context

**Language/Version**: Python 3.12 (`mcp-server` runtime)
**Primary Dependencies**: Flask, PyYAML, стандартные Python JSON/HTTP примитивы, Docker Compose v2
**Storage**: Qdrant коллекция `workspace_chunks`; in-memory состояние MCP-сессий/запросов; существующие runtime state-модули
**Testing**: pytest unit tests + contract tests (OpenAPI/JSON-RPC payload validation) + integration smoke с compose
**Target Platform**: Linux containers under Docker Engine/Docker Desktop; локальные клиенты на Windows/macOS/Linux
**Project Type**: multi-service backend (`qdrant`, `file-indexer`, `mcp-server`)
**Performance Goals**: handshake p95 < 5s; `tools/list` p95 < 1s; `tools/call` (поиск) p95 < 3s; не менее 5 одновременных MCP-сессий без протокольных ошибок
**Constraints**: без добавления новых сервисов; сохранение existing REST API; машиночитаемые JSON-RPC ошибки; UTF-8 для всех Markdown; глобальная нумерация `specs/`
**Scale/Scope**: 1 MCP transport surface (`/mcp`) + fallback (`/sse`, `/messages`) + discovery (`/.well-known/mcp`); минимум 5 MCP tools (search/source/metadata/ingestion start/ingestion status)

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

**Post-design gate review**: PASS (подтверждено артефактами `research.md`, `data-model.md`, `contracts/mcp-transport.openapi.yaml`, `quickstart.md`)

## Project Structure

### Documentation (this feature)

```text
Z:\WORK\ndlss-memory\specs\009-mcp-transport\
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- mcp-transport.openapi.yaml
`-- tasks.md
```

### Source Code (repository root)

```text
Z:\WORK\ndlss-memory\services\
|-- file-indexer/
`-- mcp-server/

Z:\WORK\ndlss-memory\infra\
`-- docker/

Z:\WORK\ndlss-memory\tests\
|-- unit/
|-- integration/
`-- contract/
```

**Structure Decision**: Реализация остается в `services/mcp-server/src` как транспортный слой (MCP protocol adapter) над существующими сервисами поиска/индексации. Контракты размещаются в `specs/009-mcp-transport/contracts/` и синхронизируются с runtime API surface. Проверки совместимости добавляются в `tests/unit`, `tests/contract`, `tests/integration` без расширения сервисного состава.

## Complexity Tracking

Нарушений Constitution Check нет. Исключения не требуются.
