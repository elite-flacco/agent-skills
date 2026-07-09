---
name: remove-worktree
description: Use when the user asks to remove a git worktree.
---

# Remove Worktree

Remove the git worktree the user names and delete its directory.

## Instructions

1. **List worktrees** to confirm the name:
   ```bash
   git worktree list
   ```
2. **Check for uncommitted changes** before removing — if present, warn the user and confirm:
   ```bash
   git -C <worktree-path> status --porcelain
   ```
3. **Remove the worktree**:
   ```bash
   git worktree remove <worktree-path>
   ```
   - If git refuses because of uncommitted/untracked files and the user confirms it's OK to discard, use `--force`.
4. **Clean up the branch** if it was exclusive to that worktree and is no longer needed:
   ```bash
   git branch -d <branch-name>
   ```
5. **Prune** stale worktree admin entries if any remain:
   ```bash
   git worktree prune
   ```
