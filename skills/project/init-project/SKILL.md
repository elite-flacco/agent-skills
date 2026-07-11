---
name: init-project
description: Use when the user asks to initialize or scaffold a new project with baseline files (framework setup, dirs, git, README) — e.g. "initialize a new project", "scaffold a new repo", "set up a new app", "create a vite app", "new next.js project", "scaffold a fastapi service". For adding lint/format/CI hooks to an existing repo, use project-bootstrap instead.
---

# Init Project

Scaffold a new project's framework skeleton, then delegate tooling and gating to sibling skills.

## Instructions

1. **Determine the framework.** Ask if it's not clear from the request or the current directory. Pick the matching scaffold command from `references/frameworks.md` (Vite, Next.js, Vue, Angular, Express, FastAPI, React Native, Electron, Node CLI, npm library).
2. **Scaffold the skeleton.** Run the framework's own scaffolder so the directory layout, build config, and `.gitignore` come from upstream rather than hand-rolled. Add `docs/` and any dirs the scaffolder omits.
3. **Initialize git + README.** `git init`, stage the scaffold, and write a `README.md` with project name, setup, and run commands. Create the initial commit.
4. **Delegate lint / format / typecheck scripts** → invoke `add-scripts` (it discovers or pins the toolchain and verifies each script exits 0).
5. **Delegate CI** → invoke `add-github-actions` (copies GitHub Actions defaults into `.github/`).
6. **(Optional) Delegate the verify-gate** → invoke `project-bootstrap` if the user wants a local verify hook on every turn (in addition to CI). Skip if they only want CI gating.
7. **Validate.** Run every script the scaffolder produced plus the ones `add-scripts` added; confirm each exits 0 before reporting done. Start the dev server to confirm it boots.

Keep this skill a thin orchestrator — it scaffolds and delegates. The framework matrix and per-framework notes live in `references/frameworks.md`; tooling defaults are owned by the `add-scripts` skill (in its own `references/toolchains.md`).
