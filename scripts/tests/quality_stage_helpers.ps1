Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function New-QualityRunReport {
    param(
        [string]$RunId,
        [string]$ArtifactsDir
    )

    return @{
        runId = $RunId
        startedAt = (Get-Date).ToString("o")
        finishedAt = $null
        status = "running"
        artifactsDir = $ArtifactsDir
        stages = @()
        failures = @()
    }
}

function Start-QualityStage {
    param([string]$Name)

    return @{
        stageName = $Name
        status = "running"
        startedAt = (Get-Date).ToString("o")
        finishedAt = $null
        durationMs = 0
        failureCode = $null
        failureMessage = $null
        artifactPaths = @()
    }
}

function Complete-QualityStage {
    param(
        [hashtable]$Stage,
        [ValidateSet("passed","failed","skipped")][string]$Status,
        [string]$FailureCode,
        [string]$FailureMessage,
        [string[]]$ArtifactPaths
    )

    $start = [datetime]::Parse($Stage.startedAt)
    $finish = Get-Date
    $Stage.status = $Status
    $Stage.finishedAt = $finish.ToString("o")
    $Stage.durationMs = [int][math]::Max(0, ($finish - $start).TotalMilliseconds)
    if ($FailureCode) { $Stage.failureCode = $FailureCode }
    if ($FailureMessage) { $Stage.failureMessage = $FailureMessage }
    if ($ArtifactPaths) { $Stage.artifactPaths = $ArtifactPaths }
}

function Save-QualityRunReport {
    param(
        [hashtable]$Report,
        [string]$Path
    )

    $Report.finishedAt = (Get-Date).ToString("o")
    if (@($Report.stages | Where-Object { $_.status -eq "failed" }).Count -gt 0) {
        $Report.status = "failed"
    } elseif (@($Report.stages | Where-Object { $_.status -eq "passed" }).Count -gt 0) {
        $Report.status = "passed"
    } else {
        $Report.status = "canceled"
    }

    $Report | ConvertTo-Json -Depth 8 | Set-Content -Path $Path -Encoding utf8
}

function Add-QualityFailure {
    param(
        [hashtable]$Report,
        [string]$Stage,
        [string]$Code,
        [string]$Message
    )

    $Report.failures += [ordered]@{
        stage = $Stage
        code = $Code
        message = $Message
    }
}
