param(
    [string]$ComposeFile = "infra/docker/docker-compose.yml",
    [string]$EnvFile = ".env.example",
    [int]$WaitSeconds = 20
)

$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

function Run-Checks {
    powershell -NoProfile -ExecutionPolicy Bypass -File "scripts/tests/us1_full_scan_recursive_indexing.ps1"
    powershell -NoProfile -ExecutionPolicy Bypass -File "scripts/tests/us2_full_scan_filtering.ps1"
    powershell -NoProfile -ExecutionPolicy Bypass -File "scripts/tests/us3_full_scan_resilience.ps1"
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
try {
    Invoke-Compose -ComposeArgs @('-f', $ComposeFile, '--env-file', $EnvFile, 'up', '-d', '--build')
    Start-Sleep -Seconds $WaitSeconds

    Run-Checks

    Copy-Item $EnvFile $tempEnv -Force
    $envLines = Get-Content -LiteralPath $tempEnv | Where-Object { $_ -notmatch '^\s*INDEX_MODE=' }
    @($envLines + "INDEX_MODE=delta-after-commit") | Set-Content -LiteralPath $tempEnv -Encoding ascii
    $env:INDEX_MODE = "delta-after-commit"

    Invoke-Compose -ComposeArgs @('-f', $ComposeFile, '--env-file', $tempEnv, 'up', '-d', '--build')
    Start-Sleep -Seconds $WaitSeconds

    $cfg = Invoke-RestMethod -Uri "http://localhost:8080/v1/system/config" -Method Get -TimeoutSec 10
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
    if (Test-Path $tempEnv) {
        Remove-Item -LiteralPath $tempEnv -Force
    }
    Invoke-Compose -ComposeArgs @('-f', $ComposeFile, '--env-file', $EnvFile, 'down')
}



