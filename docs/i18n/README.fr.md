# ndlss-memory (Francais)

Langues: [English](../../README.md) | [Русский](README.ru.md) | [Francais](README.fr.md) | [Deutsch](README.de.md) | [??](README.zh-CN.md) | [???](README.ko.md) | [???](README.ja.md)

`ndlss-memory` est une couche de memoire locale pour les agents MCP.

## Demarrage rapide sans cloner le depot

Guide complet : [Quickstart](../quickstart.md).

PowerShell (une seule commande):

```powershell
$preset = "generic"; iwr "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose-images/$preset.yml" -OutFile ndlss-compose.yml; $env:NDLSS_WORKSPACE=(Get-Location).Path; docker compose -f ndlss-compose.yml up -d
```

Recommande: epinglez la version d'image:

```powershell
$env:NDLSS_DOCKERHUB_NAMESPACE="ndlss"
$env:NDLSS_IMAGE_TAG="0.2.1"
docker compose -f ndlss-compose.yml up -d
```

Si ce tag n'est pas encore publie, laissez `NDLSS_IMAGE_TAG` vide et utilisez `latest`.

## Documentation

- [Quickstart](../quickstart.md)
- [Compose presets](../compose-presets.md)
- [Configuration](../configuration.md)
- [Contributing](../../CONTRIBUTING.md)
