Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")

& (Join-Path $root "scripts\\tests\\ingestion_test_env.ps1") | Out-Null

$baseUrl = "http://localhost:$($env:MCP_PORT)"
if (-not $env:MCP_PORT) {
    $baseUrl = "http://localhost:8080"
}

$start = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/indexing/ingestion/jobs" -ContentType "application/json" -Body "{}"
$runId = $start.runId
if (-not $runId) {
    throw "runId was not returned"
}

for ($i = 0; $i -lt 120; $i++) {
    $status = Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/indexing/ingestion/jobs/$runId"
    if ($status.status -in @("completed", "failed", "partial")) {
        break
    }
    Start-Sleep -Seconds 1
}

$summary = Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/indexing/ingestion/jobs/$runId/summary"
if (-not ($summary.totalChunks -ge 0)) {
    throw "summary.totalChunks is missing"
}

Write-Host "US1 deterministic chunking scenario finished for runId=$runId"
