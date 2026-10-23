# Loop: Multi-Subagent Regression & Release Gate

Use this verification loop before publishing a release, pushing to GitHub, or submitting a manuscript.

---

## Verification Protocol
Deploy the `Auditor` and `Reviewer` personas to run a multi-stage verification sweep:

### 1. Repository Cleanliness & Leakage Audit
- Run `git status -u` to verify no untracked secrets, credentials, model weights, or large binary caches exist.
- Verify `.gitignore` completeness against heavy directories (`data/cache/`, `figures/`, `dist/`, `paper/*.pdf`, `*.zip`).
- Ensure all public directories contain descriptive `README.md` and `.gitkeep` files where appropriate.

### 2. Static Typing & Linting Gate
- Run full repository static analysis:
  ```bash
  ruff check .
  mypy --strict .
  ```
- Must complete with 0 errors and 0 warnings.

### 3. Automated Test Suite Gate
- Run all unit, integration, and edge-case test suites:
  ```bash
  pytest tests/ -v
  ```
- All tests must pass with 0 regressions.

### 4. End-to-End Walkthrough Gate
- Execute public entrypoint or demo walkthrough:
  ```bash
  python demo.py
  ```
- Confirm runtime exits cleanly within expected time and resource budgets.

---

## Release Verdict
If any gate fails, abort release staging immediately. Deploy `roo_debugger` to isolate the failure and resolve it before re-running the gate.
