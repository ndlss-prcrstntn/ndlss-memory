Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
$compose = Join-Path $root "infra\\docker\\docker-compose.yml"
$envFile = Join-Path $root ".env.example"
$artifactDir = Join-Path $root "tests/artifacts/quality-stability"
$artifactPath = Join-Path $artifactDir "us3-e2e-summary.json"
New-Item -ItemType Directory -Path $artifactDir -Force | Out-Null
$previousEnableHttp = [Environment]::GetEnvironmentVariable("INGESTION_ENABLE_QDRANT_HTTP", "Process")

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
    $env:INGESTION_ENABLE_QDRANT_HTTP = "1"
    Invoke-Compose -ComposeArgs @('-f', $compose, '--env-file', $envFile, 'up', '-d', '--build')

    $healthOk = $false
    for ($i = 0; $i -lt 120; $i++) {
        try {
            $health = Invoke-RestMethod -Method Get -Uri "http://localhost:8080/health" -TimeoutSec 2
            if ($health.status -eq "ok") {
                $healthOk = $true
                break
            }
        } catch {}
        Start-Sleep -Milliseconds 500
    }
    if (-not $healthOk) {
        throw "Service health did not become ok"
    }

    & (Join-Path $root "scripts/tests/us1_full_scan_recursive_indexing.ps1")
    & (Join-Path $root "scripts/tests/us1_delta_changed_only.ps1")
    & (Join-Path $root "scripts/tests/us2_quality_search_flow.ps1") -SkipComposeLifecycle

    & (Join-Path $root "scripts/tests/us1_idempotent_repeat_run.ps1")
    $first = Get-Content -Raw -Path (Join-Path $artifactDir "us1-idempotency-summary.json") | ConvertFrom-Json

    & (Join-Path $root "scripts/tests/us1_idempotent_repeat_run.ps1")
    $second = Get-Content -Raw -Path (Join-Path $artifactDir "us1-idempotency-summary.json") | ConvertFrom-Json

    if ($second.secondRun.failedChunks -gt $first.secondRun.failedChunks) {
        throw "Repeat-run consistency check failed: failedChunks increased"
    }

    $summary = [ordered]@{
        runId = [guid]::NewGuid().ToString("N")
        stageName = "us3-e2e-quality"
        status = "passed"
        generatedAt = (Get-Date).ToString("o")
        checks = [ordered]@{
            composeUp = $true
            fullScan = $true
            deltaAfterCommit = $true
            semanticSearch = $true
            repeatRunConsistency = $true
        }
    }
    $summary | ConvertTo-Json -Depth 8 | Set-Content -Path $artifactPath -Encoding utf8

    Write-Host "US3 E2E quality scenario passed. artifact=$artifactPath"
}
finally {
    if ($null -eq $previousEnableHttp) {
        Remove-Item Env:INGESTION_ENABLE_QDRANT_HTTP -ErrorAction SilentlyContinue
    } else {
        $env:INGESTION_ENABLE_QDRANT_HTTP = $previousEnableHttp
    }
    Invoke-Compose -ComposeArgs @('-f', $compose, '--env-file', $envFile, 'down')
}


