# Evaluation Checklist

Run against the generated summary before saving.

## Hard Requirements (must pass all)

- [ ] Each included session's **created OR modified** timestamp falls within the target week — a session active across the boundary belongs in both weeks
- [ ] Every agent whose log directory exists was scanned; agents with no directory were skipped silently (not errored)
- [ ] Week boundaries are Monday 00:00:00 → Sunday 23:59:59 local time; filename is the Monday's date
- [ ] No project section lists zero sessions (empty projects omitted)
- [ ] Claude Code data came from both the session index AND the JSONL files (JSONL is authoritative for recent sessions)
- [ ] Codex data read from both `session_index.jsonl` and `history.jsonl`
- [ ] Project paths discovered dynamically per agent — no hardcoded username or drive prefix

## Quality Checks (must pass 80%+)

- [ ] Narrative summary names specific projects and what was done (not generic filler)
- [ ] Summary flags a dominant project or cross-project pattern if one exists
- [ ] Activity split across agents noted when notable
- [ ] Stats counts match the session lists in each section
- [ ] ZCode sessions grouped by `workspaceRoot`; `profileId` flagged only when it adds context
- [ ] Narrative stays factual (activity log, not a performance review)
