# Agent Log Parsing

Per-agent details for finding sessions that fall within the target date range. For each agent, check whether its log directory exists first; skip silently if not (the agent isn't installed).

The date-range test is: a session belongs to the week if its **created** OR **modified/updated** timestamp falls within Monday 00:00:00 → Sunday 23:59:59, local time. A session started Friday but active Monday belongs in both weeks.

## Table of Contents

- [Claude Code](#claude-code)
- [Codex](#codex)
- [Pi](#pi)
- [ZCode](#zcode)
- [Deriving project names](#deriving-project-names)

## Claude Code

**IMPORTANT:** The `sessions-index.json` files can be stale and miss recent sessions. Use a two-pass approach.

**Pass 1 — Session index (fast, may be outdated):**
Scan ALL `sessions-index.json` files under `~/.claude/projects/*/`. Filter entries where `created` or `modified` falls within the target date range. Extract `summary`, `firstPrompt`, `projectPath`, `created`, `modified`, `messageCount`.

**Pass 2 — JSONL files (authoritative, always current):**
Scan ALL `*.jsonl` files under `~/.claude/projects/*/` (exclude subdirectories like `subagents/`). Use the file's **mtime** to check if it falls within the date range. For matching files, read the first few lines to extract:

- The first `type: "user"` entry's `message.content` as the session prompt
- The `timestamp` field as the created date
- Count `type: "user"` entries for message count

**Merge** results from both passes, deduplicating by session ID (filename stem = session ID).

**Cleaning up prompts** from slash command sessions:

- Extract command name from `<command-name>/foo</command-name>` tags
- For `<local-command-caveat>` wrapped content, look for user prompts in subsequent `type: "user"` entries
- Collect the first 3-5 meaningful user prompts per session to understand what was done

## Codex

**Session index:** Parse `~/.codex/session_index.jsonl` (one JSON object per line). Filter entries where `updated_at` falls within the target date range. Extract:

- `thread_name` — the session title
- `updated_at` — timestamp

**History file:** Parse `~/.codex/history.jsonl` (one JSON object per line). Filter entries where `ts` (unix timestamp in seconds) falls within the target date range. Extract:

- `text` — the user's prompt
- `session_id` — to correlate with session index

Some sessions appear in only one of the two files — read both.

## Pi

Skip if `~/.pi/agent/sessions/` doesn't exist.

Pi stores one `.jsonl` per session under `~/.pi/agent/sessions/<encoded-cwd>/`. The directory name encodes the working directory by replacing path separators and root with `--` (e.g. `--Users-name-Documents-Projects-foo--` decodes to `/Users/name/Documents/Projects/foo`).

**Per session file:**

- **First line** is `{"type":"session",...}` — read `cwd` and `timestamp` (created date).
- **File mtime** = last activity; a session started Friday but active Monday belongs in both weeks.
- **User prompts** — scan for `{"type":"message","message":{"role":"user","content":[{"type":"text","text":"..."}]}}` entries; collect the first 3-5 meaningful ones.

Filter by first-line `timestamp` (created) OR mtime (modified) falling within the target range. Derive the project name from the `cwd`.

## ZCode

Skip if `~/.zcode/cli/agents/` doesn't exist.

ZCode stores sessions under `~/.zcode/cli/agents/sess_<id>/agent_<id>/`. Each `agent_<id>` dir has a `metadata.json` and `transcript.jsonl`.

**Per session (read `metadata.json`):**

- `cwd` / `workspaceRoot` — working directory (derive project name)
- `createdAt`, `updatedAt` — timestamps (ISO 8601)
- `prompt` / `description` — the task prompt / short description
- `status` — `completed`, etc.
- `profileId` — agent profile (e.g. `Explore`, main); useful to distinguish subagent runs from main sessions

Filter by `createdAt` OR `updatedAt` within the target range. The `prompt`/`description` is the session summary — no need to parse the transcript for the weekly summary (transcript is verbose).

**Note:** Most ZCode sessions here are subagent runs (Explore, etc.). Group by `workspaceRoot` for project attribution. Flag `profileId` if useful, but the main value is the `description` + `cwd`.

## Deriving project names

Agent log directories often encode the session's working directory (path separators replaced by `-`). Don't hardcode a specific username or drive prefix. Derive the project name generically:

1. **Claude Code** project dirs look like `<drive-or-root>-<seg>-...-Projects-<name>` (e.g. `C--Users-name-Documents-Projects-agent-skills`). The project name is the segment after the last `Projects-`. If no `Projects-` segment exists, take the final path segment.
2. **Special case:** a directory like `<home>--claude` (the encoded form of `~/.claude`) → label it `.claude`.
3. **Pi / ZCode** expose a real `cwd` field — take the final segment of that path directly.

Always discover paths dynamically from each agent's log dir; never assume a fixed home or drive layout.
