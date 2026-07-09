---
name: create-worktree
description: Use when the user asks to create a git worktree.
---

# Create Git Worktree

Create a new branch and a linked worktree for it.

## Instructions
1. **Create a new branch** with the name the user specifies.
2. **Create the worktree** inside the repo at `.worktrees/<branch-name>` (add `.worktrees/` to `.gitignore` if missing):
   ```bash
   git worktree add .worktrees/<branch-name> -b <branch-name>
   ```
   Preserve `/` in the branch name (e.g. `zcode/feat/add-login` → `.worktrees/zcode/feat/add-login`).
3. **Copy env files** from the main checkout into the new worktree root, in order, whichever exist:
   - `.env`
   - `.env.local`
   - `.env.development` / `.env.production` (if present in the main checkout)

   These are gitignored and must be copied manually — never sync them back.
4. **Confirm** the worktree is usable: `git worktree list`.
