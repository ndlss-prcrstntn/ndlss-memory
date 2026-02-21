# Integration Test: Full Scan Idempotency Cycle

## Goal

Проверить, что повторный запуск Full Scan на неизмененном наборе файлов дает
стабильную статистику без непредсказуемого роста ошибок/пропусков.

## Preconditions

- Подготовлены фикстуры Full Scan.
- Стек запущен.

## Steps

1. Запустить Full Scan (run #1) и сохранить summary.
2. Без изменений файлов запустить Full Scan (run #2).
3. Сравнить `totals` и `skipBreakdown`.

## Expected Result

- Статистика run #2 находится в ожидаемом диапазоне run #1.
- Нет регрессии по ошибкам чтения.
- API стабильно возвращает summary для обоих запусков.

