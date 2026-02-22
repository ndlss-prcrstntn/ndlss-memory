Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
$compose = Join-Path $root "infra\\docker\\docker-compose.yml"
$envFile = Join-Path $root ".env.example"
$debugLog = Join-Path $root "tests\\artifacts\\quality-stability\\ingestion-compose-debug.log"
$previousEnableHttp = [Environment]::GetEnvironmentVariable("INGESTION_ENABLE_QDRANT_HTTP", "Process")

function Invoke-Compose {
    param([string[]]$ComposeArgs)

    New-Item -ItemType Directory -Path (Split-Path $debugLog -Parent) -Force | Out-Null

    $stdoutFile = [System.IO.Path]::GetTempFileName()
    $stderrFile = [System.IO.Path]::GetTempFileName()
    try {
        $process = Start-Process -FilePath "docker" -ArgumentList (@("compose") + $ComposeArgs) -NoNewWindow -PassThru -Wait -RedirectStandardOutput $stdoutFile -RedirectStandardError $stderrFile
        $stdout = if (Test-Path $stdoutFile) { Get-Content -LiteralPath $stdoutFile } else { @() }
        $stderr = if (Test-Path $stderrFile) { Get-Content -LiteralPath $stderrFile } else { @() }
        $stdoutLines = @($stdout)
        $stderrLines = @($stderr)

        $logHeader = @(
            "[$((Get-Date).ToString("s"))] docker compose $($ComposeArgs -join ' ')",
            "exitCode=$($process.ExitCode)"
        )
        Add-Content -LiteralPath $debugLog -Value $logHeader
        if ($stdoutLines.Count -gt 0) {
            Add-Content -LiteralPath $debugLog -Value "stdout:"
            Add-Content -LiteralPath $debugLog -Value $stdoutLines
        }
        if ($stderrLines.Count -gt 0) {
            Add-Content -LiteralPath $debugLog -Value "stderr:"
            Add-Content -LiteralPath $debugLog -Value $stderrLines
        }
        Add-Content -LiteralPath $debugLog -Value ""

        @($stdoutLines + $stderrLines) | ForEach-Object {
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

function Invoke-ComposeUpWithRetry {
    param(
        [int]$MaxAttempts = 3,
        [int]$RetryDelaySeconds = 3
    )

    for ($attempt = 1; $attempt -le $MaxAttempts; $attempt++) {
        try {
            Invoke-Compose -ComposeArgs @('-f', $compose, '--env-file', $envFile, 'up', '-d', '--build')
            return
        }
        catch {
            $message = $_.Exception.Message
            if ($attempt -ge $MaxAttempts) {
                throw "compose up failed after $attempt attempts: $message"
            }

            Write-Host "compose up failed (attempt $attempt/$MaxAttempts): $message"
            Write-Host "attempting cleanup before retry..."
            try {
                Invoke-Compose -ComposeArgs @('-f', $compose, '--env-file', $envFile, 'down')
            }
            catch {
                Write-Host "cleanup down failed (ignored): $($_.Exception.Message)"
            }
            Start-Sleep -Seconds $RetryDelaySeconds
        }
    }
}

try {
    & (Join-Path $root "scripts\\tests\\ingestion_test_env.ps1") | Out-Null
    $env:INGESTION_ENABLE_QDRANT_HTTP = "1"
    Invoke-ComposeUpWithRetry -MaxAttempts 3 -RetryDelaySeconds 4
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


