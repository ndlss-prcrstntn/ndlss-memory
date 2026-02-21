# US1 Integration: Recursive Full Scan

## Goal

Проверить, что Full Scan рекурсивно обходит дерево файлов и обрабатывает
поддерживаемые типы.

## Preconditions

- Запущен стек Docker Compose.
- Подготовлены фикстуры: `powershell -File scripts/tests/full_scan_test_env.ps1`.

## Steps

1. Запустить задачу:
   - `POST /v1/indexing/full-scan/jobs` с `workspacePath`.
2. Дождаться финального статуса через:
   - `GET /v1/indexing/full-scan/jobs/{jobId}`.
3. Запросить итог:
   - `GET /v1/indexing/full-scan/jobs/{jobId}/summary`.

## Expected Result

- Задача завершена `completed`.
- `processedCount` > 0.
- `indexedCount` включает файлы из вложенных директорий.
- Ошибки запроса отсутствуют.

