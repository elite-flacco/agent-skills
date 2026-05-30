---
name: project-bootstrap
description: Use when starting a brand new project, scaffolding a fresh repo, or before running superpowers:writing-plans / executing-plans / subagent-driven-development on a repo that lacks lint/typecheck/format scripts, CI workflows, or a SubagentStop verify hook. Triggers on requests like "bootstrap this project", "set up new project", or "use project-bootstrap".
---

# Project Bootstrap

One-time setup for a new project so that every subsequent superpowers spec → plan → subagent flow is gated by automated checks (lint, typecheck, format, tests) at three layers: plan DoD, SubagentStop hook, CI.

## When to invoke

Run **once per repo**, after initial framework scaffold (e.g. `create-next-app`), **before** invoking `superpowers:brainstorming` or writing the first spec.

Skip if the repo already has all of:
- `npm run verify` script in `package.json`
- `.github/workflows/ci.yml`
- `.claude/settings.json` with a `SubagentStop` hook running `npm run verify`

## Workflow

### Step 1 — Commit baseline

Confirm scaffold is committed before adding tooling. If working tree is dirty, ask the user to commit or stash first.

```bash
git status
```

### Step 2 — Add scripts

Use the `add-scripts` skill. It adds `lint`, `typecheck`, `format`, `format:check` to `package.json`, installs deps, and verifies each runs clean. Fix any surfaced issues before continuing.

### Step 3 — Add CI workflows

Use the `add-gh-workflows` skill. It copies `~/.claude/github/` defaults into `.github/` and confirms the shared `update-changelog` and `update-readme` skills are available.

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

### Step 5 — Write the SubagentStop hook + docs reminder script

1. Copy `templates/settings.json` (from this skill) to `.claude/settings.json`. This wires two hooks for both `SubagentStop` and `Stop`:
   - **verify gate** — `git diff --quiet HEAD || npm run verify --silent` (skips on no-op subagents).
   - **docs reminder** — runs `node .claude/hooks/docs-reminder.cjs`, an advisory check that warns when code changed but `README.md` / `CLAUDE.md` / `AGENTS.md` did not.
2. Copy `templates/hooks/docs-reminder.cjs` to `.claude/hooks/docs-reminder.cjs` in the project.
3. If `.claude/settings.json` already exists, merge the hook arrays in rather than overwriting.

The docs reminder is non-blocking (exit 0). If the user wants it to block the subagent, flip the marked line in `docs-reminder.cjs` to `process.exit(2);`.

### Step 6 — Drop the plan DoD template into the repo

Copy `templates/plan-dod.md` (from this skill) to `docs/superpowers/plan-dod.md` (or wherever the project keeps superpowers docs). When invoking `superpowers:writing-plans` later, paste this block into the plan prompt so every task inherits the same Definition of Done.

### Step 6.5 — Append plan-authoring rule to project CLAUDE.md

This is the step that makes the DoD self-enforcing — without it, the user has to remember to paste `plan-dod.md` into every `writing-plans` prompt.

1. If `CLAUDE.md` doesn't exist at the repo root, create it.
2. Append the contents of `templates/claude-md-block.md` (from this skill) to `CLAUDE.md`.
3. If a "Plan authoring rules" section already exists, merge — don't duplicate.

Result: future Claude sessions read this rule before invoking `superpowers:writing-plans` and automatically inject the DoD + final docs task into the plan prompt. The user no longer has to remember.

### Step 7 — Verify the gate works end-to-end

```bash
npm run verify
```

Must exit 0. If it doesn't, fix root cause — never weaken the script to make it pass.

### Step 8 — Commit

```bash
git add package.json package-lock.json .github .claude docs/superpowers/plan-dod.md CLAUDE.md
git commit -m "chore: bootstrap scripts, CI, verify + docs-reminder hooks, plan DoD, plan-authoring rule"
```

### Step 9 — Hand off

Tell the user bootstrap is complete and they can now invoke `superpowers:brainstorming` or write a spec. The plan-authoring rule in `CLAUDE.md` will automatically inject the DoD and final docs task into every `writing-plans` invocation — no manual pasting required.

## Optional: pre-commit gate (third layer)

If the user wants commits blocked locally too:

```bash
npm i -D simple-git-hooks
```

Add to `package.json`:

```json
{
  "simple-git-hooks": { "pre-commit": "npm run verify" },
  "scripts": { "postinstall": "simple-git-hooks" }
}
```

Run `npx simple-git-hooks` once to install the hook. Skip on large test suites where this slows commits unacceptably — CI already covers it.

## Files this skill creates or modifies

| Path | Action |
|------|--------|
| `package.json` | add `lint` / `typecheck` / `format` / `format:check` / `verify` scripts |
| `.github/workflows/*.yml` | copied from `~/.claude/github/workflows/` |
| `.github/dependabot.yml` | copied from defaults |
| `update-changelog` skill | available |
| `update-readme` skill | available |
| `.claude/settings.json` | add `SubagentStop` + `Stop` hooks (verify gate + docs reminder) |
| `.claude/hooks/docs-reminder.cjs` | new — advisory script that warns when code changed but docs didn't |
| `docs/superpowers/plan-dod.md` | new — per-task DoD (incl. inline doc updates) + final docs task |
| `CLAUDE.md` | append "Plan authoring rules" section so the DoD self-injects into `writing-plans` |

## Notes

- The hook fires on **every** subagent finish in the project, not just superpowers-dispatched ones. That's intentional.
- If `npm run verify` is too slow for tight subagent loops, scope the hook command (e.g. `npm run typecheck && npm run lint`) and let CI catch the rest. Don't disable the hook entirely.
- The hook command is `git diff --quiet HEAD || npm run verify --silent` — `git diff --quiet HEAD` exits 0 when the working tree matches HEAD, so verify is skipped for read-only subagents (Explore, Plan, code-reviewer) and for write-capable subagents that happened not to modify anything. `||` is supported by bash, cmd, and PowerShell 7+. On PowerShell 5.1, replace with `git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { npm run verify --silent }`.
- This skill does **not** auto-fire. The user invokes it manually on new repos.
