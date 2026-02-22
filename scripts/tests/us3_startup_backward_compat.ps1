Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
. (Join-Path $root "scripts/tests/test_ports.ps1")
Set-DefaultTestPorts
$baseUrl = Get-TestBaseUrl

function Wait-HealthOk {
    param(
        [string]$Url,
        [int]$TimeoutSeconds = 60
    )
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        try {
            $health = Invoke-RestMethod -Method Get -Uri "$Url/health"
            if ($health.status -eq "ok") {
                return
            }
        } catch {
            Start-Sleep -Seconds 2
            continue
        }
        Start-Sleep -Seconds 2
    }
    throw "health endpoint did not return ok in $TimeoutSeconds seconds"
}

Push-Location $root
try {
    docker compose up -d --build | Out-Null

    Wait-HealthOk -Url $baseUrl -TimeoutSeconds 60

    $null = Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/system/status"
    $config = Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/system/config"
    $null = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/search/semantic" -ContentType "application/json" -Body '{"query":"healthcheck","limit":1}'

    if (-not $config.startupReadiness) {
        throw "startupReadiness is missing from /v1/system/config response"
    }

    Write-Host "[us3-startup-backward-compat] passed"
} finally {
    docker compose down | Out-Null
    Pop-Location
}
