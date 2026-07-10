---
name: clean-branches
description: Use when the user asks to clean up, delete, or prune merged or stale git branches — e.g. "clean up branches", "delete merged branches", "remove old branches", "prune remote tracking branches".
---

# Clean Branches

Clean up merged and stale git branches.

## Instructions

Follow this systematic approach. **Never delete a branch that isn't merged into the default branch** unless the user explicitly confirms — use `git branch --merged` to verify before `-d`.

### 1. Repository State Analysis

```bash
# Check current status
git status
git branch -a
git remote -v

# Detect the default branch name
git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'
```

### 2. Safety Precautions

- Ensure the working directory is clean.
- Switch to the default branch and pull latest.
- Create a backup of the current branch state if needed.

```bash
git stash push -m "Backup before branch cleanup"
git checkout main  # or master, per step 1
git pull origin main
```

### 3. Identify Merged Branches

```bash
# List merged local branches (exclude protected branches)
git branch --merged main | grep -v "main\|master\|develop\|\*"

# List merged remote branches
git branch -r --merged main | grep -v "main\|master\|develop\|HEAD"
```

### 4. Identify Stale Branches

```bash
# List branches by last commit date
git for-each-ref --format='%(committerdate) %(authorname) %(refname)' --sort=committerdate refs/heads

# Find branches older than 30 days
# macOS (BSD date): use -v-30d. Linux (GNU date): use -d '30 days ago'.
git for-each-ref --format='%(refname:short) %(committerdate)' refs/heads | awk '$2 < "'$(date -v-30d '+%Y-%m-%d' 2>/dev/null || date -d '30 days ago' '+%Y-%m-%d')'"'
```

### 5. Interactive Branch Review

Review each candidate before deletion. Check for unmerged commits and confirm purpose.

```bash
# Check for commits on the branch not in main
git log main..<branch-name> --oneline
```

### 6. Local Branch Cleanup

```bash
# Delete merged branches (interactive — prompts per branch)
git branch --merged main | grep -v "main\|master\|develop\|\*" | xargs -n 1 -p git branch -d

# Force delete only if the user explicitly confirms the branch is safe to lose
git branch -D <branch-name>
```

### 7. Remote Branch Cleanup

```bash
# Prune remote tracking branches deleted on the remote
git remote prune origin

# Delete a remote branch
git push origin --delete <branch-name>

# Remove local tracking of a deleted remote branch
git branch -dr origin/<branch-name>
```

### 8. Protected Branches

Never delete protected branches. Common defaults: `main`, `master`, `develop`, `staging`, `production`. Configure branch protection rules in your hosting provider (GitHub/Azure DevOps) rather than relying on local discipline.

### 9. Verification

```bash
# Verify important branches are still present and remote is in sync
git branch -a
git remote show origin
```

### 10. Rollback (recover a deleted branch)

Deleted branches are recoverable from the reflog until the commits are garbage-collected.

```bash
git reflog --no-merges --since="2 weeks ago"
git checkout -b <recovered-branch> <commit-hash>
```

## Advanced Cleanup

```bash
# Clean up all merged feature/hotfix/bugfix branches except protected ones
git branch --merged main | grep -E "^  (feature|hotfix|bugfix)/" | xargs -n 1 git branch -d

# Interactive cleanup with confirmation
git branch --merged main | grep -v "main\|master\|develop" | xargs -n 1 -p git branch -d

# Batch delete merged remote branches
git branch -r --merged main | grep origin | grep -v "main\|master\|develop\|HEAD" | cut -d/ -f2- | xargs -n 1 git push origin --delete
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `-D` (force) when `-d` would do | `-d` refuses unmerged branches — let it. Only `-D` when the user confirms the branch is disposable. |
| Deleting a branch not merged into the default branch | Always check `git branch --merged main` first. |
| Forgetting to prune remote tracking refs | Run `git remote prune origin` after remote deletions. |
| Not protecting important branches | Set protection rules in GitHub/Azure DevOps, not just locally. |
