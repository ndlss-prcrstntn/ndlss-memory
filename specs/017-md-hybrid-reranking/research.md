# Phase 0 Research: Reranking over Hybrid Docs Search (Markdown Only)

## Decision 1: Reranking strategy on top of hybrid candidates

- Decision: Применять reranking как второй этап ранжирования к фиксированному пулу top-N кандидатов, полученных после hybrid (BM25 + vector) этапа.
- Rationale: Это улучшает порядок top-выдачи без расширения области поиска и без изменения non-docs сценариев.
- Alternatives considered:
  - Полная замена hybrid ранжирования только reranking-этапом: отклонено, теряется устойчивость первичного candidate retrieval.
  - Reranking всех документов коллекции: отклонено из-за риска деградации latency.

## Decision 2: Scope boundary enforcement

- Decision: Reranking включается только для docs endpoint (`/v1/search/docs/query`) и связанного MCP инструмента `search_docs`.
- Rationale: Требование фичи прямо ограничивает область markdown-потоком и требует неизменности non-docs поведения.
- Alternatives considered:
  - Глобальный reranking для всех endpoint-ов: отклонено как нарушение scope.
  - Опциональный reranking-флаг в non-docs endpoint-ах: отклонено на этом этапе как избыточное расширение контракта.

## Decision 3: Fallback reliability policy

- Decision: При деградации reranking-этапа возвращать результаты первичного hybrid этапа с машиночитаемым индикатором fallback в метаданных ответа.
- Rationale: Пользователь получает полезный ответ без отказа, а система сохраняет наблюдаемость деградации.
- Alternatives considered:
  - Жестко завершать запрос ошибкой при любом сбое reranking: отклонено как ухудшение UX.
  - Тихо скрывать сбой без индикатора fallback: отклонено, усложняет диагностику.

## Decision 4: Deterministic ordering after reranking

- Decision: Для равных reranked score использовать стабильный tie-break: `documentPath`, затем `chunkIndex`.
- Rationale: Это обеспечивает повторяемость regression/contract проверок и предсказуемый пользовательский опыт.
- Alternatives considered:
  - Случайный tie-break: отклонено из-за нестабильности выдачи.
  - Tie-break по внутреннему id хранилища: отклонено как потенциально нестабильное между перезапусками.

## Decision 5: Error semantics and compatibility

- Decision: Сохранить действующие error-коды для валидации запроса, добавить явный код деградации reranking только при полном отказе fallback-механизма.
- Rationale: Это минимизирует breaking changes и поддерживает существующие интеграции.
- Alternatives considered:
  - Ввести новую обязательную схему ошибок для всех search endpoint-ов: отклонено как ненужное расширение scope.

## Decision 6: Quality acceptance metrics

- Decision: Для приемки использовать три группы метрик: качество (top-3 relevance hit), производительность (p95 latency), стабильность (repeatability/fallback success).
- Rationale: Метрики напрямую соотносятся с success criteria и позволяют объективную проверку value фичи.
- Alternatives considered:
  - Оценка только по latency: отклонено, не отражает качество ранжирования.
  - Оценка только экспертным review выдачи: отклонено, трудно автоматизировать и воспроизводить.
