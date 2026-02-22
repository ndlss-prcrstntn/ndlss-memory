param(
    [string]$BaseUrl = "",
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
. (Join-Path $root "scripts/tests/test_ports.ps1")
Set-DefaultTestPorts
if (-not $BaseUrl) {
    $BaseUrl = Get-TestBaseUrl
}

function Invoke-Compose {
    param(
        [string[]]$ComposeArgs,
        [switch]$ReturnOutput
    )

    $stdoutFile = [System.IO.Path]::GetTempFileName()
    $stderrFile = [System.IO.Path]::GetTempFileName()
    try {
        $process = Start-Process -FilePath "docker" -ArgumentList (@("compose") + $ComposeArgs) -NoNewWindow -PassThru -Wait -RedirectStandardOutput $stdoutFile -RedirectStandardError $stderrFile
        $stdout = if (Test-Path $stdoutFile) { Get-Content -LiteralPath $stdoutFile } else { @() }
        $stderr = if (Test-Path $stderrFile) { Get-Content -LiteralPath $stderrFile } else { @() }
        $combined = @($stdout + $stderr)

        foreach ($line in $combined) {
            if ($line -ne $null -and $line -ne "") {
                Write-Host $line
            }
        }

        if ($process.ExitCode -ne 0) {
            throw "docker compose failed with exit code $($process.ExitCode) (args: $($ComposeArgs -join ' '))"
        }

        if ($ReturnOutput) {
            return $combined
        }
    } finally {
        Remove-Item -LiteralPath $stdoutFile, $stderrFile -Force -ErrorAction SilentlyContinue
    }
}

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
        Invoke-Compose -ComposeArgs @("up", "-d", "mcp-server")
        Start-Sleep -Seconds 6

        $logs = Invoke-Compose -ComposeArgs @("logs", "mcp-server", "--tail", "200") -ReturnOutput
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
        Invoke-Compose -ComposeArgs @("rm", "-fsv", "mcp-server")
        Pop-Location
    }
}

$startedByScript = $false
if (-not $SkipComposeStart) {
    Push-Location $root
    try {
        Invoke-Compose -ComposeArgs @("up", "-d", "--build")
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
            Invoke-Compose -ComposeArgs @("down")
        } finally {
            Pop-Location
        }
    }
}
$global:LASTEXITCODE = 0
