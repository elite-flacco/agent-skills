# Authoring Rules

## Frontmatter

Every SKILL.md requires YAML frontmatter with exactly two fields:

```yaml
---
name: skill-name-kebab-case
description: Use when [specific triggering conditions and symptoms]
---
```

- **name:** kebab-case, verb-first when possible (e.g., `creating-reports` not `report-creator`)
- **description:** Max 1024 chars. Starts with "Use when..." Describes ONLY triggering conditions.
  - NEVER summarize the skill's workflow or process in the description
  - Why: Claude may follow the description shortcut instead of reading the full skill body
  - Include concrete triggers, symptoms, situations
  - Write in third person

### Description Examples

```yaml
# BAD: Summarizes workflow
description: Create skills by interviewing the user, deciding complexity, and scaffolding files

# BAD: Too vague
description: For making skills

# GOOD: Triggering conditions only
description: Use when creating a new skill, updating an existing skill, or restructuring a skill's format
```

## Progressive Disclosure

Three loading levels — respect them:

1. **Metadata** (name + description) — always in context. ~100 words max.
2. **SKILL.md body** — loaded when skill triggers. Target: <150 lines (structured) or <500 lines (simple).
3. **Bundled resources** — loaded as needed. Unlimited size.

Keep SKILL.md lean by pointing to reference files instead of inlining heavy content.

## Writing Style

- Use imperative/infinitive form ("Run the script" not "You should run the script")
- Prefer concise examples over verbose explanations
- One excellent example beats many mediocre ones
- Challenge each paragraph: "Does Claude really need this? Does it justify its token cost?"

## Token Efficiency

- Split content >100 lines into reference files
- Use cross-references to other skills instead of duplicating
- Compress examples — minimal viable context
- No auxiliary files (README, CHANGELOG, INSTALLATION_GUIDE, etc.)

## Keyword Coverage (CSO)

Include words Claude would search for:
- Error messages and symptoms the skill addresses
- Synonyms for key concepts
- Tool names, library names, file types
- Action verbs matching user requests

## File References in Structured Skills

When SKILL.md points to other files, be explicit about WHEN to read them:

```markdown
## When to Read What
- **Always read:** instructions/ files (core rules)
- **Read when drafting:** examples/, templates/
- **Read on demand:** references/ (for specific lookups)
- **Execute, don't read:** scripts/ (run directly)
```

Keep references one level deep from SKILL.md. No nested reference chains.
