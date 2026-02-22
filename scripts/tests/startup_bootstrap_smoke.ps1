param(
    [string]$BaseUrl = "",
    [string]$QdrantUrl = "",
    [int]$McpPort = 18080,
    [int]$QdrantPort = 16333,
    [int]$ReadyTimeoutSeconds = 180,
    [string]$ArtifactPath = "",
    [switch]$SkipComposeStart
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
. (Join-Path $root "scripts/tests/test_ports.ps1")
Set-DefaultTestPorts
$composeFile = Join-Path $root "infra\\docker\\docker-compose.yml"
$envFile = Join-Path $root ".env.example"
$tempEnvFile = Join-Path $env:TEMP "ndlss-memory-startup-bootstrap.env"
$artifactDir = Join-Path $root "tests/artifacts/quality-stability"
New-Item -ItemType Directory -Path $artifactDir -Force | Out-Null
if (-not $ArtifactPath) {
    $ArtifactPath = Join-Path $artifactDir "startup-bootstrap-smoke.json"
}
if (-not $PSBoundParameters.ContainsKey("McpPort")) {
    $McpPort = [int](Get-TestMcpPort)
}
if (-not $PSBoundParameters.ContainsKey("QdrantPort")) {
    $QdrantPort = [int](Get-TestQdrantPort)
}

$startedByScript = $false

function Save-Artifact {
    param([hashtable]$Payload)
    $targetDir = Split-Path -Parent $ArtifactPath
    if ($targetDir) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    }
    $Payload | ConvertTo-Json -Depth 12 | Set-Content -Path $ArtifactPath -Encoding utf8
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
    } finally {
        Remove-Item -LiteralPath $stdoutFile, $stderrFile -Force -ErrorAction SilentlyContinue
    }
}

function Wait-Healthy {
    param([string]$Url, [int]$TimeoutSeconds)

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        try {
            $health = Invoke-RestMethod -Method Get -Uri "$Url/health" -TimeoutSec 3
            if ($health.status -eq "ok") {
                return
            }
        } catch {
        }
        Start-Sleep -Milliseconds 500
    }
    throw "MCP health endpoint did not become ready in $TimeoutSeconds seconds"
}

function Wait-BootstrapReady {
    param([string]$Url, [int]$TimeoutSeconds)

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    $last = $null
    while ((Get-Date) -lt $deadline) {
        try {
            $last = Invoke-RestMethod -Method Get -Uri "$Url/v1/system/startup/readiness" -TimeoutSec 3
            if ($last.bootstrap.status -eq "ready" -and $last.collection.exists -eq $true) {
                return $last
            }
            if ($last.bootstrap.status -eq "failed") {
                throw "Bootstrap failed: code=$($last.bootstrap.errorCode) reason=$($last.bootstrap.reason)"
            }
        } catch {
            $last = $null
        }
        Start-Sleep -Seconds 1
    }
    throw "Startup readiness did not report bootstrap ready in $TimeoutSeconds seconds"
}

function Get-PointCount {
    param([string]$Url, [string]$CollectionName)
    $body = '{"exact":false}'
    $result = Invoke-RestMethod -Method Post -Uri "$Url/collections/$CollectionName/points/count" -ContentType "application/json" -Body $body -TimeoutSec 10
    return [int]$result.result.count
}

try {
    & (Join-Path $root "scripts/tests/idempotency_test_env.ps1") -WorkspacePath "tests/fixtures/idempotency" | Out-Null

    $resolvedBaseUrl = if ($BaseUrl) { $BaseUrl } else { "http://localhost:$McpPort" }
    $resolvedQdrantUrl = if ($QdrantUrl) { $QdrantUrl } else { "http://localhost:$QdrantPort" }

    if (-not $SkipComposeStart) {
        Copy-Item -LiteralPath $envFile -Destination $tempEnvFile -Force
        $envLines = Get-Content -LiteralPath $tempEnvFile |
            Where-Object {
                $_ -notmatch '^\s*HOST_WORKSPACE_PATH=' -and
                $_ -notmatch '^\s*INGESTION_ENABLE_QDRANT_HTTP=' -and
                $_ -notmatch '^\s*BOOTSTRAP_AUTO_INGEST_ON_START=' -and
                $_ -notmatch '^\s*BOOTSTRAP_RETRY_FAILED_ON_START=' -and
                $_ -notmatch '^\s*QDRANT_API_PORT=' -and
                $_ -notmatch '^\s*MCP_PORT=' -and
                $_ -notmatch '^\s*QDRANT_PORT='
            }
        @(
            $envLines
            "HOST_WORKSPACE_PATH=$($env:WORKSPACE_PATH_HOST)"
            "INGESTION_ENABLE_QDRANT_HTTP=1"
            "BOOTSTRAP_AUTO_INGEST_ON_START=1"
            "BOOTSTRAP_RETRY_FAILED_ON_START=1"
            "QDRANT_API_PORT=6333"
            "MCP_PORT=$McpPort"
            "QDRANT_PORT=$QdrantPort"
        ) | Set-Content -LiteralPath $tempEnvFile -Encoding utf8

        Invoke-Compose -ComposeArgs @("-f", $composeFile, "--env-file", $tempEnvFile, "up", "-d", "--build")
        $startedByScript = $true
    }

    Wait-Healthy -Url $resolvedBaseUrl -TimeoutSeconds $ReadyTimeoutSeconds
    $ready = Wait-BootstrapReady -Url $resolvedBaseUrl -TimeoutSeconds $ReadyTimeoutSeconds

    $collectionName = [string]$ready.collection.collectionName
    $pointCount = Get-PointCount -Url $resolvedQdrantUrl -CollectionName $collectionName
    if ($pointCount -le 0) {
        throw "Collection '$collectionName' has no indexed points after bootstrap"
    }

    Save-Artifact -Payload @{
        stageName = "startup-bootstrap-smoke"
        status = "passed"
        generatedAt = (Get-Date).ToString("o")
        readiness = $ready
        pointCount = $pointCount
        collectionName = $collectionName
        mcpPort = $McpPort
        qdrantPort = $QdrantPort
    }
    Write-Host "startup bootstrap smoke passed: collection=$collectionName points=$pointCount artifact=$ArtifactPath"
}
finally {
    if ($startedByScript) {
        Invoke-Compose -ComposeArgs @("-f", $composeFile, "--env-file", $tempEnvFile, "down")
        Remove-Item -LiteralPath $tempEnvFile -Force -ErrorAction SilentlyContinue
    }
}

$global:LASTEXITCODE = 0
