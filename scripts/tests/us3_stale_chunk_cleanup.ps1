Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
. (Join-Path $root "scripts/tests/test_ports.ps1")
Set-DefaultTestPorts
& (Join-Path $root "scripts\\tests\\idempotency_test_env.ps1") | Out-Null

$baseUrl = Get-TestBaseUrl
$workspaceContainer = "/workspace/tests/fixtures/idempotency"
if ($env:WORKSPACE_PATH_CONTAINER) {
    $workspaceContainer = $env:WORKSPACE_PATH_CONTAINER
}
$workspaceHost = $env:WORKSPACE_PATH_HOST
$requestBody = @{ workspacePath = $workspaceContainer } | ConvertTo-Json -Compress

for ($i = 0; $i -lt 120; $i++) {
    try {
        $health = Invoke-RestMethod -Method Get -Uri "$baseUrl/health" -TimeoutSec 2
        if ($health.status -eq "ok") {
            break
        }
    } catch {
    }
    Start-Sleep -Milliseconds 500
}

function Wait-IdempotencySummary([string]$runId) {
    for ($i = 0; $i -lt 120; $i++) {
        $status = Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/indexing/idempotency/jobs/$runId"
        if ($status.status -in @("completed", "partial", "failed")) {
            break
        }
        Start-Sleep -Milliseconds 500
    }
    return Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/indexing/idempotency/jobs/$runId/summary"
}

$run1 = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/indexing/idempotency/jobs" -ContentType "application/json" -Body $requestBody
$null = Wait-IdempotencySummary -runId $run1.runId

$deleteTarget = Join-Path $workspaceHost "changes\\deleted.txt"
if (Test-Path $deleteTarget) {
    Remove-Item -LiteralPath $deleteTarget -Force
}

$truncateTarget = Join-Path $workspaceHost "changes\\edited.txt"
if (Test-Path $truncateTarget) {
    Set-Content -LiteralPath $truncateTarget -Value "truncated content" -Encoding utf8
}

$run2 = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/indexing/idempotency/jobs" -ContentType "application/json" -Body $requestBody
$summary2 = Wait-IdempotencySummary -runId $run2.runId

if ($summary2.deletedChunks -lt 1) {
    throw "Expected deletedChunks > 0 after stale cleanup scenario"
}

if ($workspaceHost -and (Test-Path $workspaceHost)) {
    Remove-Item -LiteralPath $workspaceHost -Recurse -Force
}

Write-Host "US3 stale cleanup completed. run2=$($run2.runId)"
