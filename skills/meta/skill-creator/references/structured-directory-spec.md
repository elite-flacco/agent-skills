# Structured Directory Specification

Reference for what each directory contains and when to include it.

## Directory Reference

### instructions/

**Purpose:** Separate files for distinct rule categories. One file per concern.

**When to include:** Skill has 2+ distinct rule sets that would be confusing combined (e.g., voice rules are different from formatting rules are different from domain-specific rules).

**Naming:** Name by concern — `voice.md`, `formatting.md`, `section-guide.md`, `domain-rules.md`

**Content pattern:**
```markdown
# Voice Rules

## Tone
- Direct and conversational
- No corporate jargon

## Language
- Active voice preferred
- Short sentences for instructions, longer for explanations
```

### scripts/

**Purpose:** Executable code for deterministic, repeatable operations.

**When to include:** Skill involves tasks that are (a) repeated frequently, (b) error-prone when done manually, or (c) require deterministic reliability. Examples: file transforms, data processing, code generation, validation.

**Guidelines:**
- Test scripts by running them before shipping
- Include usage comments at the top of each script
- Claude should execute scripts, not read them into context (unless patching)

### examples/good/

**Purpose:** Annotated examples of excellent output.

**When to include:** Output quality is subjective and Claude benefits from seeing concrete "this is what good looks like." Most useful for content-producing skills.

**Content pattern:** Each example file should include:
- The example output itself
- Annotations explaining WHY it's good (inline comments or a section at the end)
- Context: what prompt/scenario produced this

### examples/bad/

**Purpose:** Anti-patterns with explanations of what's wrong.

**When to include:** There are common, non-obvious mistakes. Skip if bad output is simply "the opposite of good."

**Content pattern:** Each example should include:
- The bad output
- What's wrong with it (specific, not vague)
- How to fix it (brief pointer, not a full rewrite)

### eval/checklist.md

**Purpose:** Pass/fail criteria Claude runs against its own output before presenting to user.

**When to include:** Skill has verifiable quality criteria. Most useful for output-producing skills.

**Structure:**
```markdown
# Evaluation Checklist

## Hard Requirements (must pass all)
- [ ] Criterion 1
- [ ] Criterion 2

## Quality Checks (must pass 80%+)
- [ ] Criterion 1
- [ ] Criterion 2
```

Hard requirements come from user's non-negotiables. Quality checks come from preferences.

### eval/reviewers.md

**Purpose:** AI reviewer personas that evaluate output from different angles via parallel subagent calls.

**When to include:** Output benefits from multiple perspectives. Common for content that serves different audiences (technical vs non-technical, expert vs novice).

**Structure:**
```markdown
# Reviewers

Evaluate the draft from each perspective. Flag conflicts for user to resolve.

## [Persona Name]
- **Focus:** What this reviewer cares about
- **Ask:** The core question they evaluate against
- **Flags:** What they specifically look for
```

Suggest 2-3 personas max. More than that adds noise without value.

### templates/

**Purpose:** Output format skeletons that define structure without content.

**When to include:** Skill produces output that follows a consistent structure every time.

**Guidelines:**
- Templates are skeletons, not examples — use placeholders like `{{section_title}}`
- Include comments explaining each section's purpose
- One template per output format

### references/

**Purpose:** Heavy reference material loaded on demand.

**When to include:** Skill needs access to detailed docs, schemas, APIs, or domain knowledge that would bloat SKILL.md.

**Guidelines:**
- Files >100 lines should include a table of contents
- Include grep patterns in SKILL.md for very large files (>10k words)
- One file per domain/topic — don't dump everything in one giant file
