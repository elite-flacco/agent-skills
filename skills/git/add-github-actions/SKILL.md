---
name: add-github-actions
description: Use when the user asks to set up GitHub Actions workflows / CI for a repo — e.g. "add CI", "set up GitHub workflows", "add GitHub Actions", "configure continuous integration", "set up pipeline", "add .github/workflows yaml".
---

# Add GitHub Actions

Set up GitHub Actions workflows for a repo by copying the defaults from this skill's `templates/`.

## Instructions

1. **Use this skill's `templates/` as the source**: copy `templates/workflows/*.yml` → `.github/workflows/` and `templates/dependabot.yml` → `.github/dependabot.yml`.
2. **Copy files into the repo** under `.github/`, preserving directory structure.
3. **Skip any file that already exists** — never overwrite local customizations. Report which were skipped.
4. Confirm the shared `update-readme` skill is available through the user's skill discovery links.
5. **Summarize each added workflow** by reading its `name:` and `on:` fields — state what it runs and when it triggers (e.g. "CI: runs lint/typecheck/test on push and PR").
6. **Adapt the copies to the target repo**: remove CI steps whose npm scripts don't exist (lint / typecheck / format:check / test:run / build); the Dependabot groups assume a Next.js/npm stack — adjust the patterns to the repo's dependencies.
7. **Adapt triggers where the defaults are clearly wrong** for the target repo — branches, Node version, package manager (`npm`/`pnpm`/`yarn`). Confirm the job runs the repo's actual verify command (`npm run verify`, or the lint/typecheck/format/test scripts).
