# Research: MCP Transport Compatibility

## Decision 1: Поддерживать оба transport-режима: primary `POST /mcp` и fallback `GET /sse` + `POST /messages`

- Decision: Реализовать MCP transport в двух режимах: основной JSON-RPC endpoint `POST /mcp` и fallback для клиентов, ожидающих SSE-схему.
- Rationale: Это покрывает целевые клиенты (VS Code/Claude/Cline), снижает риск несовместимости при различиях реализаций transport в клиентах.
- Alternatives considered: 1) Только `POST /mcp`. Отклонено из-за рисков для legacy/SSE-клиентов. 2) Только SSE. Отклонено, т.к. часть клиентов ожидает streamable HTTP JSON-RPC.

## Decision 2: Добавить `/.well-known/mcp` как discovery endpoint

- Decision: Публиковать discovery-описание transport endpoint-ов и поддерживаемых capability.
- Rationale: Уменьшает ручную настройку URL в клиентах и делает on-boarding предсказуемым.
- Alternatives considered: 1) Не делать discovery. Отклонено из-за более высокого порога подключения. 2) Discovery только в документации. Отклонено как менее надежный runtime-сигнал.

## Decision 3: `tools/call` реализовать через адаптер к существующей бизнес-логике, а не через loopback REST calls

- Decision: MCP tool handlers вызывают внутренние сервисы (`SearchService`, ingestion/idempotency/delta state handlers) напрямую, не отправляя HTTP-запросы к своему же серверу.
- Rationale: Меньше накладных расходов, меньше точек отказа и единый контроль ошибок/таймаутов.
- Alternatives considered: 1) Вызывать existing `/v1/*` по HTTP внутри контейнера. Отклонено из-за лишней сложности и дублирования сетевого слоя.

## Decision 4: Унифицировать ошибки в JSON-RPC формате с маппингом текущих `errorCode`

- Decision: Любая ошибка MCP-методов возвращается в JSON-RPC `error` с консистентными code/message/data, где `data` содержит исходные `errorCode`, `details`, correlation fields.
- Rationale: Клиентам нужен машиночитаемый, стабильный формат для автоматического реагирования.
- Alternatives considered: 1) Возвращать только текстовые сообщения. Отклонено как непригодно для автоматизации.

## Decision 5: Минимальный обязательный набор MCP tools

- Decision: В MVP включить tools: `semantic_search`, `get_source_by_id`, `get_metadata_by_id`, `start_ingestion`, `get_ingestion_status`.
- Rationale: Это покрывает ключевые пользовательские сценарии из спецификации без раздувания объема первой итерации.
- Alternatives considered: 1) Включить сразу все текущие `/v1/indexing/*` и командный runtime. Отклонено для MVP: повышает риск регрессий и усложняет контракт.

## Decision 6: Контрактные и smoke-проверки MCP transport в CI как обязательный gate

- Decision: Добавить тесты handshake (`initialize`, `notifications/initialized`, `ping`), tools-list/call и негативные сценарии формата ошибок; отдельный smoke со стартом compose и проверкой MCP-клиентского сценария.
- Rationale: Протокольные регрессии быстро ломают интеграции клиентов, поэтому нужны явные gates.
- Alternatives considered: 1) Проверять только unit-уровень. Отклонено: не гарантирует end-to-end совместимость transport.

## Decision 7: Пустая/неинициализированная Qdrant-коллекция трактуется как "empty index" для MCP поиска

- Decision: При отсутствии коллекции поиск через MCP возвращает валидный пустой результат, а не backend fatal.
- Rationale: Новые проекты часто стартуют до первой ingestion; клиент должен получать предсказуемый ответ и не считать transport сломанным.
- Alternatives considered: 1) Возвращать backend error 5xx. Отклонено, т.к. это ухудшает UX и мешает автонастройке клиентов.

## Clarification Resolution

В техническом контексте не осталось `NEEDS CLARIFICATION`:
- transport strategy фиксирована (dual-mode);
- discovery strategy определена;
- минимальный набор tools и формат ошибок зафиксированы;
- тестовые gates и критерии совместимости определены.
