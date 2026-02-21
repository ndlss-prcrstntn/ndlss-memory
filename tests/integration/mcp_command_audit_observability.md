# Integration: Command Audit & Observability

## Goal

Проверить наблюдаемость вызовов secure command runtime.

## Steps

1. Выполнить один успешный вызов и один отклоненный вызов команды.
2. Запросить `GET /v1/commands/audit?limit=50`.
3. Проверить, что обе записи присутствуют с полями:
   - `requestId`, `timestamp`, `command`, `status`.
4. Применить фильтр `status=rejected` и проверить, что выдача содержит только отклоненные вызовы.
5. Убедиться, что коды ошибок в API-ответах совпадают с кодами в аудите.
