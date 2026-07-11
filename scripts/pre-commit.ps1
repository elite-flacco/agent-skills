param(
    [string]$SourceRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Stop'

function Invoke-Git([string[]]$Arguments) {
    & git @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Arguments -join ' ') failed with exit code $LASTEXITCODE."
    }
}

$ManifestPath = Join-Path $SourceRoot 'manifest.json'

Write-Host "Syncing skill manifest..."
& (Join-Path $PSScriptRoot 'sync-manifest.ps1') -SourceRoot $SourceRoot

Write-Host "Refreshing skill discovery links..."
& (Join-Path $PSScriptRoot 'link.ps1') -SourceRoot $SourceRoot

Write-Host "Validating managed skills..."
& (Join-Path $PSScriptRoot 'validate.ps1') -SourceRoot $SourceRoot

Invoke-Git @('-C', $SourceRoot, 'add', '--', $ManifestPath)
Write-Host "Pre-commit skill checks passed."
