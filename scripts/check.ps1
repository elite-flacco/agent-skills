param(
    [string]$SourceRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Stop'

& (Join-Path $PSScriptRoot 'sync-manifest.ps1') -SourceRoot $SourceRoot -Check
& (Join-Path $PSScriptRoot 'validate.ps1') -SourceRoot $SourceRoot
