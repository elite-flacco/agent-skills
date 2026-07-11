# Weekly Activity Summary Template

Output skeleton for the generated markdown file. Fill `{{placeholders}}` from the
parsed session data. Drop any section for an agent with zero sessions in range.

```markdown
# Weekly Activity Summary: {{monday-date}}

**Period:** Monday, {{month}} {{day}} — Sunday, {{month}} {{day}}, {{year}}
**Generated:** {{today}}

## Summary

[2-4 sentence narrative synthesizing the week's themes — what major areas were
worked on, key accomplishments, patterns noticed. Be specific about project names.]

## Activity by Project

### {{project-name}} (N sessions)

- Session summary or first prompt description
- Another session...

### {{another-project}} (N sessions)

- ...

## Codex Activity

### {{project-or-thread-name}}

- Thread name / prompt description
- ...

## Pi Activity

### {{project-name}}

- Session prompt description
- ...

## ZCode Activity

### {{project-name}}

- Session description / prompt (note profileId if a subagent)
- ...

## Stats

- **Total Claude Code sessions:** N
- **Total Codex sessions:** N
- **Total Pi sessions:** N
- **Total ZCode sessions:** N
- **Most active project:** {{project-name}} (N sessions)
- **Days active:** N/7
```

## Narrative summary guidelines

- Mention specific project names and what was done
- Note if a project dominated the week
- Mention any cross-project patterns (e.g. "focused on UI work across multiple projects")
- Note activity split across agents if notable (e.g. "most work in Claude Code; used ZCode Explore for codebase research")
- Keep it factual — this is a personal activity log, not a performance review
