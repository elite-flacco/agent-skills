# Emoji Conventional Commit Prefixes

Single source of truth for emoji + conventional-commit prefixes used in commit messages and PR titles. Used by the `commit` and `azdo-create-pr` skills.

Each commit/PR type pairs with an appropriate emoji. Format: `<emoji> <type>(<scope>): <description>`.

## Core types

- ✨ `feat`: New feature
- 🐛 `fix`: Bug fix
- 📝 `docs`: Documentation
- 🎨 `style`: Improve structure/format of the code
- 💄 `style`: Formatting/style
- ♻️ `refactor`: Code refactoring
- 🚚 `refactor`: Move or rename resources
- 🏗️ `refactor`: Make architectural changes
- ⚡️ `perf`: Performance improvements
- ✅ `test`: Tests
- 🤡 `test`: Mock things
- 🔧 `chore`: Tooling, configuration
- 👥 `chore`: Add or update contributors
- 🔀 `chore`: Merge branches
- 📦️ `chore`: Add or update compiled files or packages
- ➕ `chore`: Add a dependency
- ➖ `chore`: Remove a dependency
- 🌱 `chore`: Add or update seed files
- 🧑 `chore`: Improve developer experience
- 🎉 `chore`: Begin a project
- 🔖 `chore`: Release/Version tags
- 📌 `chore`: Pin dependencies to specific versions
- 📄 `chore`: Add or update license
- 🙈 `chore`: Add or update .gitignore file
- 🚀 `ci`: CI/CD improvements
- 🗃️ `db`: Perform database related changes
- 🍱 `assets`: Add or update assets

## `feat` subtypes

- 🏷️ `feat`: Add or update types
- 🌐 `feat`: Internationalization and localization
- 📱 `feat`: Work on responsive design
- 🚸 `feat`: Improve user experience / usability
- 📈 `feat`: Add or update analytics or tracking code
- 💥 `feat`: Introduce breaking changes
- ♿️ `feat`: Improve accessibility
- 🚩 `feat`: Add, update, or remove feature flags
- 🦺 `feat`: Add or update code related to validation
- ✈️ `feat`: Improve offline support

## `fix` subtypes

- 🚨 `fix`: Fix compiler/linter warnings
- 🔒️ `fix`: Fix security issues
- 🩹 `fix`: Simple fix for a non-critical issue
- 🥅 `fix`: Catch errors
- 👽️ `fix`: Update code due to external API changes
- 🔥 `fix`: Remove code or files
- 🚑️ `fix`: Critical hotfix
- 💚 `fix`: Fix CI build
- ✏️ `fix`: Fix typos
- 🔇 `fix`: Remove logs

## Notes

- Keep the first line under 72 characters.
- Use present tense, imperative mood ("add feature", not "added feature").
- When splitting commits, each commit gets its own emoji+type prefix matching its concern.
