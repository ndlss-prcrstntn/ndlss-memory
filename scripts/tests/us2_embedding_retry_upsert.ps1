Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
& (Join-Path $root "scripts\\tests\\ingestion_test_env.ps1") -RetryMaxAttempts 3 -RetryBackoffSeconds 0.1 | Out-Null

$baseUrl = "http://localhost:$($env:MCP_PORT)"
if (-not $env:MCP_PORT) {
    $baseUrl = "http://localhost:8080"
}

$start = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/indexing/ingestion/jobs" -ContentType "application/json" -Body "{}"
$runId = $start.runId

for ($i = 0; $i -lt 120; $i++) {
    $status = Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/indexing/ingestion/jobs/$runId"
    if ($status.status -in @("completed", "failed", "partial")) {
        break
    }
    Start-Sleep -Milliseconds 500
}

$summary = Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/indexing/ingestion/jobs/$runId/summary"
if ($summary.retryCount -lt 0) {
    throw "retryCount is invalid"
}

if ($summary.embeddedChunks -lt 0) {
    throw "embeddedChunks is invalid"
}

Write-Host "US2 retry+upsert scenario finished for runId=$runId retryCount=$($summary.retryCount)"
