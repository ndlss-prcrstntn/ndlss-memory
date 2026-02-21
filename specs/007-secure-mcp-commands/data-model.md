# Data Model: Безопасный запуск команд через MCP

## 1. CommandExecutionRequest

Описание: входная модель запуска команды через MCP.

Поля:

- `request_id` (string, required): уникальный идентификатор вызова.
- `command` (string, required): имя команды из allowlist.
- `args` (array[string], optional): аргументы команды.
- `working_directory` (string, required): путь запуска внутри разрешенного workspace.
- `requested_timeout_seconds` (integer, optional): запрошенный timeout.
- `requested_at` (datetime, required)
- `caller_id` (string, optional)

Валидация:

- `command` не пустая и присутствует в allowlist.
- `working_directory` после нормализации находится внутри корня workspace.
- `requested_timeout_seconds` > 0 и не превышает policy-лимит.

## 2. CommandPolicy

Описание: активная политика безопасности для выполнения команд.

Поля:

- `allowlist` (array[string], required)
- `timeout_seconds` (integer, required)
- `cpu_limit` (string, required)
- `memory_limit` (string, required)
- `run_as_non_root` (boolean, required)
- `workspace_root` (string, required)
- `audit_retention_days` (integer, required)

Валидация:

- `allowlist` содержит только непустые уникальные команды.
- `timeout_seconds` > 0.
- `audit_retention_days` >= 1.

## 3. CommandExecutionResult

Описание: итог выполнения команды.

Поля:

- `request_id` (string, required)
- `status` (enum, required): `ok | rejected | timeout | failed`
- `exit_code` (integer, optional)
- `stdout` (string, optional)
- `stderr` (string, optional)
- `error_code` (string, optional)
- `error_message` (string, optional)
- `duration_ms` (integer, required)
- `started_at` (datetime, required)
- `finished_at` (datetime, required)

Валидация:

- `status=rejected` требует `error_code`.
- `status=timeout` требует `error_code=COMMAND_TIMEOUT`.
- `status=ok` допускает `exit_code=0`.

## 4. CommandAuditRecord

Описание: запись аудита по вызову команды.

Поля:

- `audit_id` (string, required)
- `request_id` (string, required)
- `timestamp` (datetime, required)
- `command` (string, required)
- `arguments` (array[string], optional)
- `working_directory` (string, required)
- `status` (string, required)
- `error_code` (string, optional)
- `policy_snapshot` (object, required)

Валидация:

- `request_id` обязателен для трассировки.
- `status` должен совпадать со статусом `CommandExecutionResult`.

## State Transitions

- `CommandExecutionRequest`: `received -> validated -> dispatched -> completed`.
- `CommandExecutionResult`: `pending -> ok | rejected | timeout | failed`.
- `CommandAuditRecord`: создается при любом terminal-состоянии результата.
