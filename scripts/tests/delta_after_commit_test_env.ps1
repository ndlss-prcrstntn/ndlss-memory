param(
    [string]$WorkspacePath = "tests/fixtures/delta-after-commit/repo-base",
    [string]$BaseRef = "HEAD~1",
    [string]$TargetRef = "HEAD"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$sourceWorkspace = (Resolve-Path (Join-Path $root $WorkspacePath)).Path
$runtimeName = "delta-runtime-$([guid]::NewGuid().ToString('N'))"
$runtimeHostWorkspace = Join-Path (Join-Path $root 'tests\fixtures') $runtimeName

New-Item -ItemType Directory -Path $runtimeHostWorkspace -Force | Out-Null
Copy-Item -Path (Join-Path $sourceWorkspace '*') -Destination $runtimeHostWorkspace -Recurse -Force

Push-Location $runtimeHostWorkspace
try {
    $prevErrorAction = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        git init 2>$null | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "git init failed with exit code $LASTEXITCODE"
        }
        git config user.email "delta.tests@example.local" 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "git config user.email failed with exit code $LASTEXITCODE"
        }
        git config user.name "Delta Tests" 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "git config user.name failed with exit code $LASTEXITCODE"
        }
        git add . 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "git add failed with exit code $LASTEXITCODE"
        }
        git commit -m "base snapshot" 2>$null | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "git commit failed with exit code $LASTEXITCODE"
        }
    } finally {
        $ErrorActionPreference = $prevErrorAction
    }
} finally {
    Pop-Location
}

$env:WORKSPACE_PATH = $runtimeHostWorkspace
$env:WORKSPACE_PATH_HOST = $runtimeHostWorkspace
$env:WORKSPACE_PATH_CONTAINER = "/workspace/tests/fixtures/$runtimeName"
$env:INDEX_MODE = "delta-after-commit"
$env:INDEX_FILE_TYPES = ".md,.txt,.json,.yml,.yaml"
$env:INDEX_EXCLUDE_PATTERNS = ".git,node_modules,dist,build"
$env:INDEX_MAX_FILE_SIZE_BYTES = "1048576"
$env:INDEX_PROGRESS_INTERVAL_SECONDS = "5"
$env:INGESTION_CHUNK_SIZE = "128"
$env:INGESTION_CHUNK_OVERLAP = "16"
$env:INGESTION_RETRY_MAX_ATTEMPTS = "2"
$env:INGESTION_RETRY_BACKOFF_SECONDS = "0.1"
$env:DELTA_GIT_BASE_REF = $BaseRef
$env:DELTA_GIT_TARGET_REF = $TargetRef
$env:DELTA_INCLUDE_RENAMES = "1"
$env:DELTA_ENABLE_FALLBACK = "1"
$env:DELTA_BOOTSTRAP_ON_START = "0"
$env:IDEMPOTENCY_HASH_ALGORITHM = "sha256"
$env:IDEMPOTENCY_SKIP_UNCHANGED = "1"
$env:IDEMPOTENCY_ENABLE_STALE_CLEANUP = "1"

Write-Host "Prepared delta-after-commit test env host=$($env:WORKSPACE_PATH_HOST) container=$($env:WORKSPACE_PATH_CONTAINER)"
