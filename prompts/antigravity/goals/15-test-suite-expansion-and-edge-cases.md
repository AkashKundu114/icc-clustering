# Goal: Test Suite Expansion & Adversarial Edge-Case Hardening

Deploy this goal to strengthen testing coverage, uncover latent runtime errors, and verify algorithmic resilience against degenerate, malformed, or adversarial inputs.

---

## Assigned Subagent Personas
1. **Adversarial QA Tester (`roo_debugger`)**: Constructs adversarial datasets, degenerate matrices, and boundary stress tests.
2. **Coverage Analyst (`roo_ask`)**: Runs coverage diagnostics (`pytest --cov`) and maps untested branches.
3. **Robustness Engineer (`roo_coder`)**: Adds defensive type validation, assertion guards, and graceful fallbacks.

---

## Targeted Adversarial Edge Cases

Every core algorithm, solver, and metric in the codebase must be evaluated against the following failure modes:

### 1. Degenerate Input Geometries
- **Zero-variance features:** Columns where all values are identical ($x_i = c$).
- **Collinear & Rank-Deficient Matrices:** Data where $D > N$ or features are linear combinations of each other.
- **Singular Adjacency / Graph Laplacians:** Disconnected subgraphs, isolated singleton nodes, and zero-degree vertices.
- **Extreme Scale Imbalance:** Clusters where one partition contains $99\%$ of points and other partitions contain $1$ point.

### 2. Numerical Pathologies
- **NaN / Infinite Values:** Inputs containing `np.nan`, `np.inf`, `-np.inf`.
- **Tiny & Massive Floats:** Underflow risks with `1e-300` and overflow with `1e+300`.
- **Small Sample Boundaries:** Running clustering or projection with $N = 1, 2$ or $K \ge N$.

### 3. Misspecification Scenarios
- **$K$-Misspecification:** Evaluating model behavior when user-specified cluster count $K$ differs widely from the underlying true clusters ($K \pm 5$).
- **Empty / Null Input:** Empty numpy arrays or zero-length lists.

---

## Execution Steps
1. **Identify Coverage Gaps:**
   ```bash
   pytest tests/ --cov=src --cov-report=term-missing
   ```
2. **Draft Adversarial Unit Tests:** Create dedicated test modules (e.g. `tests/test_adversarial_inputs.py` or `tests/test_edge_cases.py`).
3. **Implement Defensive Safeguards:** Update algorithms in `src/` to raise explicit `ValueError` or `UserWarning` rather than crashing with unhandled exceptions.
4. **Verify Regression Suite:** Ensure all 100% of pre-existing and newly added tests pass cleanly.
