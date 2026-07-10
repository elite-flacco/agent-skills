---
name: deploy-supabase-edge-function
description: Use when the user asks to deploy a Supabase edge function (Deno) to a remote project — e.g. "deploy this edge function", "push the supabase function", "deploy to supabase". Not for local `supabase functions serve`.
---

# Deploy Supabase Edge Function

Deploy a Supabase edge function (Deno) from `supabase/functions/` to a remote Supabase project.

## When to Use

- User wants to deploy one or more edge functions to their Supabase project.
- User asks to "push" or "publish" a function.

Not for local development / testing — that's `supabase functions serve`.

## Prerequisites

- Supabase CLI available. Prefer the standalone installer or `brew install supabase/tap/supabase` so the CLI runs as `supabase` directly. `npm i -g supabase` works too; `--save-dev` + `npx` is only useful if you want it pinned to a project. Confirm with the user which they want before installing.
- Supabase access token (the user's; don't assume one exists). `supabase login` to set it.
- The project ref — usually in `supabase/config.toml` after `supabase link`. Ask the user if it's missing.

## Instructions

1. **Identify the function** — determine the name from `supabase/functions/` or ask the user which to deploy.
2. **Authenticate** — `supabase login`. Ask the user for their access token; don't assume one is set.
3. **Link the project** (if not already linked):
   ```bash
   supabase link --project-ref <project-ref>
   ```
   Ask the user for the project ref if it's not in `supabase/config.toml`.
4. **Set secrets** the function needs (if any) **before** deploying — a function that references an unset secret will deploy but 500 at runtime:
   ```bash
   supabase secrets set SUPABASE_URL=... API_KEY=...
   ```
5. **Deploy**:
   ```bash
   supabase functions deploy <function-name>
   ```
6. **Verify** — confirm the function is listed and responds:
   ```bash
   supabase functions list
   curl -i <function-url>   # with the required Authorization header if the endpoint isn't public
   ```
   Ask the user for an auth key if the endpoint requires one.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Function deploys but returns 500 | A referenced secret is unset. Check `supabase secrets list` and set anything missing before redeploying. |
| `supabase: command not found` after `npm i supabase --save-dev` | `--save-dev` doesn't put it on PATH. Use `npx supabase ...`, or install globally / via brew. |
| `Project not found` / wrong project | Confirm the project ref in `supabase/config.toml` matches the target; re-run `supabase link`. |
| Stale CLI errors on new runtime features | Edge functions run on Deno — `supabase --version` and update if deploy fails on syntax the runtime should support. |
| CORS errors when calling from the browser | Deploy with `--no-verify-jwt` only if the function is meant to be public, or call it with the anon key / the user's session token. Confirm intent with the user before disabling JWT verification. |
| Deploying the wrong function | Names come from the folder under `supabase/functions/`. Confirm the exact folder name before deploying. |

## Notes

- Edge functions run on Deno — confirm dependencies are Deno-compatible (no Node-only built-ins like `fs`/`path`).
- Secrets are per-project, not per-function; setting one makes it available to all functions in that project.
