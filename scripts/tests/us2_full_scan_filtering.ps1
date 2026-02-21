param(
    [string]$BaseUrl = "http://localhost:8080",
    [string]$WorkspacePath = "/workspace/tests/fixtures/full-scan",
    [int]$TimeoutSeconds = 60
)

$ErrorActionPreference = "Stop"

powershell -NoProfile -ExecutionPolicy Bypass -File "scripts/tests/full_scan_test_env.ps1"

$startPayload = @{ workspacePath = $WorkspacePath } | ConvertTo-Json
$startResp = Invoke-RestMethod -Uri "$BaseUrl/v1/indexing/full-scan/jobs" -Method Post -Body $startPayload -ContentType "application/json" -TimeoutSec 10
$jobId = $startResp.jobId

$deadline = (Get-Date).AddSeconds($TimeoutSeconds)
while ((Get-Date) -lt $deadline) {
    $status = Invoke-RestMethod -Uri "$BaseUrl/v1/indexing/full-scan/jobs/$jobId" -Method Get -TimeoutSec 10
    if ($status.status -eq "completed") {
        break
    }
    Start-Sleep -Seconds 2
}

$summary = Invoke-RestMethod -Uri "$BaseUrl/v1/indexing/full-scan/jobs/$jobId/summary" -Method Get -TimeoutSec 10
$codes = @($summary.skipBreakdown | ForEach-Object { $_.code })
if (-not ($codes -contains "UNSUPPORTED_TYPE")) {
    throw "Expected UNSUPPORTED_TYPE in skipBreakdown"
}
if (-not ($codes -contains "EXCLUDED_BY_PATTERN")) {
    throw "Expected EXCLUDED_BY_PATTERN in skipBreakdown"
}

Write-Host "US2 full scan filtering check passed"

