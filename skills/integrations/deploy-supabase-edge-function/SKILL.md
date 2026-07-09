---
name: deploy-supabase-edge-function
description: Use when the user asks to deploy edge function to supabase.
---

# Deploy Supabase Edge Function

Deploy an edge function to a Supabase project.

## Instructions

1. **Identify the function** — determine the function name from `supabase/functions/` or ask the user which function to deploy.
2. **Install the Supabase CLI** if not already available:
   ```bash
   npm i supabase --save-dev
   ```
3. **Authenticate** — run `supabase login`. Ask the user for their Supabase access token (don't assume one exists).
4. **Link the project**:
   ```bash
   supabase link --project-ref <project-ref>
   ```
   Ask the user for the project ref if it's not in `supabase/config.toml`.
5. **Deploy the function**:
   ```bash
   npx supabase functions deploy <function-name>
   ```
6. **Verify** — report the deployed function URL and confirm it responds (e.g. a quick `curl` with the required auth header if the endpoint is public or the user provides a key).

## Notes
- If secrets are needed (e.g. `SUPABASE_URL`, API keys), set them with `supabase secrets set KEY=value` before deploying.
- Edge functions run on Deno — confirm dependencies are Deno-compatible.
