Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
& (Join-Path $root "scripts\tests\delta_after_commit_test_env.ps1") | Out-Null

$baseUrl = "http://localhost:8080"
if ($env:MCP_PORT) {
    $baseUrl = "http://localhost:$($env:MCP_PORT)"
}

for ($i = 0; $i -lt 120; $i++) {
    try {
        $health = Invoke-RestMethod -Method Get -Uri "$baseUrl/health" -TimeoutSec 2
        if ($health.status -eq "ok") {
            break
        }
    } catch {}
    Start-Sleep -Milliseconds 500
}

$workspaceHost = $env:WORKSPACE_PATH_HOST
$workspaceContainer = $env:WORKSPACE_PATH_CONTAINER
if (-not $workspaceHost -or -not $workspaceContainer) {
    throw "WORKSPACE_PATH_HOST/WORKSPACE_PATH_CONTAINER are required"
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

function Wait-DeltaSummary([string]$runId) {
    for ($i = 0; $i -lt 120; $i++) {
        $status = Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/indexing/delta-after-commit/jobs/$runId"
        if ($status.status -in @("completed", "partial", "failed")) {
            break
        }
        Start-Sleep -Milliseconds 500
    }
    return Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/indexing/delta-after-commit/jobs/$runId/summary"
}

$seedBody = @{ workspacePath = $workspaceContainer } | ConvertTo-Json -Compress
$seedRun = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/indexing/idempotency/jobs" -ContentType "application/json" -Body $seedBody
$null = Wait-IdempotencySummary -runId $seedRun.runId

Remove-Item -LiteralPath (Join-Path $workspaceHost "docs\delete-me.md") -Force
Move-Item -LiteralPath (Join-Path $workspaceHost "docs\rename-me.md") -Destination (Join-Path $workspaceHost "docs\renamed.md")

Push-Location $workspaceHost
try {
    git add -A
    git commit -m "us2 delete and rename" | Out-Null
} finally {
    Pop-Location
}

$deltaBody = @{
    workspacePath = $workspaceContainer
    baseRef = "HEAD~1"
    targetRef = "HEAD"
} | ConvertTo-Json -Compress

$run = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/indexing/delta-after-commit/jobs" -ContentType "application/json" -Body $deltaBody
$summary = Wait-DeltaSummary -runId $run.runId

if ($summary.deletedFiles -lt 1) {
    throw "Expected deletedFiles >= 1"
}
if ($summary.renamedFiles -lt 1) {
    throw "Expected renamedFiles >= 1"
}
if ($summary.removedRecords -lt 1) {
    throw "Expected removedRecords >= 1"
}

if ($env:WORKSPACE_PATH_HOST -and (Test-Path $env:WORKSPACE_PATH_HOST)) {
    Remove-Item -LiteralPath $env:WORKSPACE_PATH_HOST -Recurse -Force
}

Write-Host "US2 delta delete+rename completed. run=$($run.runId)"
