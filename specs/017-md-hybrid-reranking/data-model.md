# Data Model: Reranking over Hybrid Docs Search (Markdown Only)

## Entity: HybridCandidateSet

- Purpose: Набор кандидатов, сформированный первичным hybrid этапом для docs-search.

### Fields

- `query` (string, required)
- `collectionScope` (string, required)
  - Allowed value: `docs_markdown`.
- `candidateCount` (integer, required)
  - Validation: `>= 0`.
- `items` (array[HybridCandidateItem], required)

## Entity: HybridCandidateItem

- Purpose: Элемент candidate-set до reranking.

### Fields

- `documentPath` (string, required)
  - Validation: нормализованный относительный markdown-путь.
- `chunkIndex` (integer, required)
  - Validation: `>= 0`.
- `snippet` (string, required)
- `hybridScore` (number, required)
  - Validation: `>= 0`.
- `signals` (object, required)
  - `lexical` (number, `>= 0`)
  - `semantic` (number, `>= 0`)

## Entity: RerankingPolicy

- Purpose: Политика работы reranking этапа.

### Fields

- `enabled` (boolean, required)
- `scope` (string, required)
  - Allowed value: `docs_markdown_only`.
- `candidateLimit` (integer, required)
  - Validation: `>= 1`.
- `fallbackMode` (string, required)
  - Allowed values: `return_hybrid_candidates`, `error_on_total_failure`.
- `tieBreakRule` (string, required)
  - Allowed value: `documentPath_then_chunkIndex`.

## Entity: RerankedResultItem

- Purpose: Финальный элемент выдачи после reranking.

### Fields

- `documentPath` (string, required)
- `chunkIndex` (integer, required)
- `snippet` (string, required)
- `score` (number, required)
  - Meaning: итоговый reranked score.
- `sourceType` (string, required)
  - Allowed value: `documentation`.
- `rankingSignals` (object, required)
  - `lexical` (number, `>= 0`)
  - `semantic` (number, `>= 0`)
  - `rerank` (number, `>= 0`)

## Entity: DocsRerankedSearchResponse

- Purpose: Ответ docs-search endpoint после reranking этапа.

### Fields

- `query` (string, required)
- `total` (integer, required)
  - Validation: `>= 0`.
- `appliedStrategy` (string, required)
  - Allowed value: `bm25_plus_vector_rerank_docs_only`.
- `fallbackApplied` (boolean, required)
- `results` (array[RerankedResultItem], required)

## Entity: SearchError

- Purpose: Машиночитаемая ошибка docs-search контракта.

### Fields

- `errorCode` (string, required)
  - Allowed values: `INVALID_REQUEST`, `SEARCH_QUERY_EMPTY`, `DOCS_COLLECTION_UNAVAILABLE`, `DOCS_RERANKING_UNAVAILABLE`, `INTERNAL_ERROR`.
- `message` (string, required)
- `details` (object, optional)

## Relationships

- `HybridCandidateSet` 1:many `HybridCandidateItem`.
- `HybridCandidateSet` 1:1 `RerankingPolicy`.
- `DocsRerankedSearchResponse` 1:many `RerankedResultItem`.

## Validation Rules

- Reranking применяется только при `collectionScope=docs_markdown`.
- При `fallbackApplied=true` результаты формируются из hybrid candidate-set без потери контрактной структуры ответа.
- Для одинакового состояния данных и запроса порядок равных score стабилизируется tie-break правилом.
- Non-docs search ответы не включают поля reranking стратегии.

## State Transitions

### Docs Search Pipeline Lifecycle

- `received` -> `validated`
  - Условие: входные параметры запроса валидны.
- `validated` -> `hybrid_selected`
  - Условие: сформирован candidate-set первичного hybrid этапа.
- `hybrid_selected` -> `reranked`
  - Условие: reranking выполнен успешно.
- `hybrid_selected` -> `fallback_returned`
  - Условие: reranking недоступен, fallback применен.
- `reranked|fallback_returned` -> `returned`
  - Условие: ответ сформирован в контрактной форме.
- `received|validated` -> `rejected`
  - Условие: невалидный запрос.

## Derived Invariants

- В `results` всегда `sourceType=documentation`.
- `appliedStrategy` соответствует docs-only reranking режиму.
- При `fallbackApplied=false` каждый результат содержит ненулевую `rankingSignals.rerank` для кандидатов reranking этапа.
- При `fallbackApplied=true` ответ остается валидным и детерминированным.
