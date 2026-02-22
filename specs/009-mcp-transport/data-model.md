# Data Model: MCP Transport Compatibility

## Entity: McpSession

- Description: Логическая сессия MCP-клиента на transport-уровне.
- Fields:
  - `sessionId` (string, required): уникальный идентификатор сессии.
  - `transport` (enum, required): `streamable-http | sse`.
  - `state` (enum, required): `created | initialized | closed | expired`.
  - `clientName` (string, optional): имя клиента из `initialize`.
  - `clientVersion` (string, optional): версия клиента из `initialize`.
  - `createdAt` (datetime, required): время создания.
  - `lastActivityAt` (datetime, required): время последнего запроса/события.
  - `expiresAt` (datetime, optional): TTL сессии.
- Validation Rules:
  - `sessionId` обязателен и уникален в активном наборе.
  - `lastActivityAt >= createdAt`.
  - `state=initialized` допускается только после успешного `initialize`.

## Entity: McpRequestEnvelope

- Description: JSON-RPC запрос, принятый transport endpoint-ом.
- Fields:
  - `requestId` (string|number|null, required): JSON-RPC id.
  - `method` (string, required): имя MCP-метода.
  - `params` (object, optional): параметры метода.
  - `sessionId` (string, optional): связанная MCP-сессия.
  - `receivedAt` (datetime, required): время приема.
- Validation Rules:
  - `method` не пустой.
  - Для `tools/call` обязателен `params.name` и объект `params.arguments`.
  - Для `notifications/initialized` допустим `requestId=null`.

## Entity: McpToolDefinition

- Description: Объявление инструмента, возвращаемого через `tools/list`.
- Fields:
  - `name` (string, required): уникальное имя tool.
  - `description` (string, required): пользовательское описание.
  - `inputSchema` (object, required): схема входных параметров.
  - `outputSchema` (object, required): схема результата.
  - `version` (string, required): версия контракта инструмента.
  - `enabled` (boolean, required): доступность инструмента.
- Validation Rules:
  - `name` уникален в каталоге.
  - `inputSchema` и `outputSchema` валидны как JSON schema object.

## Entity: McpToolInvocation

- Description: Факт выполнения `tools/call`.
- Fields:
  - `invocationId` (string, required): уникальный id вызова.
  - `sessionId` (string, required): ссылка на `McpSession`.
  - `requestId` (string|number|null, required): JSON-RPC id запроса.
  - `toolName` (string, required): имя инструмента.
  - `arguments` (object, required): параметры вызова.
  - `status` (enum, required): `ok | error`.
  - `result` (object, optional): полезная нагрузка успешного ответа.
  - `error` (object, optional): JSON-RPC ошибка (`code`, `message`, `data`).
  - `startedAt` (datetime, required): время старта.
  - `finishedAt` (datetime, required): время завершения.
  - `durationMs` (integer, required): длительность.
- Validation Rules:
  - `status=ok` требует `result` и запрещает `error`.
  - `status=error` требует `error`.
  - `durationMs >= 0`.

## Entity: McpErrorMapping

- Description: Нормализация внутренних ошибок в JSON-RPC формат.
- Fields:
  - `internalCode` (string, required): внутренний `errorCode` сервиса.
  - `jsonRpcCode` (integer, required): код JSON-RPC/MCP ошибки.
  - `messageTemplate` (string, required): стабильный шаблон сообщения.
  - `retryable` (boolean, required): можно ли повторять вызов автоматически.
  - `dataSchema` (object, required): структура поля `error.data`.
- Validation Rules:
  - `internalCode` уникален в таблице маппинга.
  - `jsonRpcCode` входит в допустимый диапазон JSON-RPC/MCP.

## Relationships

- `McpSession` 1 -> N `McpRequestEnvelope`.
- `McpSession` 1 -> N `McpToolInvocation`.
- `McpToolDefinition` 1 -> N `McpToolInvocation` (по `toolName`).
- `McpErrorMapping` применяется к `McpToolInvocation.error` при `status=error`.

## State Transitions

### McpSession

- `created -> initialized`: успешный `initialize`.
- `initialized -> closed`: клиент закрыл соединение.
- `initialized -> expired`: истечение TTL без активности.
- `closed|expired` являются terminal-state.

### McpToolInvocation

- `ok`/`error` формируются только после получения результата обработки.
- Повторный вызов с тем же `requestId` в активной сессии должен быть idempotent или явно помечаться как duplicate request.
