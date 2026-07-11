---
name: list-github-prs
description: Use when the user asks to list, show, or review open pull requests on GitHub — e.g. "show my PRs", "what PRs are open", "list pull requests", "show open PRs across my repos", "gh pr list", or review PRs across repositories.
---

# List GitHub Pull Requests

List all open PRs on the current repo, or across all of the authenticated GitHub user's repos with `--all`.

## Instructions

1. Check if the `--all` flag is provided.
2. If `--all`:
   - Get the authenticated GitHub user's username using `gh api user`.
   - List all repositories owned by the user using `gh repo list --limit 1000 --json nameWithOwner`.
     - Note: `--limit 1000` across many repos makes many API calls and can hit GitHub's rate limit. If you receive a rate-limit error, narrow the scope (fewer repos, or a specific repo) and retry.
   - For each repository, fetch open PRs using `gh pr list --repo <owner/repo> --state open --json number,title,author,headRefName,baseRefName,url,createdAt,updatedAt`.
   - Display all PRs grouped by repository.
3. If not `--all`:
   - Detect the current repository from the working directory:
     - Check if we're in a git repository using `git rev-parse --is-inside-work-tree`.
     - If not in a git repo, show an error message.
     - Get the remote URL using `git remote get-url origin` (or check other remotes if origin doesn't exist).
     - Extract the owner/repo from the remote URL:
       - For HTTPS: `https://github.com/owner/repo.git` → `owner/repo`
       - For SSH: `git@github.com:owner/repo.git` → `owner/repo`
       - Remove `.git` suffix if present.
   - Fetch open PRs for the current repo using `gh pr list --state open --json number,title,author,headRefName,baseRefName,url,createdAt,updatedAt`.
   - Display the PRs in the output format below.

## Output Format

**owner/repo** (when using `--all`)

- **#42** · [Fix token refresh](https://github.com/owner/repo/pull/42)
  - author · `fix/token-refresh` → `main`
  - created 2026-07-01 · updated 2026-07-08

- **#39** · [Add dark mode toggle](https://github.com/owner/repo/pull/39)
  - author · `feat/dark-mode` → `main`
  - created 2026-06-25 · updated 2026-07-09

If there are no open PRs, say so explicitly rather than rendering an empty list.
