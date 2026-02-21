param(
    [string]$BaseUrl = "http://localhost:8080",
    [string]$WorkspacePath = "/workspace/tests/fixtures/full-scan",
    [int]$TimeoutSeconds = 60
)

$ErrorActionPreference = "Stop"

powershell -NoProfile -ExecutionPolicy Bypass -File "scripts/tests/full_scan_test_env.ps1"

$startPayload = @{ workspacePath = $WorkspacePath } | ConvertTo-Json
$startResp = Invoke-RestMethod -Uri "$BaseUrl/v1/indexing/full-scan/jobs" -Method Post -Body $startPayload -ContentType "application/json" -TimeoutSec 10
if (-not $startResp.jobId) {
    throw "jobId missing in start response"
}

$jobId = $startResp.jobId
$deadline = (Get-Date).AddSeconds($TimeoutSeconds)
$status = $null

while ((Get-Date) -lt $deadline) {
    $status = Invoke-RestMethod -Uri "$BaseUrl/v1/indexing/full-scan/jobs/$jobId" -Method Get -TimeoutSec 10
    if ($status.status -in @("completed", "failed", "cancelled")) {
        break
    }
    Start-Sleep -Seconds 2
}

if (-not $status -or $status.status -ne "completed") {
    throw "Full scan job did not complete successfully (status=$($status.status))"
}

$summary = Invoke-RestMethod -Uri "$BaseUrl/v1/indexing/full-scan/jobs/$jobId/summary" -Method Get -TimeoutSec 10
if ([int]$summary.totals.processedCount -lt 1) {
    throw "Expected processedCount > 0"
}

Write-Host "US1 full scan recursive indexing check passed"

