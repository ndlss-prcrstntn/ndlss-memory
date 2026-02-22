param(
    [string]$ComposeFile = "infra/docker/docker-compose.yml",
    [string]$EnvFile = ".env.example",
    [int]$WaitSeconds = 40
)

$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}
. (Join-Path (Resolve-Path (Join-Path $PSScriptRoot "..\\..")) "scripts/tests/test_ports.ps1")
Set-DefaultTestPorts

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

try {
    Invoke-Compose -ComposeArgs @('-f', $ComposeFile, '--env-file', $EnvFile, 'up', '-d', '--build')
    Start-Sleep -Seconds $WaitSeconds

    $psOutputRaw = & docker compose -f $ComposeFile --env-file $EnvFile ps --format json 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "docker compose ps failed with exit code $LASTEXITCODE"
    }
    $psOutput = @($psOutputRaw) | ForEach-Object { $_ | ConvertFrom-Json }
    $required = @("qdrant", "file-indexer", "mcp-server")
    foreach ($svc in $required) {
        $service = $psOutput | Where-Object { $_.Service -eq $svc } | Select-Object -First 1
        if (-not $service) {
            throw "Service '$svc' is missing in compose ps output"
        }
        if ($service.State -ne "running") {
            throw "Service '$svc' is not running (state=$($service.State))"
        }
    }

    try {
        $health = Invoke-RestMethod -Uri "$(Get-TestBaseUrl)/health" -Method Get -TimeoutSec 10
        if ($health.status -ne "ok") {
            throw "Unexpected health status"
        }
    } catch {
        throw "Health endpoint check failed: $($_.Exception.Message)"
    }
}
finally {
    Invoke-Compose -ComposeArgs @('-f', $ComposeFile, '--env-file', $EnvFile, 'down')
}

Write-Host "US1 smoke check passed"


