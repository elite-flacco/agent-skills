#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_root="$(cd "$script_dir/../.." && pwd)"
check=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --source-root)
      source_root="$(cd "$2" && pwd)"
      shift 2
      ;;
    --check)
      check=true
      shift
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

SOURCE_ROOT="$source_root" CHECK="$check" node <<'NODE'
const fs = require('node:fs');
const path = require('node:path');

const sourceRoot = process.env.SOURCE_ROOT;
const manifestPath = path.join(sourceRoot, 'manifest.json');
const skillsRoot = path.join(sourceRoot, 'skills');
const check = process.env.CHECK === 'true';

if (!fs.existsSync(skillsRoot)) {
  throw new Error(`Missing skills directory: ${skillsRoot}`);
}

const existingManifest = fs.existsSync(manifestPath)
  ? JSON.parse(fs.readFileSync(manifestPath, 'utf8'))
  : {};

function findSkillFiles(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) files.push(...findSkillFiles(fullPath));
    if (entry.isFile() && entry.name === 'SKILL.md') files.push(fullPath);
  }
  return files;
}

const managedSkills = findSkillFiles(skillsRoot)
  .map((skillFile) => {
    const skillDir = path.dirname(skillFile);
    return {
      name: path.basename(skillDir),
      source: path.relative(skillsRoot, skillDir).split(path.sep).join('/'),
    };
  })
  .sort((a, b) => a.name.localeCompare(b.name));

const desiredManifest = {
  sourceRoot: existingManifest.sourceRoot ?? sourceRoot,
  managedSkills,
};

function comparable(manifest) {
  return JSON.stringify({
    managedSkills: manifest.managedSkills ?? [],
  });
}

if (check) {
  if (!fs.existsSync(manifestPath)) {
    console.error(`Manifest is missing: ${manifestPath}`);
    process.exit(1);
  }

  const current = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  if (comparable(current) !== comparable(desiredManifest)) {
    console.error('manifest.json managedSkills are stale. Run scripts/macos/sync-manifest.sh.');
    process.exit(1);
  }

  console.log('manifest managedSkills are current.');
  process.exit(0);
}

const desiredJson = JSON.stringify(desiredManifest, null, 4) + '\n';
const currentJson = fs.existsSync(manifestPath) ? fs.readFileSync(manifestPath, 'utf8') : '';
if (currentJson !== desiredJson) {
  fs.writeFileSync(manifestPath, desiredJson, 'utf8');
  console.log(`Updated manifest.json with ${managedSkills.length} managed skills.`);
} else {
  console.log('manifest.json is current.');
}
NODE
