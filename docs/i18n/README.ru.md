# ndlss-memory (Русский)

Язык: [English](../../README.md) | [Русский](README.ru.md) | [Francais](README.fr.md) | [Deutsch](README.de.md) | [??](README.zh-CN.md) | [???](README.ko.md) | [???](README.ja.md)

`ndlss-memory` — локальный memory-слой для MCP-агентов.

## Быстрый старт без клонирования

Полный quickstart: [Quickstart](../quickstart.md).

PowerShell (одной командой):

```powershell
$preset = "generic"; iwr "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose-images/$preset.yml" -OutFile ndlss-compose.yml; $env:NDLSS_WORKSPACE=(Get-Location).Path; docker compose -f ndlss-compose.yml up -d
```

Приоритетно: зафиксируйте версию образов:

```powershell
$env:NDLSS_DOCKERHUB_NAMESPACE="ndlss"
$env:NDLSS_IMAGE_TAG="0.2.1"
docker compose -f ndlss-compose.yml up -d
```

Если нужный тег еще не опубликован, оставьте `NDLSS_IMAGE_TAG` пустым и используйте `latest`.

## Документация

- [Quickstart](../quickstart.md)
- [Compose presets](../compose-presets.md)
- [Configuration](../configuration.md)
- [Contributing](../../CONTRIBUTING.md)
