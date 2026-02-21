param(
    [string]$ComposeFile = "infra/docker/docker-compose.yml",
    [string]$EnvFile = ".env.example",
    [int]$WaitSeconds = 20
)

$ErrorActionPreference = "Stop"

function Run-Checks {
    powershell -NoProfile -ExecutionPolicy Bypass -File "scripts/tests/us1_full_scan_recursive_indexing.ps1"
    powershell -NoProfile -ExecutionPolicy Bypass -File "scripts/tests/us2_full_scan_filtering.ps1"
    powershell -NoProfile -ExecutionPolicy Bypass -File "scripts/tests/us3_full_scan_resilience.ps1"
}

docker compose -f $ComposeFile --env-file $EnvFile up -d --build
Start-Sleep -Seconds $WaitSeconds

Run-Checks

$tempEnv = Join-Path $env:TEMP "ndlss-memory-delta-regression.env"
Copy-Item $EnvFile $tempEnv -Force
Add-Content $tempEnv "INDEX_MODE=delta-after-commit"

docker compose -f $ComposeFile --env-file $tempEnv up -d --build
Start-Sleep -Seconds $WaitSeconds

$cfg = Invoke-RestMethod -Uri "http://localhost:8080/v1/system/config" -Method Get -TimeoutSec 10
if ($cfg.indexMode -ne "delta-after-commit") {
    throw "Expected delta-after-commit mode after env override"
}

Write-Host "Full scan compose regression check passed"

