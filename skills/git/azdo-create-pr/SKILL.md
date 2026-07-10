---
name: azdo-create-pr
description: Use when the user asks to create or open a pull request in an Azure DevOps (Azure Repos / az repos) repository — e.g. "create an AzDo PR", "open a pull request in Azure DevOps", "az login", link a work item to a PR, add a PR reviewer, enable auto-complete, or format an Azure DevOps PR title.
---

# Azure DevOps Create PR

Create a well-formatted pull request in Azure DevOps with proper emoji titles and automatic work-item linking. Uses the Azure CLI (`az repos pr`), not GitHub CLI (`gh pr`).

## Prerequisites

- Azure DevOps repository (not GitHub)
- Azure CLI with the `azure-devops` extension (`az extension add --name azure-devops`)
- Authenticated (`az login` then `az devops login`)
- Changes committed on a feature branch

## Process

Follow the shared PR recipe in `../_shared/pr-recipe.md` for the common steps (verify state → push → analyze diff → write body). The Azure-DevOps-specific steps are below.

### 1. Gather PR information

Ask the user if not provided:

- **PR title** — emoji conventional-commit format (`✨ feat`, `🐛 fix`, `📝 docs`, etc.).
- **Work item ID** to link — always ask: "What work item should this PR be linked to?" Never assume or skip.

### 2. Create the PR

```bash
az repos pr create \
  --title "✨ feat(scope): description" \
  --description "<body with Summary + Test plan>" \
  --source-branch <branch> \
  --target-branch main
```

Set `--auto-complete true` only if the user asks for it.

### 3. Link the work item

After the PR is created, link the work item. Extract the PR ID from the JSON response (`pullRequestId`):

```bash
az repos pr work-item add --id <pr-id> --work-items <work-item-id>
```

### 4. Report the result

Return the PR number, a direct link to the PR, and work-item-linked confirmation. Example shape:

```
✅ Pull request created successfully!

PR #<id>: ✨ feat(scope): <title>

🔗 View PR: https://dev.azure.com/<org>/<project>/_git/<repo>/pullrequest/<id>

✅ Work item #<work-item-id> linked
```

## Error Handling

**If PR creation fails:**
- Check if the branch is pushed to remote
- Verify Azure DevOps authentication
- Ensure the target branch exists
- Check for branch policy violations

**If work-item linking fails:**
- Verify the work item ID exists
- Check user permissions
- Confirm the work item is in the same project

## Notes

- Always ask for and link a work item — it's required for AzDo tracking.
- Use Azure CLI (`az repos pr`), not GitHub CLI (`gh pr`).
- Include a test plan in the PR description.
- Never push directly to `main` — always use a feature branch.
- The full emoji + type prefix list lives in the `commit` skill's `references/emoji-commits.md`.
