---
name: add-gh-workflows
description: Use when the user asks to set up github workflows.
---

# Add GitHub Workflows

Set up GitHub Actions workflows for a repo by copying the defaults from `~/.claude/github/`.

## Instructions
1. List available default workflows in `~/.claude/github/` and show the user what's available.
2. Copy files into the current repo under `.github/`, preserving the directory structure.
3. **Skip any file that already exists** — never overwrite local customizations. Report which were skipped.
4. Confirm the shared `update-changelog` and `update-readme` skills are available through the user's skill discovery links. Do not copy retired command files into the target repo.
5. After copying, summarize which workflows were added and what each does (e.g. CI test/lint, release, changelog automation).

## Notes
- If `~/.claude/github/` doesn't exist or is empty, tell the user rather than guessing.
- Adapt workflow triggers (branches, Node version, package manager) to match the target repo where the defaults are clearly wrong.
