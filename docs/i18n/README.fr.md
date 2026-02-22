# ndlss-memory (Français)

Langues: [English](../../README.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [中文](README.zh-CN.md) | [한국어](README.ko.md) | [日本語](README.ja.md)

`ndlss-memory` est une couche de mémoire locale pour les agents MCP.

## Démarrage rapide sans cloner le dépôt

Guide complet : [Quickstart](../quickstart.md).

PowerShell (une seule commande):

```powershell
$preset = "generic"; iwr "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose-images/$preset.yml" -OutFile ndlss-compose.yml; $env:NDLSS_WORKSPACE=(Get-Location).Path; docker compose -f ndlss-compose.yml up -d
```

Recommande: épinglez la version d'image:

```powershell
$env:NDLSS_DOCKERHUB_NAMESPACE="ndlss"
$env:NDLSS_IMAGE_TAG="0.2.0"
docker compose -f ndlss-compose.yml up -d
```

Si ce tag n'est pas encore publié, laissez `NDLSS_IMAGE_TAG` vide et utilisez `latest`.

## Documentation

- [Quickstart](../quickstart.md)
- [Compose presets](../compose-presets.md)
- [Configuration](../configuration.md)
- [Contributing](../../CONTRIBUTING.md)
