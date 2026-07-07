---
name: review-code-changes
description: Use when the user asks for holistic code review, branch review, staged change review, PR-style review, architecture review, test coverage review, UI browser verification, product logic review, or third-party SDK/package usage review.
---

# Review Code Changes

## Overview

Review existing branch or staged changes like a senior engineer seeing the diff for the first time. Start from the code and runtime behavior, not from prior memory, docs, comments, or the author's stated intent; use those only later as comparison points.

The goal is not to fix the code unless explicitly asked. The goal is to surface the highest-value risks, explain them plainly, and identify the evidence needed to trust or change the work.

## When to Use

- User asks to review code, review a branch, review staged changes, inspect a PR, or give candid feedback on changes.
- User asks whether architecture, design, implementation quality, tests, or UI behavior make sense.
- User is not a software engineer and wants actionable recommendations, not only raw technical findings.
- Do not use for requests to directly implement fixes unless review is the first explicit step.

## Core Pattern

1. Establish review scope.
   - Run `git status --short --branch`.
   - Detect the default branch (`git symbolic-ref refs/remotes/origin/HEAD`, falling back to `main` or `master`); do not assume `origin/main`.
   - If the user said staged, review `git diff --staged`. If they named a branch, review `git diff <default-branch>...HEAD` (three-dot diffs from the merge base).
   - If neither is explicit, prefer the current branch diff against the default branch; mention unstaged or untracked files separately.
   - If there are no changes in scope (clean tree, branch identical to default), say so and ask what to review instead of inventing a scope.
   - Do not modify files, stage files, commit, or switch branches unless the user explicitly asks.

2. Build a fresh mental model from source.
   - Read the changed files first, then their immediate callers, callees, tests, configuration, package scripts, route definitions, and data contracts.
   - Treat comments, README claims, issue text, prior memory, and commit messages as untrusted context until the code path supports them.
   - Ask: what problem does this change appear to solve, what invariants must hold, and what could break if those invariants are wrong?

3. Review the change through the required lenses.
   - Functional behavior: infer the intended workflow from the code path, then verify inputs, outputs, data transformations, validation, state transitions, side effects, failure paths, regressions, backwards compatibility, and whether the change solves the real problem.
   - Architecture/design: check ownership boundaries, abstractions, coupling, data flow, implicit ordering, global side effects, persistence, migrations, feature flags, rollback behavior, and whether a simpler design would work.
   - Implementation quality: inspect naming, readability, type safety, validation, duplication, dead code, stale comments, cleanup, logging, observability, performance, accessibility, security, and brittle string/date handling.
   - Third-party usage: for new, upgraded, unfamiliar, or behavior-critical packages, SDKs, framework APIs, CLIs, config options, or generated types, verify against official version-specific docs, changelogs, migration guides, API references, release notes, typed declarations, or package source.
   - Tests: identify changed behavior and check whether success, failure, boundary, regression, integration, and UI states are covered; recommend only tests that reduce real risk.
   - Operations: check config, environment variables, secrets, rate limits, auth requirements, runtime support, deploy safety, monitoring, and rollback concerns when relevant.

4. Run targeted verification.
   - Prefer project scripts from `package.json`, `pyproject.toml`, `Makefile`, `justfile`, CI config, or existing docs over invented commands.
   - Run relevant lint, typecheck, unit, integration, formatting, build, or migration checks when practical.
   - If official third-party docs are unavailable or unclear, say so and distinguish inference from verified behavior.

5. Verify UI changes through the app.
   - If the diff touches UI, routing, styling, client state, forms, charts, auth screens, user-visible copy, or accessibility, run or locate the dev server.
   - Use the in-app browser wherever possible.
   - Use agent-browser for repeatable browser automation, screenshots, console inspection, responsive checks, and interaction flows.
   - Exercise the changed flow like a user: load the relevant page, interact with controls, test at least one mobile-ish and one desktop viewport, and inspect console errors.
   - Check that text does not overlap, controls are reachable, loading and error states are coherent, and the visible result matches the intended behavior.

## Parallel Review Agents

Default to a single reviewer. Go parallel only for large diffs spanning multiple subsystems (e.g. backend + frontend + config), or when browser verification or third-party docs research can run independently of code analysis. Skip it when findings depend on shared whole-system understanding or the review needs a single product judgment.

When dispatching subagents:
1. Scope the diff yourself first, then split by review lens or subsystem — never "review everything" prompts. Lenses match the review lenses above.
2. Give each subagent exact files, commands, docs targets, and output format; they return findings only and must not edit, stage, commit, or switch branches.
3. Read all results, deduplicate, resolve contradictions, rank severity, and write one final review.

## Output Format

Lead with findings, ordered by severity. Be concise and concrete.

For each finding include:
- Severity: `P0` blocks release, `P1` likely bug or major design risk, `P2` important maintainability or coverage gap, `P3` minor issue.
- File and line reference when possible.
- What can go wrong.
- Why the code makes that possible.
- Recommended fix or decision.

Then include:
- `Open questions` if reviewer confidence depends on product intent or missing context.
- `Verification` with exact commands, browser checks, and results.
- `Summary` in plain English for non-engineers: what is safe, what is risky, and what to do next.

If no issues are found, say that clearly and still report residual risk and checks run.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Trusting docs, comments, memory, or PR text before reading code | Build the model from changed code first, then compare outside context for drift |
| Reviewing only the diff | Read nearby callers, tests, config, schema, routes, and runtime entry points |
| Treating clean code as correct behavior | Trace the functional workflow and verify the change logically solves the real user or product problem |
| Guessing SDK or framework behavior from memory | Verify new, upgraded, unfamiliar, or behavior-critical third-party usage against official version-specific sources |
| Spawning subagents before understanding scope | Scope the diff first, then delegate narrow independent lenses and synthesize one final review |
| Reporting style preferences as bugs | Prioritize behavior, architecture risk, maintainability, tests, and user impact |
| Skipping UI verification because code compiles | Use the in-app browser where possible and agent-browser for repeatable user-flow checks |
| Asking for generic test coverage | Name the specific scenario or regression the missing test should catch |
| Fixing during review | Do not edit unless the user asks to address the findings |
