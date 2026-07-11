---
name: update-readme
description: Use when the user asks to update or refresh the README from recent commits/repo changes — e.g. "update the readme", "the readme is out of date", "add the new feature to the readme".
---

# Update Readme

Review changes since the last README update and refresh `README.md` to reflect them.

## Instructions

1. **Find the baseline** — identify the last commit that touched `README.md`:
   ```bash
   git log -1 --format=%H -- README.md
   ```
2. **Diff since baseline** to see what changed:
   ```bash
   git diff <last-readme-commit>..HEAD --stat
   ```
3. **Update the README** — add, revise, or remove sections to match the current state. Focus on:
   - Setup/installation steps and prerequisites
   - Available scripts and commands
   - Project structure (if it changed materially)
   - Features or capabilities added/removed
4. **Don't over-edit** — keep the existing tone and structure. Only change what the diff justifies.
5. **Format** if the project has a formatter:
   ```bash
   npm run format
   ```
6. **If the user asks to open a PR**, create a branch, commit the README change, and open a PR (use the `create-github-pr` skill).

## Notes
- Only edit `README.md` content that is now inaccurate — avoid churn.
- If the README references version numbers or badges, confirm they're still correct.
