# Data Model: Hybrid Search for Markdown Collection

## Entity: HybridDocsSearchRequest

- Purpose: Представляет входной запрос на гибридный поиск по markdown-коллекции.

### Fields

- `query` (string, required)
  - Validation: непустая строка после `trim`.
- `limit` (integer, optional)
  - Validation: `1..50`, default `10`.
- `workspacePath` (string, optional)
  - Validation: путь в пределах доступного workspace.

## Entity: CollectionScopeRule

- Purpose: Фиксирует правило применения гибридного режима только для docs-поиска.

### Fields

- `scopeName` (string, required)
  - Allowed value: `docs`.
- `collectionName` (string, required)
  - Example: `workspace_docs_chunks`.
- `hybridEnabled` (boolean, required)
  - Allowed value for this feature: `true`.
- `nonDocsBehavior` (string, required)
  - Allowed value: `unchanged`.

## Entity: HybridCandidate

- Purpose: Описывает кандидата выдачи до финального ранжирования.

### Fields

- `documentPath` (string, required)
  - Validation: нормализованный относительный путь markdown-документа.
- `chunkIndex` (integer, required)
  - Validation: `>= 0`.
- `snippet` (string, required)
  - Validation: непустой текстовый фрагмент.
- `lexicalScore` (number, required)
  - Validation: `>= 0`.
- `vectorScore` (number, required)
  - Validation: `>= 0`.
- `hybridScore` (number, required)
  - Validation: вычисляется детерминированно из lexical/vector сигналов.

## Entity: HybridDocsSearchResultItem

- Purpose: Элемент итоговой выдачи гибридного docs-search.

### Fields

- `documentPath` (string, required)
- `chunkIndex` (integer, required)
- `snippet` (string, required)
- `score` (number, required)
  - Meaning: итоговый hybrid score.
- `sourceType` (string, required)
  - Allowed value: `documentation`.
- `rankingSignals` (object, required)
  - `lexical` (number, `>= 0`)
  - `semantic` (number, `>= 0`)

## Entity: HybridDocsSearchResponse

- Purpose: Итоговый ответ API для docs hybrid search.

### Fields

- `query` (string, required)
- `total` (integer, required)
  - Validation: `>= 0`.
- `results` (array[HybridDocsSearchResultItem], required)
- `appliedStrategy` (string, required)
  - Allowed value: `bm25_plus_vector_docs_only`.

## Entity: SearchError

- Purpose: Машиночитаемая ошибка для docs-search контракта.

### Fields

- `errorCode` (string, required)
  - Allowed values: `INVALID_REQUEST`, `SEARCH_QUERY_EMPTY`, `DOCS_COLLECTION_UNAVAILABLE`, `INTERNAL_ERROR`.
- `message` (string, required)
- `details` (object, optional)

## Relationships

- `HybridDocsSearchRequest` 1:1 `HybridDocsSearchResponse`.
- `HybridDocsSearchResponse` 1:many `HybridDocsSearchResultItem`.
- `CollectionScopeRule` ограничивает формирование `HybridCandidate` только docs-коллекцией.

## Validation Rules

- Для валидного запроса `query` не может быть пустым после `trim`.
- Все результаты в ответе должны иметь `sourceType=documentation`.
- В non-docs потоках гибридная логика не применяется.
- Для неизменных данных одинаковый запрос дает стабильный порядок top-k.

## State Transitions

### Hybrid Docs Search Request Lifecycle

- `received` -> `validated`
  - Условие: `query` и `limit` прошли валидацию.
- `validated` -> `retrieved`
  - Условие: получен пул кандидатов из markdown-коллекции.
- `retrieved` -> `ranked`
  - Условие: рассчитан итоговый hybrid score и применен tie-break.
- `ranked` -> `returned`
  - Условие: сформирован ответ с `total` и `results`.
- `received` -> `rejected`
  - Условие: невалидный ввод (например, пустой `query`).

## Derived Invariants

- В выдаче hybrid docs-search отсутствуют элементы из non-markdown коллекций.
- `appliedStrategy` в успешном ответе всегда отражает docs-only hybrid режим.
- Для одинакового состояния индекса порядок равных score стабилизируется `documentPath + chunkIndex`.
