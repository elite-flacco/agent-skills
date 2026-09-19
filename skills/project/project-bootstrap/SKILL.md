---
name: project-bootstrap
description: Use when starting a brand new project, scaffolding a fresh repo, or before running superpowers:writing-plans / executing-plans / subagent-driven-development on a repo that lacks lint/typecheck/format scripts, CI workflows, or a verify hook. 
---

# Project Bootstrap

One-time setup so that every subsequent superpowers spec → plan → subagent flow is gated by automated checks (lint, typecheck, format, tests) at three layers: the `verify` script, a `Stop` hook that re-runs it, and CI.

## When to invoke

Run **once per repo**, after initial framework scaffold (e.g. `create-next-app`), **before** invoking `superpowers:brainstorming` or writing the first spec.

Skip if the repo already has all of:
- `npm run verify` script in `package.json`
- `.github/workflows/ci.yml`
- A `Stop` hook running `npm run verify` in an agent config (`.claude/settings.json`, `.zcode/config.json`, or `.codex/hooks.json`)

## Prerequisites

This skill delegates to four sibling skills — confirm they're available before starting: `add-scripts`, `add-github-actions`, `update-changelog`, `update-readme`.

## Workflow

### Step 1 — Commit baseline

Confirm the scaffold is committed before adding tooling. If the working tree is dirty, ask the user to commit or stash first.

```bash
git status
```

### Step 2 — Add scripts

Invoke `add-scripts`. It adds `lint`, `typecheck`, `format`, `format:check` to `package.json`, installs deps, and verifies each runs clean. Fix any surfaced issues before continuing.

### Step 3 — Add CI workflows

Invoke `add-github-actions`. It copies workflow defaults into `.github/`.

After it finishes, open `.github/workflows/ci.yml` and confirm the job runs:

```
npm run lint && npm run typecheck && npm run format:check && npm run test:run
```

If `ci.yml` doesn't have all four, edit it so it does.

### Step 4 — Add the `verify` aggregate script

Edit `package.json`:

```json
{
  "scripts": {
    "verify": "npm run lint && npm run typecheck && npm run format:check && npm run test:run"
  }
}
```

If the project has no test suite yet, drop `&& npm run test:run` until tests exist. Add it back the moment the first test lands.

### Step 5 — Wire the verify-gate hook

The verify-gate re-runs `npm run verify` when an agent finishes a turn that changed code.

1. **Detect installed runtimes.** Check for `~/.claude`, `~/.zcode`, `~/.codex`, `~/.pi` (home directories). Wire a config for each one present so the gated repo works no matter which agent opens it. Pi has no hook support; CI is the verification backstop there. If none are detected, ask the user which runtime they use.
2. **Copy the matching template(s)** from `templates/` to the target config: `hooks.claude.json` → `.claude/settings.json`, `hooks.zcode.json` → `.zcode/config.json`, `hooks.codex.json` → `.codex/hooks.json`.
3. **Merge, don't overwrite.** If the target config already exists, merge the hook arrays in rather than replacing the file.
4. **Codex trust:** Codex skips hooks until reviewed — tell the user to run `/hooks` and trust the new hook before it will fire.

Per-runtime wiring details and differences: `references/runtime-configs.md`.

### Step 6 — Drop the plan DoD template into the repo

Copy `templates/plan-dod.md` (from this skill) to `docs/superpowers/plan-dod.md` (or wherever the project keeps superpowers docs). When invoking `superpowers:writing-plans` later, paste this block into the plan prompt.

### Step 7 — Append plan-authoring rule to `AGENTS.md` and `CLAUDE.md`

This makes the DoD self-enforcing — without it, the user has to remember to paste `plan-dod.md` into every `writing-plans` prompt.

1. For each of `AGENTS.md` and `CLAUDE.md` at the repo root: if it doesn't exist, create it.
2. Append the contents of `templates/agents-md-block.md` (from this skill) to both files.
3. If a "Plan authoring rules" section already exists in either file, merge — don't duplicate.

### Step 8 — Verify the gate works end-to-end

```bash
npm run verify
```

Must exit 0. If it doesn't, fix root cause — never weaken the script to make it pass.

### Step 9 — Commit

```bash
git add package.json package-lock.json .github .claude .zcode .codex docs/superpowers/plan-dod.md AGENTS.md CLAUDE.md
git commit -m "chore: bootstrap scripts, CI, verify hook, plan DoD, plan-authoring rule"
```

(Drop `.claude`/`.zcode`/`.codex` for runtimes you didn't wire.)

### Step 10 — Hand off

Tell the user bootstrap is complete and they can now invoke `superpowers:brainstorming` or write a spec. If they use Codex, remind them to run `/hooks` to trust the new verify hook.

## Optional: pre-commit gate

If the user wants commits blocked locally too, `husky` + `lint-staged` (or the lighter `simple-git-hooks`) are the common choices:

```bash
npm i -D husky lint-staged
npx husky init
echo "npm run verify" > .husky/pre-commit
```

Skip on large test suites where this slows commits unacceptably — CI already covers it.

## Files this skill creates or modifies

- `package.json` — lint/typecheck/format/verify scripts
- `.github/workflows/*.yml` and `.github/dependabot.yml` — via `add-github-actions`
- `.claude/settings.json`, `.zcode/config.json`, `.codex/hooks.json` — verify-gate hook, one per detected runtime
- `docs/superpowers/plan-dod.md` — per-task DoD + final docs task
- `AGENTS.md` and `CLAUDE.md` — appended "Plan authoring rules" section

Only the runtime configs you actually need are created — one per detected runtime.

## Notes

- **If `npm run verify` is too slow** for tight loops, scope the hook command (e.g. `npm run typecheck && npm run lint`) and let CI catch the rest. Don't disable the hook entirely.
- This skill does **not** auto-fire; the user invokes it manually.
