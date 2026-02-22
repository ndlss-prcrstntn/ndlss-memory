param(
    [string]$BaseUrl = "",
    [string]$WorkspacePath = "/workspace/tests/fixtures/full-scan",
    [int]$TimeoutSeconds = 60
)

$ErrorActionPreference = "Stop"
. (Join-Path (Resolve-Path (Join-Path $PSScriptRoot "..\\..")) "scripts/tests/test_ports.ps1")
Set-DefaultTestPorts
if (-not $BaseUrl) {
    $BaseUrl = Get-TestBaseUrl
}

powershell -NoProfile -ExecutionPolicy Bypass -File "scripts/tests/full_scan_test_env.ps1"

$startPayload = @{
    workspacePath = $WorkspacePath
    maxFileSizeBytes = 128
} | ConvertTo-Json

$startResp = Invoke-RestMethod -Uri "$BaseUrl/v1/indexing/full-scan/jobs" -Method Post -Body $startPayload -ContentType "application/json" -TimeoutSec 10
$jobId = $startResp.jobId

$deadline = (Get-Date).AddSeconds($TimeoutSeconds)
while ((Get-Date) -lt $deadline) {
    $status = Invoke-RestMethod -Uri "$BaseUrl/v1/indexing/full-scan/jobs/$jobId" -Method Get -TimeoutSec 10
    if ($status.status -in @("completed", "failed", "cancelled")) {
        break
    }
    Start-Sleep -Seconds 2
}

$summary = Invoke-RestMethod -Uri "$BaseUrl/v1/indexing/full-scan/jobs/$jobId/summary" -Method Get -TimeoutSec 10
$codes = @($summary.skipBreakdown | ForEach-Object { $_.code })
if (-not ($codes -contains "FILE_TOO_LARGE")) {
    throw "Expected FILE_TOO_LARGE in skipBreakdown"
}

Write-Host "US3 full scan resilience check passed"


