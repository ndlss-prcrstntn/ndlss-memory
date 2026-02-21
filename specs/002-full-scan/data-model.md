# Data Model: Режим Full Scan

## 1. ScanJob

Описание: жизненный цикл одного запуска полной индексации.

Поля:

- `job_id` (string, required): уникальный идентификатор задачи.
- `mode` (string, required): значение `full-scan`.
- `workspace_path` (string, required): корень обхода.
- `status` (string, required): `queued | running | completed | failed | cancelled`.
- `started_at` (datetime, optional): время старта.
- `finished_at` (datetime, optional): время завершения.
- `duration_seconds` (number, optional): длительность выполнения.
- `error_count` (integer, required): количество ошибок чтения.
- `skip_count` (integer, required): количество пропущенных файлов.
- `indexed_count` (integer, required): количество файлов, прошедших в индексацию.
- `processed_count` (integer, required): общее количество просмотренных файлов.

Валидация:

- `mode` фиксирован как `full-scan` для этого контракта.
- `processed_count >= indexed_count`.
- `finished_at` заполнен только для финальных статусов.

Переходы состояния:

- `queued -> running`
- `running -> completed`
- `running -> failed`
- `running -> cancelled`

## 2. FileCandidate

Описание: обнаруженный объект файловой системы, оцененный правилами Full Scan.

Поля:

- `path` (string, required): абсолютный или workspace-relative путь.
- `extension` (string, optional): расширение файла.
- `size_bytes` (integer, required): размер файла.
- `match_supported_type` (boolean, required): признак поддержки типа.
- `match_exclude_pattern` (boolean, required): признак совпадения с исключением.
- `size_limit_exceeded` (boolean, required): признак превышения лимита.
- `decision` (string, required): `index | skip`.
- `skip_reason` (string, optional): ссылка на классификатор причин.

Валидация:

- `decision = index` только если файл поддерживаемого типа, не исключен и не превышает лимит.
- `skip_reason` обязателен при `decision = skip`.

Связи:

- Много `FileCandidate` принадлежат одному `ScanJob`.

## 3. SkipReason

Описание: стандартизированная причина пропуска файла.

Поля:

- `code` (string, required):
  - `UNSUPPORTED_TYPE`
  - `EXCLUDED_BY_PATTERN`
  - `FILE_TOO_LARGE`
  - `READ_ERROR`
  - `EMPTY_FILE`
- `message` (string, required): человекочитаемое объяснение.
- `retryable` (boolean, required): можно ли повторить обработку позже.

Валидация:

- `code` должен принадлежать перечислению.
- `message` не пустой.

## 4. ScanProgress

Описание: моментальный снимок прогресса выполнения Full Scan.

Поля:

- `job_id` (string, required)
- `status` (string, required)
- `processed_count` (integer, required)
- `indexed_count` (integer, required)
- `skip_count` (integer, required)
- `error_count` (integer, required)
- `last_event_at` (datetime, required)
- `percent_complete` (number, optional)

Валидация:

- `last_event_at` обновляется при публикации прогресса.
- Между обновлениями прогресса интервал не превышает 60 секунд при `running`.

## 5. ScanSummary

Описание: итог задачи Full Scan.

Поля:

- `job_id` (string, required)
- `result` (string, required): `completed | failed | cancelled`
- `duration_seconds` (number, required)
- `totals` (object, required):
  - `processed_count`
  - `indexed_count`
  - `skip_count`
  - `error_count`
- `skip_breakdown` (array[SkipReasonAggregate], required)

Подсущность `SkipReasonAggregate`:

- `code` (string, required)
- `count` (integer, required)

Валидация:

- Сумма `skip_breakdown.count` равна `totals.skip_count`.
- `duration_seconds >= 0`.
