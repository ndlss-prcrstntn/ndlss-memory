Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
$compose = Join-Path $root "infra\\docker\\docker-compose.yml"
$envFile = Join-Path $root ".env.example"
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
    Invoke-Compose -ComposeArgs @('-f', $compose, '--env-file', $envFile, 'ps')

    & (Join-Path $root "scripts\\tests\\us1_chunking_deterministic.ps1")
    & (Join-Path $root "scripts\\tests\\us2_embedding_retry_upsert.ps1")
    & (Join-Path $root "scripts\\tests\\us2_quality_search_flow.ps1") -SkipComposeLifecycle
    & (Join-Path $root "scripts\\tests\\us3_metadata_traceability.ps1")

    $baseUrl = "http://localhost:8080"
    if ($env:MCP_PORT) {
        $baseUrl = "http://localhost:$($env:MCP_PORT)"
    }
    $search = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/search/semantic" -ContentType "application/json" -Body '{"query":"readme","limit":3}'
    if (-not ($search.PSObject.Properties.Name -contains "results")) {
        throw "Ingestion regression search response has no results field"
    }
}
finally {
    if ($null -eq $previousEnableHttp) {
        Remove-Item Env:INGESTION_ENABLE_QDRANT_HTTP -ErrorAction SilentlyContinue
    } else {
        $env:INGESTION_ENABLE_QDRANT_HTTP = $previousEnableHttp
    }
    Invoke-Compose -ComposeArgs @('-f', $compose, '--env-file', $envFile, 'down')
}

Write-Host "Ingestion compose regression completed"


