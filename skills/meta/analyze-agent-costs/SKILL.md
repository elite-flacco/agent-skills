---
name: analyze-agent-costs
description: Use when the user wants to understand cost attribution, token usage, or turn timelines from a Claude agent session — e.g. asks "where did my tokens go", "how much did each subagent cost", "visualize this audit.jsonl", or points at an audit.jsonl / session transcript log from Claude Code, agent mode, or the Agent SDK.
---

# Analyze Agent Costs

## Overview

Parse a Claude agent `audit.jsonl` (Claude Code / desktop agent mode / Agent SDK session log) into per-agent cost attribution and a turn timeline. Produces a stdout summary plus a self-contained HTML report with a clickable agent explorer.

## When to Use

- User provides an `audit.jsonl` (often under `~/Library/Application Support/Claude/local-agent-mode-sessions/.../audit.jsonl`) and asks about cost, tokens, turns, or subagents
- Questions like "why was this session expensive", "main agent vs subagents", "what happened turn by turn"
- NOT for LangSmith/LangChain traces (use the langsmith skills) or API billing exports

## Core Pattern

Run the bundled script — don't re-derive the parsing logic. Path is relative to this skill's directory, so resolve the skill dir first (skills are discovered from a flat symlink like `~/.zcode/skills/analyze-agent-costs/`, not the cwd):

```bash
python3 "$(skill dir of analyze-agent-costs)/scripts/analyze_audit.py" <audit.jsonl> -o report.html          # table + HTML report
python3 "$(skill dir of analyze-agent-costs)/scripts/analyze_audit.py" <audit.jsonl> --json                  # structured data for widgets
```

If the agent can't resolve the skill dir, locate it via its discovery symlink: `readlink -f ~/.zcode/skills/analyze-agent-costs` (or the equivalent under `~/.claude/skills`, `~/.codex/skills`, `~/.pi/agent/skills`).

Use `--json` output as the data source when rendering inline chat visualizations instead of the HTML file.

## How the Log Is Structured (for interpretation and debugging)

- `assistant` rows are **streaming snapshots**: one API request appears multiple times with the same `request_id` and identical usage. Always dedupe by `request_id` before summing.
- `parent_tool_use_id` groups rows by agent: `null` = main agent; otherwise it's the `Task`/`Agent` tool_use id that spawned the subagent. Subagent names come from that tool call's `description` input.
- The final `result` row is authoritative: `total_cost_usd`, `num_turns`, and per-model `modelUsage` totals.
- `num_turns` counts SDK message exchanges; unique `request_id`s count billable API calls; raw assistant rows count neither.

## Known Caveats (state these when presenting results)

| Caveat | Why |
|--------|-----|
| Output tokens per agent are **estimates** | Per-request usage is captured at stream start (`output_tokens` ≈ 1). The script distributes the authoritative `modelUsage` output total by generated content chars, folding each subagent's final report (found in the parent's tool_results) back into that subagent. |
| Server-side search model split evenly | WebSearch runs on Haiku server-side; the log only reports its usage as session totals, so cost is split per WebSearch call count. |
| Some cost is unattributed | Some requests never receive audit rows; the script reports the residual vs `total_cost_usd` (typically ~4%). |
| Pricing table needs maintenance | `PRICING` in the script maps model-id prefixes to $/MTok (input, output, cache read, 5m/1h cache write). Verify against the claude-api skill or docs when a new model appears. |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Summing usage across all assistant rows | Dedupe by `request_id` first — snapshots repeat |
| Trusting per-request `output_tokens` | Use `modelUsage` totals; per-agent output must be estimated |
| Ignoring the Haiku line in `modelUsage` | That's the WebSearch engine — often a third or more of session cost including $0.01/search fees |
| Reading cache write as normal input | 1h-tier cache writes bill at 2× input rate; cache reads at 0.1× — the ratio drives main-agent economics |
