# Parallel Review Agents

Default to a single reviewer. Go parallel only for large diffs spanning multiple subsystems (e.g. backend + frontend + config), or when browser verification or third-party docs research can run independently of code analysis. Skip it when findings depend on shared whole-system understanding or the review needs a single product judgment.

When dispatching subagents:
1. Scope the diff yourself first, then split by review lens or subsystem — never "review everything" prompts. Lenses match the review lenses in [review-lenses.md](review-lenses.md).
2. Give each subagent exact files, commands, docs targets, and output format; they return findings only and must not edit, stage, commit, or switch branches.
3. Read all results, deduplicate, resolve contradictions, rank severity, and write one final review.
