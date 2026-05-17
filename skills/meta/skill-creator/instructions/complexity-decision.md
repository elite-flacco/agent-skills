# Complexity Decision: Simple vs Structured

Evaluate these signals and recommend a mode. State reasoning clearly. User has final say.

## Structured Signals

Any of these suggest structured mode:

- **Output-producing:** Skill creates user-facing content (writing, reports, designs, presentations)
- **Multiple rule categories:** Distinct sets of rules that don't belong in one section (voice rules, formatting rules, domain rules, section-specific guidance)
- **Subjective quality:** Output quality benefits from annotated good/bad examples
- **Large scope:** Content would exceed ~200 lines as a single SKILL.md
- **Verifiable criteria:** There are concrete pass/fail criteria worth codifying in a checklist
- **Scripted operations:** Repeatable tasks best handled by deterministic scripts (file transforms, data processing, code generation)

## Simple Signals

These suggest a single-file skill:

- **Process/technique skill:** Teaches a method, workflow, or debugging approach
- **Uniform rules:** All guidance is one coherent set, not multiple categories
- **Code/action output:** Output is code, commands, or actions — not prose
- **Compact:** Fits comfortably under 200 lines
- **No templates needed:** Output doesn't follow a fixed skeleton
- **No scripts needed:** No deterministic automation required

## How to Present

State the recommendation with the top 1-2 reasons:

> "This looks like a content-producing skill with distinct voice and formatting concerns — I'd recommend **structured mode**. Want to go with that, or keep it simple?"

> "This is a compact debugging technique — **simple mode** makes sense here. Unless you see a reason to go structured?"

If signals are mixed, default to simple — the user can always request structured.
