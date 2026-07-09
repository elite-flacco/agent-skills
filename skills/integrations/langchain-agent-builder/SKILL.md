---
name: langchain-agent-builder
description: Use when starting a new LangChain, LangGraph, or deepagents agent from scratch, when deciding whether an agent needs LangGraph or deepagents instead of plain LangChain, or when scaffolding agent code that must have LangSmith tracing (thread_id, traces, runs) wired correctly from the start.
---

# LangChain Agent Builder

## Overview

Scaffold a new LangChain-family agent by first deciding the right framework tier (LangChain / LangGraph / deepagents), then verifying the exact APIs against current docs, then generating code with correct LangSmith tracing wired in by default. Do not skip steps to save time — stale APIs and mis-wired tracing are the two failure modes this skill exists to prevent.

Not for: querying/debugging existing traces, building datasets, or writing evaluators — see [Cross-references](#cross-references).

## Workflow

1. Read `instructions/decision-checklist.md` and ask the user those questions before writing any code. Do not guess the framework tier from the request alone.
2. Once a tier is chosen, read `instructions/doc-verification.md` and fetch current docs for that tier. Never generate agent code from training-data memory of these APIs — they change often (renamed functions, deprecated imports).
3. Read `instructions/tracing-rules.md` — the thread_id/trace/run wiring rules apply to every generated agent regardless of tier.
4. Read `instructions/session-thread-config.md` for the stable invocation contract. This is a wiring pattern, not a complete agent template.
5. Read `instructions/scaffold-output-format.md`, then generate code from the verified docs and the user's actual tools/model/prompt. Do not copy starter code from this skill; copy from current docs only after checking it against the installed package versions.
6. After scaffolding, tell the user which existing skill to reach for next instead of re-explaining it yourself (see below).

## Cross-references

This skill only owns "how to correctly wire tracing metadata while building an agent." For everything else LangSmith-related, use the existing skills — don't duplicate their content:

- **Enabling tracing generally / querying or exporting existing traces** → `langsmith-trace`
- **Building evaluation datasets** → `langsmith-dataset`
- **Writing evaluators / running evaluations** → `langsmith-evaluator`
- **Clearing/resetting feedback scores** → `langsmith-clear-feedback`

## When to Read What

- **Always read:** `instructions/decision-checklist.md`, `instructions/doc-verification.md`, `instructions/tracing-rules.md`, `instructions/session-thread-config.md`, `instructions/scaffold-output-format.md` — every agent-scaffolding request needs all five.
