---
name: add-scripts
description: Use when the user asks to add lint, typecheck, format, or build scripts to a project's package.json — e.g. "add lint and format scripts", "add a typecheck script", "set up npm scripts", "add eslint", "add prettier", "add biome".
---

# Add Scripts

Add `lint`, `typecheck`, `format:check`, and `format` scripts to a project so the same checks run locally and in CI.

## Instructions

1. **Discover the existing toolchain.** Before installing anything, check what's already wired: read `package.json` scripts, and look for config files — `eslint.config.*`, `biome.json`, `.prettierrc*`, `tsconfig.json`. Wire scripts to the tools already present; don't reinstall.
2. **If greenfield JS/TS, pin defaults.** ESLint + Prettier (or Biome as the all-in-one alternative):
   - `eslint .` — lint
   - `tsc --noEmit` — typecheck (TS only)
   - `prettier --check .` — format:check (include `**/*.md`)
   - `prettier --write .` — format autofix
   - Biome alternative: `biome check .` / `biome check --write .`
3. **For non-JS stacks**, use the matching defaults in `references/toolchains.md` (Python: ruff/mypy/black; Go: golangci-lint/gofmt; Rust: clippy/rustfmt).
4. **Install only what's missing** — one devDependency per tool not already in `devDependencies`.
5. **Run every script and confirm it exits 0.** Fix surfaced issues before reporting done; don't weaken a script to make it pass.
