Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
& (Join-Path $root "scripts\\tests\\idempotency_test_env.ps1") | Out-Null

$baseUrl = "http://localhost:8080"
if ($env:MCP_PORT) {
    $baseUrl = "http://localhost:$($env:MCP_PORT)"
}
$workspaceContainer = "/workspace/tests/fixtures/idempotency"
if ($env:WORKSPACE_PATH_CONTAINER) {
    $workspaceContainer = $env:WORKSPACE_PATH_CONTAINER
}
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

function Wait-RunSummary([string]$runId) {
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
$summary1 = Wait-RunSummary -runId $run1.runId

$run2 = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/indexing/idempotency/jobs" -ContentType "application/json" -Body $requestBody
$summary2 = Wait-RunSummary -runId $run2.runId

if ($summary2.failedChunks -gt $summary1.failedChunks) {
    throw "Second run increased failedChunks unexpectedly"
}

if ($summary2.skippedChunks -lt 1) {
    throw "Expected skippedChunks > 0 on second unchanged run"
}

if ($env:WORKSPACE_PATH_HOST -and (Test-Path $env:WORKSPACE_PATH_HOST)) {
    Remove-Item -LiteralPath $env:WORKSPACE_PATH_HOST -Recurse -Force
}

Write-Host "US1 repeat-run completed. run1=$($run1.runId) run2=$($run2.runId)"
