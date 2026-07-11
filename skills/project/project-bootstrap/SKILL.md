---
name: project-bootstrap
description: Use when starting a brand new project, scaffolding a fresh repo, or before running superpowers:writing-plans / executing-plans / subagent-driven-development on a repo that lacks lint/typecheck/format scripts, CI workflows, or a verify hook. Triggers on "bootstrap this project", "set up new project", or "use project-bootstrap". Works across Claude Code, ZCode, and Codex runtimes.
---

# Project Bootstrap

One-time setup for a new project so that every subsequent superpowers spec → plan → subagent flow is gated by automated checks (lint, typecheck, format, tests) at three layers: the `verify` script, a `Stop` hook that re-runs it, and CI. Runtime-agnostic — detects which coding agent(s) are installed and wires the hook for each.

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

Invoke `add-github-actions`. It copies workflow defaults into `.github/` and confirms the shared `update-changelog` and `update-readme` skills are available.

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

The verify-gate runs `npm run verify` when a coding agent finishes a turn that changed code. It's the same command in every runtime — only the config wrapper, the available hook events, and the timeout unit differ. See `references/runtime-configs.md` for the per-runtime details.

1. **Detect installed runtimes.** Check for `~/.claude`, `~/.zcode`, `~/.codex` (home directories). Wire a config for each one present so the gated repo works no matter which agent opens it. If none are detected, ask the user which runtime they use.
2. **Copy the matching template(s)** from this skill to the target path:

   | Runtime | Template | Target path |
   |---|---|---|
   | Claude Code | `templates/hooks.claude.json` | `.claude/settings.json` |
   | ZCode | `templates/hooks.zcode.json` | `.zcode/config.json` |
   | Codex | `templates/hooks.codex.json` | `.codex/hooks.json` |

3. **Merge, don't overwrite.** If the target config already exists, merge the hook arrays in rather than replacing the file.
4. **Codex trust:** Codex skips hooks until reviewed — tell the user to run `/hooks` and trust the new hook before it will fire.

The shared gate command in all three templates is:

```bash
git diff --quiet HEAD || npm run verify || exit 2
```

`git diff --quiet HEAD` exits 0 when the working tree matches HEAD, so verify is skipped for read-only turns. On failure, `exit 2` tells every runtime to surface the failure to the agent (block-and-continue) rather than silently erroring.

### Step 6 — Drop the plan DoD template into the repo

Copy `templates/plan-dod.md` (from this skill) to `docs/superpowers/plan-dod.md` (or wherever the project keeps superpowers docs). When invoking `superpowers:writing-plans` later, paste this block into the plan prompt so every task inherits the same Definition of Done.

### Step 7 — Append plan-authoring rule to `AGENTS.md`

This makes the DoD self-enforcing — without it, the user has to remember to paste `plan-dod.md` into every `writing-plans` prompt.

1. If `AGENTS.md` doesn't exist at the repo root, create it.
2. Append the contents of `templates/agents-md-block.md` (from this skill) to `AGENTS.md`.
3. If a "Plan authoring rules" section already exists, merge — don't duplicate.

Result: future agent sessions read this rule before invoking `superpowers:writing-plans` and automatically inject the DoD + final docs task into the plan prompt.

### Step 8 — Verify the gate works end-to-end

```bash
npm run verify
```

Must exit 0. If it doesn't, fix root cause — never weaken the script to make it pass.

### Step 9 — Commit

```bash
git add package.json package-lock.json .github .claude .zcode .codex docs/superpowers/plan-dod.md AGENTS.md
git commit -m "chore: bootstrap scripts, CI, verify hook, plan DoD, plan-authoring rule"
```

(Add only the runtime config dirs you actually created — drop `.claude`/`.zcode`/`.codex` as needed.)

### Step 10 — Hand off

Tell the user bootstrap is complete and they can now invoke `superpowers:brainstorming` or write a spec. The plan-authoring rule in `AGENTS.md` will inject the DoD and final docs task into every `writing-plans` invocation. If they use Codex, remind them to run `/hooks` to trust the new verify hook.

## Optional: pre-commit gate (third layer)

If the user wants commits blocked locally too, `husky` + `lint-staged` (or the lighter `simple-git-hooks`) are the common choices:

```bash
npm i -D husky lint-staged
npx husky init
echo "npm run verify" > .husky/pre-commit
```

Skip on large test suites where this slows commits unacceptably — CI already covers it.

## Files this skill creates or modifies

| Path | Action |
|------|--------|
| `package.json` | add `lint` / `typecheck` / `format` / `format:check` / `verify` scripts |
| `.github/workflows/*.yml` | copied by `add-github-actions` |
| `.github/dependabot.yml` | copied by `add-github-actions` |
| `.claude/settings.json` | add `Stop` + `SubagentStop` verify hook (Claude Code runtime) |
| `.zcode/config.json` | add `Stop` verify hook (ZCode runtime) |
| `.codex/hooks.json` | add `Stop` + `SubagentStop` verify hook (Codex runtime) |
| `docs/superpowers/plan-dod.md` | new — per-task DoD + final docs task |
| `AGENTS.md` | append "Plan authoring rules" section so the DoD self-injects into `writing-plans` |

Only the runtime configs you actually need are created — one per detected runtime.

## Notes

- **Per-subagent vs per-turn.** Claude Code and Codex support a `SubagentStop` event (verify re-runs after each subagent finishes). ZCode does not — its gate fires on `Stop` (turn end) only. In all three, CI remains the per-commit backstop.
- **If `npm run verify` is too slow** for tight loops, scope the hook command (e.g. `npm run typecheck && npm run lint`) and let CI catch the rest. Don't disable the hook entirely.
- **Cross-runtime differences** — timeout units (ms vs seconds), config shape, and enablement flags — are documented in `references/runtime-configs.md`. The hook *command* is identical everywhere.
- This skill does **not** auto-fire. The user invokes it manually on new repos.
