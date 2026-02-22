param(
    [switch]$SkipComposeLifecycle
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
& (Join-Path $root "scripts\tests\ingestion_test_env.ps1") -WorkspacePath "tests/fixtures/idempotency" | Out-Null

$baseUrl = "http://localhost:8080"
if ($env:MCP_PORT) {
    $baseUrl = "http://localhost:$($env:MCP_PORT)"
}
$composeFile = Join-Path $root "infra\docker\docker-compose.yml"
$envFile = Join-Path $root ".env.example"
$tempEnvFile = Join-Path $env:TEMP "ndlss-memory-us2-quality.env"
$previousEnableHttp = [Environment]::GetEnvironmentVariable("INGESTION_ENABLE_QDRANT_HTTP", "Process")
$manageComposeLifecycle = -not $SkipComposeLifecycle

$artifactDir = Join-Path $root "tests/artifacts/quality-stability"
New-Item -ItemType Directory -Path $artifactDir -Force | Out-Null
$artifactPath = Join-Path $artifactDir "us2-integration-summary.json"
$workspacePathContainer = "/workspace/tests/fixtures/idempotency"
$qdrantPort = if ($env:QDRANT_PORT) { $env:QDRANT_PORT } else { "6333" }
$qdrantBaseUrl = "http://localhost:$qdrantPort"
$qdrantCollection = if ($env:QDRANT_COLLECTION_NAME) { $env:QDRANT_COLLECTION_NAME } else { "workspace_chunks" }
$embeddingVectorSize = if ($env:INGESTION_EMBEDDING_VECTOR_SIZE) { [int]$env:INGESTION_EMBEDDING_VECTOR_SIZE } else { 16 }

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
    if ($manageComposeLifecycle) {
        Copy-Item -LiteralPath $envFile -Destination $tempEnvFile -Force
        $tempEnvLines = Get-Content -LiteralPath $tempEnvFile | Where-Object { $_ -notmatch '^\s*INGESTION_ENABLE_QDRANT_HTTP=' }
        @($tempEnvLines + "INGESTION_ENABLE_QDRANT_HTTP=1") | Set-Content -LiteralPath $tempEnvFile -Encoding ascii
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
        throw "MCP health did not become ok in US2 search flow"
    }

    $collectionExists = $true
    try {
        $null = Invoke-RestMethod -Method Get -Uri "$qdrantBaseUrl/collections/$qdrantCollection" -TimeoutSec 5
    } catch {
        $collectionExists = $false
    }
    if (-not $collectionExists) {
        $collectionBody = @{
            vectors = @{
                size = $embeddingVectorSize
                distance = "Cosine"
            }
        } | ConvertTo-Json -Depth 5
        $null = Invoke-RestMethod -Method Put -Uri "$qdrantBaseUrl/collections/$qdrantCollection" -ContentType "application/json" -Body $collectionBody -TimeoutSec 10
    }

    $ingestionBody = @{ workspacePath = $workspacePathContainer } | ConvertTo-Json -Compress
    $run = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/indexing/ingestion/jobs" -ContentType "application/json" -Body $ingestionBody
    $runId = $run.runId
    for ($i = 0; $i -lt 120; $i++) {
        $status = Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/indexing/ingestion/jobs/$runId"
        if ($status.status -in @("completed", "failed", "partial")) {
            break
        }
        Start-Sleep -Milliseconds 500
    }

    $summary = Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/indexing/ingestion/jobs/$runId/summary"
    if ($summary.failedChunks -gt 0) {
        throw "Ingestion failedChunks is greater than zero for runId=$runId"
    }

    $searchBody = @{ query = "readme"; limit = 5; filters = @{ fileType = ".md" } } | ConvertTo-Json -Depth 6
    try {
        $search = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/search/semantic" -ContentType "application/json" -Body $searchBody
    } catch {
        if ($_.Exception.Response) {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $responseBody = $reader.ReadToEnd()
            throw "Semantic search request failed: $responseBody"
        }
        throw
    }

    if (-not ($search.PSObject.Properties.Name -contains "status")) {
        throw "Semantic search response has no status"
    }
    if (-not ($search.PSObject.Properties.Name -contains "results")) {
        throw "Semantic search response has no results"
    }

    $resultCount = @($search.results).Count
    $sourceChecked = $false
    $metadataChecked = $false
    if ($resultCount -gt 0) {
        $resultId = $search.results[0].resultId
        $source = Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/search/results/$resultId/source"
        $metadata = Invoke-RestMethod -Method Get -Uri "$baseUrl/v1/search/results/$resultId/metadata"
        if ($source.status -ne "ok") {
            throw "Source endpoint did not return status=ok"
        }
        if ($metadata.status -ne "ok") {
            throw "Metadata endpoint did not return status=ok"
        }
        $sourceChecked = $true
        $metadataChecked = $true
    }

    $result = [ordered]@{
        runId = [guid]::NewGuid().ToString("N")
        stageName = "us2-integration-search"
        status = "passed"
        generatedAt = (Get-Date).ToString("o")
        ingestionRunId = $runId
        ingestionSummary = $summary
        searchStatus = $search.status
        searchResultCount = $resultCount
        sourceChecked = $sourceChecked
        metadataChecked = $metadataChecked
    }
    $result | ConvertTo-Json -Depth 8 | Set-Content -Path $artifactPath -Encoding utf8

    Write-Host "US2 search flow completed. ingestionRunId=$runId results=$resultCount artifact=$artifactPath"
}
finally {
    if ($null -eq $previousEnableHttp) {
        Remove-Item Env:INGESTION_ENABLE_QDRANT_HTTP -ErrorAction SilentlyContinue
    } else {
        $env:INGESTION_ENABLE_QDRANT_HTTP = $previousEnableHttp
    }
    if ($manageComposeLifecycle) {
        Invoke-Compose -ComposeArgs @('-f', $composeFile, '--env-file', $tempEnvFile, 'down')
        if (Test-Path $tempEnvFile) {
            Remove-Item -LiteralPath $tempEnvFile -Force
        }
    }
}
