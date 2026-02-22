param(
    [switch]$SkipComposeLifecycle
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
$composeFile = Join-Path $root "infra\\docker\\docker-compose.yml"
$envFile = Join-Path $root ".env.example"
. (Join-Path $root "scripts/tests/test_ports.ps1")
Set-DefaultTestPorts
$manageComposeLifecycle = -not $SkipComposeLifecycle

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

function Wait-Health {
    param([string]$BaseUrl)
    for ($i = 0; $i -lt 120; $i++) {
        try {
            $health = Invoke-RestMethod -Method Get -Uri "$BaseUrl/health" -TimeoutSec 2
            if ($health.status -eq "ok") {
                return
            }
        } catch {
        }
        Start-Sleep -Milliseconds 500
    }
    throw "MCP server health did not become ok in time"
}

$baseUrl = Get-TestBaseUrl

$artifactDir = Join-Path $root "tests/artifacts/quality-stability"
New-Item -ItemType Directory -Path $artifactDir -Force | Out-Null
$artifactPath = Join-Path $artifactDir "mcp-transport-smoke.json"

try {
    if ($manageComposeLifecycle) {
        Invoke-Compose -ComposeArgs @("-f", $composeFile, "--env-file", $envFile, "up", "-d", "--build")
    }

    Wait-Health -BaseUrl $baseUrl

    try {
        Invoke-RestMethod -Method Get -Uri "$baseUrl/mcp" -TimeoutSec 3 | Out-Null
        throw "Expected GET /mcp to return method-not-allowed"
    } catch {
        if (-not $_.Exception.Response) {
            throw
        }
        if ([int]$_.Exception.Response.StatusCode -ne 405) {
            throw "GET /mcp returned unexpected status code"
        }
    }

    $discovery = Invoke-RestMethod -Method Get -Uri "$baseUrl/.well-known/mcp"
    if (-not ($discovery.transports | Where-Object { $_.url -like "*/mcp" })) {
        throw "Discovery transports do not include /mcp endpoint"
    }

    $sessionId = [guid]::NewGuid().ToString("N")
    $initBody = @{
        jsonrpc = "2.0"
        id = 1
        method = "initialize"
        params = @{ clientInfo = @{ name = "quality-smoke"; version = "1.0.0" } }
    } | ConvertTo-Json -Depth 6

    $init = Invoke-RestMethod -Method Post -Uri "$baseUrl/mcp" -Headers @{ "X-MCP-Session-Id" = $sessionId } -ContentType "application/json" -Body $initBody
    if (-not $init.result.protocolVersion) {
        throw "Initialize response has no protocolVersion"
    }

    $toolsListBody = @{
        jsonrpc = "2.0"
        id = 2
        method = "tools/list"
        params = @{}
    } | ConvertTo-Json -Depth 5
    $toolsList = Invoke-RestMethod -Method Post -Uri "$baseUrl/mcp" -Headers @{ "X-MCP-Session-Id" = $sessionId } -ContentType "application/json" -Body $toolsListBody
    if (-not ($toolsList.result.tools | Where-Object { $_.name -eq "semantic_search" })) {
        throw "tools/list response does not include semantic_search"
    }

    $unknownBody = @{
        jsonrpc = "2.0"
        id = 3
        method = "unknown/method"
        params = @{}
    } | ConvertTo-Json -Depth 4
    try {
        Invoke-RestMethod -Method Post -Uri "$baseUrl/mcp" -Headers @{ "X-MCP-Session-Id" = $sessionId } -ContentType "application/json" -Body $unknownBody | Out-Null
        throw "Expected unknown method request to fail"
    } catch {
        if (-not $_.Exception.Response) {
            throw
        }
        $statusCode = [int]$_.Exception.Response.StatusCode
        if ($statusCode -notin @(400, 404)) {
            throw "Unknown method returned unexpected HTTP status: $statusCode"
        }

        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $body = $reader.ReadToEnd()
        if ($body -and $body.Trim()) {
            $parsed = $null
            try {
                $parsed = $body | ConvertFrom-Json -Depth 8
            } catch {
                throw "Unknown method response is not valid JSON: $body"
            }

            $jsonrpcCode = $null
            $domainCode = $null
            if ($parsed -and $parsed.error) {
                $jsonrpcCode = $parsed.error.code
                if ($parsed.error.data) {
                    $domainCode = $parsed.error.data.errorCode
                }
            }

            if ($jsonrpcCode -ne -32601 -and $domainCode -ne "METHOD_NOT_SUPPORTED") {
                throw "Unknown method did not return expected JSON-RPC error. body=$body"
            }
        }
    }

    [ordered]@{
        runId = [guid]::NewGuid().ToString("N")
        status = "passed"
        generatedAt = (Get-Date).ToString("o")
        baseUrl = $baseUrl
        discoveryTransportCount = @($discovery.transports).Count
    } | ConvertTo-Json -Depth 6 | Set-Content -Path $artifactPath -Encoding utf8

    Write-Host "MCP transport smoke completed. artifact=$artifactPath"
}
finally {
    if ($manageComposeLifecycle) {
        Invoke-Compose -ComposeArgs @("-f", $composeFile, "--env-file", $envFile, "down")
    }
}

