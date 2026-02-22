param(
    [string]$RootPath = ".",
    [string[]]$IncludeExtensions = @(".md", ".yaml", ".yml", ".py", ".ps1", ".json"),
    [switch]$AllFiles
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$root = Resolve-Path $RootPath
$utf8Strict = New-Object System.Text.UTF8Encoding($false, $true)
$invalid = @()

$candidateFiles = @()
if ($AllFiles) {
    $tracked = @()
    try {
        $null = git -C $root rev-parse --is-inside-work-tree 2>$null
        $tracked = git -C $root ls-files
    } catch {
        $tracked = @()
    }

    if ($tracked.Count -gt 0) {
        foreach ($path in $tracked) {
            $full = Join-Path $root $path
            if (-not (Test-Path $full -PathType Leaf)) { continue }
            if ($IncludeExtensions -contains ([System.IO.Path]::GetExtension($full).ToLowerInvariant())) {
                $candidateFiles += $full
            }
        }
    } else {
        $candidateFiles = Get-ChildItem -Path $root -Recurse -File |
            Where-Object { $IncludeExtensions -contains $_.Extension.ToLowerInvariant() } |
            Select-Object -ExpandProperty FullName
    }
} else {
    $changed = @()
    try {
        $null = git -C $root rev-parse --is-inside-work-tree 2>$null
        $statusLines = git -C $root status --porcelain
        foreach ($line in $statusLines) {
            if (-not $line) { continue }
            $path = $line.Substring(3)
            if ($path.Contains(" -> ")) {
                $path = $path.Split(" -> ")[-1]
            }
            $changed += $path
        }
    } catch {
        $changed = @()
    }

    foreach ($path in $changed) {
        $full = Join-Path $root $path
        if (-not (Test-Path $full -PathType Leaf)) { continue }
        if ($IncludeExtensions -contains ([System.IO.Path]::GetExtension($full).ToLowerInvariant())) {
            $candidateFiles += $full
        }
    }

    $candidateFiles = $candidateFiles | Select-Object -Unique
    if ($candidateFiles.Count -eq 0) {
        Write-Host "UTF-8 verification skipped: no changed files matching requested extensions."
        exit 0
    }
}

foreach ($file in $candidateFiles) {
    try {
        $bytes = [System.IO.File]::ReadAllBytes($file)
        $null = $utf8Strict.GetString($bytes)
    } catch {
        $invalid += $file
    }
}

if ($invalid.Count -gt 0) {
    Write-Host "Non-UTF8 files detected:"
    $invalid | ForEach-Object { Write-Host " - $_" }
    exit 1
}

Write-Host "UTF-8 verification passed. Checked files: $($candidateFiles.Count)"
