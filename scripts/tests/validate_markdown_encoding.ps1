param(
    [string[]]$Paths = @(
        "README.md",
        "docs/testing",
        "tests/contract",
        "tests/integration",
        "specs/008-quality-stability-tests"
    )
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$utf8Strict = New-Object System.Text.UTF8Encoding($false, $true)
$invalid = @()

foreach ($path in $Paths) {
    if (-not (Test-Path $path)) {
        continue
    }

    $item = Get-Item $path
    if ($item.PSIsContainer) {
        $files = Get-ChildItem -Path $item.FullName -Recurse -File -Filter "*.md" -ErrorAction SilentlyContinue
    } else {
        $files = @($item)
    }

    foreach ($file in $files) {
        if ($file.Extension -ne ".md") {
            continue
        }
        try {
            $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
            [void]$utf8Strict.GetString($bytes)
        } catch {
            $invalid += $file.FullName
        }
    }
}

if (@($invalid).Count -gt 0) {
    Write-Host "Invalid Markdown encoding detected (must be UTF-8):"
    $invalid | ForEach-Object { Write-Host " - $_" }
    exit 1
}

Write-Host "All checked Markdown files are valid UTF-8."
