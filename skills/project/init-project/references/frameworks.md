# Framework scaffold commands

One entry per supported framework. Run the framework's own scaffolder so the
directory layout, build config, and `.gitignore` come from upstream — don't
hand-roll what the CLI generates. Tooling (lint/format/typecheck) is added in a
later step via the `add-scripts` skill; testing config is part of the scaffold
where noted.

## Web — React

```bash
npm create vite@latest <name> -- --template react-ts
```

Produces Vite + React + TypeScript. Add a testing layer (`vitest`) separately
if the template doesn't include it.

Next.js alternative: `npx create-next-app@latest` (App Router, TypeScript, ESLint,
Tailwind built in; add Vitest separately).

## Web — Vue

```bash
npm create vue@latest <name>
```

Vue 3 + TypeScript + Vite; prompts for router, Pinia, Vitest, ESLint/Prettier.

## Web — Angular

```bash
npx @angular/cli new <name> --style=scss --routing
```

Angular CLI project with TypeScript, Karma/Jasmine testing, and Angular's own
lint/build pipeline.

## API — Express

No first-party scaffolder; minimal setup:

```bash
npm init -y
npm i express
npm i -D typescript @types/node @types/express tsx
npx tsc --init
```

Create `src/index.ts` (Express app), `src/routes/`, and a `start` script
(`tsx watch src/index.ts`). Add Jest or Vitest for route tests.

## API — FastAPI (Python)

```bash
pip install "fastapi[standard]"
```

Create `app/main.py` with an `APIRouter`, `app/models/` for Pydantic, and
`tests/` with `pytest`. Add `pyproject.toml` for ruff/mypy/black config (see
`add-scripts/references/toolchains.md`).

## Mobile — React Native

```bash
npx react-native init <name> --template react-native-template-typescript
```

Or Expo: `npx create-expo-app <name>`. Includes Metro, the native toolchain,
and Jest.

## Desktop — Electron

```bash
npm init electron-app@latest <name> -- --template=typescript
```

Electron Forge scaffold with `src/main.ts` (main process) and `src/renderer/`
(UI). Add a bundler (Vite/Webpack) for the renderer.

## CLI — Node

```bash
npm init -y
npm i commander
npm i -D typescript @types/node tsup
```

`src/index.ts` with a `commander` program; `tsup` for bundling to CJS/ESM. Add
a `bin` field in `package.json`.

## Library — npm

```bash
npm init -y
npm i -D typescript tsup vitest
```

`src/index.ts` entry, `tsup` for bundling, `vitest` for tests. Set `type:
"module"` (or CJS) and a `files` array in `package.json` for publishing.
