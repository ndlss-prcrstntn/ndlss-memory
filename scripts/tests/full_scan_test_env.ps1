param(
    [string]$FixtureRoot = "tests/fixtures/full-scan",
    [switch]$Clean
)

$ErrorActionPreference = "Stop"

if ($Clean) {
    if (Test-Path $FixtureRoot) {
        Remove-Item -Recurse -Force $FixtureRoot
    }
}

$dirs = @(
    "$FixtureRoot/valid/nested",
    "$FixtureRoot/excluded/node_modules",
    "$FixtureRoot/unsupported",
    "$FixtureRoot/oversized",
    "$FixtureRoot/corrupted"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

Set-Content -Path "$FixtureRoot/valid/readme.md" -Value "# valid markdown"
Set-Content -Path "$FixtureRoot/valid/nested/data.json" -Value "{`"ok`": true}"
Set-Content -Path "$FixtureRoot/excluded/node_modules/skip.txt" -Value "should be excluded"
Set-Content -Path "$FixtureRoot/unsupported/image.png" -Value "not supported"

# ~2KB oversized fixture by default; tests can lower size limit for deterministic skip.
$large = "A" * 2048
Set-Content -Path "$FixtureRoot/oversized/big.txt" -Value $large

Write-Host "Full-scan fixture environment prepared at $FixtureRoot"

