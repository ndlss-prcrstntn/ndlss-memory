param(
    [string]$ComposeFile = "infra/docker/docker-compose.yml",
    [string]$BaseEnvFile = ".env.example"
)

$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
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

$tempEnv = Join-Path $env:TEMP "ndlss-memory-us2.env"
Copy-Item $BaseEnvFile $tempEnv -Force
$tempEnvLines = Get-Content -LiteralPath $tempEnv | Where-Object { $_ -notmatch '^\s*MCP_PORT=' -and $_ -notmatch '^\s*INDEX_MODE=' }
@($tempEnvLines + "MCP_PORT=18080" + "INDEX_MODE=delta-after-commit") | Set-Content -LiteralPath $tempEnv -Encoding ascii

try {
    Invoke-Compose -ComposeArgs @('-f', $ComposeFile, '--env-file', $tempEnv, 'up', '-d', '--build')
    Start-Sleep -Seconds 20

    $config = Invoke-RestMethod -Uri "http://localhost:18080/v1/system/config" -Method Get -TimeoutSec 10
    if ($config.indexMode -ne "delta-after-commit") {
        throw "INDEX_MODE override not applied"
    }
    if ([int]$config.mcpPort -ne 18080) {
        throw "MCP_PORT override not applied"
    }
}
finally {
    Invoke-Compose -ComposeArgs @('-f', $ComposeFile, '--env-file', $tempEnv, 'down')
    if (Test-Path $tempEnv) {
        Remove-Item -LiteralPath $tempEnv -Force
    }
}

Write-Host "US2 env override check passed"



