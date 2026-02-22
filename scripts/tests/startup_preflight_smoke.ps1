param(
    [string]$BaseUrl = "http://localhost:8080",
    [int]$ReadyTimeoutSeconds = 60,
    [ValidateSet("ready", "failfast-qdrant")]
    [string]$Mode = "ready",
    [string]$ArtifactPath = "",
    [switch]$SkipComposeStart
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")

function Save-StartupPreflightArtifact {
    param(
        [hashtable]$Payload,
        [string]$Path
    )
    if (-not $Path) {
        return
    }
    $dir = Split-Path -Parent $Path
    if ($dir) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    $Payload | ConvertTo-Json -Depth 10 | Set-Content -Path $Path -Encoding utf8
}

function Invoke-HealthCheck {
    param(
        [string]$Url,
        [int]$TimeoutSeconds
    )
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        try {
            $health = Invoke-RestMethod -Method Get -Uri "$Url/health"
            if ($health.status -eq "ok") {
                return
            }
        } catch {
            Start-Sleep -Seconds 2
            continue
        }
        Start-Sleep -Seconds 2
    }
    throw "health endpoint did not return ok in $TimeoutSeconds seconds"
}

function Invoke-ReadinessCheck {
    param(
        [string]$Url,
        [int]$TimeoutSeconds
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        try {
            $ready = Invoke-RestMethod -Method Get -Uri "$Url/v1/system/startup/readiness"
            if ($ready.status -eq "ready") {
                return $ready
            }
        } catch {
            Start-Sleep -Seconds 2
            continue
        }
        Start-Sleep -Seconds 2
    }

    throw "startup readiness endpoint did not return ready in $TimeoutSeconds seconds"
}

if ($Mode -eq "failfast-qdrant") {
    Push-Location $root
    $previousQdrantHost = $env:QDRANT_HOST
    try {
        $env:QDRANT_HOST = "qdrant-unreachable"
        docker compose up -d mcp-server | Out-Null
        Start-Sleep -Seconds 6

        $logs = docker compose logs mcp-server --tail 200
        if ($logs -notmatch "STARTUP_PREFLIGHT_FAILED") {
            throw "mcp-server logs do not contain STARTUP_PREFLIGHT_FAILED"
        }
        Save-StartupPreflightArtifact -Path $ArtifactPath -Payload @{
            mode = $Mode
            status = "passed"
            checkedAt = (Get-Date).ToString("o")
        }
        Write-Host "[startup-preflight-smoke] failfast-qdrant scenario passed"
        exit 0
    } finally {
        if ($null -eq $previousQdrantHost) {
            Remove-Item Env:QDRANT_HOST -ErrorAction SilentlyContinue
        } else {
            $env:QDRANT_HOST = $previousQdrantHost
        }
        docker compose rm -fsv mcp-server | Out-Null
        Pop-Location
    }
}

$startedByScript = $false
if (-not $SkipComposeStart) {
    Push-Location $root
    try {
        docker compose up -d --build | Out-Null
        $startedByScript = $true
    } finally {
        Pop-Location
    }
}

try {
    Invoke-HealthCheck -Url $BaseUrl -TimeoutSeconds $ReadyTimeoutSeconds
    $readyPayload = Invoke-ReadinessCheck -Url $BaseUrl -TimeoutSeconds $ReadyTimeoutSeconds

    if (-not $readyPayload.serviceReadiness) { throw "missing serviceReadiness in readiness payload" }
    if (-not $readyPayload.workspacePath) { throw "missing workspacePath in readiness payload" }
    if (-not $readyPayload.mcpEndpoint) { throw "missing mcpEndpoint in readiness payload" }
    if (-not $readyPayload.collectionName) { throw "missing collectionName in readiness payload" }

    Save-StartupPreflightArtifact -Path $ArtifactPath -Payload @{
        mode = $Mode
        status = "passed"
        checkedAt = (Get-Date).ToString("o")
        readiness = $readyPayload
    }

    Write-Host "[startup-preflight-smoke] ready scenario passed"
    Write-Host ($readyPayload | ConvertTo-Json -Depth 8)
} finally {
    if ($startedByScript) {
        Push-Location $root
        try {
            docker compose down | Out-Null
        } finally {
            Pop-Location
        }
    }
}
