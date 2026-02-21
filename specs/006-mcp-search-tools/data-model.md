# Data Model: MCP-инструменты поиска

## 1. SearchQuery

Описание: входная модель semantic search запроса.

Поля:

- `query_text` (string, required): поисковая фраза пользователя.
- `limit` (integer, optional): максимальное число результатов.
- `path_filter` (string, optional): точный путь файла.
- `folder_filter` (string, optional): фильтр по папке.
- `file_type_filter` (string, optional): фильтр по типу файла (например, `.md`).
- `requested_at` (datetime, required)

Валидация:

- `query_text` не пустой после trim.
- `limit` > 0 при передаче.
- `path_filter`, `folder_filter`, `file_type_filter` могут использоваться совместно.

## 2. SearchResult

Описание: единица выдачи semantic search.

Поля:

- `result_id` (string, required): стабильный идентификатор результата.
- `score` (number, required): оценка релевантности.
- `snippet` (string, required): фрагмент контента.
- `source_path` (string, required): путь к источнику.
- `file_type` (string, required)
- `metadata_ref` (string, required): ссылка/ключ на метаданные.

Валидация:

- `result_id` уникален в рамках ответа.
- `score` в допустимом диапазоне ранжирования системы.

## 3. DocumentSource

Описание: источник контента, запрашиваемый по `result_id`.

Поля:

- `result_id` (string, required)
- `content` (string, required)
- `source_path` (string, required)
- `chunk_index` (integer, optional)
- `retrieved_at` (datetime, required)

Валидация:

- Для валидного `result_id` возвращается не пустой `content`.

## 4. DocumentMetadata

Описание: метаданные документа, запрашиваемые по `result_id`.

Поля:

- `result_id` (string, required)
- `file_name` (string, required)
- `file_type` (string, required)
- `source_path` (string, required)
- `content_hash` (string, optional)
- `indexed_at` (datetime, optional)

Валидация:

- Для валидного `result_id` обязательны `file_name`, `file_type`, `source_path`.

## 5. SearchResponseEnvelope

Описание: стандартный формат ответа search-tools.

Поля:

- `status` (string, required): `ok | empty | error`.
- `results` (array[SearchResult], optional)
- `source` (DocumentSource, optional)
- `metadata` (DocumentMetadata, optional)
- `error` (object, optional): `{code, message, details?}`
- `meta` (object, required): служебные поля ответа (время, limit, count).

Валидация:

- `status=empty` допускает пустой `results` и не требует `error`.
- `status=error` требует непустой `error.code`.
- `status=ok` требует соответствующий полезный payload (`results` или `source`/`metadata`).
