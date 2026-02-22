# ndlss-memory (한국어)

언어: [English](../../README.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [中文](README.zh-CN.md) | [한국어](README.ko.md) | [日本語](README.ja.md)

`ndlss-memory`는 MCP 에이전트를 위한 로컬 메모리 계층입니다.

## 저장소 클론 없이 원커맨드 시작

전체 가이드: `../quickstart.md`.

PowerShell (한 줄):

```powershell
$preset = "generic"; iwr "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose/$preset.yml" -OutFile ndlss-compose.yml; $env:NDLSS_WORKSPACE=(Get-Location).Path; docker compose -f ndlss-compose.yml up -d --build
```

## 문서

- `../quickstart.md`
- `../compose-presets.md`
- `../configuration.md`
- `../../CONTRIBUTING.md`
