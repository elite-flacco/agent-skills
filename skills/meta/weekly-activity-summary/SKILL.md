---
name: weekly-activity-summary
description: Use when the user wants to summarize their weekly coding-agent activity or review what they worked on — e.g. "generate a weekly summary", "what did I work on this week", "summarize my week", "weekly review". Covers Claude Code, Codex, Pi, and ZCode sessions.
---

# Weekly Activity Summary

Scan activity logs across coding agents (Claude Code, Codex, Pi, ZCode) to produce a weekly summary of what was accomplished, saved as a markdown file. Skip any agent whose log directory doesn't exist (e.g. an agent isn't installed).

## Usage

```
weekly-activity-summary          # current week (Monday through today)
weekly-activity-summary last     # previous completed week (Mon-Sun)
```

- Output is saved to `<cwd>/weekly-summaries/YYYY-MM-DD.md` (date of Monday)

## Workflow

### Step 1: Determine the date range

- Check for `last` (only argument) to decide current vs previous week
- **Current week:** Monday of this week through today (inclusive)
- **Previous week:** Monday through Sunday of last week
- Use the Monday's date for the filename (e.g. `2026-03-30.md`)

### Step 2: Gather sessions from each agent

A session belongs to the week if its **created OR modified** timestamp falls within Monday 00:00:00 → Sunday 23:59:59 local time. For the per-agent log locations, field names, and parsing rules, read [references/agent-logs.md](references/agent-logs.md):

- **Claude Code** — two-pass (session index + JSONL); JSONL is authoritative for recent sessions
- **Codex** — `session_index.jsonl` + `history.jsonl`
- **Pi** — one `.jsonl` per session under `~/.pi/agent/sessions/`
- **ZCode** — `metadata.json` per `agent_<id>` dir; group by `workspaceRoot`

Skip any agent whose log directory doesn't exist.

### Step 3: Generate the summary

Fill the output skeleton in [templates/weekly-activity-summary.md](templates/weekly-activity-summary.md) — one section per agent, grouped by project. Apply the narrative-summary guidelines at the end of that template.

### Step 4: Save the file

```bash
mkdir -p <cwd>/weekly-summaries
```

Write to `<cwd>/weekly-summaries/YYYY-MM-DD.md`. If the file already exists, ask before overwriting.

## Verification

Before saving, run [eval/checklist.md](eval/checklist.md) against the draft — confirm week boundaries, dual-source coverage (Claude Code + Codex), dynamic path discovery, and that the counts match.

## When to Read What

- **Read first:** [references/agent-logs.md](references/agent-logs.md) — where each agent stores sessions and how to parse them
- **Read when drafting:** [templates/weekly-activity-summary.md](templates/weekly-activity-summary.md) — output skeleton + narrative guidelines
- **Run before saving:** [eval/checklist.md](eval/checklist.md) — pass/fail checks on the draft
