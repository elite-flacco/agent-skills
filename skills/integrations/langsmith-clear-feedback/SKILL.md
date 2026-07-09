---
name: langsmith-clear-feedback
description: Use when the user asks to clear, delete, reset, remove, or inspect LangSmith evaluator feedback scores for an experiment or tracing project.
---

# LangSmith Clear Feedback

Use this skill for deleting or inspecting LangSmith feedback records, especially when repeated evaluator runs create duplicate averaged scores in an experiment table.

## Guardrails

- Treat deletion as destructive. Run a dry-run first unless the user already gave explicit deletion approval in the current turn.
- Scope deletion with at least `--session-id` and `--key`. Prefer also using `--source auto_eval` for evaluator scores.
- Do not delete human/app feedback unless the user explicitly asks for that source.
- If an evaluator bug caused bad scores, preserve the run/evaluator IDs in the final answer so the issue can be reported or revisited.
- After deletion, verify the remaining count with the same filters.

## Script

Use the bundled script (path is relative to this skill's directory):

```bash
python3 scripts/clear_feedback.py \
  --session-id <experiment-or-project-id> \
  --key <feedback-key> \
  --source auto_eval
```

The script reads `LANGSMITH_API_KEY` and optional `LANGSMITH_ENDPOINT` from the environment. If the current repo has a `.env`, load it first:

```bash
set -a; source .env; set +a
```

## Dry Run

Dry-run is the default. It prints matching feedback record IDs, run IDs, scores, source metadata, and comments.

```bash
python3 scripts/clear_feedback.py --session-id <uuid> --key correctness --source auto_eval
```

## Delete

Only delete after reviewing the dry-run output:

```bash
python3 scripts/clear_feedback.py \
  --session-id <uuid> \
  --key correctness \
  --source auto_eval \
  --confirm-delete
```

Useful narrowing filters:

```bash
--rule-id <run-rule-id>
--created-after 2026-06-02T23:00:00Z
--created-before 2026-06-03T00:00:00Z
--comment-contains "assistant response is empty"
```

## Output Checklist

In the final response, include:

- Which session/experiment ID was targeted.
- Which key/source/rule/time/comment filters were used.
- How many records matched.
- How many were deleted.
- Verification count after deletion.
