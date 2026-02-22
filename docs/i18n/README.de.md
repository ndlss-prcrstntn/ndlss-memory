# ndlss-memory (Deutsch)

Sprachen: [English](../../README.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [中文](README.zh-CN.md) | [한국어](README.ko.md) | [日本語](README.ja.md)

`ndlss-memory` ist eine lokale Memory-Schicht für MCP-Agenten.

## Schnellstart ohne Repository-Klon

Vollständige Anleitung: [Quickstart](../quickstart.md).

PowerShell (ein Befehl):

```powershell
$preset = "generic"; iwr "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose-images/$preset.yml" -OutFile ndlss-compose.yml; $env:NDLSS_WORKSPACE=(Get-Location).Path; docker compose -f ndlss-compose.yml up -d
```

Empfohlen: Image-Version fixieren:

```powershell
$env:NDLSS_DOCKERHUB_NAMESPACE="ndlss"
$env:NDLSS_IMAGE_TAG="0.2.0"
docker compose -f ndlss-compose.yml up -d
```

Falls der Tag noch nicht veröffentlicht ist, `NDLSS_IMAGE_TAG` leer lassen und `latest` verwenden.

## Dokumentation

- [Quickstart](../quickstart.md)
- [Compose presets](../compose-presets.md)
- [Configuration](../configuration.md)
- [Contributing](../../CONTRIBUTING.md)
