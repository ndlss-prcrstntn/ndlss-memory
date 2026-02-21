Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$composeFile = Join-Path $root "infra\docker\docker-compose.yml"
$envFile = Join-Path $root ".env.example"

try {
    docker compose -f $composeFile --env-file $envFile up -d --build
    docker compose -f $composeFile --env-file $envFile ps

    & (Join-Path $root "scripts\tests\us1_delta_changed_only.ps1")
    & (Join-Path $root "scripts\tests\us2_delta_delete_rename.ps1")
    & (Join-Path $root "scripts\tests\us3_delta_fallback_full_scan.ps1")

    Write-Host "Delta-after-commit compose regression completed"
}
finally {
    docker compose -f $composeFile --env-file $envFile down
}
