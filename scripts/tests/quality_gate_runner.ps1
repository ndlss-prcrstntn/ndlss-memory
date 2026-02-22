param(
    [switch]$SkipUnit,
    [switch]$SkipIntegration,
    [switch]$SkipContract,
    [switch]$SkipE2E,
    [string]$ArtifactsDir = "tests/artifacts/quality-stability"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
. (Join-Path $root "scripts/tests/quality_stage_helpers.ps1")

$artifactRoot = Join-Path $root $ArtifactsDir
New-Item -ItemType Directory -Path $artifactRoot -Force | Out-Null
$reportPath = Join-Path $artifactRoot "quality-run-report.json"

$runId = [guid]::NewGuid().ToString("N")
$report = New-QualityRunReport -RunId $runId -ArtifactsDir $ArtifactsDir

function Invoke-Stage {
    param(
        [hashtable]$Report,
        [string]$Name,
        [scriptblock]$Body,
        [switch]$Skip,
        [string]$FailureCode,
        [string[]]$ArtifactPaths
    )

    $stage = Start-QualityStage -Name $Name
    Write-Host "[quality] stage '$Name' started"
    try {
        if ($Skip) {
            Complete-QualityStage -Stage $stage -Status "skipped"
            Write-Host "[quality] stage '$Name' skipped"
        } else {
            & $Body
            $existingArtifacts = @()
            foreach ($path in ($ArtifactPaths | Where-Object { $_ })) {
                if (Test-Path $path) {
                    $existingArtifacts += $path
                }
            }
            Complete-QualityStage -Stage $stage -Status "passed" -ArtifactPaths $existingArtifacts
            Write-Host "[quality] stage '$Name' passed in $($stage.durationMs)ms"
        }
    } catch {
        $code = if ($FailureCode) { $FailureCode } else { "$($Name.ToUpperInvariant())_FAILED" }
        $msg = $_.Exception.Message
        Complete-QualityStage -Stage $stage -Status "failed" -FailureCode $code -FailureMessage $msg
        Add-QualityFailure -Report $Report -Stage $Name -Code $code -Message $msg
        Write-Host "[quality] stage '$Name' failed code=$code message=$msg"
    }

    $Report.stages += $stage
}

$python = Join-Path $root ".venv/Scripts/python.exe"
if (-not (Test-Path $python)) {
    $python = "python"
}

Invoke-Stage -Report $report -Name "unit" -Skip:$SkipUnit -Body {
    & $python -m pytest "tests/unit/file_indexer" "tests/unit/mcp_server"
    if ($LASTEXITCODE -ne 0) {
        throw "pytest unit suite failed with exit code $LASTEXITCODE"
    }
}

$us1Artifact = Join-Path $artifactRoot "us1-idempotency-summary.json"
Invoke-Stage -Report $report -Name "us1" -Skip:$SkipUnit -FailureCode "US1_IDEMPOTENCY_FAILED" -ArtifactPaths @($us1Artifact) -Body {
    & (Join-Path $root "scripts/tests/idempotency_compose_regression.ps1")
    if (-not $?) {
        throw "US1 idempotency compose regression script failed"
    }
}

$us1PersistenceArtifact = Join-Path $artifactRoot "us1-ingestion-collection-summary.json"
Invoke-Stage -Report $report -Name "us1_persistence" -Skip:$SkipIntegration -FailureCode "US1_PERSISTENCE_FAILED" -ArtifactPaths @($us1PersistenceArtifact) -Body {
    & (Join-Path $root "scripts/tests/us1_ingestion_collection_creation.ps1")
    if (-not $?) {
        throw "US1 ingestion collection creation script failed"
    }
}

Invoke-Stage -Report $report -Name "integration" -Skip:$SkipIntegration -Body {
    & (Join-Path $root "scripts/tests/full_scan_compose_regression.ps1")
    & (Join-Path $root "scripts/tests/delta_after_commit_compose_regression.ps1")
    & (Join-Path $root "scripts/tests/ingestion_compose_regression.ps1")
}

$us2Artifact = Join-Path $artifactRoot "us2-integration-summary.json"
Invoke-Stage -Report $report -Name "us2" -Skip:$SkipIntegration -FailureCode "US2_SEARCH_FLOW_FAILED" -ArtifactPaths @($us2Artifact) -Body {
    & (Join-Path $root "scripts/tests/us2_quality_search_flow.ps1")
    if (-not $?) {
        throw "US2 search flow script failed"
    }
}

$us2CustomPortArtifact = Join-Path $artifactRoot "us2-custom-port-summary.json"
Invoke-Stage -Report $report -Name "us2_custom_port" -Skip:$SkipIntegration -FailureCode "US2_CUSTOM_PORT_FAILED" -ArtifactPaths @($us2CustomPortArtifact) -Body {
    & (Join-Path $root "scripts/tests/us2_custom_qdrant_external_port.ps1")
    if (-not $?) {
        throw "US2 custom external port script failed"
    }
}

Invoke-Stage -Report $report -Name "contract" -Skip:$SkipContract -Body {
    & (Join-Path $root "scripts/tests/contract_quality_stability.ps1")
    if (-not $?) {
        throw "contract checks script failed"
    }
}

Invoke-Stage -Report $report -Name "mcp_transport" -Skip:$SkipIntegration -FailureCode "MCP_TRANSPORT_COMPAT_FAILED" -Body {
    & (Join-Path $root "scripts/tests/mcp_transport_compatibility_smoke.ps1")
    if (-not $?) {
        throw "MCP transport compatibility smoke failed"
    }
}

$us3Artifact = Join-Path $artifactRoot "us3-e2e-summary.json"
Invoke-Stage -Report $report -Name "us3" -Skip:$SkipE2E -FailureCode "US3_E2E_FAILED" -ArtifactPaths @($us3Artifact) -Body {
    $e2eScript = Join-Path $root "scripts/tests/quality_stability_e2e.ps1"
    if (-not (Test-Path $e2eScript)) {
        throw "missing E2E runner: $e2eScript"
    }
    & $e2eScript
    if (-not $?) {
        throw "E2E suite script failed"
    }
}

Save-QualityRunReport -Report $report -Path $reportPath

if ($report.status -ne "passed") {
    Write-Host "Quality run failed. report=$reportPath"
    exit 1
}

Write-Host "Quality run passed. report=$reportPath"
