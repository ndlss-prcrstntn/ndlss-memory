param(
    [switch]$SkipComposeLifecycle
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
. (Join-Path $root "scripts/tests/test_ports.ps1")
Set-DefaultTestPorts
& (Join-Path $root "scripts/tests/ingestion_test_env.ps1") -WorkspacePath "tests/fixtures/idempotency" | Out-Null

$composeFile = Join-Path $root "infra\\docker\\docker-compose.yml"
$envFile = Join-Path $root ".env.example"
$tempEnvFile = Join-Path $env:TEMP "ndlss-memory-us1-ingestion.env"
$manageComposeLifecycle = -not $SkipComposeLifecycle

$artifactDir = Join-Path $root "tests/artifacts/quality-stability"
New-Item -ItemType Directory -Path $artifactDir -Force | Out-Null
$artifactPath = Join-Path $artifactDir "us1-ingestion-collection-summary.json"

$mcpPort = Get-TestMcpPort
$qdrantPort = Get-TestQdrantPort
$baseUrl = "http://localhost:$mcpPort"
$qdrantBaseUrl = "http://localhost:$qdrantPort"
$workspacePathContainer = "/workspace/tests/fixtures/idempotency"
$collectionName = if ($env:QDRANT_COLLECTION_NAME) { $env:QDRANT_COLLECTION_NAME } else { "workspace_chunks" }

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
            Where-Object { $_ -notmatch '^\s*INGESTION_ENABLE_QDRANT_HTTP=' -and $_ -notmatch '^\s*QDRANT_API_PORT=' }
        @($envLines + "INGESTION_ENABLE_QDRANT_HTTP=1" + "QDRANT_API_PORT=6333") | Set-Content -LiteralPath $tempEnvFile -Encoding ascii
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
        throw "MCP health did not become ok in US1 ingestion collection creation test"
    }

    $collectionMissingBefore = $false
    try {
        $null = Invoke-RestMethod -Method Get -Uri "$qdrantBaseUrl/collections/$collectionName" -TimeoutSec 5
        Invoke-RestMethod -Method Delete -Uri "$qdrantBaseUrl/collections/$collectionName" -TimeoutSec 10 | Out-Null
        Start-Sleep -Seconds 1
        $collectionMissingBefore = $true
    } catch {
        $collectionMissingBefore = $true
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
    if ($null -eq $status -or $status.status -notin @("completed", "partial", "failed")) {
        throw "Ingestion status polling timed out for runId=$runId"
    }
    if ($status.status -ne "completed") {
        throw "Ingestion did not complete successfully. status=$($status.status) errorCode=$($status.errorCode) errorMessage=$($status.errorMessage)"
    }

    $summary = Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/indexing/ingestion/jobs/$runId/summary"
    if ($summary.failedChunks -gt 0) {
        throw "Ingestion summary reported failed chunks ($($summary.failedChunks))"
    }

    $collection = Invoke-RestMethod -Method Get -Uri "$qdrantBaseUrl/collections/$collectionName"
    $countResponse = Invoke-RestMethod -Method Post -Uri "$qdrantBaseUrl/collections/$collectionName/points/count" -ContentType "application/json" -Body '{"exact":true}'
    $count = [int]$countResponse.result.count
    if ($count -le 0) {
        throw "Collection '$collectionName' contains no points after ingestion"
    }

    [ordered]@{
        runId = [guid]::NewGuid().ToString("N")
        stageName = "us1-ingestion-collection-creation"
        status = "passed"
        generatedAt = (Get-Date).ToString("o")
        ingestionRunId = $runId
        collectionName = $collectionName
        collectionMissingBefore = $collectionMissingBefore
        pointsCount = $count
        persistence = $summary.persistence
    } | ConvertTo-Json -Depth 8 | Set-Content -Path $artifactPath -Encoding utf8

    Write-Host "US1 ingestion collection creation passed. runId=$runId points=$count artifact=$artifactPath"
}
finally {
    if ($manageComposeLifecycle) {
        Invoke-Compose -ComposeArgs @('-f', $composeFile, '--env-file', $tempEnvFile, 'down')
        if (Test-Path $tempEnvFile) {
            Remove-Item -LiteralPath $tempEnvFile -Force
        }
    }
}
