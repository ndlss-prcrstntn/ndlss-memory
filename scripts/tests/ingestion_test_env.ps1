param(
    [string]$WorkspacePath = "tests/fixtures/chunking-embeddings",
    [string]$ChunkSize = "120",
    [string]$ChunkOverlap = "24",
    [string]$RetryMaxAttempts = "3",
    [string]$RetryBackoffSeconds = "0.1"
)

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
$env:WORKSPACE_PATH = (Resolve-Path (Join-Path $root $WorkspacePath)).Path
$env:INDEX_MODE = "full-scan"
$env:INDEX_FILE_TYPES = ".md,.txt,.json,.yml,.yaml"
$env:INDEX_EXCLUDE_PATTERNS = ".git,node_modules,dist,build"
$env:INDEX_MAX_FILE_SIZE_BYTES = "1048576"
$env:INDEX_PROGRESS_INTERVAL_SECONDS = "5"
$env:INGESTION_CHUNK_SIZE = $ChunkSize
$env:INGESTION_CHUNK_OVERLAP = $ChunkOverlap
$env:INGESTION_RETRY_MAX_ATTEMPTS = $RetryMaxAttempts
$env:INGESTION_RETRY_BACKOFF_SECONDS = $RetryBackoffSeconds
$env:INGESTION_EMBEDDING_VECTOR_SIZE = "16"
$env:INGESTION_ENABLE_QDRANT_HTTP = "0"
$env:INGESTION_UPSERT_TIMEOUT_SECONDS = "5"
$env:QDRANT_COLLECTION_NAME = "workspace_chunks"

Write-Host "Prepared ingestion test env for workspace: $($env:WORKSPACE_PATH)"
