Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
. (Join-Path $root "scripts/tests/test_ports.ps1")
Set-DefaultTestPorts
& (Join-Path $root "scripts\\tests\\ingestion_test_env.ps1") | Out-Null

$baseUrl = Get-TestBaseUrl

$run = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/indexing/ingestion/jobs" -ContentType "application/json" -Body "{}"
$runId = $run.runId

for ($i = 0; $i -lt 120; $i++) {
    $status = Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/indexing/ingestion/jobs/$runId"
    if ($status.status -in @("completed", "failed", "partial")) {
        break
    }
    Start-Sleep -Seconds 1
}

$summary = Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/indexing/ingestion/jobs/$runId/summary"
$coverage = $summary.metadataCoverage
$required = @("path", "fileName", "fileType", "contentHash", "timestamp")
foreach ($field in $required) {
    if (-not $coverage.PSObject.Properties.Name.Contains($field)) {
        throw "Missing metadataCoverage field: $field"
    }
}

Write-Host "US3 metadata traceability scenario finished for runId=$runId"
