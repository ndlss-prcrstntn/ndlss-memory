# Integration: Command Resource & Workspace Isolation

## Goal

Проверить изоляцию рабочей директории и ограничение ресурсов выполнения.

## Steps

1. Вызов с `workingDirectory=/workspace`:
   - Ожидание: команда выполняется.
2. Вызов с `workingDirectory=/etc`:
   - Ожидание: отклонение, `WORKSPACE_ISOLATION_VIOLATION`.
3. Вызов ресурсоемкой команды (или длительной):
   - Ожидание: выполнение ограничивается политикой timeout/limits.
4. Проверить, что после завершения нет зависших дочерних процессов по этому requestId.
