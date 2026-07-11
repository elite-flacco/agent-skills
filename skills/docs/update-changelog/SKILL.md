---
name: update-changelog
description: Use when the user asks to update or generate a project changelog (CHANGELOG.md) or release notes from recent commits/repo changes — e.g. "update the changelog", "add a changelog entry", "what changed since the last release", "generate release notes".
---

# Update Changelog

Maintain a project changelog following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format. If the changelog does not exist, create it from `templates/CHANGELOG.md`. If it exists, update it with all notable changes since it was last updated.

## Instructions

1. If `CHANGELOG.md` does not exist, create it from [templates/CHANGELOG.md](templates/CHANGELOG.md). Otherwise read the existing file.
2. Determine the scope of changes since the last changelog entry — diff against the last version tag or the last dated entry:
   ```bash
   git log <last-tag>..HEAD --oneline   # or a range that covers the gap
   ```
3. Categorize changes under the Keep a Changelog sections (Added / Changed / Deprecated / Removed / Fixed / Security). Include only user-facing changes; skip purely internal refactors unless they affect behavior.
4. Unless `--no-version` is specified, add a version entry dated today (move Unreleased items under the new version). With `--no-version`, add entries under `## [Unreleased]` only.
5. When `--create-pr` is specified, create a pull request with the changelog changes.
6. Format the changelog with the project's formatter (e.g. `npm run format` / `pnpm format` / `dprint fmt`) — use whatever the repo already defines.

## Automation (optional)

For repos using conventional commits, generation can be automated:

```bash
# conventional-changelog (angular preset)
npm install -D conventional-changelog-cli
npx conventional-changelog -p angular -i CHANGELOG.md -s

# auto-changelog
npm install -D auto-changelog
npx auto-changelog
```

Keep entries clear, categorized, and focused on user-facing changes.
