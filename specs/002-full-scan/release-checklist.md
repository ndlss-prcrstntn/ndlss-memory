# Release checklist: 002-full-scan

## Validation results (2026-02-21)

- [x] `docker compose -f infra/docker/docker-compose.yml --env-file .env.example config` проходит без ошибок.
- [x] Контракт Full Scan синхронизирован:
  - `specs/002-full-scan/contracts/full-scan-indexing.openapi.yaml`
  - `services/mcp-server/openapi/full-scan-indexing.openapi.yaml`
- [x] Добавлены сценарии US1-US3 для full-scan в `tests/integration/` и `tests/contract/`.
- [x] Добавлены скрипты регрессии и smoke-проверок Full Scan в `scripts/tests/`.
- [x] Обновлены env-параметры и документация конфигурации (`.env.example`, `docs/configuration.md`).
- [x] Обновлен troubleshooting и roadmap-статусы в `README.md`.
- [x] Quickstart синхронизирован с текущими endpoint Full Scan.

## Follow-up

1. Установить `pytest` в среде разработки для запуска unit-тестов Python.
2. Прогнать `scripts/tests/full_scan_compose_regression.ps1` на чистом окружении.

