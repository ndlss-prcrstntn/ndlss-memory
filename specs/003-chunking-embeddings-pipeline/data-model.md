# Data Model: Пайплайн чанкинга и эмбеддингов

## 1. ChunkingConfig

Описание: runtime-конфигурация разбиения контента.

Поля:

- `chunk_size` (integer, required): размер чанка.
- `chunk_overlap` (integer, required): overlap соседних чанков.
- `max_chunks_per_file` (integer, optional): ограничение числа чанков на файл.
- `retry_max_attempts` (integer, required): лимит retry для эмбеддингов.
- `retry_backoff_seconds` (number, required): пауза между retry.

Валидация:

- `chunk_size >= 1`
- `chunk_overlap >= 0`
- `chunk_overlap < chunk_size`
- `retry_max_attempts >= 1`
- `retry_backoff_seconds > 0`

## 2. ChunkRecord

Описание: результат чанкинга одного фрагмента файла.

Поля:

- `chunk_id` (string, required): детерминированный идентификатор чанка.
- `file_path` (string, required)
- `file_name` (string, required)
- `file_type` (string, required)
- `chunk_index` (integer, required): порядковый номер чанка в файле.
- `content` (string, required): текст чанка.
- `content_hash` (string, required): hash полного контента файла.
- `processed_at` (datetime, required): timestamp обработки.

Валидация:

- `chunk_index >= 0`
- `content` не пустой для успешного чанка.

Связи:

- Один файл имеет много `ChunkRecord`.

## 3. EmbeddingTask

Описание: выполнение генерации эмбеддинга для конкретного чанка.

Поля:

- `task_id` (string, required)
- `chunk_id` (string, required)
- `status` (string, required): `queued | running | success | failed`
- `attempt_count` (integer, required)
- `last_error_code` (string, optional)
- `last_error_message` (string, optional)
- `started_at` (datetime, optional)
- `finished_at` (datetime, optional)

Валидация:

- `attempt_count >= 0`
- `attempt_count <= retry_max_attempts`
- `finished_at` обязателен для `success|failed`.

Переходы состояния:

- `queued -> running`
- `running -> success`
- `running -> failed`
- `failed -> running` (retry)

## 4. VectorRecord

Описание: сохраненная запись в векторном хранилище.

Поля:

- `vector_id` (string, required): ключ upsert.
- `chunk_id` (string, required)
- `embedding` (array[number], required)
- `metadata` (object, required):
  - `file_path`
  - `file_name`
  - `file_type`
  - `content_hash`
  - `timestamp`

Валидация:

- `embedding` имеет фиксированную размерность для выбранной модели.
- `vector_id` стабилен для одного и того же chunk source.

## 5. IngestionRunSummary

Описание: агрегированный итог одного запуска ingestion.

Поля:

- `run_id` (string, required)
- `status` (string, required): `completed | failed | partial`
- `total_files` (integer, required)
- `total_chunks` (integer, required)
- `embedded_chunks` (integer, required)
- `failed_chunks` (integer, required)
- `retry_count` (integer, required)
- `started_at` (datetime, required)
- `finished_at` (datetime, required)

Валидация:

- `embedded_chunks + failed_chunks <= total_chunks`
- `finished_at >= started_at`

Связи:

- Один `IngestionRunSummary` агрегирует много `EmbeddingTask` и `VectorRecord`.
