---
name: merge-branch
description: Use when the user asks to merge the current feature branch into the default branch — e.g. "merge this branch", "merge into main", "ship this branch", or after a PR is approved and ready to land.
---

# Merge The Current Branch

Merge the current feature branch into the repository's default branch and push. Prefer merging through an approved PR when one exists; fall back to a local merge otherwise.

## Instructions

### 1. Identify the branches

Never assume the default branch is `main` — detect it.

```bash
git branch --show-current                                              # feature branch
git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'   # default branch
```

If `origin/HEAD` isn't set, run `git remote set-head origin -a` first, or fall back to whichever of `main`/`master` exists.

### 2. Prefer merging via the PR

If an open PR exists for the branch, merge it through the host so branch protection, required checks, and review approvals are honored:

```bash
gh pr checks                    # confirm CI is green first
gh pr merge --merge             # or --squash / --rebase per repo convention
```

This is the safest path on any repo with a protected default branch — a local push to `main` will just be rejected. Only fall back to a local merge (below) when there is no PR / no host, or the user explicitly wants a local merge.

### 3. Local merge fallback

**Stash first if the tree is dirty** — `git checkout` fails when uncommitted changes would be overwritten:

```bash
git stash push -u -m "merge-branch: pre-merge stash"   # only if `git status` shows changes
```

Update the default branch, then merge:

```bash
git checkout <default-branch>
git pull origin <default-branch>
git merge --no-ff <feature-branch>    # --no-ff keeps branch history; use plain merge if the repo prefers linear history
```

### 4. Resolve conflicts

If the merge stops on conflicts, resolve them preserving the intent of the feature branch, then continue:

```bash
# edit conflicted files, then:
git add <resolved-files>
git merge --continue
```

Abort with `git merge --abort` if you need to back out. After resolving, run the project's build/tests to confirm the merged result is sound before pushing.

### 5. Push

```bash
git push origin <default-branch>
```

Restore the stash from step 3 if you created one: `git stash pop`.

### 6. Clean up (optional)

Only after the merge has landed on the remote:

```bash
git branch -d <feature-branch>              # -d refuses if not merged — let it
git push origin --delete <feature-branch>
```

## Command Options

- `--squash` / `--rebase`: pass through to `gh pr merge` when the repo prefers a squashed or rebased history.
- `--ff`: use a plain fast-forward merge instead of `--no-ff` for a linear history.
- `--no-cleanup`: keep the feature branch after merging.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Hardcoding `main` as the target | Detect it via `origin/HEAD`; some repos use `master`, `develop`, or `trunk`. |
| Pushing a local merge to a protected branch | Merge through the PR (`gh pr merge`) so protection rules and required checks pass. |
| `git checkout` fails on a dirty tree | Stash (`git stash push -u`) before switching branches, pop after. |
| Merging before CI is green | Run `gh pr checks` (or wait for checks) before merging. |
| Force-deleting the branch with `-D` | Use `-d` — it refuses to drop an unmerged branch, which is the safety you want. |
| Pushing without verifying a conflict resolution | Build/test the merged tree before `git push`. |
