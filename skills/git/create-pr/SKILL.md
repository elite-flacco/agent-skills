---
name: create-pr
description: Use when the user asks to create or open a GitHub pull request — e.g. "create a PR", "open a pull request", "make a PR", or push a branch and open it for review.
---

# Create Pull Request

Assume you are already on a branch and changes have been committed.

## Instructions

1. **Verify state** — confirm you're on a feature branch (not `main`), changes are committed, and the branch isn't already merged.
2. **Push** — push the branch to remote with `-u` if it's a new branch:
   ```bash
   git push -u origin <branch-name>
   ```
3. **Summarize changes** — diff against the base branch to understand what changed:
   ```bash
   git log <base>..HEAD --oneline
   git diff <base>...HEAD --stat
   ```
4. **Write the PR body** with these sections:
   - **Summary** — what changed and why, 1–3 sentences.
   - **Changes** — bullet list of notable changes grouped by area.
   - **Test plan** — concrete steps you ran (or should run) to verify; reference commands, tests, or manual checks.
5. **Open the PR** with `gh pr create`, setting title, body, base, and (if relevant) reviewers/labels/draft:
   ```bash
   gh pr create --base main --title "<title>" --body-file <body-file> [--draft] [--reviewer ...]
   ```
6. **Return the PR URL.**

## Notes
- Match the repo's existing PR style (check recent merged PRs for conventions like emoji title prefixes).
- Keep the title under 72 chars; use the body for detail.
- If tests or CI are expected, mention their status.
