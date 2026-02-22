# Research: First-Run Bootstrap for Zero-Friction Indexing

## Decision 1: Хранить состояние bootstrap в Qdrant как персистентный маркер workspace

- **Decision**: Использовать персистентный bootstrap-marker в Qdrant (служебная запись по ключу workspace) как источник истины «первый запуск уже выполнен».
- **Rationale**: Qdrant уже является постоянным storage в стеке и переживает рестарты; это исключает зависимость от writable workspace (который смонтирован read-only) и позволяет идемпотентно принимать решение на старте.
- **Alternatives considered**:
  - Хранить marker в памяти процесса.
    - Отклонено: теряется при рестарте, приводит к повторному bootstrap.
  - Хранить marker в файле внутри workspace.
    - Отклонено: workspace read-only по текущему контракту compose.

## Decision 2: Авто-создание коллекции выполнять через idempotent ensure-операцию на старте

- **Decision**: Перед авто-ingestion запускать операцию `ensure_collection` (проверка существования + создание при отсутствии) для целевой коллекции.
- **Rationale**: Это закрывает главный первый барьер DX и устраняет ошибку «коллекция отсутствует» в новых workspace.
- **Alternatives considered**:
  - Создавать коллекцию только в ручном endpoint ingestion.
    - Отклонено: противоречит цели zero-friction первого запуска.
  - Падать при отсутствии коллекции и требовать manual fix.
    - Отклонено: ухудшает UX и увеличивает время до первого поиска.

## Decision 3: Авто-bootstrap запускать один раз на workspace и блокировать повторный дорогой старт

- **Decision**: Запускать авто-bootstrap только когда marker отсутствует или помечен как failed-retryable; при `completed` запускать только lightweight readiness-проверки без полного reindex.
- **Rationale**: Выполняется цель «searchable без ручных API» и одновременно исключается повторный дорогой полный bootstrap на каждом restart.
- **Alternatives considered**:
  - Всегда запускать full bootstrap на старте.
    - Отклонено: избыточная нагрузка и риск дублирования операций.
  - Никогда не запускать автоматически.
    - Отклонено: не выполняет требования фичи.

## Decision 4: Сохранить manual ingestion API неизменным и расширить только наблюдаемость

- **Decision**: Не менять поведение существующих ручных endpoint запуска индексации; добавить bootstrap-диагностику в статус/summary и в startup readiness.
- **Rationale**: Backward compatibility для текущих клиентов и скриптов, при этом появляется прозрачность авто-bootstrap.
- **Alternatives considered**:
  - Ввести отдельный обязательный bootstrap endpoint и депрекейтнуть текущие.
    - Отклонено: breaking change и лишняя миграция.

## Decision 5: Публиковать bootstrap-состояние в двух каналах — логи старта и summary endpoint

- **Decision**: Обязательный structured log (`bootstrap-started/bootstrapped/skipped/failed`) и сериализация bootstrap-блока в `startup/readiness` и ingestion summary/status endpoint.
- **Rationale**: Оператор получает быстрый human-readable сигнал в логах и машинно-обрабатываемый статус через API.
- **Alternatives considered**:
  - Только логи.
    - Отклонено: трудно автоматизировать проверки.
  - Только API.
    - Отклонено: хуже первичная диагностика через `docker compose logs`.

## Decision 6: Проверки регрессий включают сценарий нестандартного внешнего Qdrant порта

- **Decision**: В регрессионных сценариях верифицировать, что внутренний сервисный трафик к Qdrant не зависит от внешнего host-port mapping (`QDRANT_PORT`) и остается рабочим при нестандартном внешнем порте.
- **Rationale**: Этот класс сбоев уже наблюдался в эксплуатации и напрямую влияет на auto-bootstrap.
- **Alternatives considered**:
  - Проверять только дефолтный порт 6333.
    - Отклонено: не ловит ранее проявленный production-like дефект.

