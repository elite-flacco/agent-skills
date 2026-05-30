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
const backupRoot = path.join(sourceRoot, 'backups');
const stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d{3}Z$/, 'Z');

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function moveToBackup(source, category) {
  if (!fs.existsSync(source)) return;
  const targetDir = path.join(backupRoot, category, stamp);
  ensureDir(targetDir);
  const backupPath = path.join(targetDir, path.basename(source));
  fs.renameSync(source, backupPath);
  console.log(`Backed up ${source} -> ${backupPath}`);
}

function ensureSymlink(linkPath, targetPath, backupCategory) {
  if (!fs.existsSync(targetPath)) {
    throw new Error(`Cannot link missing target: ${targetPath}`);
  }

  let existing = null;
  try {
    existing = fs.lstatSync(linkPath);
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
  }

  if (existing) {
    if (existing.isSymbolicLink() && fs.realpathSync(linkPath) === fs.realpathSync(targetPath)) {
      console.log(`Already linked: ${linkPath}`);
      return;
    }
    moveToBackup(linkPath, backupCategory);
  }

  fs.symlinkSync(targetPath, linkPath, 'dir');
  console.log(`Linked ${linkPath} -> ${targetPath}`);
}

const claudeSkills = path.join(os.homedir(), '.claude', 'skills');
const codexSkills = path.join(os.homedir(), '.codex', 'skills');
ensureDir(claudeSkills);
ensureDir(codexSkills);

for (const skill of manifest.managedSkills) {
  const targetPath = path.join(sourceRoot, 'skills', skill.source);
  ensureSymlink(path.join(claudeSkills, skill.name), targetPath, 'claude-skills');
  ensureSymlink(path.join(codexSkills, skill.name), targetPath, 'codex-skills');
}

console.log(`Linked ${manifest.managedSkills.length} skills into ${claudeSkills} and ${codexSkills}.`);
NODE
