param(
    [switch]$SkipComposeLifecycle
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
& (Join-Path $root "scripts/tests/ingestion_test_env.ps1") -WorkspacePath "tests/fixtures/idempotency" | Out-Null

$composeFile = Join-Path $root "infra\\docker\\docker-compose.yml"
$envFile = Join-Path $root ".env.example"
$tempEnvFile = Join-Path $env:TEMP "ndlss-memory-us2-custom-port.env"
$manageComposeLifecycle = -not $SkipComposeLifecycle

$artifactDir = Join-Path $root "tests/artifacts/quality-stability"
New-Item -ItemType Directory -Path $artifactDir -Force | Out-Null
$artifactPath = Join-Path $artifactDir "us2-custom-port-summary.json"

$mcpPort = if ($env:MCP_PORT) { $env:MCP_PORT } else { "18080" }
$qdrantPort = if ($env:QDRANT_PORT) { $env:QDRANT_PORT } else { "16333" }
$baseUrl = "http://localhost:$mcpPort"
$workspacePathContainer = "/workspace/tests/fixtures/idempotency"

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
    if ($manageComposeLifecycle) {
        Copy-Item -LiteralPath $envFile -Destination $tempEnvFile -Force
        $envLines = Get-Content -LiteralPath $tempEnvFile |
            Where-Object {
                $_ -notmatch '^\s*MCP_PORT=' -and
                $_ -notmatch '^\s*QDRANT_PORT=' -and
                $_ -notmatch '^\s*QDRANT_API_PORT=' -and
                $_ -notmatch '^\s*INGESTION_ENABLE_QDRANT_HTTP='
            }
        @(
            $envLines
            "MCP_PORT=$mcpPort"
            "QDRANT_PORT=$qdrantPort"
            "QDRANT_API_PORT=6333"
            "INGESTION_ENABLE_QDRANT_HTTP=1"
        ) | Set-Content -LiteralPath $tempEnvFile -Encoding ascii

        Invoke-Compose -ComposeArgs @('-f', $composeFile, '--env-file', $tempEnvFile, 'up', '-d', '--build')
    }

    $healthy = $false
    for ($i = 0; $i -lt 120; $i++) {
        try {
            $health = Invoke-RestMethod -Method Get -Uri "$baseUrl/health" -TimeoutSec 2
            if ($health.status -eq "ok") {
                $healthy = $true
                break
            }
        } catch {
        }
        Start-Sleep -Milliseconds 500
    }
    if (-not $healthy) {
        throw "MCP health did not become ok with custom external QDRANT_PORT=$qdrantPort"
    }

    $run = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/indexing/ingestion/jobs" -ContentType "application/json" -Body (@{ workspacePath = $workspacePathContainer } | ConvertTo-Json -Compress)
    $runId = $run.runId

    $status = $null
    for ($i = 0; $i -lt 180; $i++) {
        $status = Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/indexing/ingestion/jobs/$runId"
        if ($status.status -in @("completed", "failed", "partial")) {
            break
        }
        Start-Sleep -Milliseconds 500
    }
    if ($null -eq $status -or $status.status -notin @("completed", "failed", "partial")) {
        throw "Ingestion status polling timed out for runId=$runId"
    }
    if ($status.status -eq "failed") {
        throw "Ingestion failed under custom port configuration. errorCode=$($status.errorCode) errorMessage=$($status.errorMessage)"
    }

    $searchBody = @{ query = "readme"; limit = 5 } | ConvertTo-Json -Compress
    $search = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/search/semantic" -ContentType "application/json" -Body $searchBody
    if (-not ($search.PSObject.Properties.Name -contains "status")) {
        throw "Semantic search response missing status under custom QDRANT_PORT"
    }

    [ordered]@{
        runId = [guid]::NewGuid().ToString("N")
        stageName = "us2-custom-qdrant-external-port"
        status = "passed"
        generatedAt = (Get-Date).ToString("o")
        mcpPort = [int]$mcpPort
        qdrantExternalPort = [int]$qdrantPort
        ingestionRunId = $runId
        ingestionStatus = $status.status
        ingestionErrorCode = $status.errorCode
        searchStatus = $search.status
        searchResultCount = @($search.results).Count
    } | ConvertTo-Json -Depth 8 | Set-Content -Path $artifactPath -Encoding utf8

    Write-Host "US2 custom external port scenario passed. runId=$runId artifact=$artifactPath"
}
finally {
    if ($manageComposeLifecycle) {
        Invoke-Compose -ComposeArgs @('-f', $composeFile, '--env-file', $tempEnvFile, 'down')
        if (Test-Path $tempEnvFile) {
            Remove-Item -LiteralPath $tempEnvFile -Force
        }
    }
}
