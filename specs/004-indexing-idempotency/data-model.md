# Data Model: Идемпотентность индексации

## 1. FileFingerprint

Описание: текущий и предыдущий отпечаток файла для решения о пропуске,
обновлении или удалении записей.

Поля:

- `file_path` (string, required): относительный путь файла в workspace.
- `content_hash` (string, required): SHA256 хеш текущей версии контента.
- `previous_hash` (string, optional): хеш из последней успешной синхронизации.
- `status` (string, required): `new | unchanged | changed | deleted | failed`.
- `detected_at` (datetime, required): время вычисления fingerprint.

Валидация:

- `content_hash` должен быть 64-символьной hex-строкой для non-deleted статуса.
- `status=deleted` допускает пустой `content_hash`.

## 2. ChunkIdentity

Описание: детерминированная идентичность чанка в контексте версии файла.

Поля:

- `chunk_id` (string, required): deterministic ID.
- `file_path` (string, required)
- `file_hash` (string, required)
- `chunk_index` (integer, required)
- `chunk_text_hash` (string, required)

Валидация:

- `chunk_index >= 0`.
- `chunk_id` уникален в рамках коллекции.

Связи:

- Один `FileFingerprint` (`status != deleted`) имеет много `ChunkIdentity`.

## 3. ChunkSyncResult

Описание: результат синхронизации для отдельного чанка.

Поля:

- `chunk_id` (string, required)
- `operation` (string, required): `updated | skipped | deleted | failed`.
- `reason_code` (string, required): машиночитаемый код причины.
- `message` (string, optional)
- `processed_at` (datetime, required)

Валидация:

- `reason_code` обязателен для всех операций, включая успех (`UPDATED`, `SKIPPED_UNCHANGED`, `DELETED_STALE`, ...).

Переходы состояния:

- `planned -> updated`
- `planned -> skipped`
- `planned -> deleted`
- `planned -> failed`

## 4. StaleChunkSet

Описание: множество chunk IDs, которые существовали ранее, но отсутствуют в
актуальной версии файла.

Поля:

- `file_path` (string, required)
- `obsolete_chunk_ids` (array[string], required)
- `computed_from_hash` (string, required)

Валидация:

- `obsolete_chunk_ids` не содержит дубликатов.

## 5. IndexSyncSummary

Описание: агрегированный итог запуска идемпотентной синхронизации.

Поля:

- `run_id` (string, required)
- `status` (string, required): `completed | partial | failed`
- `total_files` (integer, required)
- `updated_chunks` (integer, required)
- `skipped_chunks` (integer, required)
- `deleted_chunks` (integer, required)
- `failed_chunks` (integer, required)
- `started_at` (datetime, required)
- `finished_at` (datetime, required)

Валидация:

- `updated_chunks + skipped_chunks + deleted_chunks + failed_chunks >= 0`.
- `finished_at >= started_at`.

Связи:

- Один `IndexSyncSummary` агрегирует множество `ChunkSyncResult`.
