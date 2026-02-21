# Release checklist: 001-base-docker-compose

## Validation results (2026-02-21)

- [x] `docker compose -f infra/docker/docker-compose.yml --env-file .env.example config` проходит без ошибок.
- [x] Запуск контейнеров и проверка health (`scripts/tests/us1_compose_up_healthy.ps1`) проходит успешно.
- [x] Проверка переопределения env (`scripts/tests/us2_env_override.ps1`) проходит успешно.
- [x] Скрипт диагностики `scripts/ops/stack-status.ps1` возвращает `overallStatus: healthy`.
- [x] Контракт статуса синхронизирован между `specs/.../contracts` и `services/mcp-server/openapi`.
- [x] `.env.example` содержит обязательные параметры и ограничения безопасности.
- [x] Quickstart и troubleshooting обновлены.
- [x] Добавлен сценарий проверки персистентности Qdrant: `tests/integration/qdrant_persistence_cycle.md`.

## Follow-up

1. По необходимости выполнить `powershell -NoProfile -File scripts/dev/down.ps1` для остановки локального стека.
