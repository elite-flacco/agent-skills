---
name: create-worktrees-for-pr
description: Use when the user wants git worktrees for all open pull requests so each can be reviewed in parallel — e.g. "create worktrees for all PRs", "check out every open PR", "set up worktrees for review".
---

# Create Worktrees For Open PRs

Create one git worktree per open pull request, so each PR can be built, run, and reviewed in its own checkout.

## When to Use

- User wants to review multiple open PRs and needs each checked out locally.
- User asks to "create worktrees for all PRs" or similar.

For a **single** new-branch worktree, use the `create-worktree` skill instead. To **remove** worktrees, use `remove-worktree`.

## Instructions

1. Ensure `.worktrees/` exists and is gitignored (add `.worktrees/` to `.gitignore` if missing).
2. Verify the GitHub CLI is authenticated: `gh auth status`.
3. For each open PR's head branch, create a worktree at `.worktrees/<branch>` (preserving `/` in the name):

   ```bash
   gh pr list --json headRefName --jq '.[].headRefName' | while read -r branch; do
     path=".worktrees/$branch"
     if [ -d "$path" ]; then
       echo "Worktree for $branch already exists — skipping"
       continue
     fi
     mkdir -p "$path"
     git worktree add "$path" "$branch"
   done
   ```

4. **Copy env files** (`.env`, `.env.local`, `.env.*`) from the main checkout into each new worktree root — they're gitignored and must be copied manually. Never sync them back. (Same rule as `create-worktree`.)
5. List the result: `git worktree list`.

## Notes

- Branches that no longer have a remote ref will fail at `git worktree add`; report which ones and skip them.
- These worktrees are removed the same way as any other — use `remove-worktree`.
