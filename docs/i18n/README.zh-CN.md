# ndlss-memory（简体中文）

语言: [English](../../README.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [中文](README.zh-CN.md) | [한국어](README.ko.md) | [日本語](README.ja.md)

`ndlss-memory` 是一个面向 MCP Agent 的本地记忆层。

## 无需克隆仓库的一键启动

完整指南：[Quickstart](../quickstart.md)。

PowerShell（一条命令）：

```powershell
$preset = "generic"; iwr "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose-images/$preset.yml" -OutFile ndlss-compose.yml; $env:NDLSS_WORKSPACE=(Get-Location).Path; docker compose -f ndlss-compose.yml up -d
```

建议优先固定镜像版本：

```powershell
$env:NDLSS_DOCKERHUB_NAMESPACE="ndlss"
$env:NDLSS_IMAGE_TAG="0.2.0"
docker compose -f ndlss-compose.yml up -d
```

如果该 tag 尚未发布，请留空 `NDLSS_IMAGE_TAG` 并使用 `latest`。

## 文档

- [Quickstart](../quickstart.md)
- [Compose presets](../compose-presets.md)
- [Configuration](../configuration.md)
- [Contributing](../../CONTRIBUTING.md)
