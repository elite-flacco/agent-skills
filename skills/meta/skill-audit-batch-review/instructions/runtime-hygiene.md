# Runtime Hygiene

Use these checks when skills are installed or discovered by multiple agents.

## Discovery Surfaces

Expected user skill discovery directories on this machine:

- Claude Code: `~/.claude/skills`
- Codex: `~/.codex/skills`
- Pi: `~/.pi/agent/skills`
- ZCode: `~/.zcode/skills`

In this repo, these should usually be symlinks to directories under `skills/<category>/<skill-name>`. Do not create or edit discovery-surface files directly; update the source skill and run the repo link script.

## Manifest Hygiene

- `manifest.json` should contain one entry per managed skill.
- The manifest `name` should match the skill directory leaf and `SKILL.md` frontmatter name.
- The manifest `source` should point to the categorized directory under `skills/`.
- After adding, moving, or renaming skills in this repo, run:

```bash
./scripts/macos/sync-manifest.sh
./scripts/macos/link.sh
./scripts/macos/validate.sh
```

## Runtime Reference Drift

Flag stale or runtime-specific assumptions when a skill is meant to work across agents:

- Hard-coded `~/.claude/skills` without Codex/Pi/ZCode equivalents.
- Mentions of `.claude` config when the task is about Codex, Pi, or ZCode runtime config.
- Missing ZCode references for repo-wide discovery or link validation.
- Instructions that say "Claude" generically when they mean the active coding agent.
- Paths copied from old names after a rename.

Do not flag a runtime-specific path when the skill is intentionally specific to that runtime and says so clearly.

## Hook and Script Decisions

- Prefer a script for checks that are useful on demand or during audits.
- Prefer a hook only for fast, deterministic checks that should run for every relevant commit.
- Avoid hooks that require network access, browser automation, API keys, or subjective review.

