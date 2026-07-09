---
name: weekly-digest
description: Use when the user wants to summarize their weekly coding-agent activity, generate a weekly digest, review what they worked on, or use weekly-digest. Covers Claude Code, Codex, Pi, and ZCode sessions.
---

# Weekly Digest

Scan activity logs across coding agents (Claude Code, Codex, Pi, ZCode) to produce a weekly summary of what was accomplished, saved as a markdown file. Skip any agent whose log directory doesn't exist (e.g. an agent isn't installed).

## Usage

```
weekly-digest <mode>          # current week (Monday through today)
weekly-digest <mode> last     # previous completed week (Mon-Sun)
```

- `mode` is required: `work` or `personal` (determines output folder)
- Output is saved to `<cwd>/<mode>/weekly-summaries/YYYY-MM-DD.md` (date of Monday)

## Workflow

### Step 1: Determine the date range

- Parse the `mode` argument (first arg) — must be `work` or `personal`
- Check for `last` (second arg) to decide current vs previous week
- **Current week:** Monday of this week through today (inclusive)
- **Previous week:** Monday through Sunday of last week
- Use the Monday's date for the filename (e.g. `2026-03-30.md`)

### Step 2: Gather Claude Code sessions

**IMPORTANT:** The `sessions-index.json` files can be stale and miss recent sessions. Use a two-pass approach:

**Pass 1 — Session index (fast, may be outdated):**
Scan ALL `sessions-index.json` files under `~/.claude/projects/*/`. Filter entries where `created` or `modified` falls within the target date range. Extract `summary`, `firstPrompt`, `projectPath`, `created`, `modified`, `messageCount`.

**Pass 2 — JSONL files (authoritative, always current):**
Scan ALL `*.jsonl` files under `~/.claude/projects/*/` (exclude subdirectories like `subagents/`). Use the file's **mtime** to check if it falls within the date range. For matching files, read the first few lines to extract:
- The first `type: "user"` entry's `message.content` as the session prompt
- The `timestamp` field as the created date
- Count `type: "user"` entries for message count

**Merge** results from both passes, deduplicating by session ID (filename stem = session ID).

**Deriving project names** from the directory name:
- Format is `C--Users-shuan-Documents-Projects-<name>` — extract everything after `Projects-`
- For `C--Users-shuan--claude`, use `.claude`

**Cleaning up prompts** from slash command sessions:
- Extract command name from `<command-name>/foo</command-name>` tags
- For `<local-command-caveat>` wrapped content, look for user prompts in subsequent `type: "user"` entries
- Collect the first 3-5 meaningful user prompts per session to understand what was done

### Step 3: Gather Codex sessions

**Session index:** Parse `~/.codex/session_index.jsonl` (one JSON object per line). Filter entries where `updated_at` falls within the target date range. Extract:
- `thread_name` — the session title
- `updated_at` — timestamp

**History file:** Parse `~/.codex/history.jsonl` (one JSON object per line). Filter entries where `ts` (unix timestamp in seconds) falls within the target date range. Extract:
- `text` — the user's prompt
- `session_id` — to correlate with session index

### Step 4: Gather Pi sessions

Skip if `~/.pi/agent/sessions/` doesn't exist.

Pi stores one `.jsonl` per session under `~/.pi/agent/sessions/<encoded-cwd>/`. The directory name encodes the working directory by replacing path separators and root with `--` (e.g. `--Users-name-Documents-Projects-foo--` decodes to `/Users/name/Documents/Projects/foo`).

**Per session file:**
- **First line** is `{"type":"session",...}` — read `cwd` and `timestamp` (created date).
- **File mtime** = last activity; a session started Friday but active Monday belongs in both weeks.
- **User prompts** — scan for `{"type":"message","message":{"role":"user","content":[{"type":"text","text":"..."}]}}` entries; collect the first 3–5 meaningful ones.

Filter by first-line `timestamp` (created) OR mtime (modified) falling within the target range. Derive the project name from the `cwd`.

### Step 5: Gather ZCode sessions

Skip if `~/.zcode/cli/agents/` doesn't exist.

ZCode stores sessions under `~/.zcode/cli/agents/sess_<id>/agent_<id>/`. Each `agent_<id>` dir has a `metadata.json` and `transcript.jsonl`.

**Per session (read `metadata.json`):**
- `cwd` / `workspaceRoot` — working directory (derive project name)
- `createdAt`, `updatedAt` — timestamps (ISO 8601)
- `prompt` / `description` — the task prompt / short description
- `status` — `completed`, etc.
- `profileId` — agent profile (e.g. `Explore`, main); useful to distinguish subagent runs from main sessions

Filter by `createdAt` OR `updatedAt` within the target range. The `prompt`/`description` is the session summary — no need to parse the transcript for a digest (transcript is verbose).

**Note:** Most ZCode sessions here are subagent runs (Explore, etc.). Group by `workspaceRoot` for project attribution. Flag `profileId` if useful, but the main value is the `description` + `cwd`.

### Step 6: Generate the summary

Create a markdown file with this structure:

```markdown
# Weekly Digest: YYYY-MM-DD

**Period:** Monday, Month DD — Sunday, Month DD, YYYY
**Generated:** YYYY-MM-DD

## Summary

[2-4 sentence narrative synthesizing the week's themes — what major areas were
worked on, key accomplishments, patterns noticed. Be specific about project names.]

## Activity by Project

### project-name (N sessions)

- Session summary or first prompt description
- Another session...

### another-project (N sessions)

- ...

## Codex Activity

### project-or-thread-name

- Thread name / prompt description
- ...

## Pi Activity

### project-name

- Session prompt description
- ...

## ZCode Activity

### project-name

- Session description / prompt (note profileId if a subagent)
- ...

## Stats

- **Total Claude Code sessions:** N
- **Total Codex sessions:** N
- **Total Pi sessions:** N
- **Total ZCode sessions:** N
- **Most active project:** project-name (N sessions)
- **Days active:** N/7
```

Guidelines for the narrative summary:
- Mention specific project names and what was done
- Note if a project dominated the week
- Mention any cross-project patterns (e.g. "focused on UI work across multiple projects")
- Note activity split across agents if notable (e.g. "most work in Claude Code; used ZCode Explore for codebase research")
- Keep it factual — this is a personal activity log, not a performance review

### Step 7: Save the file

```bash
mkdir -p <cwd>/<mode>/weekly-summaries
```

Write to `<cwd>/<mode>/weekly-summaries/YYYY-MM-DD.md`.

If the file already exists, ask before overwriting.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Filtering only by `created` date | Check both created AND modified/updated — a session started Friday but continued Monday belongs in both weeks |
| Hardcoding project paths | Always discover dynamically from each agent's log dir |
| Missing Codex data | Check both `session_index.jsonl` and `history.jsonl` — some sessions may only appear in one |
| Missing an agent's data | Each agent's dir may not exist (agent not installed) — check existence first and skip silently |
| Wrong week boundaries | Monday 00:00:00 through Sunday 23:59:59 in local time |
| Empty projects in output | Skip projects with 0 sessions in the target range |
| ZCode noise | ZCode `metadata.json` covers mostly subagent runs — group by `workspaceRoot`, flag `profileId` only if useful |
