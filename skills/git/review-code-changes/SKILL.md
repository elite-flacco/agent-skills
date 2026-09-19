---
name: review-code-changes
description: Use when the user asks for holistic code review, branch review, staged change review, PR-style review, architecture review, test coverage review, UI browser verification, product logic review, or third-party SDK/package usage review.
---

# Review Code Changes

## Overview

Review a branch or staged changes like a senior engineer seeing the diff for the first time: start from the code and runtime behavior, not from prior memory, docs, comments, or the author's stated intent; use those only later as comparison points. Surface the highest-value risks, explain them plainly, and identify the evidence needed to trust or change the work.

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

3. Review the change through the required lenses in [references/review-lenses.md](references/review-lenses.md) — functional behavior, architecture/design, implementation quality, third-party usage, tests, and operations. Not every lens applies to every diff, but skip a lens deliberately, not by accident.

4. Run targeted verification.
   - Prefer project scripts from `package.json`, `pyproject.toml`, `Makefile`, `justfile`, CI config, or existing docs over invented commands.
   - Run relevant lint, typecheck, unit, integration, formatting, build, or migration checks when practical.
   - Exercise the code directly, not only through the test suite. Tests confirm the code does what the author expected; they don't reveal what they didn't think of. Run the real query against the live database, call the function with inputs from real source files, replay an actual request. Escaping or quoting that behaves differently than assumed, off-by-ones in date or pagination math, fields that are null in real input, logic that only triggers under specific data shapes — these are often obvious the moment you run them, and invisible when you only read.
   - Locate real input data before inventing test cases — the populated database, local data directories, captured API responses, log files. Fixtures encode the author's assumptions; real data breaks them.
   - If official third-party docs are unavailable or unclear, say so and distinguish inference from verified behavior.

5. Verify UI changes through the app.
   - If the diff touches UI, routing, styling, client state, forms, charts, auth screens, user-visible copy, or accessibility, run or locate the dev server.
   - Use the in-app browser wherever possible.
   - Use agent-browser for repeatable browser automation, screenshots, console inspection, responsive checks, and interaction flows.
   - Exercise the changed flow like a user: load the relevant page, interact with controls, test at least one mobile-ish and one desktop viewport, and inspect console errors.
   - Check that text does not overlap, controls are reachable, loading and error states are coherent, and the visible result matches the intended behavior.

For large multi-subsystem diffs, dispatch parallel review agents — see `references/parallel-review.md`.

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

Check `references/common-mistakes.md` before finalizing.

## Notes

- To enumerate PRs first, use the `list-github-prs` skill.
