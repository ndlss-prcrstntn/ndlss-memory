# Startup Preflight Readiness Integration

## Purpose

Проверить startup preflight, ready summary и обратную совместимость API.

## Scenario A: Ready Path

1. Запустить `docker compose up -d`.
2. Проверить `GET /health` -> `200`.
3. Проверить `GET /v1/system/startup/readiness` -> `200`.
4. Убедиться, что ответ содержит обязательные поля ready summary.
5. Проверить наличие startup-ready записи в логах `mcp-server` и `file-indexer`:
   - `event=startup-ready` в логе `mcp-server`;
   - `startup-ready summary service=file-indexer ...` в логе `file-indexer`.

## Scenario B: Qdrant Fail-Fast

1. Запустить `mcp-server` c некорректным `QDRANT_HOST`.
2. Убедиться, что процесс не переходит в ready-состояние.
3. Проверить структурированную startup-ошибку:
   - `errorCode=STARTUP_PREFLIGHT_FAILED`
   - `failedChecks[*].checkId` содержит `qdrant_reachability`
   - `failedChecks[*].errorCode` содержит `PREFLIGHT_QDRANT_UNREACHABLE`.

## Scenario C: Workspace Fail-Fast

1. Передать невалидный `WORKSPACE_PATH`.
2. Убедиться, что preflight завершается ошибкой до запуска рабочих задач:
   - `errorCode=STARTUP_PREFLIGHT_FAILED`
   - `failedChecks[*].errorCode` содержит `PREFLIGHT_WORKSPACE_NOT_FOUND` или `PREFLIGHT_WORKSPACE_NOT_READABLE`.

## Scenario D: Git Required in Delta Mode

1. Включить `INDEX_MODE=delta-after-commit`.
2. Удалить git из PATH контейнера/использовать образ без git.
3. Проверить fail-fast с кодом ошибки проверки git:
   - `errorCode=STARTUP_PREFLIGHT_FAILED`
   - `failedChecks[*].errorCode` содержит `PREFLIGHT_GIT_NOT_AVAILABLE` или `PREFLIGHT_GIT_REPOSITORY_REQUIRED`.

## Scenario E: Backward Compatibility

1. В ready-сценарии проверить существующие endpoint:
   - `/v1/system/status`
   - `/v1/system/config`
   - `/v1/search/semantic`
2. Убедиться, что контракт не сломан (добавление полей допустимо).
3. Повторить запуск как минимум на `deploy/compose/generic.yml` и
   `deploy/compose-images/generic.yml` с одинаковыми результатами по endpoint.
