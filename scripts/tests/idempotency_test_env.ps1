param(
    [string]$WorkspacePath = "tests/fixtures/idempotency",
    [string]$ChunkSize = "128",
    [string]$ChunkOverlap = "16",
    [string]$RetryMaxAttempts = "2",
    [string]$RetryBackoffSeconds = "0.1"
)

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
$sourceWorkspace = (Resolve-Path (Join-Path $root $WorkspacePath)).Path
$runtimeName = "idempotency-runtime-$([guid]::NewGuid().ToString('N'))"
$runtimeHostWorkspace = Join-Path (Join-Path $root 'tests\\fixtures') $runtimeName
New-Item -ItemType Directory -Path $runtimeHostWorkspace -Force | Out-Null
Copy-Item -Path (Join-Path $sourceWorkspace '*') -Destination $runtimeHostWorkspace -Recurse -Force
$env:WORKSPACE_PATH = $runtimeHostWorkspace
$env:WORKSPACE_PATH_HOST = $runtimeHostWorkspace
$env:WORKSPACE_PATH_CONTAINER = "/workspace/tests/fixtures/$runtimeName"
$env:INDEX_MODE = "full-scan"
$env:INDEX_FILE_TYPES = ".md,.txt,.json,.yml,.yaml"
$env:INDEX_EXCLUDE_PATTERNS = ".git,node_modules,dist,build"
$env:INDEX_MAX_FILE_SIZE_BYTES = "1048576"
$env:INDEX_PROGRESS_INTERVAL_SECONDS = "5"
$env:INGESTION_CHUNK_SIZE = $ChunkSize
$env:INGESTION_CHUNK_OVERLAP = $ChunkOverlap
$env:INGESTION_RETRY_MAX_ATTEMPTS = $RetryMaxAttempts
$env:INGESTION_RETRY_BACKOFF_SECONDS = $RetryBackoffSeconds
$env:IDEMPOTENCY_HASH_ALGORITHM = "sha256"
$env:IDEMPOTENCY_SKIP_UNCHANGED = "1"
$env:IDEMPOTENCY_ENABLE_STALE_CLEANUP = "1"
$env:IDEMPOTENCY_MAX_DELETE_BATCH = "1000"

Write-Host "Prepared idempotency test env host=$($env:WORKSPACE_PATH_HOST) container=$($env:WORKSPACE_PATH_CONTAINER)"
