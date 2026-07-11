---
name: capture-session-learning
description: Use when the user wants to capture, document, or save durable learnings from the current technical session, create a learning note, identify knowledge gaps or next topics, or get relevant resources to read or watch.
---

# Capture Session Learning

Turn the current session into a durable Markdown learning note. Synthesize what became understood; do not produce a chronological transcript or a generic session summary.

## Workflow

1. Review the conversation and any artifacts inspected or changed during the session. Separate verified facts from hypotheses, and omit routine execution details.
2. Infer a concise topic and filename from the session. Use a user-provided topic when available; do not ask for confirmation unless the topic is genuinely ambiguous.
3. Extract the durable learning:
   - concepts and the mental model behind them
   - root causes and diagnostic signals
   - decisions and why they were made
   - reusable techniques or patterns
   - failed approaches, misconceptions, and important caveats
   - open questions and useful next topics
4. Include only minimal code or command examples that materially improve recall. Never include secrets, credentials, personal data, or large copied outputs.
5. When resource recommendations are requested or would materially improve the note, research them on the live web:
   - prefer official documentation, primary sources, recognized conference talks, and authoritative maintainers
   - verify that every URL opens and supports the recommendation
   - select 3–5 resources rather than returning a broad link dump
   - state why each resource is relevant and what the user should focus on
   - distinguish introductory material from deeper study
6. Choose the destination:
   - use a path or learning-notes convention the user supplied
   - otherwise inspect the current workspace for an established learning, notes, or documentation location
   - if no convention exists, ask the user where durable personal notes should live before writing outside the current workspace
7. Write the note using the structure below. Omit empty sections instead of filling them with placeholders.
8. Read the saved file back and confirm that it contains the central lesson, actionable detail, and working resource links.

## Note Structure

```markdown
# <Topic>

**Date:** YYYY-MM-DD

## In Brief

<A concise explanation of the central lesson.>

## What I Learned

<Durable concepts, techniques, and decisions.>

## Why It Works

<The underlying technical model.>

## What Went Wrong

<Symptoms, root causes, misleading signals, and failed approaches.>

## Reusable Patterns

<Rules or techniques worth applying elsewhere.>

## Examples

<Only the smallest useful examples.>

## Open Questions

<Remaining gaps or worthwhile next topics.>

## Recommended Resources

- [Resource](https://example.com) — why it is relevant and what to focus on
```

## Quality Bar

- Write in the user's voice as a reusable note, without conversation meta-commentary.
- Prefer causal explanations and concrete evidence over vague takeaways.
- Preserve uncertainty where the session did not establish a fact.
- Do not claim the note was added to a personal knowledge base unless an actual supported ingestion step succeeded.
- Report the saved path and briefly summarize what was captured.
