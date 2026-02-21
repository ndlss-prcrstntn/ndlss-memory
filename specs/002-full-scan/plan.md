# План реализации: Режим Full Scan

**Ветка**: `002-full-scan` | **Дата**: 2026-02-21 | **Спецификация**: `Z:\WORK\ndlss-memory\specs\002-full-scan\spec.md`
**Вход**: Спецификация фичи из `Z:\WORK\ndlss-memory\specs\002-full-scan\spec.md`

**Примечание**: Этот файл заполнен командой `/speckit.plan`.

## Summary

Реализовать полноценный режим `full-scan` для `file-indexer`: рекурсивный обход
директории, фильтрация по типам, исключения по паттернам, контроль размера
файлов, устойчивое продолжение при ошибках чтения и наблюдаемый прогресс.
Результат должен быть доступен через формализованный контракт статуса задачи
индексации и сценарий быстрого запуска.

## Technical Context

**Language/Version**: Python 3.12 (mcp-server), POSIX shell (file-indexer runtime), Docker Compose v2
**Primary Dependencies**: Flask API в `mcp-server`, Qdrant HTTP API, Docker Compose CLI
**Storage**: Qdrant (векторное хранилище), файловая система workspace (read-only mount), runtime-отчеты задач сканирования
**Testing**: unit-тесты фильтрации/валидации, integration-тесты full-scan в compose, contract-тесты API задач индексации, регрессия режимов `full-scan` и `delta-after-commit`
**Target Platform**: Linux containers в Docker Engine/Docker Desktop (Windows/macOS/Linux host)
**Project Type**: multi-service backend (qdrant + file-indexer + mcp-server)
**Performance Goals**: full-scan до 10 000 файлов завершается <= 15 минут; обновление прогресса не реже 60 секунд
**Constraints**: без добавления новых сервисов; конфигурация только через env/конфиг; соблюдение allowlist/timeout/isolation для команд MCP
**Scale/Scope**: один workspace на запуск, один активный full-scan job на инстанс, фокус на scan/filter/progress/error handling

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

**Post-design gate review**: PASS (подтверждено артефактами `research.md`, `data-model.md`, `contracts/full-scan-indexing.openapi.yaml`, `quickstart.md`)

## Project Structure

### Documentation (this feature)

```text
Z:\WORK\ndlss-memory\specs\002-full-scan\
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- full-scan-indexing.openapi.yaml
`-- tasks.md
```

### Source Code (repository root)

```text
Z:\WORK\ndlss-memory\services\
|-- file-indexer/
|   |-- scripts/
|   |-- config/
|   `-- src/
|-- mcp-server/
|   |-- src/
|   `-- openapi/
`-- shared/

Z:\WORK\ndlss-memory\infra\docker\
`-- docker-compose.yml

Z:\WORK\ndlss-memory\tests\
|-- unit/
|-- integration/
`-- contract/
```

**Structure Decision**: Документацию и контракты фичи сохраняем в `specs/002-full-scan`,
а реализацию и тесты размещаем в текущих сервисных каталогах без изменения
архитектурного состава стека.

## Complexity Tracking

Нарушений Constitution Check нет. Дополнительные исключения не требуются.
