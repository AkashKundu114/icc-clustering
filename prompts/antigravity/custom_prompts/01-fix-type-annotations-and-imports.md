# Custom Prompt: Strict Static Typing & Clean Imports Sweep

- **Target Systems:** All source modules under `src/` and test suites under `tests/`.
- **Assigned Persona:** `roo_coder` (Implementation), `roo_debugger` (Verification).

---

## Technical Instructions
1. Run static analysis:
   ```bash
   mypy --strict src/
   ruff check src/ tests/
   ```
2. Remove all unused imports (`F401`), sort import blocks per PEP 8 (`I001`), and eliminate ambiguous variable names (e.g. `l`, `O`, `I`).
3. Replace raw untyped declarations with explicit generic types:
   - Use `np.ndarray[Any, np.dtype[np.float64]]` or `NDArray[np.float64]`.
   - Annotate return types on all public functions and classes.
   - For optional parameters, use `Optional[T]` or `T | None`.
4. Ensure `py.typed` marker file exists in package roots.

## Acceptance Criteria
- `ruff check src/ tests/` exits with 0 errors.
- `mypy -p <package_name>` completes with 0 errors.
- `pytest tests/` passes with 0 regressions.
