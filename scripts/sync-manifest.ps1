param(
    [string]$SourceRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path,
    [switch]$Check
)

$ErrorActionPreference = 'Stop'

$ManifestPath = Join-Path $SourceRoot 'manifest.json'
$SkillsRoot = Join-Path $SourceRoot 'skills'

if (-not (Test-Path -LiteralPath $SkillsRoot)) {
    throw "Missing skills directory: $SkillsRoot"
}

$ExistingRetiredDiscovery = [ordered]@{
    claudeCommandMarkdown = $true
    codexGeneratedClaudeCommandWrappers = $true
    codexClaudeSkillPrefixJunctions = $true
}

if (Test-Path -LiteralPath $ManifestPath) {
    $ExistingManifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
    if ($ExistingManifest.retiredDiscovery) {
        $ExistingRetiredDiscovery = [ordered]@{}
        foreach ($Property in $ExistingManifest.retiredDiscovery.PSObject.Properties) {
            $ExistingRetiredDiscovery[$Property.Name] = $Property.Value
        }
    }
}

$SkillRootWithSeparator = $SkillsRoot.TrimEnd('\') + '\'
$ManagedSkills = Get-ChildItem -LiteralPath $SkillsRoot -Recurse -Filter 'SKILL.md' -File |
    ForEach-Object {
        $SkillDirectory = Split-Path -Parent $_.FullName
        $RelativeSource = $SkillDirectory.Substring($SkillRootWithSeparator.Length).Replace('\', '/')
        $Name = Split-Path -Leaf $SkillDirectory

        [pscustomobject][ordered]@{
            name = $Name
            source = $RelativeSource
        }
    } |
    Sort-Object name

$Manifest = [pscustomobject][ordered]@{
    sourceRoot = $SourceRoot
    managedSkills = @($ManagedSkills)
    retiredDiscovery = [pscustomobject]$ExistingRetiredDiscovery
}

$DesiredJson = ($Manifest | ConvertTo-Json -Depth 10) + [Environment]::NewLine

if ($Check) {
    if (-not (Test-Path -LiteralPath $ManifestPath)) {
        Write-Error "Manifest is missing: $ManifestPath"
        exit 1
    }

    $CurrentJson = Get-Content -LiteralPath $ManifestPath -Raw
    if ($CurrentJson -ne $DesiredJson) {
        Write-Error "manifest.json is stale. Run scripts/sync-manifest.ps1 or commit with the repo hook enabled."
        exit 1
    }

    Write-Host "manifest.json is current."
    exit 0
}

$CurrentJson = ''
if (Test-Path -LiteralPath $ManifestPath) {
    $CurrentJson = Get-Content -LiteralPath $ManifestPath -Raw
}

if ($CurrentJson -ne $DesiredJson) {
    [IO.File]::WriteAllText($ManifestPath, $DesiredJson, [Text.UTF8Encoding]::new($false))
    Write-Host "Updated manifest.json with $($ManagedSkills.Count) managed skills."
} else {
    Write-Host "manifest.json is current."
}
