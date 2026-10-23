# Custom Prompt: Adversarial & Boundary Condition Unit Tests

- **Target Systems:** Algorithm solvers, projections, and evaluation metrics in `src/`.
- **Assigned Persona:** `roo_debugger` (Adversarial Testing).

---

## Technical Instructions
1. Create or extend `tests/test_edge_cases.py` and `tests/test_adversarial_inputs.py`.
2. Construct parameterized unit tests evaluating:
   - **Degenerate Geometries:** All zeros, identical duplicate rows, rank-1 matrices, single sample ($N=1$).
   - **Extreme Dimensionality:** Extreme $D \gg N$ (e.g. $N=10, D=5{,}000$) and $N \gg D$ ($N=5{,}000, D=2$).
   - **Pathological Noise:** Gaussian noise at SNR $\to 0$, Cauchy heavy-tailed noise, and zero-inflation.
   - **Cluster Misspecification:** Testing with requested $K=1$, $K \ge N$, and non-contiguous cluster labels.
3. Verify that solvers raise descriptive `ValueError` exceptions with helpful diagnostic messages instead of crashing with cryptic linear algebra or index errors.

## Acceptance Criteria
- `pytest tests/test_edge_cases.py -v` passes with 100% assertions satisfied.
- Code coverage across error-handling branches in `src/` increases without regressions.
