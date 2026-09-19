# Review Process

## Scope

- Prefer the user's named skill files, categories, or repos.
- If scope is "all skills", enumerate skill files with `rg --files skills | rg '/SKILL\.md$'`.
- Exclude backup, generated, vendored, and discovery symlink directories unless the user explicitly asks for them.
- Preserve unrelated local changes. Do not stage, commit, rename, or delete unless asked.

## Batching

- Use a single reviewer for fewer than 8 skills or when the same design judgment spans all files.
- Use subagents for larger audits when each batch can be reviewed independently.
- Batch by category or responsibility, not by arbitrary count alone.
- Give each subagent exact file paths and require:
  - scorecard results using `instructions/rubric.md`
  - file/line evidence for every issue
  - no edits, staging, commits, branch changes, or link-script runs

## Evidence Rules

- Read each selected `SKILL.md` in full before scoring it.
- Verify referenced local files exist when the skill tells agents to read, run, or import them.
- Distinguish mechanical facts from judgment:
  - Mechanical: missing file, stale path, broken manifest entry, invalid frontmatter.
  - Judgment: trigger too broad, workflow too vague, overlap with another skill.
- Do not count many subagent reports from one parent task as many independent signals.
- Treat one-off complaints as feedback, not as proof that a new artifact is needed.

## Synthesis

- Group findings by reusable problem, not by the order files were reviewed.
- Prefer improving an existing skill when the repeated problem belongs to that skill's domain.
- Recommend a script for deterministic checks that are repeated and error-prone.
- Recommend a hook only when the check is cheap, reliable, and should block or warn on every relevant local change.
- Recommend an automation only when the work is periodic and useful without an immediate user prompt.
- Recommend no new artifact when the issue is isolated, subjective, or already covered by an existing skill.

## Output

- Lead with the highest-value findings and decisions.
- Keep scorecards compact; avoid turning the report into a full copy of each skill.
- Include concrete suggested names and trigger criteria for any proposed skill, script, hook, or automation.
- Include exact verification commands and results.

