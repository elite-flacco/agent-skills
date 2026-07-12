# Definition of Done

Paste this block into every `superpowers:writing-plans` prompt so each task inherits the same completion bar.

---

## Definition of Done (applies to every task in this plan)

A task is complete only when ALL of the following are true:

1. **Acceptance criteria met** — code implements what the task specifies, nothing more.
2. **`npm run verify` exits 0** — lint, typecheck, format check, and tests all pass. Do not weaken the script to make it pass; fix root cause.
3. **Behavior is covered by a test** — follow `superpowers:test-driven-development`. New behavior without a test is incomplete.
4. **No scope creep** — no files created or modified outside what the task specifies. No drive-by refactors. No "while I'm here" cleanups.
5. **No suppressions** — no `eslint-disable`, `@ts-ignore`, `.skip`, or `--no-verify` added to make checks pass. If a check is wrong, fix the check in a separate task.
6. **Docs updated inline** — if this task changes user-facing behavior (setup, scripts, env vars, features) update `README.md` in the same task. If it changes architecture, file layout, data flow, or conventions, update `AGENTS.md` and `CLAUDE.md` in the same task. State "no doc impact" explicitly in the task report when none apply. Doc edits count toward DoD and must pass `npm run verify`.

If `npm run verify` fails after edits:
- Read the failure output.
- Fix the underlying cause in the code under test.
- Re-run `npm run verify` until clean.
- Only then report the task complete.

The verify-gate hook in your agent's config (`.claude/settings.json`, `.zcode/config.json`, or `.codex/hooks.json`) re-runs `npm run verify` automatically when a turn/subagent finishes. An agent that reports done with failing checks will be blocked.

---

## Plan structure requirement

The final task in every plan generated using this block MUST be:

### Task N (final): Update documentation

- Review changes across all prior tasks in this plan.
- Update `README.md` for any user-facing changes (setup, scripts, features, env vars, deployment).
- Update `AGENTS.md` and `CLAUDE.md` for any architectural changes (new modules, data flow, conventions, file layout, build steps).
- If no doc updates are needed, state that explicitly in the task report and skip the edits.
- Standard DoD applies: `npm run verify` must pass after any doc edits.

Do not skip this task. Do not merge it into another task. It always runs last so it can see the cumulative diff from all prior work.
