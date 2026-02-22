# ndlss-memory (한국어)

언어: [English](../../README.md) | [Русский](README.ru.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [中文](README.zh-CN.md) | [한국어](README.ko.md) | [日本語](README.ja.md)

`ndlss-memory`는 MCP 에이전트를 위한 로컬 메모리 계층입니다.

## 저장소 클론 없이 원커맨드 시작

전체 가이드: [Quickstart](../quickstart.md).

PowerShell (한 줄):

```powershell
$preset = "generic"; iwr "https://raw.githubusercontent.com/ndlss-prcrstntn/ndlss-memory/main/deploy/compose-images/$preset.yml" -OutFile ndlss-compose.yml; $env:NDLSS_WORKSPACE=(Get-Location).Path; docker compose -f ndlss-compose.yml up -d
```

권장: 이미지 버전을 고정해서 실행하세요:

```powershell
$env:NDLSS_DOCKERHUB_NAMESPACE="ndlss"
$env:NDLSS_IMAGE_TAG="0.2.0"
docker compose -f ndlss-compose.yml up -d
```

해당 태그가 아직 없으면 `NDLSS_IMAGE_TAG`를 비우고 `latest`를 사용하세요.

## 문서

- [Quickstart](../quickstart.md)
- [Compose presets](../compose-presets.md)
- [Configuration](../configuration.md)
- [Contributing](../../CONTRIBUTING.md)
