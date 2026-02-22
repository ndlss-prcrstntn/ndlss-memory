# Quickstart: Проверка startup preflight и ready summary

Этот сценарий проверяет фичу `011-startup-preflight-summary` локально через Docker Compose.

## Предусловия

- Docker Engine + Docker Compose v2
- Рабочая директория: `Z:\WORK\ndlss-memory`

## 1. Позитивный старт (ожидается `ready`)

1. Запустите стек:

```powershell
Set-Location 'Z:\WORK\ndlss-memory'
docker compose up -d
```

2. Проверьте health:

```powershell
Invoke-RestMethod -Method Get -Uri 'http://localhost:8080/health'
```

3. Проверьте агрегированную startup-ready сводку:

```powershell
Invoke-RestMethod -Method Get -Uri 'http://localhost:8080/v1/system/startup/readiness'
```

Ожидается:
- `status = ready`
- заполнены `workspacePath`, `indexMode`, `mcpEndpoint`, `collectionName`
- в `preflightChecks` проверки `qdrant_reachability` и `workspace_readable` со статусом `passed`

4. Проверьте startup summary в логах:

```powershell
docker compose logs mcp-server --tail 200
docker compose logs file-indexer --tail 200
```

## 2. Негативный старт: недоступный Qdrant

1. Остановите стек:

```powershell
docker compose down
```

2. Запустите только `mcp-server` с заведомо неверным Qdrant host:

```powershell
$env:QDRANT_HOST='qdrant-unreachable'
docker compose up mcp-server
```

Ожидается:
- сервис завершает старт fail-fast;
- в выводе есть структурированная startup-ошибка с `errorCode`;
- указано действие для исправления (`action`/`recommendedActions`).

3. Сбросьте переменную окружения:

```powershell
Remove-Item Env:QDRANT_HOST -ErrorAction SilentlyContinue
```

## 3. Негативный старт: git обязателен для delta-after-commit

1. Остановите стек и запустите с `INDEX_MODE=delta-after-commit` в окружении без git (или временно подмените PATH так, чтобы `git` был недоступен в контейнере).
2. Ожидайте fail-fast с кодом ошибки проверки git и рекомендацией.

## 4. Проверка обратной совместимости

1. После успешного старта проверьте, что существующие endpoint работают как раньше:

```powershell
Invoke-RestMethod -Method Get -Uri 'http://localhost:8080/v1/system/status'
Invoke-RestMethod -Method Get -Uri 'http://localhost:8080/v1/system/config'
Invoke-RestMethod -Method Post -Uri 'http://localhost:8080/v1/search/semantic' -ContentType 'application/json' -Body '{"query":"healthcheck","limit":1}'
```

2. Убедитесь, что ответы приходят без изменения базового контракта (расширение полей допустимо, удаление/поломка существующих полей недопустимы).

## 5. Очистка

```powershell
Set-Location 'Z:\WORK\ndlss-memory'
docker compose down
```

## 6. Smoke-проверки скриптами

Ready-сценарий:

```powershell
Set-Location 'Z:\WORK\ndlss-memory'
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/tests/startup_preflight_smoke.ps1 -Mode ready
```

Fail-fast сценарий (недоступный Qdrant):

```powershell
Set-Location 'Z:\WORK\ndlss-memory'
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/tests/startup_preflight_smoke.ps1 -Mode failfast-qdrant
```
