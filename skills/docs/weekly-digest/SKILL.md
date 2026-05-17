---
name: weekly-digest
description: Use when the user wants to summarize their weekly Claude Code and Codex activity, generate a weekly digest, review what they worked on, or run /weekly-digest.
---

# Weekly Digest

Scan Claude Code and Codex activity logs to produce a weekly summary of what was accomplished, saved as a markdown file.

## Usage

```
/weekly-digest <mode>          # current week (Monday through today)
/weekly-digest <mode> last     # previous completed week (Mon-Sun)
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

### Step 4: Generate the summary

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

## Stats

- **Total Claude Code sessions:** N
- **Total Codex sessions:** N
- **Most active project:** project-name (N sessions)
- **Days active:** N/7
```

Guidelines for the narrative summary:
- Mention specific project names and what was done
- Note if a project dominated the week
- Mention any cross-project patterns (e.g. "focused on UI work across multiple projects")
- Keep it factual — this is a personal activity log, not a performance review

### Step 5: Save the file

```bash
mkdir -p <cwd>/<mode>/weekly-summaries
```

Write to `<cwd>/<mode>/weekly-summaries/YYYY-MM-DD.md`.

If the file already exists, ask before overwriting.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Filtering only by `created` date | Check both `created` AND `modified` — a session started Friday but continued Monday belongs in both weeks |
| Hardcoding project paths | Always discover from `~/.claude/projects/` and `~/.codex/` dynamically |
| Missing Codex data | Check both `session_index.jsonl` and `history.jsonl` — some sessions may only appear in one |
| Wrong week boundaries | Monday 00:00:00 through Sunday 23:59:59 in local time |
| Empty projects in output | Skip projects with 0 sessions in the target range |
