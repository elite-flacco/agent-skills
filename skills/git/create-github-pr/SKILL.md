---
name: create-github-pr
description: Use when the user asks to create or open a GitHub pull request — e.g. "create a PR", "open a pull request", "make a PR", "gh pr create", "open it for review", or push a branch and open it for review. Also covers draft PRs, requesting reviewers, and choosing a base branch.
---

# Create GitHub Pull Request

Create a GitHub pull request. Assume you are already on a branch and changes have been committed.

## Instructions

Follow the PR recipe in `references/pr-recipe.md` (verify state → push → analyze diff → write body). Then open the PR with `gh`:

```bash
gh pr create --base <base> --title "<title>" --body-file <body-file> [--draft] [--reviewer ...] [--label ...]
```

Return the PR URL.

## Notes

- If the repo has a `.github/PULL_REQUEST_TEMPLATE.md`, follow its required sections instead of inventing your own.
- `--draft` opens a draft PR; `--reviewer` and `--label` are optional — only set them when the user asks.
- Match the repo's existing PR style (check recent merged PRs for conventions like emoji title prefixes).
- Keep the title under 72 chars; use the body for detail.
- If tests or CI are expected, mention their status.
