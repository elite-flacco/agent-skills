#!/usr/bin/env node
/**
 * Audit mechanical hygiene for an agent-skills style repo.
 *
 * Usage:
 *   node scripts/audit-skill-links-and-runtime-refs.mjs [repo-root]
 *
 * Checks:
 *   - manifest entries match skill directories and SKILL.md frontmatter names
 *   - discovery links exist and point at the expected source directory
 *   - broad multi-runtime skills mention runtime-specific discovery surfaces when relevant
 *   - obvious stale path references to missing local skill files
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';

const repoRoot = path.resolve(process.argv[2] ?? process.cwd());
const skillsRoot = path.join(repoRoot, 'skills');
const manifestPath = path.join(repoRoot, 'manifest.json');
const failures = [];
const warnings = [];

function exists(filePath) {
  try {
    fs.accessSync(filePath);
    return true;
  } catch {
    return false;
  }
}

function walk(dir, predicate, acc = []) {
  if (!exists(dir)) return acc;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!['.git', 'node_modules', 'backups'].includes(entry.name)) walk(full, predicate, acc);
    } else if (predicate(full)) {
      acc.push(full);
    }
  }
  return acc;
}

function parseFrontmatter(text) {
  const match = text.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return {};
  const result = {};
  for (const line of match[1].split('\n')) {
    const parts = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (parts) result[parts[1]] = parts[2].trim().replace(/^["']|["']$/g, '');
  }
  return result;
}

function realpathOrNull(filePath) {
  try {
    return fs.realpathSync(filePath);
  } catch {
    return null;
  }
}

if (!exists(skillsRoot)) {
  console.error(`Missing skills directory: ${skillsRoot}`);
  process.exit(2);
}

const skillFiles = walk(skillsRoot, (filePath) => path.basename(filePath) === 'SKILL.md');
const skillByName = new Map();
for (const skillFile of skillFiles) {
  const text = fs.readFileSync(skillFile, 'utf8');
  const frontmatter = parseFrontmatter(text);
  const dir = path.dirname(skillFile);
  const name = path.basename(dir);
  const rel = path.relative(skillsRoot, dir).split(path.sep).join('/');

  if (!frontmatter.name) failures.push(`Missing frontmatter name: ${skillFile}`);
  if (frontmatter.name && frontmatter.name !== name) {
    failures.push(`Frontmatter name '${frontmatter.name}' does not match directory '${name}': ${skillFile}`);
  }
  if (!frontmatter.description?.startsWith('Use when ')) {
    failures.push(`Description must start with 'Use when': ${skillFile}`);
  }
  if (skillByName.has(name)) failures.push(`Duplicate skill name '${name}': ${skillByName.get(name)} and ${skillFile}`);
  skillByName.set(name, { dir, rel, text });
}

if (exists(manifestPath)) {
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  const manifestNames = new Set();
  for (const entry of manifest.managedSkills ?? []) {
    manifestNames.add(entry.name);
    const skill = skillByName.get(entry.name);
    if (!skill) {
      failures.push(`Manifest entry has no matching skill directory: ${entry.name} (${entry.source})`);
      continue;
    }
    if (entry.source !== skill.rel) {
      failures.push(`Manifest source mismatch for ${entry.name}: expected ${skill.rel}, got ${entry.source}`);
    }
  }
  for (const name of [...skillByName.keys()].sort()) {
    if (!manifestNames.has(name)) warnings.push(`Skill is not listed in manifest.json: ${name}`);
  }
} else {
  warnings.push(`Missing manifest.json: ${manifestPath}`);
}

const discoveryRoots = [
  path.join(os.homedir(), '.claude', 'skills'),
  path.join(os.homedir(), '.codex', 'skills'),
  path.join(os.homedir(), '.pi', 'agent', 'skills'),
  path.join(os.homedir(), '.zcode', 'skills'),
];

for (const [name, skill] of skillByName) {
  for (const root of discoveryRoots) {
    if (!exists(root)) continue;
    const linkPath = path.join(root, name);
    if (!exists(linkPath)) {
      warnings.push(`Missing discovery link: ${linkPath}`);
      continue;
    }
    const stat = fs.lstatSync(linkPath);
    if (!stat.isSymbolicLink()) {
      failures.push(`Discovery entry is not a symlink: ${linkPath}`);
      continue;
    }
    const actual = realpathOrNull(linkPath);
    const expected = realpathOrNull(skill.dir);
    if (actual !== expected) {
      failures.push(`Discovery link target mismatch: ${linkPath} -> ${actual}; expected ${expected}`);
    }
  }
}

for (const [name, skill] of skillByName) {
  const supportText = walk(skill.dir, (filePath) => filePath.endsWith('.md'))
    .map((filePath) => fs.readFileSync(filePath, 'utf8'))
    .join('\n');
  const combinedText = `${skill.text}\n${supportText}`;
  const mentionsMultipleAgents = /\b(Codex|Pi|ZCode|Claude Code)\b/.test(combinedText);
  const mentionsSkillDiscovery =
    /~\/\.claude\/skills|~\/\.codex\/skills|~\/\.pi\/agent\/skills|~\/\.zcode\/skills/.test(combinedText);
  if (mentionsMultipleAgents && mentionsSkillDiscovery) {
    for (const marker of ['~/.claude/skills', '~/.codex/skills', '~/.pi/agent/skills', '~/.zcode/skills']) {
      if (!combinedText.includes(marker)) warnings.push(`${name}: multi-agent runtime text does not mention ${marker}`);
    }
  }

  const localSkillRefs = [...combinedText.matchAll(/skills\/[A-Za-z0-9_.\/-]+\/SKILL\.md/g)].map((match) => match[0]);
  for (const ref of localSkillRefs) {
    const target = path.join(repoRoot, ref);
    if (!exists(target)) warnings.push(`${name}: references missing local skill file ${ref}`);
  }
}

for (const warning of warnings) console.log(`WARN ${warning}`);
for (const failure of failures) console.error(`FAIL ${failure}`);
console.log(`Audited ${skillByName.size} skills, ${warnings.length} warnings, ${failures.length} failures.`);
process.exit(failures.length ? 1 : 0);
