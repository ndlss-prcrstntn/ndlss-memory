# Research: Watch Mode Incremental Indexing

## Decision 1: Использовать событийный watcher с fallback-поллингом

- **Decision**: Реализовать primary detection через файловые события watcher-а и fallback на периодический reconcile scan для устойчивости при потерях событий.
- **Rationale**: Чисто событийный подход дает низкую задержку, а fallback-поллинг закрывает edge cases Docker-mounted FS и burst-условия.
- **Alternatives considered**:
  - Только поллинг: проще, но выше latency и лишняя нагрузка.
  - Только события: быстрее, но выше риск рассинхронизации при пропущенных уведомлениях.

## Decision 2: Коалесценция и дедупликация по ключу файла

- **Decision**: Собирать события в краткое окно коалесценции и обрабатывать последнюю релевантную операцию на файл (`delete` приоритетнее `update`, `update` приоритетнее `create`).
- **Rationale**: Burst-изменения не должны порождать каскад дорогих reindex операций для одного и того же файла.
- **Alternatives considered**:
  - Обрабатывать каждое событие отдельно: увеличивает нагрузку и риск гонок.
  - Полная batch-обработка всех файлов: теряется преимущество инкрементальности.

## Decision 3: Инкрементальная обработка через существующий idempotency/ingestion pipeline

- **Decision**: Для `create/update` вызывать инкрементальный ingestion для конкретных файлов, для `delete` использовать cleanup-ветку существующей idempotency логики.
- **Rationale**: Переиспользование зрелого pipeline снижает риск регрессий и сохраняет единые правила чанкинга/метаданных.
- **Alternatives considered**:
  - Новый отдельный watch-pipeline с нуля: дублирование логики и повышенный риск расхождений.

## Decision 4: Retry/backoff политика watcher-а

- **Decision**: Применять ограниченный экспоненциальный backoff с jitter и автоматическим возвратом в `running` после успешной проверки окружения.
- **Rationale**: Устраняет «залипание» в ошибке и предотвращает агрессивные циклы перезапуска.
- **Alternatives considered**:
  - Бесконечный tight-loop retry: риск деградации CPU.
  - Остановка watcher до ручного рестарта: не соответствует требованиям zero-touch recovery.

## Decision 5: Наблюдаемость watch-режима через отдельный статус + расширение summary

- **Decision**: Добавить watch-статус endpoint и встроить watch-поля в системные status/summary payload (state, lastEventAt, queueDepth, processed/failed counters, lastError).
- **Rationale**: Оператор получает и быстрый точечный статус, и агрегированную картину без ломки существующего API.
- **Alternatives considered**:
  - Только логи: плохо автоматизируется.
  - Только новый endpoint без интеграции в текущие summary: фрагментированная диагностика.

## Decision 6: Гарантия отсутствия регрессий для full-scan и delta-after-commit

- **Decision**: Ввести отдельные regression сценарии переключения режимов и проверить неизменность текущих контрактов для `full-scan`/`delta-after-commit`.
- **Rationale**: Watch-mode внедряется как добавочный режим и не должен влиять на существующих пользователей.
- **Alternatives considered**:
  - Тестировать только watch: риск скрытых side-effect в shared runtime логике.
