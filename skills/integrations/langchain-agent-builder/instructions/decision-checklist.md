# Decision Checklist: LangChain vs LangGraph vs deepagents

Ask these one at a time (or as a short batch) before writing code. Real answers are fuzzy — use judgment on the final call and state your reasoning, don't apply a rigid flowchart.

## Questions to ask

1. **Turn shape** — Is this a single-shot request→response (retrieve, summarize, classify, one tool call), or a multi-turn conversation where the agent needs to remember earlier turns / reasoning across steps?
2. **Control flow** — Does the agent need to loop, branch, retry, or revisit earlier steps based on intermediate results (cyclic reasoning), or is a linear chain of steps enough?
3. **Persistence** — Does state need to survive across turns or process restarts (checkpointing), or is in-memory-for-one-call enough?
4. **Parallel sub-agents** — Does the task decompose into independent sub-tasks that should run with their own isolated context (e.g. "research 5 topics then merge"), or is it one agent using tools directly?
5. **Autonomy/horizon** — Is this a long-horizon task the agent should plan across multiple steps on its own (todo-list-style self-tracking), possibly touching many files/tools over an extended run — or a short, bounded interaction?
6. **Human-in-the-loop** — Does a human need to approve/edit/interrupt mid-run (e.g. before a risky tool call), requiring pause/resume?
7. **Context management** — Will the agent accumulate enough tool output/history that it needs its own scratch filesystem or summarization to avoid blowing the context window?

## How to decide

- **Plain LangChain** (LCEL chain, or a simple tool-calling loop): single-turn or lightly-tooled, no cyclic control flow, no cross-turn persistence needed. Q1–Q3 all "no"/simple.
- **LangGraph**: multi-turn or needs cycles/branching, needs checkpointed persistence across turns, and/or needs human-in-the-loop interrupts. Q2, Q3, or Q6 answered "yes" but Q4/Q5 are modest.
- **deepagents** (built on LangGraph): everything LangGraph needs, plus long-horizon autonomous planning, parallel sub-agents with isolated context, and/or its own virtual filesystem/context-management to survive long runs. Q4, Q5, or Q7 answered "yes".

State the recommendation and the specific answers that drove it — e.g. "You said this needs to remember prior turns and pause for approval before sending emails, so LangGraph with a checkpointer and an interrupt before that tool call." Let the user override.
