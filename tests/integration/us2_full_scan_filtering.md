# US2 Integration: File Type and Exclude Filtering

## Goal

Подтвердить, что `INDEX_FILE_TYPES` и `INDEX_EXCLUDE_PATTERNS` влияют на итог
Full Scan предсказуемо.

## Preconditions

- Стек запущен.
- Подготовлены фикстуры `scripts/tests/full_scan_test_env.ps1`.

## Steps

1. Запустить Full Scan для директории фикстур.
2. Дождаться завершения и получить summary.
3. Проверить `skipBreakdown`.

## Expected Result

- В summary присутствует `UNSUPPORTED_TYPE` для неподдерживаемых расширений.
- В summary присутствует `EXCLUDED_BY_PATTERN` для файлов из исключенных путей.
- Поддерживаемые файлы остаются в обработке.

