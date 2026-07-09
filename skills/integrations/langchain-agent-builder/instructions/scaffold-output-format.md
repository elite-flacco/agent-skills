# Scaffold Output Format

Before writing agent code, collect current documentation evidence and show it briefly in the response or implementation notes.

## Required Evidence

State the verified source for each of these before final code is considered complete:

1. Selected tier: plain LangChain, LangGraph, or deepagents, with the checklist answers that drove the choice.
2. Current package/API surface: import path, factory or graph constructor, and invocation shape.
3. Model construction: provider package, model string or client object, and required environment variables.
4. State persistence: whether there is no checkpointer, an in-memory checkpointer, a durable checkpointer, or deployment-managed persistence.
5. LangSmith correlation: where `thread_id` is passed for tracing and, when applicable, checkpointing.

## Code Rules

- Build from the current docs and installed versions, not from memorized examples.
- Use the smallest complete code needed for the user's project.
- Keep the caller responsible for creating and storing `session_id`.
- If docs are inconclusive, mark the uncertain API explicitly and leave a TODO rather than inventing a confident import or argument name.
- If the user's project already has a model client, tool wrapper, tracing setup, or session store, adapt to that local pattern instead of introducing a parallel one.

## Final Response

Include:

- The tier chosen and why.
- The docs or installed package versions checked.
- The files changed or scaffolded.
- How to run the new agent.
- Any unresolved API/version uncertainty.
