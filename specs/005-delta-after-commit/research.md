# Research: Delta-after-commit режим

## Контекст

Фича: `005-delta-after-commit`
Цель: определить надежный шаблон расчета delta-изменений по Git, корректную
обработку `added/modified/deleted/renamed` и безопасный fallback на full-scan.

## Исследовательские задачи

- Task: "Find best practices for Git diff based incremental indexing"
- Task: "Find robust rename/delete handling patterns for vector index sync"
- Task: "Find fallback strategy when Git metadata is unavailable"
- Task: "Find observability patterns for long-running delta indexing jobs"

## Решения

### Decision: Использовать `git diff --name-status --find-renames` как источник change set
- Rationale: формат `name-status` дает однозначную классификацию (`A`, `M`, `D`, `R`) и
  достаточно контекста для действий index/delete/relink.
- Alternatives considered:
  - `git status --porcelain`: отклонено, отражает только рабочее состояние и менее
    пригоден для повторяемого сравнения двух ревизий.
  - Парсинг `git log --name-status`: отклонено как более сложный и дорогой для run-time.

### Decision: Вводить единый нормализованный `GitChangeSet` перед применением фильтров
- Rationale: сначала нормализуем изменения по типам и путям, затем применяем
  общие правила фильтрации файлов; это сохраняет единое поведение с full-scan.
- Alternatives considered:
  - Фильтровать прямо в потоке вывода Git: отклонено, сложнее трассировать причины skip.
  - Отдельная логика фильтров только для delta: отклонено, риск расхождения режимов.

### Decision: Для `renamed` выполнять удаление старого пути и индексацию нового пути в одном run
- Rationale: гарантируется отсутствие устаревшей привязки и сохраняется
  актуальность поиска сразу после завершения delta-run.
- Alternatives considered:
  - Обрабатывать rename как `modified` только по новому пути: отклонено, оставляет
    stale записи по старому пути.
  - Отложенное удаление старого пути отдельным cleanup-джобом: отклонено как менее консистентное.

### Decision: Любая критическая ошибка Git-diff переключает run в `full-scan-fallback`
- Rationale: выполняется требование отказоустойчивости без ручного вмешательства,
  при этом run остается наблюдаемым через единый статус и reason code.
- Alternatives considered:
  - Прерывать run ошибкой: отклонено, ухудшает операционную надежность.
  - Игнорировать ошибку и продолжать с пустым diff: отклонено, риск пропустить изменения.

### Decision: Причины fallback и skip фиксировать машиночитаемыми кодами
- Rationale: контрактная проверка и автоматическая диагностика требуют стабильных
  кодов (`GIT_DIFF_FAILED`, `BASE_REF_NOT_FOUND`, `RENAMED_SOURCE_REMOVED`, ...).
- Alternatives considered:
  - Только текстовые сообщения в логах: отклонено, сложно автоматизировать проверку.

## Outcome

`NEEDS CLARIFICATION` отсутствуют. Все неопределенности по source-of-truth,
rename/delete и fallback закрыты решениями выше.
