param(
    [string]$ComposeFile = "infra/docker/docker-compose.yml",
    [string]$EnvFile = ".env.example",
    [switch]$RemoveVolumes
)

$ErrorActionPreference = "Stop"

$cmd = "docker compose -f $ComposeFile --env-file $EnvFile down"
if ($RemoveVolumes) { $cmd += " -v" }
Invoke-Expression $cmd
Write-Host "Compose stack stopped"
