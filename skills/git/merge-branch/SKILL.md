---
name: merge-branch
description: Use when the user asks to merge the current feature branch into main — e.g. "merge this branch", "merge into main", "ship this branch", or after a PR is approved and ready to land.
---

# Merge The Current Branch

Merge the current feature branch into `main` and push. Ignore untracked files or uncommitted changes.

## Instructions

1. **Confirm the target** — identify the main branch (`main` or `master`) and current branch:
   ```bash
   git branch --show-current
   ```
2. **Check CI** — if there's an open PR, confirm CI is green before merging:
   ```bash
   gh pr checks
   ```
3. **Switch to main and update**:
   ```bash
   git checkout main
   git pull origin main
   ```
4. **Merge** the feature branch. Prefer `--no-ff` to preserve branch history unless the repo convention differs:
   ```bash
   git merge --no-ff <branch-name>
   ```
5. **Resolve conflicts** if any arise — keep the intent of the feature branch, and validate that the result builds/tests.
6. **Push** main to remote:
   ```bash
   git push origin main
   ```
7. **Clean up** (optional) — delete the merged local and remote branch:
   ```bash
   git branch -d <branch-name>
   git push origin --delete <branch-name>
   ```
