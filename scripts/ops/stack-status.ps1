param(
    [string]$BaseUrl = "http://localhost:8080"
)

$ErrorActionPreference = "Stop"

$status = Invoke-RestMethod -Uri "$BaseUrl/v1/system/status" -Method Get -TimeoutSec 10
Write-Host "Overall status: $($status.overallStatus)"
foreach ($svc in $status.services) {
    Write-Host (" - {0}: {1}" -f $svc.name, $svc.status)
}
