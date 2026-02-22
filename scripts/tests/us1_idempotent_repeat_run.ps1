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
$artifactDir = Join-Path $root "tests/artifacts/quality-stability"
New-Item -ItemType Directory -Path $artifactDir -Force | Out-Null
$artifactPath = Join-Path $artifactDir "us1-idempotency-summary.json"

function Wait-ForHealth {
    param(
        [string]$Url,
        [int]$MaxAttempts = 120,
        [int]$SleepMs = 500
    )

    Write-Host "[US1] waiting for MCP health at $Url/health"
    for ($i = 0; $i -lt $MaxAttempts; $i++) {
        try {
            $health = Invoke-RestMethod -Method Get -Uri "$Url/health" -TimeoutSec 2
            if ($health.status -eq "ok") {
                Write-Host "[US1] health is ok after $($i + 1) attempts"
                return
            }
        } catch {
        }

        if ((($i + 1) % 10) -eq 0) {
            Write-Host "[US1] still waiting for health... attempt=$($i + 1)/$MaxAttempts"
        }
        Start-Sleep -Milliseconds $SleepMs
    }

    throw "MCP health did not become ok within $MaxAttempts attempts"
}

function Wait-RunSummary([string]$runId) {
    $lastStatus = ""
    Write-Host "[US1] waiting for idempotency job status runId=$runId"
    for ($i = 0; $i -lt 120; $i++) {
        try {
            $status = Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/indexing/idempotency/jobs/$runId"
            if ($status.status -ne $lastStatus) {
                $lastStatus = [string]$status.status
                Write-Host "[US1] runId=$runId status=$lastStatus attempt=$($i + 1)/120"
            }
            if ($status.status -in @("completed", "partial", "failed")) {
                $summary = Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/indexing/idempotency/jobs/$runId/summary"
                Write-Host "[US1] runId=$runId finished status=$($status.status)"
                return $summary
            }
        } catch {
            if ((($i + 1) % 10) -eq 0) {
                Write-Host "[US1] waiting runId=$runId... temporary request failure, attempt=$($i + 1)/120"
            }
        }

        if ((($i + 1) % 10) -eq 0 -and $lastStatus) {
            Write-Host "[US1] waiting runId=$runId... currentStatus=$lastStatus attempt=$($i + 1)/120"
        }
        Start-Sleep -Milliseconds 500
    }
    throw "Timeout waiting for idempotency job completion runId=$runId"
}

Wait-ForHealth -Url $baseUrl

Write-Host "[US1] starting first idempotency run"
$run1 = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/indexing/idempotency/jobs" -ContentType "application/json" -Body $requestBody
$summary1 = Wait-RunSummary -runId $run1.runId

Write-Host "[US1] starting second idempotency run"
$run2 = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/indexing/idempotency/jobs" -ContentType "application/json" -Body $requestBody
$summary2 = Wait-RunSummary -runId $run2.runId

if ($summary1.updatedChunks -lt 1 -and $summary1.skippedChunks -lt 1) {
    throw "Expected first run to update or skip at least one chunk"
}

if ($summary2.failedChunks -gt $summary1.failedChunks) {
    throw "Second run increased failedChunks unexpectedly"
}

if ($summary2.skippedChunks -lt 1) {
    throw "Expected skippedChunks > 0 on second unchanged run"
}

$duplicateCount1 = if ($summary1.PSObject.Properties.Name -contains "duplicateCount") { [int]$summary1.duplicateCount } else { 0 }
$duplicateCount2 = if ($summary2.PSObject.Properties.Name -contains "duplicateCount") { [int]$summary2.duplicateCount } else { 0 }
if ($duplicateCount2 -gt $duplicateCount1) {
    throw "Second run increased duplicateCount unexpectedly"
}

$result = [ordered]@{
    runId = [guid]::NewGuid().ToString("N")
    stageName = "us1-idempotency-repeat-run"
    status = "passed"
    startedAt = (Get-Date).ToString("o")
    firstRun = $summary1
    secondRun = $summary2
    checks = [ordered]@{
        firstRunUpdatedChunks = $summary1.updatedChunks
        secondRunSkippedChunks = $summary2.skippedChunks
        duplicateCountStable = ($duplicateCount2 -le $duplicateCount1)
    }
}
$result | ConvertTo-Json -Depth 8 | Set-Content -Path $artifactPath -Encoding utf8

if ($env:WORKSPACE_PATH_HOST -and (Test-Path $env:WORKSPACE_PATH_HOST)) {
    Remove-Item -LiteralPath $env:WORKSPACE_PATH_HOST -Recurse -Force
}

Write-Host "US1 repeat-run completed. run1=$($run1.runId) run2=$($run2.runId) artifact=$artifactPath"
