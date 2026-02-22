# Tasks: Непрерывный Watch Mode

**Input**: Документы из `/specs/013-watch-mode-indexing/`  
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/watch-mode-indexing.openapi.yaml`, `quickstart.md`

**Tests**: Добавлены обязательные unit/integration/contract проверки для критериев успеха watch-режима и конституционных требований по регрессиям и наблюдаемости.

**Organization**: Задачи сгруппированы по user story, чтобы каждая история реализовывалась и тестировалась независимо.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Подготовить конфигурацию окружения и compose-пресеты для нового режима `INDEX_MODE=watch`.

- [X] T001 Добавить конфигурацию режима `watch` и переменные watcher в `docker-compose.yml`
- [X] T002 [P] Добавить переменные watch-режима в `deploy/compose-images/generic.yml`
- [X] T003 [P] Добавить переменные watch-режима в `deploy/compose-images/typescript.yml`
- [X] T004 [P] Добавить переменные watch-режима в `deploy/compose-images/csharp.yml`
- [X] T005 Обновить переменные и примеры запуска watch-режима в `.env.example`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Реализовать базовые компоненты watch-runtime, которые блокируют все user story.

- [X] T006 Создать модели watch-событий и состояния runtime в `services/mcp-server/src/watch_mode_models.py`
- [X] T007 Создать хранилище состояния watch-runtime в `services/mcp-server/src/watch_mode_state.py`
- [X] T008 Реализовать коалесценцию и дедупликацию событий в `services/mcp-server/src/watch_mode_coalescer.py`
- [X] T009 Реализовать адаптер наблюдения файловой системы с fallback reconcile в `services/mcp-server/src/watch_mode_watcher.py`
- [X] T010 Реализовать оркестратор инкрементальной обработки watch-событий в `services/mcp-server/src/watch_mode_orchestrator.py`
- [X] T011 [P] Добавить unit-тесты для моделей/стейта/коалесцера watch-режима в `tests/unit/mcp_server/test_watch_mode_state.py`
- [X] T012 Добавить поддержку `INDEX_MODE=watch` в runtime-валидацию `services/file-indexer/scripts/validate-config.sh`

**Checkpoint**: Базовые компоненты watch-runtime готовы, можно реализовывать пользовательские сценарии.

---

## Phase 3: User Story 1 - Автообновление поиска (Priority: P1) MVP

**Goal**: После изменения файлов поиск обновляется автоматически без ручного запуска ingestion job.

**Independent Test**: Запустить стек в режиме watch, создать/изменить/удалить файл в workspace и подтвердить, что результаты поиска обновляются без ручного API-триггера.

### Tests for User Story 1

- [X] T013 [P] [US1] Добавить integration-тест автоиндексации create/update событий в `tests/integration/test_watch_mode_incremental_create_update.py`
- [X] T014 [P] [US1] Добавить integration-тест очистки индекса при delete-событии в `tests/integration/test_watch_mode_incremental_delete.py`
- [X] T015 [P] [US1] Добавить contract-тест watch status endpoint в `tests/contract/test_watch_mode_status_contract.py`

### Implementation for User Story 1

- [X] T016 [US1] Реализовать запуск watch-loop при `INDEX_MODE=watch` в `services/mcp-server/src/system_status_handler.py`
- [X] T017 [US1] Реализовать обработку create/update/delete через существующий ingestion pipeline в `services/mcp-server/src/watch_mode_orchestrator.py`
- [X] T018 [US1] Добавить idempotent-фильтрацию повторной обработки одного файла в `services/mcp-server/src/watch_mode_orchestrator.py`
- [X] T019 [US1] Пробросить watch-конфигурацию и heartbeat-лог в `services/file-indexer/scripts/entrypoint.sh`
- [X] T020 [US1] Обновить feature quickstart для сценария автоиндексации в `specs/013-watch-mode-indexing/quickstart.md`

**Checkpoint**: US1 завершена, автообновление поиска работает без ручного запуска ingestion.

---

## Phase 4: User Story 2 - Устойчивый наблюдатель (Priority: P2)

**Goal**: Watch-режим переживает burst-изменения и временные ошибки без ручного рестарта.

**Independent Test**: Сгенерировать burst событий и временную ошибку зависимости; убедиться, что watch переходит в recovering и автоматически возвращается в running.

### Tests for User Story 2

- [X] T021 [P] [US2] Добавить unit-тест retry/backoff политики watcher в `tests/unit/mcp_server/test_watch_mode_retry_policy.py`
- [X] T022 [P] [US2] Добавить integration-тест устойчивости при burst-обновлениях в `tests/integration/test_watch_mode_burst_stability.py`
- [X] T023 [P] [US2] Добавить integration-тест автоматического восстановления watcher после ошибки в `tests/integration/test_watch_mode_recovery.py`

### Implementation for User Story 2

- [X] T024 [US2] Реализовать retry/backoff с jitter и ограничением попыток в `services/mcp-server/src/watch_mode_watcher.py`
- [X] T025 [US2] Реализовать переходы состояния `running/recovering/failed` и счетчики ошибок в `services/mcp-server/src/watch_mode_state.py`
- [X] T026 [US2] Реализовать fallback reconcile-scan для пропущенных событий в `services/mcp-server/src/watch_mode_orchestrator.py`
- [X] T027 [US2] Добавить структурированные watch-логи по событиям восстановления в `services/mcp-server/src/watch_mode_orchestrator.py`

**Checkpoint**: US2 завершена, watcher стабилен при burst-нагрузке и временных ошибках.

---

## Phase 5: User Story 3 - Прозрачный статус watch (Priority: P3)

**Goal**: Оператор получает прозрачный статус watch-режима через API и summary без разбора сырых логов.

**Independent Test**: Запросить `/v1/indexing/watch/status` и `/v1/indexing/watch/summary`, получить полные поля состояния и сведения о последней обработке, включая ошибки.

### Tests for User Story 3

- [X] T028 [P] [US3] Добавить contract-тест watch summary endpoint в `tests/contract/test_watch_mode_summary_contract.py`
- [X] T029 [P] [US3] Добавить integration-тест наблюдаемости watch-статуса и ошибок в `tests/integration/test_watch_mode_observability.py`

### Implementation for User Story 3

- [X] T030 [US3] Добавить endpoint `GET /v1/indexing/watch/status` в `services/mcp-server/src/system_status_handler.py`
- [X] T031 [US3] Добавить endpoint `GET /v1/indexing/watch/summary` в `services/mcp-server/src/system_status_handler.py`
- [X] T032 [US3] Расширить summary/state модель полями watch-активности в `services/mcp-server/src/ingestion_state.py`
- [X] T033 [US3] Синхронизировать OpenAPI контракты watch endpoint в `services/mcp-server/openapi/compose-observability.openapi.yaml`
- [X] T034 [US3] Синхронизировать feature-контракт в `specs/013-watch-mode-indexing/contracts/watch-mode-indexing.openapi.yaml`

**Checkpoint**: US3 завершена, watch-статус и сводка доступны и пригодны для операционной диагностики.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Финальная регрессия, документация и качество релизного состояния.

- [X] T035 [P] Добавить регрессионный тест сохранения поведения `full-scan`/`delta-after-commit` в `tests/integration/test_watch_mode_regression_existing_modes.py`
- [X] T036 Обновить пользовательскую документацию watch-режима и MCP endpoint в `README.md`
- [X] T037 [P] Обновить эксплуатационную документацию watch-настроек и диагностики в `docs/configuration.md`
- [X] T038 Исправить кодировку и перепроверить UTF-8 для feature quickstart в `specs/013-watch-mode-indexing/quickstart.md`
- [X] T039 Выполнить quality/stability suite для watch-режима через `scripts/tests/run_quality_stability_suite.ps1`

---

## Dependencies & Execution Order

- Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5 -> Phase 6
- User stories стартуют только после завершения Foundational phase.
- Внутри каждой user story сначала выполняются тестовые задачи, затем реализация.

## User Story Dependency Graph

- US1 -> US2 -> US3

## Parallel Execution Examples

### US1

- Параллельно запускать `T013`, `T014`, `T015` (разные тестовые файлы).
- После `T016` параллельно выполнять `T019` и `T020`.

### US2

- Параллельно запускать `T021`, `T022`, `T023`.
- После `T024` параллельно выполнять `T026` и `T027`.

### US3

- Параллельно запускать `T028` и `T029`.
- После `T030` параллельно выполнять `T033` и `T034`.

## Implementation Strategy

### MVP First (US1)

1. Завершить Phase 1 и Phase 2.
2. Реализовать Phase 3 (US1) и подтвердить автоиндексацию create/update/delete без ручного trigger.
3. Выпустить инкремент при готовности MVP.

### Incremental Delivery

1. Добавить Phase 4 (US2) для устойчивости watcher-а при burst и ошибках.
2. Добавить Phase 5 (US3) для полной операционной наблюдаемости через API.
3. Завершить Phase 6 с регрессией существующих режимов, документацией и quality-suite.

