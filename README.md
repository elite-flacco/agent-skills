# Personal Agent Skills

A collection of skills covering git/PR workflows, project bootstrapping, frontend/design, cloud deployment, integrations, and more, shared across Claude Code, Codex, Pi, and ZCode.

## Layout

- `skills/` contains categorized real skill folders. Each leaf folder should include a `SKILL.md`.
- `scripts/` contains PowerShell scripts for Windows; `scripts/macos/` contains bash equivalents.
  - `sync-manifest` regenerates `manifest.json` from `skills/**/SKILL.md`.
  - `link` creates discovery junctions/symlinks in `~/.claude/skills`, `~/.codex/skills`, `~/.pi/agent/skills`, and `~/.zcode/skills`, and removes stale links left behind by renamed or deleted skills (only links that point into this repo; anything else is left alone).
  - `check` verifies `manifest.json`, managed skill files, and matching junctions.
  - `validate` checks `SKILL.md` files for corrupted UTF-8.
- `.githooks/pre-commit` detects the OS and delegates to the platform-specific scripts. It syncs generated metadata, refreshes discovery links, validates, and stages `manifest.json`.
- `backups/` stores replaced discovery folders when a setup script needs to move an existing conflicting path out of the way.
- `manifest.json` lists the managed skills.

Sync only creates/updates a symlink per managed skill (named after `manifest.json`'s `name` field) inside each agent's skills folder — it never touches or replaces the folder as a whole. This is intentional: it lets `~/.claude/skills`, `~/.codex/skills`, `~/.pi/agent/skills`, and `~/.zcode/skills` also hold skills you download or install from elsewhere, alongside the ones managed by this repo.

Discovery folders remain flat. `manifest.json` maps each flat discovery name to a categorized source folder:

```json
{
  "name": "git-commit",
  "source": "git/commit"
}
```

This creates:

```text
~/.claude/skills/git-commit -> skills/git/commit
~/.codex/skills/git-commit  -> skills/git/commit
~/.pi/agent/skills/git-commit -> skills/git/commit
~/.zcode/skills/git-commit -> skills/git/commit
```

## Typical Workflow

Install the repository hook once:

```powershell
# Windows
powershell -ExecutionPolicy Bypass -File .\scripts\install-hooks.ps1
```

```bash
# macOS
./scripts/macos/install-hooks.sh
./scripts/macos/link.sh
```

After that, create and edit skills in the appropriate category under `skills/`. On commit, the hook stages skill-file changes, regenerates `manifest.json`, refreshes skill discovery links, validates the repo, and stages the generated manifest update automatically.

For a manual check without committing, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check.ps1
```

On macOS:

```bash
./scripts/macos/check.sh
```

Commit changes from this repository.

## Encoding Guard

Codex and Windows PowerShell can display or accidentally preserve UTF-8 mojibake when handling emoji, arrows, curly quotes, and dashes. The pre-commit hook runs `validate` automatically; to check manually, run `scripts/validate.ps1` (Windows) or `scripts/macos/validate.sh` (macOS). It fails when `SKILL.md` files contain common corrupted UTF-8 marker characters.
