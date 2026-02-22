Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
$composeFile = Join-Path $root "infra\\docker\\docker-compose.yml"
$envFile = Join-Path $root ".env.example"
. (Join-Path $root "scripts/tests/test_ports.ps1")
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
    Invoke-Compose -ComposeArgs @('-f', $composeFile, '--env-file', $envFile, 'up', '-d', '--build')
    Invoke-Compose -ComposeArgs @('-f', $composeFile, '--env-file', $envFile, 'ps')

    & (Join-Path $root "scripts\\tests\\us1_idempotent_repeat_run.ps1")
    & (Join-Path $root "scripts\\tests\\us2_deterministic_chunk_updates.ps1")
    & (Join-Path $root "scripts\\tests\\us3_stale_chunk_cleanup.ps1")
}
finally {
    Invoke-Compose -ComposeArgs @('-f', $composeFile, '--env-file', $envFile, 'down')
}

Write-Host "Idempotency compose regression completed"


