---
name: {{skill-name}}
description: Use when {{triggering conditions — be specific, never summarize workflow}}
---

# {{Skill Name}}

## Overview

{{1-2 sentences: what this skill does and the core principle.}}

## Workflow

{{Numbered steps showing the process. Each step references which files to read/execute.}}

1. Read `instructions/{{file}}.md` for {{purpose}}
2. Read `instructions/{{file}}.md` for {{purpose}}
3. {{Check examples, use templates, run scripts — as relevant}}
4. Draft output {{using templates/ if applicable}}
5. Run `eval/checklist.md` against draft
6. {{If reviewers exist:}} Run `eval/reviewers.md` for multi-perspective review

## When to Read What

- **Always read:** `instructions/` — core rules that apply to every use
- **Read when drafting:** `examples/`, `templates/` — reference material for output
- **Read on demand:** `references/` — for specific lookups when needed
- **Execute, don't read:** `scripts/` — run directly for deterministic tasks
