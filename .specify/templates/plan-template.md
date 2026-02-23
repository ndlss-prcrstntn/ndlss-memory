# План реализации: [FEATURE]

**Ветка**: `[###-feature-name]` | **Дата**: [DATE] | **Спецификация**: [link]
**Вход**: Спецификация фичи из `/specs/[###-feature-name]/spec.md`

**Примечание**: Этот файл заполняется командой `/speckit.plan`.

## Summary

[Кратко: основное требование, технический подход и ожидаемый результат]

## Technical Context

**Language/Version**: [например, Python 3.12 или NEEDS CLARIFICATION]
**Primary Dependencies**: [например, FastAPI, qdrant-client или NEEDS CLARIFICATION]
**Storage**: [например, Qdrant, файлы, N/A]
**Testing**: [например, pytest, docker compose integration tests]
**Target Platform**: [например, Linux + Docker Engine]
**Project Type**: [например, multi-service backend]
**Performance Goals**: [конкретные метрики, например p95 < 300ms]
**Constraints**: [лимиты, безопасность, сетевые ограничения]
**Scale/Scope**: [масштаб данных, число инструментов MCP, объем файлов]

## Constitution Check

*GATE: Должен пройти до Phase 0 research. Повторно проверить после Phase 1 design.*

- [ ] Состав сервисов не нарушает конституцию: только `qdrant`, `file-indexer`, `mcp-server`.
- [ ] Предусмотрены оба режима индексатора: `full-scan` и `delta-after-commit`.
- [ ] В плане есть проверка идемпотентности индексации (без дубликатов при повторном запуске).
- [ ] MCP-инструменты имеют формализованные контракты ввода/вывода и машиночитаемые ошибки.
- [ ] Для запуска команд описаны ограничения безопасности: allowlist, таймауты, изоляция.
- [ ] Для локальной разработки предусмотрены уникальные порты и явный env-профиль MCP.
- [ ] Явно разделены семантики `health` и `startup/readiness` в сценариях валидации.
- [ ] Для multi-module задач описан MCP-контекстный проход и последующая file-level верификация.
- [ ] Включены обязательные проверки: тесты, `docker compose up`, MCP-контракты,
      регрессия индексатора в обоих режимах.
- [ ] Запланировано обновление `README.md` и quickstart в том же изменении.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
`-- tasks.md
```

### Source Code (repository root)

```text
services/
|-- file-indexer/
|-- mcp-server/
`-- shared/

infra/
`-- docker/

tests/
|-- contract/
|-- integration/
`-- unit/
```

**Structure Decision**: [Выбранная структура и причины]

## Complexity Tracking

> **Заполнять только если есть нарушения Constitution Check и они оправданы.**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|--------------------------------------|
| [пример] | [причина] | [почему простой путь не подходит] |

