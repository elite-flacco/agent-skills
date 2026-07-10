# Review Lenses

The six lenses used by the `review-code-changes` skill. Read the change through
each lens; not every lens applies to every diff, but skip a lens deliberately,
not by accident.

## 1. Functional behavior

Infer the intended workflow from the code path, then verify:

- Inputs and outputs
- Data transformations
- Validation
- State transitions
- Side effects
- Failure paths
- Regressions
- Backwards compatibility
- Whether the change solves the real problem

## 2. Architecture / design

Check:

- Ownership boundaries
- Abstractions
- Coupling
- Data flow
- Implicit ordering
- Global side effects
- Persistence
- Migrations
- Feature flags
- Rollback behavior
- Whether a simpler design would work

## 3. Implementation quality

Inspect:

- Naming
- Readability
- Type safety
- Validation
- Duplication
- Dead code
- Stale comments
- Cleanup
- Logging
- Observability
- Performance
- Accessibility
- Security
- Brittle string/date handling

## 4. Third-party usage

For new, upgraded, unfamiliar, or behavior-critical packages, SDKs, framework
APIs, CLIs, config options, or generated types, verify against official
version-specific sources:

- Docs
- Changelogs
- Migration guides
- API references
- Release notes
- Typed declarations
- Package source

## 5. Tests

Identify changed behavior and check coverage for:

- Success cases
- Failure cases
- Boundary conditions
- Regression scenarios
- Integration
- UI states

Recommend only tests that reduce real risk — don't ask for generic coverage.

## 6. Operations

Check when relevant:

- Config
- Environment variables
- Secrets
- Rate limits
- Auth requirements
- Runtime support
- Deploy safety
- Monitoring
- Rollback concerns
