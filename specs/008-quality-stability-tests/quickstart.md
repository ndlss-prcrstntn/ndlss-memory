# Quickstart: Качество и стабильность

## Цель

Проверить, что quality-gates для `ndlss-memory` воспроизводимы и покрывают unit, integration, contract и E2E сценарии, включая идемпотентность повторного запуска.

## Prerequisites

- Docker Engine + Docker Compose v2
- Python окружение с `pytest`
- Доступ к репозиторию `Z:\WORK\ndlss-memory`

## 1. Поднять стек

```powershell
Set-Location Z:\WORK\ndlss-memory
powershell -File scripts/dev/up.ps1
```

Ожидаемый результат: сервисы `qdrant`, `file-indexer`, `mcp-server` в состоянии healthy.

## 2. Запустить unit-проверки

```powershell
.\.venv\Scripts\python.exe -m pytest tests/unit/file_indexer
.\.venv\Scripts\python.exe -m pytest tests/unit/mcp_server
```

Ожидаемый результат: PASS по чанкингу, хешированию, фильтрации и поисковой/командной логике MCP.

## 3. Запустить quality suite

```powershell
powershell -File scripts/tests/run_quality_stability_suite.ps1
```

Ожидаемый результат: формируется `tests/artifacts/quality-stability/quality-run-report.json`
со статусом `passed`.

## 4. Запустить integration-сценарии по отдельности

```powershell
powershell -File scripts/tests/full_scan_compose_regression.ps1
powershell -File scripts/tests/delta_after_commit_compose_regression.ps1
powershell -File scripts/tests/idempotency_compose_regression.ps1
powershell -File scripts/tests/ingestion_compose_regression.ps1
```

Ожидаемый результат: корректная запись в Qdrant, поиск через MCP и стабильные summary endpoint-ы.

## 5. Проверить контракты quality-run

```powershell
powershell -File scripts/tests/contract_quality_stability.ps1
Get-Content tests/artifacts/quality-stability/contract-check-summary.md
```

Ожидаемый результат: contract summary содержит `failed: 0`.

## 6. Выполнить E2E smoke

```powershell
powershell -File scripts/tests/quality_stability_e2e.ps1
```

Ожидаемый результат: создается `tests/artifacts/quality-stability/us3-e2e-summary.json` с флагами всех этапов.

## 7. Проверка идемпотентности повторного запуска

```powershell
powershell -File scripts/tests/us1_idempotent_repeat_run.ps1
powershell -File scripts/tests/us1_idempotent_repeat_run.ps1
Get-Content tests/artifacts/quality-stability/us1-idempotency-summary.json
```

Ожидаемый результат: повторный прогон не увеличивает `failedChunks` и `duplicateCount`.

## 8. Проверка кодировки Markdown

```powershell
powershell -File scripts/tests/validate_markdown_encoding.ps1
```

Ожидаемый результат: скрипт завершает работу с кодом 0.

## 9. Остановка стека

```powershell
powershell -File scripts/dev/down.ps1
```
