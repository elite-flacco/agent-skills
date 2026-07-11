<!-- Append this block to the project's AGENTS.md during bootstrap. -->

## Plan authoring rules

When invoking `superpowers:writing-plans` in this repo, the invoker MUST:

1. Include the full contents of `docs/superpowers/plan-dod.md` in the writing-plans prompt so every task inherits the project's Definition of Done.
2. Require that the plan's **final task** is always:

   > **Task N (final): Update documentation**
   > Review changes across all prior tasks in this plan. Update `README.md` for any user-facing changes (setup, scripts, features, env vars). Update `AGENTS.md` for any architectural changes (new modules, data flow, conventions, file layout). If no doc updates are needed, state that explicitly and skip. Standard DoD applies — `npm run verify` must pass.

3. Never weaken the DoD or remove the final docs task to fit a smaller plan. If the work is too small to need a plan, skip `writing-plans` entirely.

These rules apply to every plan generated in this repo, including plans created mid-session or by subagents.
