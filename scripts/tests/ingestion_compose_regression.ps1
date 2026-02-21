Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
$compose = Join-Path $root "infra\\docker\\docker-compose.yml"
$envFile = Join-Path $root ".env.example"

docker compose -f $compose --env-file $envFile up -d --build
docker compose -f $compose --env-file $envFile ps

& (Join-Path $root "scripts\\tests\\us1_chunking_deterministic.ps1")
& (Join-Path $root "scripts\\tests\\us2_embedding_retry_upsert.ps1")
& (Join-Path $root "scripts\\tests\\us3_metadata_traceability.ps1")

docker compose -f $compose --env-file $envFile down

Write-Host "Ingestion compose regression completed"
