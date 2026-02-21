# Regression Test: Delta-after-commit after Full Scan Changes

## Goal

Убедиться, что изменения Full Scan не ломают базовый сценарий режима
`delta-after-commit`.

## Preconditions

- Запущен compose-стек.
- `INDEX_MODE=delta-after-commit`.

## Steps

1. Перезапустить стек с `INDEX_MODE=delta-after-commit`.
2. Проверить `GET /v1/system/config`:
   - `indexMode == "delta-after-commit"`.
3. Запустить `GET /health` и `GET /v1/system/status`.

## Expected Result

- `mcp-server` и `file-indexer` остаются healthy.
- Конфигурация режима корректная.
- Full Scan API доступен и не влияет на стабильность режима `delta-after-commit`.

