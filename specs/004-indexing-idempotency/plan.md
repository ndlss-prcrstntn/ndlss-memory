# План реализации: Идемпотентность индексации

**Ветка**: `004-indexing-idempotency` | **Дата**: 2026-02-21 | **Спецификация**: `Z:\WORK\ndlss-memory\specs\004-indexing-idempotency\spec.md`
**Вход**: Спецификация фичи из `Z:\WORK\ndlss-memory\specs\004-indexing-idempotency\spec.md`

**Примечание**: Этот файл заполнен командой `/speckit.plan`.

## Summary

Реализовать идемпотентную индексацию контента: вычисление SHA256 fingerprint файла,
сравнение хеша перед upsert, deterministic ID для чанков, корректное обновление
измененных записей и удаление устаревших чанков. Результат: повторные запуски на
неизмененных данных не создают дубликаты, а изменения и удаления файлов
синхронизируются в индексе в рамках одного запуска.

## Technical Context

**Language/Version**: Python 3.12 (`mcp-server`, модули ingestion), POSIX shell для runtime entrypoint
**Primary Dependencies**: Flask API (`mcp-server`), встроенные Python-модули `hashlib`/`pathlib`, Qdrant HTTP API, Docker Compose v2
**Storage**: Qdrant коллекции чанков, runtime in-memory state для запусков синхронизации, workspace bind mount
**Testing**: unit tests (chunk identity/hash sync), integration tests (idempotency cycle), contract tests ingestion endpoints, compose regression scripts
**Target Platform**: Linux containers (Docker Engine / Docker Desktop)
**Project Type**: multi-service backend (`qdrant`, `file-indexer`, `mcp-server`)
**Performance Goals**: повторный запуск на неизмененных данных не увеличивает уникальные записи >1%; >=99% измененных файлов синхронизируются без дубликатов
**Constraints**: без добавления новых сервисов; сохраняется поддержка `full-scan` и `delta-after-commit`; ошибки синхронизации машиночитаемые; markdown в UTF-8
**Scale/Scope**: один workspace на стек, один активный ingestion/sync run в рантайме, синхронизация file->chunk records без UI

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

**Post-design gate review**: PASS (подтверждено артефактами `research.md`, `data-model.md`, `contracts/idempotency-indexing.openapi.yaml`, `quickstart.md`)

## Project Structure

### Documentation (this feature)

```text
Z:\WORK\ndlss-memory\specs\004-indexing-idempotency\
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- idempotency-indexing.openapi.yaml
`-- tasks.md
```

### Source Code (repository root)

```text
Z:\WORK\ndlss-memory\services\
|-- file-indexer/
|   |-- src/ingestion_pipeline/
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

**Structure Decision**: Бизнес-логика идемпотентной синхронизации хранится в
`services/file-indexer/src/ingestion_pipeline` (hash/deterministic-id/sync),
контроль и наблюдаемость запусков — через `services/mcp-server/src` и отдельный
OpenAPI контракт. Документы фичи централизованы в
`Z:\WORK\ndlss-memory\specs\004-indexing-idempotency`.

## Complexity Tracking

Нарушений Constitution Check нет. Исключения не требуются.
