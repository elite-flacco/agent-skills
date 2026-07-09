# Tracing Rules

Every agent this skill scaffolds gets LangSmith tracing wired in by default, with this exact session/trace/run mapping. This is the part that's easy to get subtly wrong, so follow it literally.

## The mapping

| Concept | Scope | Rule |
|---|---|---|
| `thread_id` | One conversation (all turns, one user, one chat session) | Generate **once per conversation**, in the calling application — never regenerated per turn. |
| Trace (root run) | One turn (one user message → one agent response) | Each turn's top-level `.invoke()`/`.stream()` call is its own trace root. |
| Run (span) | One step inside a turn (one LLM call, one tool call, one graph node) | Comes from normal automatic parent/child run nesting — do not hand-create runs per LLM call. |

## Concretely

1. **Generate the session id once**, at conversation start, in the calling app (e.g. `from langsmith import uuid7; session_id = str(uuid7())`). Keep it in memory/session state for the life of the conversation — not derived fresh each turn.
2. **Use the SAME id in two places, every turn:**
   - As `thread_id` in the LangGraph checkpointer config: `config = {"configurable": {"thread_id": session_id}, "metadata": {"thread_id": session_id}}`
   - As `thread_id` (or `session_id`) in LangSmith metadata on that turn's invocation — same dict, same value. Don't let these drift into two different ids.
3. **One call per turn = one trace.** Do not wrap multiple turns inside one outer `@traceable`/traced function — that would merge many turns into a single trace. Call `.invoke()`/`.stream()` fresh for each incoming user message, passing the config above each time.
4. **Let nested runs happen automatically.** LangChain/LangGraph already emit a child run for every LLM call, tool call, and graph node under whatever the current trace root is — don't manually instantiate `RunTree`s per step. Only add explicit `name=`/`metadata=` on tool functions and graph nodes so those spans are readable in the UI (e.g. `@tool(name="search_docs")`, or a node function named descriptively rather than `node_1`).
5. **For plain LangChain (no LangGraph)**, there's no checkpointer, so the session id only needs to go into LangSmith metadata — but the per-turn-is-a-trace rule still applies: one `.invoke()` per turn, with `{"metadata": {"thread_id": session_id}}` passed via `config=`.

## Common mistakes to avoid

- Regenerating `thread_id` per turn (breaks the LangSmith Threads view — turns won't group).
- Using a different id for the LangGraph checkpointer than for LangSmith metadata (breaks correlation between persisted state and trace grouping).
- Wrapping the whole conversation loop in one traced function (collapses all turns into one trace, destroying the "trace = one turn" property).
- Manually creating child runs/spans for each LLM call (redundant — automatic nesting already does this, and manual runs often end up detached from the real parent).

For the mechanics of *enabling* tracing (env vars, `@traceable`, `wrap_openai`) or *querying* existing traces/runs, defer to the `langsmith-trace` skill — this file only covers the thread/trace/run *mapping*, not the plumbing.
