# Doc Verification

Before writing any agent code, verify current API shape against live docs — do not rely on training-data memory. LangChain/LangGraph/deepagents rename imports and deprecate APIs frequently (e.g. `AgentExecutor` largely superseded by `create_agent`/graph-based patterns; import paths move between `langchain`, `langchain-core`, `langchain-community` regularly).

## Where to look

- **Unified docs (all three frameworks):** https://docs.langchain.com/ — check `oss/python/langchain`, `oss/python/langgraph`, and `oss/python/deepagents/overview` sections.
- **API reference (exact function/class signatures):** https://reference.langchain.com/python/{langchain,langgraph,deepagents}
- **LangSmith tracing/threads specifically:** https://docs.langchain.com/langsmith/threads
- **deepagents source/examples (fastest-moving of the three):** https://github.com/langchain-ai/deepagents/tree/main/examples
- If the user's project is JS/TS, use the `deepagentsjs` and `langgraphjs` equivalents instead.

## What to verify, specifically

1. The current import path and constructor/factory name for the chosen tier (e.g. `create_agent`, `create_deep_agent`, `StateGraph`) — these get renamed across minor versions.
2. The current checkpointer API if using LangGraph/deepagents persistence (e.g. which package `InMemorySaver`/`PostgresSaver` currently live in).
3. The current model-string or client-construction convention (e.g. `"anthropic:claude-..."` shorthand vs explicit client object) for whichever provider the user is using.
4. Any breaking changes called out in the package's recent release notes if the installed version is pinned in the user's project (`pip show langchain langgraph deepagents` or check `package.json`/`pyproject.toml`/`requirements.txt`).

Fetch, don't guess — use WebFetch/WebSearch against the above before finalizing generated code. If fetching fails or is inconclusive, say so explicitly to the user rather than silently falling back to memorized APIs.
