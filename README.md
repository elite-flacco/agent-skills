# Personal Agent Skills

This repository is the source of truth for user-authored skills shared across Claude Code and Codex.

## Layout

- `skills/` contains categorized real skill folders. Each leaf folder should include a `SKILL.md`.
- `legacy-claude-commands/` preserves the old Claude Code slash command markdown files after conversion.
- `scripts/link.ps1` creates discovery junctions in `~/.claude/skills` and `~/.codex/skills`.
- `scripts/validate.ps1` verifies every managed skill has a `SKILL.md` and matching junctions.
- `backups/` stores replaced discovery folders and retired command files from migrations.
- `manifest.json` lists the managed skills and converted command sources.

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
```

## Typical Workflow

Create and edit skills in the appropriate category under `skills/`, update `manifest.json`, then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\link.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\validate.ps1
```

Commit changes from this repository.

## Encoding Guard

Codex and Windows PowerShell can display or accidentally preserve UTF-8 mojibake when handling emoji, arrows, curly quotes, and dashes. Before committing, run `scripts/validate.ps1`; it fails when `SKILL.md` files contain common corrupted UTF-8 marker characters.
