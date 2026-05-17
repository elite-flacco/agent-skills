# Eval Layer Guide

How to build the eval/ directory for output-producing skills.

## When to Include Eval

Include eval when the skill produces user-facing output where quality can be checked:
- Writing (blog posts, docs, reports)
- Design artifacts (component specs, mockups)
- Generated content (emails, presentations, proposals)

Skip eval for process/technique skills — those are validated by usage, not self-evaluation.

## Building checklist.md

### Step 1: Gather Criteria From Interview

During the interview, ask:
- "What are the non-negotiable criteria?" → These become **Hard Requirements**
- "What would make output great vs just okay?" → These become **Quality Checks**

### Step 2: Write Actionable Checks

Each checklist item should be:
- **Binary** — clearly pass or fail, no subjective judgment
- **Specific** — "Uses active voice in all headings" not "Good writing"
- **Checkable** — Claude can verify without external tools

Bad: `- [ ] Well-written`
Good: `- [ ] All headings use active voice (verb-first)`

Bad: `- [ ] Appropriate length`
Good: `- [ ] Each section is 100-300 words`

### Step 3: Set Thresholds

- **Hard Requirements:** Must pass ALL. Failure = revise before presenting.
- **Quality Checks:** Must pass 80%+. Failures below threshold = revise. Above threshold = note in review but present anyway.

## Building reviewers.md

### When to Use Reviewers

Use when output serves multiple audiences or has multiple quality dimensions that one perspective can't cover.

Examples:
- Technical blog post → Technical Accuracy reviewer + Readability reviewer
- User-facing docs → Developer reviewer + End User reviewer
- Marketing copy → Brand Voice reviewer + Conversion reviewer

### Designing Personas

Each persona needs:

1. **Focus:** One clear dimension they evaluate (not everything)
2. **Ask:** A single core question that drives their review
3. **Flags:** 3-5 specific things they look for

Keep personas distinct — if two personas would flag the same issues, merge them.

### How Reviewers Run

1. Draft is completed and passes checklist
2. Each reviewer runs as a parallel subagent call
3. Each subagent receives: the draft + the persona definition + the skill's instructions
4. Results are collected and summarized
5. Conflicts between reviewers are flagged for user to resolve

### Persona Count

- 2-3 personas is the sweet spot
- 1 persona = just use the checklist instead
- 4+ personas = too much noise, reviewers start contradicting each other

### Example Personas

**Technical Reviewer:**
- Focus: Accuracy and completeness
- Ask: "Is every technical claim correct? Are there gaps?"
- Flags: Incorrect terminology, missing caveats, oversimplifications, outdated information

**End User Reviewer:**
- Focus: Clarity and actionability
- Ask: "Could someone new follow this and succeed?"
- Flags: Assumed knowledge, missing steps, jargon without explanation, unclear next actions

**Brand Voice Reviewer:**
- Focus: Tone and consistency
- Ask: "Does this sound like us?"
- Flags: Off-brand language, inconsistent tone, generic phrasing, missed personality cues
