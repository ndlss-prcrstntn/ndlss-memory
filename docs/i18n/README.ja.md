# ndlss-memory（日本語）

言語: [English](../../README.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [中文](README.zh-CN.md) | [한국어](README.ko.md) | [日本語](README.ja.md)

`ndlss-memory` は MCP エージェント向けのローカルメモリレイヤーです。

## リポジトリをクローンせずにワンコマンド起動

完全ガイド: [Quickstart](../quickstart.md)。

PowerShell（1行）:

```powershell
$preset = "generic"; iwr "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose-images/$preset.yml" -OutFile ndlss-compose.yml; $env:NDLSS_WORKSPACE=(Get-Location).Path; docker compose -f ndlss-compose.yml up -d
```

推奨: イメージのバージョンを固定して起動:

```powershell
$env:NDLSS_DOCKERHUB_NAMESPACE="ndlss"
$env:NDLSS_IMAGE_TAG="0.2.0"
docker compose -f ndlss-compose.yml up -d
```

該当タグが未公開の場合は `NDLSS_IMAGE_TAG` を空にして `latest` を使用してください。

## ドキュメント

- [Quickstart](../quickstart.md)
- [Compose presets](../compose-presets.md)
- [Configuration](../configuration.md)
- [Contributing](../../CONTRIBUTING.md)
