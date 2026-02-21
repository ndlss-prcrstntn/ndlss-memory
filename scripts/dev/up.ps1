param(
    [string]$ComposeFile = "infra/docker/docker-compose.yml",
    [string]$EnvFile = ".env.example"
)

$ErrorActionPreference = "Stop"

docker compose -f $ComposeFile --env-file $EnvFile up -d --build
Write-Host "Compose stack started"
