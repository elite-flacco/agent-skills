param(
    [string]$SourceRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Stop'

$ManifestPath = Join-Path $SourceRoot 'manifest.json'
if (-not (Test-Path -LiteralPath $ManifestPath)) {
    throw "Missing manifest: $ManifestPath"
}

$Manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
$BackupRoot = Join-Path $SourceRoot 'backups'
$Stamp = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')

function Ensure-Directory([string]$Path) {
    New-Item -ItemType Directory -Path $Path -Force | Out-Null
}

function Move-ToBackup([string]$Path, [string]$Category) {
    if (-not (Test-Path -LiteralPath $Path)) {
        return
    }

    $TargetDir = Join-Path $BackupRoot (Join-Path $Category $Stamp)
    Ensure-Directory $TargetDir
    $BackupPath = Join-Path $TargetDir (Split-Path -Leaf $Path)
    Move-Item -LiteralPath $Path -Destination $BackupPath
    Write-Host "Backed up $Path -> $BackupPath"
}

function Ensure-Junction([string]$LinkPath, [string]$TargetPath, [string]$BackupCategory) {
    if (-not (Test-Path -LiteralPath $TargetPath)) {
        throw "Cannot link missing target: $TargetPath"
    }

    if (Test-Path -LiteralPath $LinkPath) {
        $Existing = Get-Item -LiteralPath $LinkPath -Force
        $ExistingTarget = @($Existing.Target) -join ''
        if ($Existing.LinkType -eq 'Junction' -and $ExistingTarget -eq $TargetPath) {
            Write-Host "Already linked: $LinkPath"
            return
        }

        Move-ToBackup $LinkPath $BackupCategory
    }

    New-Item -ItemType Junction -Path $LinkPath -Target $TargetPath | Out-Null
    Write-Host "Linked $LinkPath -> $TargetPath"
}

function Get-SkillName($Skill) {
    if ($Skill -is [string]) {
        return $Skill
    }

    return $Skill.name
}

function Get-SkillSource($Skill) {
    if ($Skill -is [string]) {
        return Join-Path 'skills' $Skill
    }

    return Join-Path 'skills' $Skill.source
}

function Remove-StaleLinks([string]$Root, [System.Collections.Generic.HashSet[string]]$ManagedNames) {
    $SkillsRoot = Join-Path $SourceRoot 'skills'
    foreach ($Item in Get-ChildItem -LiteralPath $Root -Force) {
        if ($ManagedNames.Contains($Item.Name)) {
            continue
        }
        if ($Item.LinkType -ne 'Junction') {
            continue
        }
        $Target = @($Item.Target) -join ''
        if ($Target -eq $SkillsRoot -or $Target.StartsWith($SkillsRoot + [IO.Path]::DirectorySeparatorChar)) {
            $Item.Delete()
            Write-Host "Pruned stale link $($Item.FullName) -> $Target"
        }
    }
}

$ClaudeSkills = Join-Path $env:USERPROFILE '.claude\skills'
$CodexSkills = Join-Path $env:USERPROFILE '.codex\skills'
$PiSkills = Join-Path $env:USERPROFILE '.pi\agent\skills'
$ZcodeSkills = Join-Path $env:USERPROFILE '.zcode\skills'
$ManagedNames = [System.Collections.Generic.HashSet[string]]::new()
foreach ($Skill in $Manifest.managedSkills) {
    $ManagedNames.Add((Get-SkillName $Skill)) | Out-Null
}
foreach ($Root in @($ClaudeSkills, $CodexSkills, $PiSkills, $ZcodeSkills)) {
    Ensure-Directory $Root
    Remove-StaleLinks $Root $ManagedNames
}

foreach ($Skill in $Manifest.managedSkills) {
    $SkillName = Get-SkillName $Skill
    $TargetPath = Join-Path $SourceRoot (Get-SkillSource $Skill)
    Ensure-Junction (Join-Path $ClaudeSkills $SkillName) $TargetPath 'claude-skills'
    Ensure-Junction (Join-Path $CodexSkills $SkillName) $TargetPath 'codex-skills'
    Ensure-Junction (Join-Path $PiSkills $SkillName) $TargetPath 'pi-skills'
    Ensure-Junction (Join-Path $ZcodeSkills $SkillName) $TargetPath 'zcode-skills'
}
