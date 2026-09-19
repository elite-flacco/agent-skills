# Common Mistakes

| Mistake | Fix |
|---------|-----|
| Trusting docs, comments, memory, or PR text before reading code | Build the model from changed code first, then compare outside context for drift |
| Reviewing only the diff | Read nearby callers, tests, config, schema, routes, and runtime entry points |
| Treating clean code as correct behavior | Trace the functional workflow and verify the change logically solves the real user or product problem |
| Guessing SDK or framework behavior from memory | Verify new, upgraded, unfamiliar, or behavior-critical third-party usage against official version-specific sources |
| Treating a passing test suite as evidence of correctness | Tests pass against the author's own assumptions; run the code against real data — the live DB, local source files, actual API responses — to surface what they didn't expect |
| Trusting a comment that asserts third-party behavior | A comment like "this is free" or "the API requires X" is an unverified claim; read the actual doc, spec, or SDK field and confirm it independently |
| Spawning subagents before understanding scope | Scope the diff first, then delegate narrow independent lenses and synthesize one final review |
| Reporting style preferences as bugs | Prioritize behavior, architecture risk, maintainability, tests, and user impact |
| Skipping UI verification because code compiles | Use the in-app browser where possible and agent-browser for repeatable user-flow checks |
| Asking for generic test coverage | Name the specific scenario or regression the missing test should catch |
| Fixing during review | Do not edit unless the user asks to address the findings |
