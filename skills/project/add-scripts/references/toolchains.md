# Default toolchains by stack

Pinned commands so two runs produce the same output. Use the row matching the
project's primary language. Each lists a linter, type checker (where one
exists), and formatter. Wire these into `lint`, `typecheck`, `format:check`,
and `format` (or the project's equivalent — `make targets`, `pyproject` scripts,
etc.).

## JavaScript / TypeScript (default)

| Script | ESLint + Prettier | Biome (all-in-one) |
|---|---|---|
| `lint` | `eslint .` | `biome check .` |
| `typecheck` | `tsc --noEmit` | `tsc --noEmit` |
| `format:check` | `prettier --check .` | `biome check .` |
| `format` | `prettier --write .` | `biome check --write .` |

Include `**/*.md` in Prettier's range so docs formatting is gated too. Biome
covers lint + format in one tool; drop ESLint/Prettier if Biome is present.

## Python

| Script | Command |
|---|---|
| `lint` | `ruff check .` |
| `typecheck` | `mypy .` (or `pyright`) |
| `format:check` | `black --check .` + `ruff format --check .` |
| `format` | `black .` + `ruff format .` |

`ruff` handles import sorting and linting; `black` is the formatter (or `ruff
format`, which is Black-compatible). Wire into `[tool.*]` in `pyproject.toml`.

## Go

| Script | Command |
|---|---|
| `lint` | `golangci-lint run` |
| `format:check` | `gofmt -l . \| read; test $? -eq 1` (fails if any file needs formatting) |
| `format` | `gofmt -w .` |

Go has no separate typecheck — the compiler (`go build ./...`) and
`golangci-lint` cover it.

## Rust

| Script | Command |
|---|---|
| `lint` | `cargo clippy -- -D warnings` |
| `format:check` | `cargo fmt -- --check` |
| `format` | `cargo fmt` |

`cargo build` / `cargo check` covers type checking.
