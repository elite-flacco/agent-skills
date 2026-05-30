#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_root="$(cd "$script_dir/../.." && pwd)"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source-root)
      source_root="$(cd "$2" && pwd)"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

SOURCE_ROOT="$source_root" node <<'NODE'
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');

const sourceRoot = process.env.SOURCE_ROOT;
const manifest = JSON.parse(fs.readFileSync(path.join(sourceRoot, 'manifest.json'), 'utf8'));
const failures = [];
const claudeSkills = path.join(os.homedir(), '.claude', 'skills');
const codexSkills = path.join(os.homedir(), '.codex', 'skills');

function hasMojibake(text) {
  for (const char of text) {
    const code = char.charCodeAt(0);
    if ([0x00e2, 0x00f0, 0x00c3, 0x00c2, 0xfffd].includes(code)) return true;
  }
  return false;
}

for (const skill of manifest.managedSkills) {
  const targetPath = path.join(sourceRoot, 'skills', skill.source);
  const skillFile = path.join(targetPath, 'SKILL.md');
  const sourceLeaf = path.basename(skill.source);

  if (sourceLeaf !== skill.name) {
    failures.push(`Manifest source leaf '${sourceLeaf}' must match skill name '${skill.name}'.`);
  }

  if (!fs.existsSync(skillFile)) {
    failures.push(`Missing SKILL.md: ${skillFile}`);
  } else {
    const skillText = fs.readFileSync(skillFile, 'utf8');
    if (hasMojibake(skillText)) {
      failures.push(`Potential mojibake in SKILL.md; check for corrupted UTF-8 marker characters: ${skillFile}`);
    }
    const namePattern = new RegExp(`^name:\\s*${skill.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\s*$`, 'm');
    if (!namePattern.test(skillText)) {
      failures.push(`SKILL.md name does not match manifest name '${skill.name}': ${skillFile}`);
    }
  }

  for (const root of [claudeSkills, codexSkills]) {
    const linkPath = path.join(root, skill.name);
    let stat = null;
    try {
      stat = fs.lstatSync(linkPath);
    } catch (error) {
      if (error.code !== 'ENOENT') throw error;
    }

    if (!stat) {
      failures.push(`Missing discovery link: ${linkPath}`);
      continue;
    }
    if (!stat.isSymbolicLink()) {
      failures.push(`Expected symlink, found non-symlink: ${linkPath}`);
    } else if (fs.realpathSync(linkPath) !== fs.realpathSync(targetPath)) {
      failures.push(`Unexpected target for ${linkPath}; expected ${targetPath}; got ${fs.realpathSync(linkPath)}`);
    }
  }
}

if (failures.length > 0) {
  for (const failure of failures) console.error(failure);
  process.exit(1);
}

console.log(`Validated ${manifest.managedSkills.length} managed skills.`);
NODE
