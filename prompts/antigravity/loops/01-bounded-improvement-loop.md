# Loop: Multi-Subagent Bounded Implementation Plan Execution

Use this loop when executing an approved Implementation Plan or resolving prioritized custom prompts.

---

## Run Budget & Operating Boundaries
- **Maximum Iterations:** 5 iterations per session. Never run indefinitely.
- **Subagent Orchestration:** Each iteration should engage specialized personas:
  - `Codebase Researcher`: Gathers localized context and confirms caller dependencies before changes.
  - `Engineer (roo_coder)`: Implements surgical, minimal edits adhering to existing patterns.
  - `Verifier / Debugger (roo_debugger)`: Runs tests, diagnoses failures, and fixes stack traces.
  - `Reviewer (roo_reviewer)`: Audits git diffs for regressions, leaked secrets, or collateral churn.
- **Resource Budget:** Adhere to `configs/agent.local.yaml` limits (RAM, CPU workers, GPU fractions).
- **Scope Limit:** Strictly confined to current repository files specified in the active plan phase.

---

## Iteration Protocol

### Step 1: Phase Selection & Objective Locking
1. Review the Implementation Plan and previous iteration logs in `prompts/antigravity/logs/`.
2. Select the next single, coherent task from the plan.
3. State the exact objective, target files, and acceptance criteria in the current iteration log.

### Step 2: Context Gathering via Researcher Subagent
1. Inspect git status to guarantee no uncommitted conflicting edits exist.
2. Examine the target functions, callers, and test files.
3. Verify the existing baseline behavior and establish failure reproduction when fixing a defect.

### Step 3: Surgical Implementation via Coder Subagent
1. Implement the minimal required change to satisfy the acceptance criteria.
2. Avoid cosmetic reformatting, stylistic churn, or unrelated file changes.
3. Preserve all documentation, docstrings, and non-deprecated public interfaces.

### Step 4: Verification via Debugger Subagent
1. Run targeted unit tests and static checks (`pytest tests/test_target.py`, `ruff check`, `mypy`).
2. Run broader regression tests across dependent modules.
3. Record exact execution commands, runtimes, and outputs in the iteration log.
4. If failures occur, diagnose root cause surgically. Never remove or weaken tests to force a green status.

### Step 5: Diff Review via Reviewer Subagent
1. Audit `git diff` against acceptance criteria.
2. Ensure no secrets, tokens, generated caches, or temporary files are staged.
3. Confirm that empirical claims or paper macros remain synchronized if metrics changed.

---

## Gate & Termination Rules

### Continue to next iteration ONLY IF:
- The current phase passed all verification gates.
- Remaining phases in the implementation plan are unblocked and within budget.
- No user-input blocker or ambiguous requirement arose.

### STOP IMMEDIATELY IF:
- A security or privacy concern is encountered.
- Repeated test failures indicate an unrecognized design flaw requiring owner consultation.
- The task requires external network access, cloud credentials, or destructive filesystem actions.
- The 5-iteration budget limit is reached.

---

## Final Deliverable
Upon completing the plan or stopping:
- Compile a comprehensive final report summarizing iterations completed, files modified, verification outcomes, and any deferred/blocked items.
- Leave git state clean, test suites passing, and changes uncommitted.
