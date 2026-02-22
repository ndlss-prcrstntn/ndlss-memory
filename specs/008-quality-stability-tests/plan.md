# План реализации: Качество и стабильность

**Ветка**: `008-quality-stability-tests` | **Дата**: 2026-02-21 | **Спецификация**: `Z:\WORK\ndlss-memory\specs\008-quality-stability-tests\spec.md`
**Вход**: Спецификация фичи из `Z:\WORK\ndlss-memory\specs\008-quality-stability-tests\spec.md`

**Примечание**: Этот файл заполнен командой `/speckit.plan`.

## Summary

Добавить формализованный контур качества для существующего стека: unit, integration, contract и E2E проверки с фокусом на idempotency индексации и корректность MCP-поиска. Технический подход: расширение текущих `tests/*` артефактов, унификация сценариев запуска и фиксация API-контрактов проверяемых endpoint-ов. Ожидаемый результат: воспроизводимый quality-run с однозначным итогом PASS/FAIL и диагностикой по этапам.

## Technical Context

**Language/Version**: Python 3.12 (сервисы и unit-проверки), PowerShell 7+ (compose/e2e orchestration)
**Primary Dependencies**: pytest, Flask, PyYAML, Docker Compose CLI v2
**Storage**: Qdrant (`qdrant_data` volume), файловые fixtures и markdown-отчеты в `tests/`
**Testing**: pytest unit tests + contract markdown checks + integration/E2E compose сценарии
**Target Platform**: Linux-контейнеры под Docker Engine/Docker Desktop, запуск из Windows PowerShell
**Project Type**: multi-service backend (`qdrant`, `file-indexer`, `mcp-server`)
**Performance Goals**: unit-набор < 90s; integration-набор < 12m; E2E smoke < 15m на эталонном окружении; 100% deterministic PASS/FAIL статус прогона
**Constraints**: без добавления новых сервисов; обязательная проверка `full-scan` и `delta-after-commit`; проверка идемпотентности без дублей; Markdown только UTF-8
**Scale/Scope**: покрытие `tests/unit/file_indexer`, `tests/unit/mcp_server`, `tests/integration/*quality*|*regression*`, `tests/contract/*`; один workspace/один compose стек

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

**Post-design gate review**: PASS (подтверждено артефактами `research.md`, `data-model.md`, `contracts/quality-stability-tests.openapi.yaml`, `quickstart.md`)

## Project Structure

### Documentation (this feature)

```text
Z:\WORK\ndlss-memory\specs\008-quality-stability-tests\
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- quality-stability-tests.openapi.yaml
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

**Structure Decision**: Не добавлять новые сервисы/подсистемы; реализовать фичу через расширение существующей тестовой структуры и контрактов API `mcp-server`. Валидация запуска и межсервисного поведения остается в compose-скриптах из `scripts/tests/` и интеграционных сценариях в `tests/integration/`.

## Complexity Tracking

Нарушений Constitution Check нет. Исключения не требуются.

