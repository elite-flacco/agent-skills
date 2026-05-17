---
name: azdo-create-pr
description: Create Azure DevOps pull requests with proper formatting, emoji titles, and work item linking. Use when user asks to create a PR, make a pull request, or uses /create-pr command in Azure DevOps repositories.
---

# Azure DevOps Create PR

This skill helps create well-formatted pull requests in Azure DevOps with proper emoji titles and automatic work item linking.

## Prerequisites

- Must be in an Azure DevOps repository (not GitHub)
- Azure CLI with DevOps extension installed
- Must be authenticated (`az devops login`)
- Must have changes committed on a feature branch

## Process

### 1. Verify Current State

Check that you're ready to create a PR:

```bash
git status
git log origin/main..HEAD --oneline
git diff origin/main...HEAD --stat
```

Verify:
- You're on a feature branch (not main)
- There are commits to include in the PR
- Changes are committed (working directory is clean)

### 2. Check if Branch is Pushed

```bash
git branch -vv
```

If the branch doesn't track a remote or is behind/ahead, push it:

```bash
git push -u origin <branch-name>
```

### 3. Gather PR Information

Ask the user if not provided:

**Required:**
- PR title (use emoji conventional commit format: ✨ feat, 🐛 fix, 📝 docs, etc.)
- Work item ID to link (ask: "What work item should this PR be linked to?")

**Optional:**
- Additional description details beyond the summary

### 4. Analyze Changes

Review the commit history and diff to understand:
- What changes are included
- Key features or fixes
- Files affected

### 5. Create PR with az CLI

Use `az repos pr create` with proper formatting. Build the description in a format like this:

```bash
az repos pr create --title "✨ Your PR Title" --description "DESCRIPTION_TEXT" --source-branch BRANCH --target-branch main
```

Where DESCRIPTION_TEXT follows this structure:
```
## Summary

- Bullet point summary of changes
- Key features added
- Important fixes

## Test plan

- [ ] Checklist item 1
- [ ] Checklist item 2
- [ ] Verify feature X works

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Guidelines for PR description:**
- Start with a clear summary section
- Use bullet points for readability
- Include a test plan with checkboxes
- Focus on the "why" and impact, not just "what" changed
- Keep it concise but informative

### 6. Link Work Item

After PR is created successfully, link the work item:

```bash
az repos pr work-item add --id <pr-id> --work-items <work-item-id>
```

Extract the PR ID from the JSON response (field: `pullRequestId`)

### 7. Display Success Message

Show the user:
- ✅ PR created with number
- 🔗 Direct link to the PR
- ✅ Work item linked confirmation

Example:
```
✅ Pull request created successfully!

PR #116837: ✨ Add HTML conversion and improve changelog PR fetching

🔗 View PR: https://dev.azure.com/org/project/_git/repo/pullrequest/116837

✅ Work item #353253 linked
```

## Emoji Conventional Commit Prefixes

Use these for PR titles:

- ✨ `feat`: New feature
- 🐛 `fix`: Bug fix
- 📝 `docs`: Documentation changes
- 🔧 `chore`: Tooling, configuration
- ♻️ `refactor`: Code refactoring
- ⚡️ `perf`: Performance improvements
- ✅ `test`: Tests
- 🚀 `ci`: CI/CD improvements
- 🎨 `style`: Code formatting/structure
- 💚 `fix`: Fix CI build
- 🔒️ `fix`: Security fix
- 🚑️ `fix`: Critical hotfix

## Error Handling

**If PR creation fails:**
- Check if branch is pushed to remote
- Verify Azure DevOps authentication
- Ensure target branch exists
- Check for branch policy violations

**If work item linking fails:**
- Verify work item ID exists
- Check if user has permissions
- Confirm work item is in the same project

## Important Notes

- **Always ask for work item ID** - don't assume or skip this step
- **Always link work item** - this is critical for tracking
- Use Azure CLI (`az repos pr`), not GitHub CLI (`gh pr`)
- PR title should use emoji conventional commit format
- Include test plan in PR description
- Don't push directly to main - always use a feature branch

## Example Flow

```
User: "Create a PR"
Claude: "What work item should this PR be linked to?"
User: "353253"
Claude:
  1. Verifies branch state
  2. Pushes branch if needed
  3. Creates PR with proper title and description
  4. Links work item 353253
  5. Shows success message with PR link
```
