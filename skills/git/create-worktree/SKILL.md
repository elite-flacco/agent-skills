---
name: create-worktree
description: Use when the user asks to create or add a git worktree, work in an isolated checkout, or set up a parallel branch directory.
---

# Create Git Worktree

Create a safe linked checkout for a new or existing branch.

## Instructions

1. Inspect the repository before changing it:

   ```bash
   git status --short --branch
   git worktree list
   git branch --list <branch-name>
   ```

2. Choose the branch name:
   - Respect a name explicitly supplied by the user.
   - Otherwise use the active coding agent's prefix: `codex/`, `claude/`, or `zcode/`.
   - Follow `<agent>/<type>/<short-kebab-description>`, where type is `feat`, `fix`, `chore`, or `exp`.

3. Ensure `.worktrees/` is ignored. Add it to the repository's `.gitignore` only when missing.

4. Create the worktree at `.worktrees/<branch-name>`, preserving `/` in the branch name:
   - Existing local branch: `git worktree add .worktrees/<branch-name> <branch-name>`
   - New branch: `git worktree add -b <branch-name> .worktrees/<branch-name> <base-ref>`

   Use the base ref requested by the user. If none was requested, use the currently checked-out commit and state that choice. Do not attach a branch already checked out in another worktree.

5. Copy environment files from the main checkout into the new worktree root, in order, whichever exist:
   - `.env`
   - `.env.local`
   - `.env.development` / `.env.production` (if present in the main checkout)

   Treat these as independent local copies: never commit them or sync them back. Do not overwrite a file that already exists in the target.

6. Confirm the result with `git worktree list` and report the branch, base ref, and absolute worktree path.
