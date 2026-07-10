# PR Recipe (shared)

Shared recipe for creating a pull request, used by the `create-pr` (GitHub) and
`azdo-create-pr` (Azure DevOps) skills. Both follow these steps; only the final
open-the-PR command and any platform-specific extras (e.g. AzDo work-item
linking) differ — see your own skill for those.

## 1. Verify state

Confirm you're ready to open a PR:

- On a feature branch, not `main`
- Working tree is clean (changes committed)
- The branch isn't already merged

```bash
git status
git log origin/main..HEAD --oneline   # or <base>..HEAD
git diff origin/main...HEAD --stat
```

## 2. Push the branch

If the branch doesn't track a remote or is behind/ahead, push it:

```bash
git push -u origin <branch-name>
```

## 3. Analyze the diff

Read the commit log and diff against the base branch to understand what's in the
PR — what changed, key features/fixes, and which files are affected. This feeds
the PR body.

## 4. Write the PR body

Structure the body as **Summary** + **Test plan**:

```
## Summary

- Bullet point summary of changes
- Key features added
- Important fixes

## Test plan

- [ ] Checklist item 1
- [ ] Checklist item 2
- [ ] Verify feature X works
```

Guidelines:
- Start with a clear summary section — focus on the "why" and impact, not just a file listing.
- Use bullet points for readability.
- Include a test plan with checkboxes — concrete steps you ran (or should run) to verify: commands, tests, or manual checks.
- Keep it concise but informative.

Keep the title under 72 characters; use emoji conventional-commit format
(`✨ feat(scope): ...`). The full emoji + type list is in the `commit` skill's
`references/emoji-commits.md`. Match the repo's existing PR style — check recent
merged PRs for conventions.
