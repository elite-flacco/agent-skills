---
name: skill-audit-batch-review
description: Use when reviewing multiple agent skills, auditing many SKILL.md files, creating a skill scorecard, checking stale Claude/Codex/Pi/ZCode runtime references, validating skill discovery links, or splitting skill review work across subagents.
---

# Skill Audit Batch Review

## Overview

Review a collection of agent skills as a system, not as isolated markdown files. Find reusable fixes, stale runtime assumptions, overlap, weak triggers, missing verification, and discovery/link hygiene issues without letting parallel subagent batches inflate the strength of a pattern.

## Workflow

1. Establish scope.
   - Identify the skill roots or specific files under review.
   - Run `git status --short --branch` if inside a repo and note unrelated local changes.
   - If the request is broad, default to `skills/**/*.md` in the current repo and exclude generated backups unless the user names them.

2. Read the core instructions.
   - Read `instructions/review-process.md` for batching, evidence, and synthesis rules.
   - Read `instructions/rubric.md` for the scorecard dimensions.
   - Read `instructions/runtime-hygiene.md` when the audit involves Claude Code, Codex, Pi, ZCode, discovery links, manifests, symlinks, hooks, or runtime config.

3. Run deterministic hygiene checks when reviewing this `agent-skills` repo or a compatible skill repo.
   - Execute `node "$(skill dir of skill-audit-batch-review)/scripts/audit-skill-links-and-runtime-refs.mjs" <repo-root>`.
   - Treat script output as evidence, not as the whole review.
   - If the skill dir cannot be resolved from the active discovery surface, locate it with `readlink -f ~/.codex/skills/skill-audit-batch-review` or the matching Claude/Pi/ZCode skills directory.

4. Review the skills.
   - For small scopes, read every `SKILL.md` yourself.
   - For large scopes, split into explicit batches and use subagents only for independent file review. Give each subagent exact files and the rubric; require file/line evidence and no edits.
   - Read and synthesize all subagent results yourself. Deduplicate related findings.

5. Produce the audit report.
   - Use `templates/audit-report.md`.
   - Recommend a new skill, hook, script, or automation only when multiple pieces of evidence show a reusable pattern.
   - If the evidence is thin, explicitly say no new reusable artifact is warranted.

6. Evaluate before finalizing.
   - Run `eval/checklist.md` against the report.
   - If edits were requested, make the narrowest changes and run the repo's validation commands.

## When to Read What

- **Always read:** `instructions/review-process.md`, `instructions/rubric.md`
- **Read when relevant:** `instructions/runtime-hygiene.md`
- **Read when drafting:** `templates/audit-report.md`
- **Run before reporting when possible:** `scripts/audit-skill-links-and-runtime-refs.mjs`
- **Run before finishing:** `eval/checklist.md`

