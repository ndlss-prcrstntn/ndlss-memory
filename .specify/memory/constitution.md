<!--
Sync Impact Report
- Version change: 1.0.0 -> 1.1.0
- Modified principles:
  - Development Workflow and Delivery Gates (добавлено обязательное обновление статусов roadmap/checklist после implementation)
- Added sections:
  - Architecture and Operational Constraints
  - Development Workflow and Delivery Gates
- Removed sections:
  - None
- Templates requiring updates:
  - ✅ updated: .specify/templates/plan-template.md
  - ✅ updated: .specify/templates/spec-template.md
  - ✅ updated: .specify/templates/tasks-template.md
  - ⚠ pending: .specify/templates/commands/*.md (directory is missing in current repository)
  - ✅ updated: README.md
  - ✅ updated: .codex/prompts/speckit.analyze.md
  - ✅ updated: .codex/prompts/speckit.checklist.md
  - ✅ updated: .codex/prompts/speckit.clarify.md
  - ✅ updated: .codex/prompts/speckit.constitution.md
  - ✅ updated: .codex/prompts/speckit.implement.md
  - ✅ updated: .codex/prompts/speckit.plan.md
  - ✅ updated: .codex/prompts/speckit.specify.md
  - ✅ updated: .codex/prompts/speckit.tasks.md
  - ✅ updated: .codex/prompts/speckit.taskstoissues.md
- Follow-up TODOs:
  - TODO(COMMAND_TEMPLATES): if Speckit command templates are later added at .specify/templates/commands/*.md, localize them to Russian and align them with this constitution.
-->
# ndlss-memory Constitution

## Core Principles

### I. Docker Compose Reproducibility
Все обязательные компоненты проекта ДОЛЖНЫ запускаться одной командой
`docker compose up` без локальной установки зависимостей, кроме Docker и Git.
Состав сервисов фиксирован: `qdrant`, `file-indexer`, `mcp-server`.
Каждый сервис ДОЛЖЕН иметь стабильные `healthcheck`, предсказуемые переменные
окружения и документированные volume-монты.
Рационал: воспроизводимость и простой запуск для любого пользователя.

### II. Deterministic File Indexing
`file-indexer` ДОЛЖЕН работать как минимум в двух режимах:
`full-scan` (полная индексация) и `delta-after-commit` (только измененные файлы
после commit). Типы индексируемых файлов ДОЛЖНЫ задаваться через конфиг или
переменные окружения, а не кодом. Индексация ДОЛЖНА быть идемпотентной:
повторный запуск без изменений не создает дубликатов в векторном хранилище.
Рационал: предсказуемое качество индекса и контролируемая стоимость обработки.

### III. Secure MCP Interoperability
`mcp-server` ДОЛЖЕН предоставлять интерфейс, совместимый с MCP, чтобы им могла
пользоваться любая модель или агент. Все инструменты MCP ДОЛЖНЫ иметь четкие
контракты ввода/вывода, машиночитаемые ошибки и таймауты. Запуск команд ДОЛЖЕН
быть ограничен allowlist-политикой, изоляцией контейнера и запретом на
неограниченный доступ к хост-системе.
Рационал: совместимость между провайдерами ИИ без компромисса по безопасности.

### IV. Quality Gates and Test Discipline
Каждое изменение ДОЛЖНО проходить минимум четыре проверки:
1. unit/integration тесты для затронутой логики;
2. проверка Docker Compose запуска с нуля;
3. проверка MCP-контрактов (инструменты отвечают по спецификации);
4. проверка отсутствия регрессий индексации в обоих режимах.
Изменение нельзя считать завершенным, пока все обязательные проверки не пройдены.
Рационал: стабильность поставки важнее скорости без верификации.

### V. Documentation as a Product
Проект ДОЛЖЕН поддерживать актуальные `README.md`, quickstart, примеры
конфигурации и описание ограничений безопасности. Любое изменение публичного
поведения ДОЛЖНО сопровождаться обновлением документации в том же PR.
Документация ДОЛЖНА быть понятной внешнему пользователю GitHub без контекста
внутренней команды.
Рационал: для open-source проекта документация является частью продукта.

## Architecture and Operational Constraints

1. Архитектура ограничена тремя сервисами: `qdrant`, `file-indexer`, `mcp-server`.
2. `qdrant` ДОЛЖЕН использовать persistent volume для сохранения индекса между
перезапусками.
3. `file-indexer` ДОЛЖЕН читать файлы через volume из рабочей директории и уважать
исключения (`.git`, бинарные артефакты, секреты).
4. `mcp-server` ДОЛЖЕН запрашивать данные через явные API/контракты, а не через
непрозрачный доступ к внутреннему состоянию контейнеров.
5. Все сетевые порты, лимиты ресурсов и политики рестарта ДОЛЖНЫ быть явными в
`docker-compose.yml`.

## Development Workflow and Delivery Gates

1. Перед реализацией изменений ДОЛЖНЫ быть обновлены `spec.md`, `plan.md` и
`tasks.md` для соответствующей фичи.
2. PR ДОЛЖЕН содержать: ссылку на спецификацию, список затронутых сервисов,
результаты тестов и изменения документации.
3. Если изменение затрагивает MCP-инструменты или формат индекса, ДОЛЖЕН быть
описан план миграции и обратная совместимость.
4. Любое ослабление требований этой конституции требует явного исключения в PR с
обоснованием и сроком устранения.
5. После завершения implementation ДОЛЖНЫ быть явно отмечены выполненные пункты
в пользовательских roadmap/checklist-артефактах (например, в `README.md`,
`tasks.md`, release-checklist), если они затронуты изменением.

## Governance

Эта конституция имеет приоритет над локальными практиками и шаблонами.
Изменения принимаются только через PR с отдельным разделом `Constitution Impact`.
Порядок изменения версий:
- MAJOR: удаление принципа, несовместимое изменение governance или обязательных
quality gates;
- MINOR: добавление нового принципа/раздела или существенное расширение требований;
- PATCH: редакционные правки без изменения нормативного смысла.

Проверка соблюдения проводится для каждого PR и релиза:
- reviewer обязан проверить соответствие принципам и quality gates;
- отсутствие подтверждения compliance блокирует merge;
- обнаруженные нарушения фиксируются как отдельные задачи с дедлайном.

**Version**: 1.1.0 | **Ratified**: 2026-02-21 | **Last Amended**: 2026-02-21


