Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
$artifactDir = Join-Path $root "tests/artifacts/quality-stability"
New-Item -ItemType Directory -Path $artifactDir -Force | Out-Null
$summaryPath = Join-Path $artifactDir "contract-check-summary.md"

$checks = @()

function Add-CheckResult {
    param(
        [string]$Name,
        [bool]$Passed,
        [string]$Details
    )

    $script:checks += [pscustomobject]@{
        Name = $Name
        Passed = $Passed
        Details = $Details
    }
}

$requiredFiles = @(
    "tests/contract/quality_stage_result_contract.md",
    "tests/contract/mcp_search_tools_contract.md",
    "specs/008-quality-stability-tests/contracts/quality-stability-tests.openapi.yaml",
    "services/mcp-server/openapi/quality-stability-tests.openapi.yaml"
)

foreach ($file in $requiredFiles) {
    $exists = Test-Path (Join-Path $root $file)
    Add-CheckResult -Name "file:$file" -Passed $exists -Details ($(if ($exists) { "exists" } else { "missing" }))
}

$openApiPath = Join-Path $root "specs/008-quality-stability-tests/contracts/quality-stability-tests.openapi.yaml"
if (Test-Path $openApiPath) {
    $openApiRaw = Get-Content -Raw -Path $openApiPath
    $requiredPatterns = @(
        "/v1/indexing/full-scan/jobs",
        "/v1/indexing/delta-after-commit/jobs",
        "/v1/indexing/idempotency/jobs",
        "/v1/search/semantic",
        "/v1/search/results/{resultId}/source",
        "/v1/search/results/{resultId}/metadata",
        "components:",
        "ApiError"
    )

    foreach ($pattern in $requiredPatterns) {
        $ok = $openApiRaw -match [regex]::Escape($pattern)
        Add-CheckResult -Name "openapi:$pattern" -Passed $ok -Details ($(if ($ok) { "present" } else { "missing" }))
    }
}

$contractPath = Join-Path $root "tests/contract/quality_stage_result_contract.md"
if (Test-Path $contractPath) {
    $contractRaw = Get-Content -Raw -Path $contractPath
    $mustHave = @("stageName", "status", "durationMs", "runId", "failures")
    foreach ($item in $mustHave) {
        $ok = $contractRaw -match [regex]::Escape($item)
        Add-CheckResult -Name "stage-contract:$item" -Passed $ok -Details ($(if ($ok) { "present" } else { "missing" }))
    }
}

$failed = @($checks | Where-Object { -not $_.Passed })

$lines = @()
$lines += "# Contract Check Summary"
$lines += ""
$lines += "| Check | Status | Details |"
$lines += "|-------|--------|---------|"
foreach ($row in $checks) {
    $status = if ($row.Passed) { "PASS" } else { "FAIL" }
    $lines += "| $($row.Name) | $status | $($row.Details) |"
}
$lines += ""
$lines += "- total: $(@($checks).Count)"
$lines += "- failed: $($failed.Count)"
$lines += "- generatedAt: $((Get-Date).ToString('o'))"

$lines | Set-Content -Path $summaryPath -Encoding utf8

if ($failed.Count -gt 0) {
    Write-Host "Contract checks failed. See $summaryPath"
    exit 1
}

Write-Host "Contract checks passed. Summary: $summaryPath"
