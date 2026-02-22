# ndlss-memory（日本語）

言語: [English](../../README.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [中文](README.zh-CN.md) | [한국어](README.ko.md) | [日本語](README.ja.md)

`ndlss-memory` は MCP エージェント向けのローカルメモリレイヤーです。

## リポジトリをクローンせずにワンコマンド起動

完全ガイド: `../quickstart.md`。

PowerShell（1行）:

```powershell
$preset = "generic"; iwr "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose/$preset.yml" -OutFile ndlss-compose.yml; $env:NDLSS_WORKSPACE=(Get-Location).Path; docker compose -f ndlss-compose.yml up -d --build
```

## ドキュメント

- `../quickstart.md`
- `../compose-presets.md`
- `../configuration.md`
- `../../CONTRIBUTING.md`
