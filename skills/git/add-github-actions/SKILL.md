---
name: add-github-actions
description: Use when the user asks to set up GitHub Actions workflows / CI for a repo — e.g. "add CI", "set up GitHub workflows", "add GitHub Actions", "configure continuous integration", "set up pipeline", "add .github/workflows yaml".
---

# Add GitHub Actions

Set up GitHub Actions workflows for a repo by copying the defaults from the agent's home directory.

## Instructions

1. **Locate the workflow defaults.** They live under `<runtime-home>/github/` — check in this order and use the first that exists: `~/.zcode/github/`, `~/.codex/github/`, `~/.claude/github/`. List what's available and show the user before copying.
2. **Copy files into the repo** under `.github/`, preserving directory structure.
3. **Skip any file that already exists** — never overwrite local customizations. Report which were skipped.
4. Confirm the shared `update-changelog` and `update-readme` skills are available through the user's skill discovery links. Do not copy retired command files into the target repo.
5. **Summarize each added workflow** by reading its `name:` and `on:` fields — state what it runs and when it triggers (e.g. "CI: runs lint/typecheck/test on push and PR").
6. **Adapt triggers where the defaults are clearly wrong** for the target repo — branches, Node version, package manager (`npm`/`pnpm`/`yarn`). Confirm the job runs the repo's actual verify command (`npm run verify`, or the lint/typecheck/format/test scripts).

## Notes
- If no `<runtime-home>/github/` directory exists or it's empty, tell the user rather than guessing — don't fabricate workflow YAML from scratch here.
