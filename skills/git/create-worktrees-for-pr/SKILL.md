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

Read `create-worktree` before proceeding and apply its shared placement, gitignore, environment-file, and verification conventions to every worktree created here.

## Instructions

1. Verify the GitHub CLI is authenticated: `gh auth status`.
2. Fetch current remote branches: `git fetch --all --prune`.
3. For each open PR's head branch, create a worktree at `.worktrees/<branch>` (preserving `/` in the name):

   ```bash
   gh pr list --json headRefName --jq '.[].headRefName' | while read -r branch; do
     path=".worktrees/$branch"
     if [ -d "$path" ]; then
       echo "Worktree for $branch already exists — skipping"
       continue
     fi
     mkdir -p "$(dirname "$path")"
     git worktree add "$path" "$branch"
   done
   ```

4. Apply the shared environment-file rules from `create-worktree` to each new checkout.
5. List the result with `git worktree list` and report created, skipped, and failed branches separately.

## Notes

- Branches that no longer have a remote ref will fail at `git worktree add`; report which ones and skip them.
- These worktrees are removed the same way as any other — use `remove-worktree`.
