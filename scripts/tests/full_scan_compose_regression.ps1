param(
    [string]$ComposeFile = "infra/docker/docker-compose.yml",
    [string]$EnvFile = ".env.example",
    [int]$WaitSeconds = 20
)

$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}
$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
. (Join-Path $root "scripts/tests/test_ports.ps1")
Set-DefaultTestPorts

function Run-Checks {
    $baseUrl = Get-TestBaseUrl
    powershell -NoProfile -ExecutionPolicy Bypass -File "scripts/tests/us1_full_scan_recursive_indexing.ps1" -BaseUrl $baseUrl
    powershell -NoProfile -ExecutionPolicy Bypass -File "scripts/tests/us2_full_scan_filtering.ps1" -BaseUrl $baseUrl
    powershell -NoProfile -ExecutionPolicy Bypass -File "scripts/tests/us3_full_scan_resilience.ps1" -BaseUrl $baseUrl
}

function Invoke-Compose {
    param([string[]]$ComposeArgs)

    $stdoutFile = [System.IO.Path]::GetTempFileName()
    $stderrFile = [System.IO.Path]::GetTempFileName()
    try {
        $process = Start-Process -FilePath "docker" -ArgumentList (@("compose") + $ComposeArgs) -NoNewWindow -PassThru -Wait -RedirectStandardOutput $stdoutFile -RedirectStandardError $stderrFile
        $stdout = if (Test-Path $stdoutFile) { Get-Content -LiteralPath $stdoutFile } else { @() }
        $stderr = if (Test-Path $stderrFile) { Get-Content -LiteralPath $stderrFile } else { @() }

        @($stdout + $stderr) | ForEach-Object {
            if ($_ -ne $null -and $_ -ne "") {
                Write-Host $_
            }
        }

        if ($process.ExitCode -ne 0) {
            throw "docker compose failed with exit code $($process.ExitCode) (args: $($ComposeArgs -join ' '))"
        }
    }
    finally {
        Remove-Item -LiteralPath $stdoutFile, $stderrFile -Force -ErrorAction SilentlyContinue
    }
}

$tempEnv = Join-Path $env:TEMP "ndlss-memory-delta-regression.env"
$previousIndexMode = [Environment]::GetEnvironmentVariable("INDEX_MODE", "Process")
$previousPreflightGitRequired = [Environment]::GetEnvironmentVariable("STARTUP_PREFLIGHT_REQUIRE_GIT_FOR_DELTA", "Process")
try {
    Invoke-Compose -ComposeArgs @('-f', $ComposeFile, '--env-file', $EnvFile, 'up', '-d', '--build')
    Start-Sleep -Seconds $WaitSeconds

    Run-Checks

    Copy-Item $EnvFile $tempEnv -Force
    $envLines = Get-Content -LiteralPath $tempEnv | Where-Object { $_ -notmatch '^\s*INDEX_MODE=' }
    @(
        $envLines
        "INDEX_MODE=delta-after-commit"
        "STARTUP_PREFLIGHT_REQUIRE_GIT_FOR_DELTA=0"
    ) | Set-Content -LiteralPath $tempEnv -Encoding ascii
    $env:INDEX_MODE = "delta-after-commit"
    $env:STARTUP_PREFLIGHT_REQUIRE_GIT_FOR_DELTA = "0"

    Invoke-Compose -ComposeArgs @('-f', $ComposeFile, '--env-file', $tempEnv, 'up', '-d', '--build')
    Start-Sleep -Seconds $WaitSeconds

    $cfg = Invoke-RestMethod -Uri "$(Get-TestBaseUrl)/v1/system/config" -Method Get -TimeoutSec 10
    if ($cfg.indexMode -ne "delta-after-commit") {
        throw "Expected delta-after-commit mode after env override"
    }

    Write-Host "Full scan compose regression check passed"
}
finally {
    if ($null -eq $previousIndexMode) {
        Remove-Item Env:INDEX_MODE -ErrorAction SilentlyContinue
    } else {
        $env:INDEX_MODE = $previousIndexMode
    }
    if ($null -eq $previousPreflightGitRequired) {
        Remove-Item Env:STARTUP_PREFLIGHT_REQUIRE_GIT_FOR_DELTA -ErrorAction SilentlyContinue
    } else {
        $env:STARTUP_PREFLIGHT_REQUIRE_GIT_FOR_DELTA = $previousPreflightGitRequired
    }
    if (Test-Path $tempEnv) {
        Remove-Item -LiteralPath $tempEnv -Force
    }
    Invoke-Compose -ComposeArgs @('-f', $ComposeFile, '--env-file', $EnvFile, 'down')
}



