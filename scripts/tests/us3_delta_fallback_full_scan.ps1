Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
. (Join-Path $root "scripts/tests/test_ports.ps1")
Set-DefaultTestPorts
& (Join-Path $root "scripts\tests\delta_after_commit_test_env.ps1") | Out-Null

$baseUrl = Get-TestBaseUrl

for ($i = 0; $i -lt 120; $i++) {
    try {
        $health = Invoke-RestMethod -Method Get -Uri "$baseUrl/health" -TimeoutSec 2
        if ($health.status -eq "ok") {
            break
        }
    } catch {}
    Start-Sleep -Milliseconds 500
}

$workspaceContainer = $env:WORKSPACE_PATH_CONTAINER
if (-not $workspaceContainer) {
    throw "WORKSPACE_PATH_CONTAINER is required"
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

$deltaBody = @{
    workspacePath = $workspaceContainer
    baseRef = "definitely-missing-ref"
    targetRef = "HEAD"
} | ConvertTo-Json -Compress

$run = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/indexing/delta-after-commit/jobs" -ContentType "application/json" -Body $deltaBody
$summary = Wait-DeltaSummary -runId $run.runId

if ($summary.effectiveMode -ne "full-scan-fallback") {
    throw "Expected effectiveMode=full-scan-fallback, got '$($summary.effectiveMode)'"
}
if (-not $summary.fallbackReasonCode) {
    throw "Expected fallbackReasonCode to be present"
}

if ($env:WORKSPACE_PATH_HOST -and (Test-Path $env:WORKSPACE_PATH_HOST)) {
    Remove-Item -LiteralPath $env:WORKSPACE_PATH_HOST -Recurse -Force
}

Write-Host "US3 delta fallback completed. run=$($run.runId) reason=$($summary.fallbackReasonCode)"
