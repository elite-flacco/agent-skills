# Skill Audit Rubric

Score each dimension as `pass`, `minor`, `major`, or `not applicable`. Use `major` only when the issue can cause repeated wrong behavior, missed activation, broken execution, or avoidable user friction.

## Trigger Clarity

- Frontmatter description starts with `Use when`.
- Triggers are specific enough for discovery.
- Description does not summarize the workflow.
- Important synonyms are covered without making the skill always-on.

## Scope Boundaries

- The skill says when to use it and, where useful, when not to use it.
- It does not overlap another skill without routing guidance.
- It does not widen user requests beyond the named repo, files, or workflow.

## Progressive Disclosure

- `SKILL.md` stays lean and points to references only when needed.
- Referenced files are loaded conditionally, not all at once.
- Large examples, templates, scripts, and detailed domain rules live outside `SKILL.md`.

## Operational Accuracy

- Commands are runnable from the stated working directory.
- Paths are correct for the repo layout and discovery surfaces.
- The skill does not assume one agent runtime when it claims to work across Claude Code, Codex, Pi, or ZCode.
- Network, browser, API key, and permission requirements are explicit when they matter.

## Verification Quality

- The skill identifies project-provided checks before inventing new ones.
- It has concrete pass/fail criteria for produced artifacts or edits.
- It distinguishes failed checks caused by the change from pre-existing failures.

## Artifact Judgment

- Recommendations for new skills, hooks, scripts, automations, or docs are supported by repeated evidence.
- The proposed artifact has a clear trigger, owner, and maintenance surface.
- The audit avoids creating artifacts for one-off issues.

## Writing Quality

- Instructions are imperative, concise, and easy to execute.
- The skill avoids long generic advice and token-heavy background.
- Examples are minimal and actually clarify expected behavior.

