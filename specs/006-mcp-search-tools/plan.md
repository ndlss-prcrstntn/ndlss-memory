# План реализации: MCP-инструменты поиска

**Ветка**: `006-mcp-search-tools` | **Дата**: 2026-02-21 | **Спецификация**: `Z:\WORK\ndlss-memory\specs\006-mcp-search-tools\spec.md`
**Вход**: Спецификация фичи из `Z:\WORK\ndlss-memory\specs\006-mcp-search-tools\spec.md`

**Примечание**: Этот файл заполнен командой `/speckit.plan`.

## Summary

Реализовать набор MCP-инструментов поиска: semantic search, получение источника
по ID и получение метаданных документа по ID, с поддержкой фильтрации по пути,
папке и типу файла, предсказуемым структурированным ответом и корректной
обработкой пустых результатов. Ожидаемый результат: пользователь проходит цепочку
"поиск -> источник -> метаданные" без ручной донастройки и с машиночитаемыми
ошибками.

## Technical Context

**Language/Version**: Python 3.12 (`mcp-server`), POSIX shell (`file-indexer` runtime), Docker Compose v2
**Primary Dependencies**: Flask, PyYAML, Qdrant HTTP API, существующие ingestion/idempotency state-модули
**Storage**: Qdrant коллекция `workspace_chunks`, in-memory state для MCP job/request tracking, bind-mounted workspace
**Testing**: pytest unit tests, contract markdown checks, integration сценарии через PowerShell scripts, compose regression
**Target Platform**: Linux containers under Docker Engine / Docker Desktop
**Project Type**: multi-service backend (`qdrant`, `file-indexer`, `mcp-server`)
**Performance Goals**: >=95% поисковых запросов semantic search на эталонном наборе завершаются < 2s; пустая выдача обрабатывается без internal error
**Constraints**: не добавлять новые сервисы; сохранить совместимость режимов `full-scan` и `delta-after-commit`; ответы/ошибки MCP машиночитаемые; markdown в UTF-8
**Scale/Scope**: один workspace на стек, одна коллекция поиска, 3 MCP search tools (`semantic-search`, `get-source-by-id`, `get-document-metadata`)

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

**Post-design gate review**: PASS (подтверждено артефактами `research.md`, `data-model.md`, `contracts/mcp-search-tools.openapi.yaml`, `quickstart.md`)

## Project Structure

### Documentation (this feature)

```text
Z:\WORK\ndlss-memory\specs\006-mcp-search-tools\
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- mcp-search-tools.openapi.yaml
`-- tasks.md
```

### Source Code (repository root)

```text
Z:\WORK\ndlss-memory\services\
|-- file-indexer/
|   |-- src/
|   `-- scripts/
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

**Structure Decision**: Реализацию MCP search tools и обработку ответов/ошибок
выполнять в `services/mcp-server/src/system_status_handler.py` и смежных
state/error-модулях. Переиспользовать текущую модель хранения чанков в
`workspace_chunks` и существующие метаданные ingestion pipeline. Контракты
зафиксировать отдельно в `specs/006-mcp-search-tools/contracts/`.

## Complexity Tracking

Нарушений Constitution Check нет. Исключения не требуются.
