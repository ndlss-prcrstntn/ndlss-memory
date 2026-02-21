# US3 Integration: Resilience and Summary

## Goal

Проверить, что Full Scan устойчив к ошибкам чтения и ограничениям размера, не
падает целиком и возвращает корректный summary.

## Preconditions

- Запущен стек.
- Подготовлены фикстуры.

## Steps

1. Запустить Full Scan с низким лимитом размера файла.
2. Получить прогресс до завершения.
3. Запросить summary после завершения.

## Expected Result

- Задача достигает состояния `completed` или контролируемого `failed` с ошибкой.
- `skipBreakdown` содержит минимум `FILE_TOO_LARGE` для oversized файла.
- Endpoint summary возвращает машиночитаемую структуру с totals и skipBreakdown.

