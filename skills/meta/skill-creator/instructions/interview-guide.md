# Interview Guide

Ask questions one at a time. Prefer multiple choice when possible. Don't front-load — build understanding iteratively.

## Common Questions (Both Modes)

Ask these in roughly this order, skipping any already answered:

1. **Purpose:** What does this skill do? What problem does it solve?
2. **Triggers:** What would a user say or do that should activate this skill? Give examples.
3. **Knowledge gap:** What does Claude NOT already know that this skill needs to teach? (This is the most important question — if Claude already knows it, the skill is wasted tokens.)
4. **Examples:** Can you give 2-3 examples of how the skill would be used?
5. **Existing patterns:** Are there existing skills or codebases to reference?
6. **Anti-patterns:** What should the skill explicitly avoid doing?

## Additional Questions for Structured Mode

Only ask about directories that seem relevant based on earlier answers. Skip irrelevant ones.

### instructions/
> "You mentioned [X] and [Y] as different kinds of rules. Should these live as separate instruction files (e.g., voice rules vs formatting rules), or are they cohesive enough for one set?"

### scripts/
> "Are there operations this skill repeats that should be scripted for reliability? What language would they be in?"

### examples/good/
> "Can you show me what great output looks like? Or should I draft examples for your review?"

### examples/bad/
> "Are there common mistakes or anti-patterns you've seen that we should show as 'don't do this'?"

### eval/checklist.md
> "What are the non-negotiable criteria for output? What makes it pass vs fail?"

### eval/reviewers.md
> "Would it help to have multiple reviewer perspectives? For example, a technical accuracy reviewer and an end-user clarity reviewer?"

### templates/
> "Does the output follow a consistent structure? Should we create a template skeleton?"

### references/
> "Is there heavy reference material (docs, schemas, APIs) the skill needs access to?"

## Concluding the Interview

When you have enough to draft, summarize what you plan to create:

> "Here's what I'll build:
> - `SKILL.md` — orchestrator with workflow
> - `instructions/voice.md` — tone and language rules
> - `instructions/formatting.md` — structure and layout rules
> - `examples/good/blog-post.md` — annotated example
> - `eval/checklist.md` — quality criteria
> - `templates/post-template.md` — output skeleton
>
> Sound right, or should I add/remove anything?"

Wait for approval before scaffolding.
