# Data Model: Базовый Docker Compose стек

## 1. ComposeService

Описание: логическая модель обязательного сервиса в compose-стеке.

Поля:

- `name` (string, required): уникальное имя сервиса.
  Ограничение: `qdrant | file-indexer | mcp-server`.
- `role` (string, required): назначение сервиса в системе.
- `image` (string, required): ссылка на контейнерный образ.
- `health_status` (string, required): текущее состояние healthcheck.
  Ограничение: `starting | healthy | unhealthy | stopped`.
- `restart_policy` (string, required): политика рестарта.
- `ports` (array[string], optional): опубликованные порты.
- `depends_on` (array[string], optional): зависимости на другие сервисы.
- `volumes` (array[string], optional): привязанные volume/mount.

Валидация:

- `name` должен быть уникальным внутри стека.
- `health_status` обязан соответствовать перечислению.
- `depends_on` не может ссылаться на неизвестный сервис.

Состояния:

- `starting -> healthy`
- `starting -> unhealthy`
- `healthy -> unhealthy`
- `healthy -> stopped`
- `unhealthy -> starting` (после рестарта)

## 2. RuntimeConfig

Описание: набор runtime-параметров, приходящих из `.env`.

Поля:

- `project_name` (string, required)
- `qdrant_port` (integer, required)
- `mcp_port` (integer, required)
- `index_mode` (string, required): `full-scan | delta-after-commit`
- `index_file_types` (array[string], required)
- `index_exclude_patterns` (array[string], required)
- `command_allowlist` (array[string], required)
- `command_timeout_seconds` (integer, required)

Валидация:

- Порты в диапазоне `1..65535`.
- `index_mode` только из допустимого списка.
- `command_timeout_seconds` > 0.

Связи:

- `RuntimeConfig` применяется ко всем `ComposeService`.
- Изменение `RuntimeConfig` требует перезапуска зависимых сервисов.

## 3. VolumeBinding

Описание: политика хранения и доступа к данным.

Поля:

- `binding_id` (string, required)
- `service_name` (string, required)
- `source` (string, required): volume name или host path.
- `target` (string, required): путь в контейнере.
- `mode` (string, required): `ro | rw`.
- `persistence_class` (string, required): `persistent | ephemeral`.

Валидация:

- Для `qdrant` `persistence_class` MUST быть `persistent`.
- Для mount рабочей директории индексатора `mode` SHOULD быть `ro`, если не
  требуется запись.

## 4. ServiceHealthReport

Описание: агрегированный отчет для диагностики запуска.

Поля:

- `timestamp` (datetime, required)
- `overall_status` (string, required): `healthy | degraded | down`
- `services` (array[ComposeServiceStatus], required)
- `issues` (array[string], optional)

Подсущность `ComposeServiceStatus`:

- `name` (string)
- `status` (string)
- `last_check` (datetime)
- `details` (string)

Правила:

- `overall_status = healthy`, только если все обязательные сервисы `healthy`.
- Если хотя бы один сервис `unhealthy`, общий статус не может быть `healthy`.
