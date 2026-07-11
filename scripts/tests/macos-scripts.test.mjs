import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { describe, it } from 'node:test';

const repoRoot = path.resolve(import.meta.dirname, '..', '..');

function run(command, args, options = {}) {
  return execFileSync(command, args, {
    cwd: repoRoot,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    ...options,
  });
}

function tempHome() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'agent-skills-home-'));
}

describe('macOS setup scripts', () => {
  it('keeps macOS scripts separate from the PowerShell scripts', () => {
    for (const script of [
      'check.sh',
      'install-hooks.sh',
      'link.sh',
      'pre-commit.sh',
      'sync-manifest.sh',
      'validate.sh',
    ]) {
      const fullPath = path.join(repoRoot, 'scripts', 'macos', script);
      assert.equal(fs.existsSync(fullPath), true, `${script} should exist`);
      assert.equal((fs.statSync(fullPath).mode & 0o111) !== 0, true, `${script} should be executable`);
      assert.equal(fs.existsSync(path.join(repoRoot, 'scripts', `${path.basename(script, '.sh')}-macos.sh`)), false);
    }

    assert.equal(fs.existsSync(path.join(repoRoot, 'scripts', 'link.ps1')), true);
    assert.equal(fs.existsSync(path.join(repoRoot, 'scripts', 'check.ps1')), true);
  });

  it('links every managed skill into all agent discovery folders', () => {
    const home = tempHome();
    const output = run('bash', ['scripts/macos/link.sh'], {
      env: { ...process.env, HOME: home },
    });
    const manifest = JSON.parse(fs.readFileSync(path.join(repoRoot, 'manifest.json'), 'utf8'));

    assert.match(output, new RegExp(`Linked ${manifest.managedSkills.length} skills`));
    for (const skill of manifest.managedSkills) {
      for (const root of ['.claude/skills', '.codex/skills', '.pi/agent/skills', '.zcode/skills']) {
        const linkPath = path.join(home, root, skill.name);
        assert.equal(fs.lstatSync(linkPath).isSymbolicLink(), true, `${linkPath} should be a symlink`);
        assert.equal(
          fs.realpathSync(linkPath),
          fs.realpathSync(path.join(repoRoot, 'skills', skill.source)),
        );
      }
    }
  });

  it('prunes stale links into this repo but leaves foreign entries alone', () => {
    const home = tempHome();
    const claudeSkills = path.join(home, '.claude', 'skills');
    fs.mkdirSync(claudeSkills, { recursive: true });

    const staleLink = path.join(claudeSkills, 'renamed-away-skill');
    fs.symlinkSync(path.join(repoRoot, 'skills', 'no-longer-exists'), staleLink, 'dir');
    const foreignLink = path.join(claudeSkills, 'foreign-skill');
    fs.symlinkSync(os.tmpdir(), foreignLink, 'dir');
    const plainDir = path.join(claudeSkills, 'plain-dir-skill');
    fs.mkdirSync(plainDir);

    const output = run('bash', ['scripts/macos/link.sh'], {
      env: { ...process.env, HOME: home },
    });

    assert.match(output, /Pruned stale link .*renamed-away-skill/);
    assert.throws(() => fs.lstatSync(staleLink), { code: 'ENOENT' }, 'stale repo link should be removed');
    assert.equal(fs.lstatSync(foreignLink).isSymbolicLink(), true, 'foreign link should survive');
    assert.equal(fs.statSync(plainDir).isDirectory(), true, 'plain directory should survive');
  });

  it('validates linked skills and manifest skill metadata without rewriting sourceRoot', () => {
    const home = tempHome();
    run('bash', ['scripts/macos/link.sh'], {
      env: { ...process.env, HOME: home },
    });

    const output = run('bash', ['scripts/macos/check.sh'], {
      env: { ...process.env, HOME: home },
    });

    assert.match(output, /manifest managedSkills are current/);
    assert.match(output, /Validated \d+ managed skills/);
  });

  it('does not keep retired discovery metadata or cleanup switches', () => {
    const manifest = JSON.parse(fs.readFileSync(path.join(repoRoot, 'manifest.json'), 'utf8'));
    assert.equal(Object.hasOwn(manifest, 'retiredDiscovery'), false);

    for (const script of ['link.sh', 'pre-commit.sh', 'sync-manifest.sh']) {
      const scriptText = fs.readFileSync(path.join(repoRoot, 'scripts', 'macos', script), 'utf8');
      assert.equal(scriptText.includes('retire'), false, `${script} should not include retire behavior`);
      assert.equal(scriptText.includes('claude-command-'), false, `${script} should not clean old wrapper names`);
      assert.equal(scriptText.includes('claude-skill-'), false, `${script} should not clean old prefixed names`);
      assert.equal(scriptText.includes('retiredDiscovery'), false, `${script} should not preserve retired metadata`);
    }

    for (const script of ['link.ps1', 'pre-commit.ps1', 'sync-manifest.ps1']) {
      const scriptText = fs.readFileSync(path.join(repoRoot, 'scripts', script), 'utf8');
      assert.equal(scriptText.includes('Retire'), false, `${script} should not include retire behavior`);
      assert.equal(scriptText.includes('retiredDiscovery'), false, `${script} should not preserve retired metadata`);
      assert.equal(scriptText.includes('claude-command-*'), false, `${script} should not clean old wrapper names`);
      assert.equal(scriptText.includes('claude-skill-*'), false, `${script} should not clean old prefixed names`);
    }
  });

  it('installs the shared hooks path', () => {
    const tmpRepo = fs.mkdtempSync(path.join(os.tmpdir(), 'agent-skills-repo-'));
    fs.cpSync(repoRoot, tmpRepo, {
      recursive: true,
      filter: (source) => !source.includes(`${path.sep}.git${path.sep}`) && !source.endsWith(`${path.sep}.git`),
    });
    execFileSync('git', ['init'], { cwd: tmpRepo, stdio: 'ignore' });

    const output = execFileSync('bash', ['scripts/macos/install-hooks.sh'], {
      cwd: tmpRepo,
      encoding: 'utf8',
    });
    const hooksPath = execFileSync('git', ['config', '--get', 'core.hooksPath'], {
      cwd: tmpRepo,
      encoding: 'utf8',
    }).trim();

    assert.match(output, /Configured Git hooks path: \.githooks/);
    assert.equal(hooksPath, '.githooks');
  });
});
