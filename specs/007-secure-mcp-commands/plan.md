# План реализации: Безопасный запуск команд через MCP

**Ветка**: `007-secure-mcp-commands` | **Дата**: 2026-02-21 | **Спецификация**: `Z:\WORK\ndlss-memory\specs\007-secure-mcp-commands\spec.md`
**Вход**: Спецификация фичи из `Z:\WORK\ndlss-memory\specs\007-secure-mcp-commands\spec.md`

**Примечание**: Этот файл заполнен командой `/speckit.plan`.

## Summary

Реализовать безопасный рантайм запуска команд через MCP с обязательной allowlist-проверкой,
таймаутами, ограничением прав выполнения, ограничением ресурсов, изоляцией рабочей директории,
машиночитаемыми ошибками и аудитом каждого вызова. Ожидаемый результат: команды выполняются
предсказуемо и безопасно, а оператор может однозначно диагностировать причины отказов.

## Technical Context

**Language/Version**: Python 3.12 (`mcp-server`), POSIX shell runtime в контейнере
**Primary Dependencies**: Flask, PyYAML, стандартные средства управления процессами и таймаутами, Docker Compose policy
**Storage**: in-memory state для статусов выполнения + append-only аудит в файловом хранилище контейнера
**Testing**: pytest unit tests, contract markdown checks, integration сценарии через PowerShell scripts, compose regression
**Target Platform**: Linux containers under Docker Engine / Docker Desktop
**Project Type**: multi-service backend (`qdrant`, `file-indexer`, `mcp-server`)
**Performance Goals**: 100% блокировка команд вне allowlist до запуска; 100% timeout команд завершается принудительно; >=95% разрешенных команд завершаются < 5s на эталонном наборе
**Constraints**: не добавлять новые сервисы; сохранить совместимость режимов `full-scan` и `delta-after-commit`; ответы/ошибки MCP машиночитаемые; markdown в UTF-8
**Scale/Scope**: один workspace на стек, один командный рантайм в `mcp-server`, аудит всех MCP command-вызовов, политики allowlist/timeout/resource/isolation

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

**Post-design gate review**: PASS (подтверждено артефактами `research.md`, `data-model.md`, `contracts/mcp-command-security.openapi.yaml`, `quickstart.md`)

## Project Structure

### Documentation (this feature)

```text
Z:\WORK\ndlss-memory\specs\007-secure-mcp-commands\
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- mcp-command-security.openapi.yaml
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

**Structure Decision**: Реализацию безопасного запуска команд и аудита выполнять в `services/mcp-server/src/` с выделением policy/state/error модулей и подключением endpoint-обработчиков в существующий HTTP handler. Контракт зафиксировать отдельно в `specs/007-secure-mcp-commands/contracts/` и синхронизировать копию в `services/mcp-server/openapi/`.

## Complexity Tracking

Нарушений Constitution Check нет. Исключения не требуются.
