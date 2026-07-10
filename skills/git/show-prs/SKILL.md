---
name: show-prs
description: Use when the user asks to list, show, or review open pull requests — e.g. "show my PRs", "what PRs are open", "list pull requests", "show open PRs across my repos".
---

# Show Open Pull Requests

This command pulls all open PRs on a given repo or all your repos.

## Instructions

1. Check if the `--all` flag is provided
2. If `--all`:
   - Get the authenticated GitHub user's username using `gh api user`
   - List all repositories owned by the user using `gh repo list --limit 1000 --json nameWithOwner`
   - For each repository, fetch open PRs using `gh pr list --repo <owner/repo> --state open --json number,title,author,headRefName,baseRefName,url,createdAt,updatedAt`
   - Display all PRs grouped by repository
3. If not `--all`:
   - Detect the current repository from the working directory:
     - Check if we're in a git repository using `git rev-parse --is-inside-work-tree`
     - If not in a git repo, show an error message
     - Get the remote URL using `git remote get-url origin` (or check other remotes if origin doesn't exist)
     - Extract the owner/repo from the remote URL:
       - For HTTPS: `https://github.com/owner/repo.git` → `owner/repo`
       - For SSH: `git@github.com:owner/repo.git` → `owner/repo`
       - Remove `.git` suffix if present
   - Fetch open PRs for the current repo using `gh pr list --state open --json number,title,author,headRefName,baseRefName,url,createdAt,updatedAt`
   - Display the PRs in a formatted, readable way

## Output Format

Display PRs with:
- Repository name (when using `--all`)
- PR number and title (include hyperlink to the PR)
- Author
- Branch information (head -> base)
- Created and updated dates
- Format the output in a clear, readable table or list format, with the section header bolded
