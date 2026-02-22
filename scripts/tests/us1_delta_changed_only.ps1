Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

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

Copy-Item -Path (Join-Path $root "tests\fixtures\delta-after-commit\changes\added.md") -Destination (Join-Path $workspaceHost "docs\added.md") -Force
Add-Content -Path (Join-Path $workspaceHost "docs\stable.md") -Value "`n$(Get-Content -Raw (Join-Path $root "tests\fixtures\delta-after-commit\changes\modified-extra.txt"))"

Push-Location $workspaceHost
try {
    $prevErrorAction = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        git add . 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "git add failed with exit code $LASTEXITCODE"
        }
        git commit -m "us1 added and modified" 2>$null | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "git commit failed with exit code $LASTEXITCODE"
        }
    } finally {
        $ErrorActionPreference = $prevErrorAction
    }
} finally {
    Pop-Location
}

$body = @{
    workspacePath = $workspaceContainer
    baseRef = "HEAD~1"
    targetRef = "HEAD"
} | ConvertTo-Json -Compress

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

$run = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/indexing/delta-after-commit/jobs" -ContentType "application/json" -Body $body
$summary = Wait-DeltaSummary -runId $run.runId

if ($summary.effectiveMode -ne "delta-after-commit") {
    throw "Expected effectiveMode=delta-after-commit, got '$($summary.effectiveMode)'"
}
if ($summary.addedFiles -lt 1) {
    throw "Expected addedFiles >= 1"
}
if ($summary.modifiedFiles -lt 1) {
    throw "Expected modifiedFiles >= 1"
}
if ($summary.indexedFiles -lt 1) {
    throw "Expected indexedFiles >= 1"
}

if ($env:WORKSPACE_PATH_HOST -and (Test-Path $env:WORKSPACE_PATH_HOST)) {
    Remove-Item -LiteralPath $env:WORKSPACE_PATH_HOST -Recurse -Force
}

Write-Host "US1 delta changed-only completed. run=$($run.runId)"
