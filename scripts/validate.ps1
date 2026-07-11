param(
    [string]$SourceRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
)

$ErrorActionPreference = 'Stop'

$ManifestPath = Join-Path $SourceRoot 'manifest.json'
$Manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
$ClaudeSkills = Join-Path $env:USERPROFILE '.claude\skills'
$CodexSkills = Join-Path $env:USERPROFILE '.codex\skills'
$PiSkills = Join-Path $env:USERPROFILE '.pi\agent\skills'
$ZcodeSkills = Join-Path $env:USERPROFILE '.zcode\skills'
$Failures = New-Object System.Collections.Generic.List[string]

function Test-Mojibake([string]$Text) {
    foreach ($Char in $Text.ToCharArray()) {
        $Code = [int][char]$Char
        if ($Code -eq 0x00E2 -or $Code -eq 0x00F0 -or $Code -eq 0x00C3 -or $Code -eq 0x00C2 -or $Code -eq 0xFFFD) {
            return $true
        }
    }

    return $false
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

foreach ($Skill in $Manifest.managedSkills) {
    $SkillName = Get-SkillName $Skill
    $SkillSource = Get-SkillSource $Skill
    $TargetPath = Join-Path $SourceRoot $SkillSource
    $SkillFile = Join-Path $TargetPath 'SKILL.md'
    $SourceLeaf = Split-Path -Leaf $SkillSource

    if ($SourceLeaf -ne $SkillName) {
        $Failures.Add("Manifest source leaf '$SourceLeaf' must match skill name '$SkillName'.")
    }

    if (-not (Test-Path -LiteralPath $SkillFile)) {
        $Failures.Add("Missing SKILL.md: $SkillFile")
    } else {
        $SkillText = [IO.File]::ReadAllText($SkillFile, [Text.Encoding]::UTF8)
        if (Test-Mojibake $SkillText) {
            $Failures.Add("Potential mojibake in SKILL.md; check for corrupted UTF-8 marker characters: $SkillFile")
        }

        $NameLine = Select-String -LiteralPath $SkillFile -Pattern "^name:\s*$([regex]::Escape($SkillName))\s*$" -Quiet
        if (-not $NameLine) {
            $Failures.Add("SKILL.md name does not match manifest name '$SkillName': $SkillFile")
        }
    }

    foreach ($Root in @($ClaudeSkills, $CodexSkills, $PiSkills, $ZcodeSkills)) {
        $LinkPath = Join-Path $Root $SkillName
        if (-not (Test-Path -LiteralPath $LinkPath)) {
            $Failures.Add("Missing discovery link: $LinkPath")
            continue
        }

        $Item = Get-Item -LiteralPath $LinkPath -Force
        $ActualTarget = @($Item.Target) -join ''
        if ($Item.LinkType -ne 'Junction') {
            $Failures.Add("Expected junction, found $($Item.LinkType): $LinkPath")
        }
        elseif ($ActualTarget -ne $TargetPath) {
            $Failures.Add("Unexpected target for $LinkPath; expected $TargetPath; got $ActualTarget")
        }
    }
}

if ($Failures.Count -gt 0) {
    $Failures | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Host "Validated $($Manifest.managedSkills.Count) managed skills."
