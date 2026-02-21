param(
    [string]$ComposeFile = "infra/docker/docker-compose.yml",
    [string]$EnvFile = ".env.example",
    [int]$WaitSeconds = 40
)

$ErrorActionPreference = "Stop"

docker compose -f $ComposeFile --env-file $EnvFile up -d --build
Start-Sleep -Seconds $WaitSeconds

$psOutput = docker compose -f $ComposeFile --env-file $EnvFile ps --format json | ForEach-Object { $_ | ConvertFrom-Json }
$required = @("qdrant", "file-indexer", "mcp-server")
foreach ($svc in $required) {
    $service = $psOutput | Where-Object { $_.Service -eq $svc } | Select-Object -First 1
    if (-not $service) {
        throw "Service '$svc' is missing in compose ps output"
    }
    if ($service.State -ne "running") {
        throw "Service '$svc' is not running (state=$($service.State))"
    }
}

try {
    $health = Invoke-RestMethod -Uri "http://localhost:8080/health" -Method Get -TimeoutSec 10
    if ($health.status -ne "ok") {
        throw "Unexpected health status"
    }
} catch {
    throw "Health endpoint check failed: $($_.Exception.Message)"
}

Write-Host "US1 smoke check passed"
