---
name: commit
description: Use when the user asks to commit staged or modified changes — e.g. "commit this", "create a commit", "make a commit", "git add", "amend", "stash", "write a commit message", "conventional commit", "pre-commit hook", or split changes into multiple commits.
---

# Commit Changes

Create well-formatted commits with emoji conventional-commit messages. Split changes into multiple commits when the diff contains distinct logical changes.

## Instructions

1. Unless skipped with `--no-verify`, run the project's full verification suite before committing — whatever checks the project defines (lint, typecheck, test, build, format check). Discover them from `package.json` scripts, `Makefile`, or CI config (`.github/workflows/`), not by assuming a specific toolchain. Do not hardcode a single framework's commands.
2. Update `README.md` as needed.
3. Check which files are staged with `git status`.
4. If 0 files are staged, add all modified and new files with `git add`.
5. Do not add any untracked files if files are already staged.
6. Run a `git diff` (staged) to understand what is being committed.
7. Analyze the diff to determine if multiple distinct logical changes are present.
8. If multiple distinct changes are detected, suggest breaking the commit into smaller commits (see Guidelines for Splitting below).
9. For each commit (or the single commit if not split), write a commit message in emoji conventional-commit format — see `references/emoji-commits.md` for the full emoji + type list.
10. If currently on the `main` branch, push to remote after committing.

## Guidelines for Splitting Commits

Split commits based on these criteria:

1. **Different concerns**: changes to unrelated parts of the codebase
2. **Different types of changes**: mixing features, fixes, refactoring, etc.
3. **File patterns**: changes to different types of files (e.g. source code vs documentation)
4. **Logical grouping**: changes that would be easier to understand or review separately
5. **Size**: very large changes that would be clearer broken down

## Command Options

- `--no-verify`: skip running the pre-commit verification suite

## Important Notes

- By default, the verification suite runs before committing to ensure code quality.
- If format check fails, run the project's format command to fix. If other checks fail, ask the user whether to fix first or proceed with the commit anyway.
- If specific files are already staged, commit only those files; do not stage any untracked files.
- If no files are staged, stage all modified and new files automatically.
- Construct the commit message based on the changes detected in the diff.
- Review the diff to identify whether multiple commits would be more appropriate.
