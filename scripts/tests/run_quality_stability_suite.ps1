param(
    [switch]$SkipUnit,
    [switch]$SkipIntegration,
    [switch]$SkipContract,
    [switch]$SkipE2E,
    [string]$ArtifactsDir = "tests/artifacts/quality-stability"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
$runner = Join-Path $root "scripts/tests/quality_gate_runner.ps1"
$regressionLog = Join-Path $root "$ArtifactsDir/final-regression-log.md"
New-Item -ItemType Directory -Path (Split-Path -Parent $regressionLog) -Force | Out-Null

$runnerParams = @{
    ArtifactsDir = $ArtifactsDir
}
if ($SkipUnit) { $runnerParams.SkipUnit = $true }
if ($SkipIntegration) { $runnerParams.SkipIntegration = $true }
if ($SkipContract) { $runnerParams.SkipContract = $true }
if ($SkipE2E) { $runnerParams.SkipE2E = $true }

$start = Get-Date
$argText = ($runnerParams.GetEnumerator() | ForEach-Object { "-$($_.Key) $($_.Value)" }) -join " "
$header = @(
    "# Quality Stability Run",
    "",
    "- startedAt: $($start.ToString('o'))",
    "- args: $argText",
    ""
)
$header | Set-Content -Path $regressionLog -Encoding utf8

Write-Host "[suite] started at $($start.ToString('o'))"
Write-Host "[suite] args: $argText"
Write-Host "[suite] includes mcp_transport compatibility stage via quality_gate_runner.ps1"
$runnerOutput = & $runner @runnerParams *>&1 | ForEach-Object {
    $line = if ($_ -is [System.Management.Automation.ErrorRecord]) {
        $_.ToString()
    } else {
        [string]$_
    }
    if ($line -ne "") {
        Add-Content -Path $regressionLog -Value $line -Encoding utf8
        Write-Host $line
    }
}
$exitCode = $LASTEXITCODE

if ($null -ne $runnerOutput) {
    $null = $runnerOutput
}

$end = Get-Date
@(
    "",
    "- finishedAt: $($end.ToString('o'))",
    "- exitCode: $exitCode"
) | Add-Content -Path $regressionLog -Encoding utf8

exit $exitCode
