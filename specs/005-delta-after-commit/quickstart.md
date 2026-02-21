# Quickstart: Delta-after-commit режим

## Цель

Проверить, что режим `delta-after-commit` индексирует только измененные файлы,
корректно обрабатывает удаление/rename и автоматически уходит в `full-scan`
при ошибке получения Git diff.

## Требования

- Docker Engine / Docker Desktop
- Docker Compose v2
- Git-репозиторий с тестовыми файлами в workspace

## Подготовка

1. Поднимите стек:

```bash
docker compose -f Z:\WORK\ndlss-memory\infra\docker\docker-compose.yml --env-file Z:\WORK\ndlss-memory\.env.example up -d --build
```

2. Проверьте здоровье сервисов:

```bash
curl http://localhost:8080/health
pwsh Z:\WORK\ndlss-memory\scripts\ops\stack-status.ps1
```

3. Убедитесь, что установлен режим:

- `INDEX_MODE=delta-after-commit`
- корректен `HOST_WORKSPACE_PATH`

## Сценарий 1: Добавленные и измененные файлы

1. Подготовьте базовую ревизию и внесите изменения (`A`, `M`).
2. Запустите delta job:

```bash
curl -X POST http://localhost:8080/v1/indexing/delta-after-commit/jobs \
  -H "Content-Type: application/json" \
  -d '{"baseRef":"HEAD~1","targetRef":"HEAD"}'
```

3. Получите статус:

```bash
curl http://localhost:8080/v1/indexing/delta-after-commit/jobs/<runId>
```

Ожидание:

- `effectiveMode=delta-after-commit`
- `addedFiles`/`modifiedFiles` отражают реальные изменения
- `indexedFiles` > 0 для затронутых файлов

Автоматизированный прогон:

```powershell
pwsh scripts/tests/us1_delta_changed_only.ps1
```

## Сценарий 2: Удаление и rename

1. Удалите один файл и переименуйте другой.
2. Повторите запуск `POST /v1/indexing/delta-after-commit/jobs`.
3. После завершения запросите summary:

```bash
curl http://localhost:8080/v1/indexing/delta-after-commit/jobs/<runId>/summary
```

Ожидание:

- `deletedFiles` и `renamedFiles` увеличены.
- `removedRecords` > 0 для stale/removed путей.
- В `reasonBreakdown` присутствуют коды удаления/rename-перехода.

Автоматизированный прогон:

```powershell
pwsh scripts/tests/us2_delta_delete_rename.ps1
```

## Сценарий 3: Fallback на full-scan

1. Передайте заведомо некорректный `baseRef` или смоделируйте ошибку Git.
2. Запустите delta job.
3. Проверьте статус/summary.

Ожидание:

- `effectiveMode=full-scan-fallback`.
- `fallbackReasonCode` заполнен.
- Run завершен без ручного рестарта стека.

Автоматизированный прогон:

```powershell
pwsh scripts/tests/us3_delta_fallback_full_scan.ps1
```

## Troubleshooting

- `409 DELTA_ALREADY_RUNNING`: дождитесь завершения активного run.
- `404 RUN_NOT_FOUND`: проверьте корректность `runId`.
- `409 RUN_NOT_FINISHED` для summary: повторите запрос после terminal статуса.
- Частые fallback: проверьте доступность Git в контейнере и валидность `baseRef/targetRef`.
- Нулевой `indexedFiles` при ожидаемых изменениях: проверьте фильтры `INDEX_FILE_TYPES` и `INDEX_EXCLUDE_PATTERNS`.
