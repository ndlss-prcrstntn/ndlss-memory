# Quickstart: 5-10 минут до первого поиска

## 1. Подготовка

Требования:

- Docker Engine + Docker Compose v2
- PowerShell (Windows PowerShell или PowerShell 7+)

В корне проекта создайте `.env` из минимального шаблона:

```powershell
Copy-Item .env.minimal.example .env
```

## 2. Запуск стека

Вариант A (zero-friction, из корня):

```powershell
docker compose up -d --build
```

Вариант B (через проектный скрипт):

```powershell
powershell -File scripts/dev/up.ps1
```

Проверка:

```powershell
docker compose ps
curl http://localhost:8080/health
```

Ожидаемый результат: сервис `mcp-server` отвечает `200` на `/health`.

## 3. Первый semantic search запрос

```powershell
curl -X POST http://localhost:8080/v1/search/semantic `
  -H "Content-Type: application/json" `
  -d "{\"query\":\"docker compose healthcheck\",\"limit\":5}"
```

Если данных еще нет, запустите ingestion job:

```powershell
curl -X POST http://localhost:8080/v1/indexing/ingestion/jobs `
  -H "Content-Type: application/json" `
  -d "{\"workspacePath\":\"/workspace\"}"
```

Повторите запрос поиска после завершения job.

## 4. Подключение MCP-клиента

Минимальный пример client config:

```json
{
  "servers": {
    "ndlss-memory": {
      "transport": "http",
      "url": "http://localhost:8080"
    }
  }
}
```

После этого MCP-клиент может вызывать search/source/metadata tools без дополнительной ручной настройки инфраструктуры.

## 5. Остановка

```powershell
docker compose down
```
