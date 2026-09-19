---
name: frontend-rules
description: Use when writing or modifying any UI file, component, CSS, or Tailwind class in a Next.js / React / Tailwind project, when scaffolding a new frontend project, or when reviewing existing UI code for design-system compliance.
---

# Frontend Rules

This skill is **rigid** — follow every rule exactly. The rules live in `references/rules.md`. Read that file in full before writing or reviewing any UI code.

## Routing

- **New project:** invoke the `setup-tailwind-design-system` skill as a standalone step BEFORE writing any UI code or dispatching any UI subagent — `globals.css` with semantic tokens must exist before the UI prompt is written.
- **Existing project:** read `globals.css` before touching anything. Check what tokens and `@layer components` classes already exist. Never add new raw values — add a token first.
- **Project without these tokens/classes** (Tailwind v3, shadcn, or another design system): do not restructure a foreign system beyond the user's ask — apply only the portable rules (no inline styles, no arbitrary values, component reuse before duplication, TypeScript) and flag the gap to the user.

## Subagent Handoff

Subagents may not have skill access — they start fresh. When dispatching a subagent for UI work, paste the content of `references/rules.md` (sections 2–12, rephrased as imperatives the subagent can follow standalone) into its prompt:

- **Scaffolding subagent (new project):** invoke `setup-tailwind-design-system` yourself first, read the CSS template from it, and include it in the subagent prompt along with the rules.
- **Component/page subagent (existing project):** instruct it to read `globals.css` first (that file IS the design system), then paste the rules.

## Verification

After UI changes, visually verify per section 13 of `references/rules.md` — browser check at desktop and mobile widths, interactions and states, console errors — then run the Quick Self-Check checklist at the end of that file before committing.
