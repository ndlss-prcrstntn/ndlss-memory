Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\\..")
$composeFile = Join-Path $root "infra\\docker\\docker-compose.yml"
$envFile = Join-Path $root ".env.example"

docker compose -f $composeFile --env-file $envFile up -d --build
docker compose -f $composeFile --env-file $envFile ps

& (Join-Path $root "scripts\\tests\\us1_idempotent_repeat_run.ps1")
& (Join-Path $root "scripts\\tests\\us2_deterministic_chunk_updates.ps1")
& (Join-Path $root "scripts\\tests\\us3_stale_chunk_cleanup.ps1")

docker compose -f $composeFile --env-file $envFile down

Write-Host "Idempotency compose regression completed"
