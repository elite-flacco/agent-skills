---
allowed-tools: Bash(supabase:*), Bash(npx supabase:*)
description: Deploy edge function to Supabase
---

# Deploy Edge Function $ARGUMENTS to Supabase

## Instructions

1) Check if Supabase CLI is already installed, if not install it by running `npm i supabase --save-dev`.
2) Log in to Supabase by running `supabase login`. Ask the user for their Supabase access token.
3) Link your Supabase project by running `supabase link --project-ref <string>`. Ask the user for the project ref.
4) Deploy the edge function to Supabase by running `npx supabase functions deploy <function-name>`.
