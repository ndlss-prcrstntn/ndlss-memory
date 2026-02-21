param(
    [string]$ComposeFile = "infra/docker/docker-compose.yml",
    [string]$BaseEnvFile = ".env.example"
)

$ErrorActionPreference = "Stop"

$tempEnv = Join-Path $env:TEMP "ndlss-memory-us2.env"
Copy-Item $BaseEnvFile $tempEnv -Force
Add-Content $tempEnv "MCP_PORT=18080"
Add-Content $tempEnv "INDEX_MODE=delta-after-commit"

docker compose -f $ComposeFile --env-file $tempEnv up -d --build
Start-Sleep -Seconds 20

$config = Invoke-RestMethod -Uri "http://localhost:18080/v1/system/config" -Method Get -TimeoutSec 10
if ($config.indexMode -ne "delta-after-commit") {
    throw "INDEX_MODE override not applied"
}
if ([int]$config.mcpPort -ne 18080) {
    throw "MCP_PORT override not applied"
}

Write-Host "US2 env override check passed"

