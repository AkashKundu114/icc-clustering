# Goal: Code Quality and Maintainability

Improve readability and long-term maintainability without changing intended behavior.

## Inspect
- Duplicated logic, oversized modules, unclear names, dead code, unnecessary abstraction, hidden side effects, weak error handling, type gaps, inconsistent interfaces, and fragile configuration.
- Project structure, import boundaries, dependency sprawl, test quality, and docs that disagree with actual behavior.

## Execution
1. Establish baseline checks.
2. Select the highest-value, well-evidenced findings.
3. Refactor in small, behavior-preserving steps.
4. Add regression tests before or with bug fixes.
5. Run focused tests and broader checks when feasible.
6. Inspect the diff for unrelated churn and public API changes.

## Acceptance criteria
- Changes have a clear rationale.
- Behavior changes are covered by tests.
- No validation is removed just to make tests pass.
- Public interfaces and migration needs are documented.
- Any unverified issue remains clearly marked as unresolved.
