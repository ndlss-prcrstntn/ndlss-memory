---

description: "Шаблон списка задач для реализации фичи"
---

# Tasks: [FEATURE NAME]

**Input**: Документы из `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Тесты включаются обязательно для требований из конституции (MCP-контракты,
индексация, compose запуск). Для остального - по необходимости.

**Organization**: Задачи группируются по user story для независимой реализации.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Можно выполнять параллельно (разные файлы, нет зависимостей)
- **[Story]**: Привязка к user story (US1, US2, US3)
- Всегда указывайте точные пути к файлам

## Path Conventions

- **Multi-service backend**: `services/`, `infra/`, `tests/`
- **Single project**: `src/`, `tests/`
- Используйте структуру из `plan.md` как источник истины

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Инициализация проекта и окружения

- [ ] T001 Создать/уточнить структуру директорий по `plan.md`
- [ ] T002 Настроить `docker-compose.yml` с тремя сервисами и healthcheck
- [ ] T003 [P] Подготовить `.env.example` с параметрами индексации и безопасности
- [ ] T004 [P] Настроить базовые инструменты качества (lint/format/test)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Базовые компоненты, блокирующие все user story

- [ ] T005 Реализовать конфигурацию типов файлов и исключений для индексатора
- [ ] T006 [P] Реализовать режим `full-scan`
- [ ] T007 [P] Реализовать режим `delta-after-commit`
- [ ] T008 Добавить защиту от дубликатов при повторной индексации
- [ ] T009 [P] Реализовать контракты MCP-инструментов (schema + error model)
- [ ] T010 Реализовать безопасный запуск команд (allowlist + timeout + sandbox)
- [ ] T011 [P] Настроить структурированное логирование и метрики

**Checkpoint**: Основа готова, можно реализовывать user stories

---

## Phase 3: User Story 1 - [Title] (Priority: P1) MVP

**Goal**: [Что поставляется пользователю]

**Independent Test**: [Как проверить историю отдельно]

### Tests for User Story 1

- [ ] T012 [P] [US1] Contract tests MCP в `tests/contract/`
- [ ] T013 [P] [US1] Integration test для `docker compose up` и базового запроса
- [ ] T014 [P] [US1] Regression test идемпотентности индексации

### Implementation for User Story 1

- [ ] T015 [P] [US1] Реализовать модели/DTO в [path]
- [ ] T016 [US1] Реализовать сервисную логику в [path]
- [ ] T017 [US1] Добавить обработку ошибок и таймаутов
- [ ] T018 [US1] Обновить документацию (`README.md`, quickstart)

**Checkpoint**: User Story 1 завершена и проверена независимо

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal**: [Описание]

**Independent Test**: [Описание]

### Tests for User Story 2

- [ ] T019 [P] [US2] Contract/integration tests в `tests/`

### Implementation for User Story 2

- [ ] T020 [P] [US2] Реализовать [компонент] в [path]
- [ ] T021 [US2] Интегрировать с общими сервисами
- [ ] T022 [US2] Обновить документацию и примеры

---

## Phase 5: User Story 3 - [Title] (Priority: P3)

**Goal**: [Описание]

**Independent Test**: [Описание]

### Tests for User Story 3

- [ ] T023 [P] [US3] Contract/integration tests в `tests/`

### Implementation for User Story 3

- [ ] T024 [P] [US3] Реализовать [компонент] в [path]
- [ ] T025 [US3] Интегрировать и валидировать в compose окружении

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Финальные улучшения для всех user stories

- [ ] TXXX [P] Обновить документацию и changelog
- [ ] TXXX Провести рефакторинг и удаление техдолга
- [ ] TXXX [P] Усилить тест-покрытие для критичных путей
- [ ] TXXX Проверить безопасность запуска команд и ограничения контейнера
- [ ] TXXX Валидировать quickstart на чистом окружении

---

## Dependencies & Execution Order

- Setup -> Foundational -> User Stories -> Polish
- User stories стартуют только после завершения Foundational
- Истории могут идти параллельно при отсутствии конфликтов
- Внутри каждой истории: тесты/контракты до финальной интеграции

---

## Notes

- Задачи с `[P]` безопасны для параллельного выполнения
- Каждая user story должна быть независимо демонстрируема
- Изменения без обновления документации считаются незавершенными
- Нарушения конституции фиксируются отдельной задачей с дедлайном

