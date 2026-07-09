# Session and Thread Config Pattern

Use this as the stable contract for session identity and tracing correlation. It is not a full LangChain, LangGraph, or deepagents template.

## Ownership

- The calling application owns the conversation id.
- Generate one id at conversation start, store it in the caller's session state, and pass the same value on every turn.
- Do not create the id at module import time inside the agent file.
- Do not regenerate the id inside a per-turn handler.

## Invocation Shape

For LangGraph or deepagents with checkpointed state, the same id must be present in both places:

```python
config = {
    "configurable": {"thread_id": session_id},
    "metadata": {"thread_id": session_id},
}

agent.invoke(current_turn_input, config=config)
```

For plain LangChain without a checkpointer, only metadata is required:

```python
config = {"metadata": {"thread_id": session_id}}

agent.invoke(current_turn_input, config=config)
```

## Rules

- `configurable.thread_id` controls checkpoint lookup for graph-backed agents.
- `metadata.thread_id` controls LangSmith thread grouping.
- When both are used, they must have the same value.
- One top-level invoke or stream call handles one user turn and creates one trace.
- Conversation history belongs either in the caller's input messages for non-checkpointed agents or in the graph checkpointer for checkpointed agents. Do not mix both unless the current docs recommend it for the chosen framework.
