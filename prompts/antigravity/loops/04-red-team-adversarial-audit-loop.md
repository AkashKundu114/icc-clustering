# Loop: Red-Team Adversarial & Boundary Stress Audit

Use this loop when running adversarial security, mathematical robustness, and edge-case stress tests. It employs a two-sided attacker/defender protocol between subagents.

---

## Operating Budget & Setup
- **Maximum Iterations:** 4 iterations per run.
- **Assigned Subagent Personas:**
  - `Red-Team Attacker (roo_debugger)`: Probes for algorithmic failure modes, numerical singularities, unhandled exceptions, and memory exhaustion.
  - `Blue-Team Defender (roo_coder)`: Implements defensive guards, sanitized inputs, and robust mathematical fallbacks.
  - `Verification Auditor (roo_reviewer)`: Confirms that fixes do not compromise standard performance or break backward compatibility.

---

## Iteration Protocol

### 1. Attack Vector Selection
The Red-Team Attacker formulates one targeted stress vector:
- **Zero/Negative Variance:** Feeding features with zero variance or rank-deficient feature matrices ($D \gg N$).
- **Ill-Conditioned Graph Laplacians:** Constructing disconnected similarity graphs with zero eigenvalues or isolated vertices.
- **Pathological Numerical Floats:** Subnormal numbers (`1e-320`), NaNs, $\pm\infty$, or catastrophic floating-point cancellation.
- **Resource Bombing:** Submitting inputs designed to trigger $\mathcal{O}(N^3)$ computational slowdown or quadratic memory expansion.

### 2. Failure Isolation & Proof-of-Break
- The Attacker writes a minimal reproducible test case (e.g. in `tests/test_adversarial_inputs.py`) demonstrating an unhandled crash, silent wrong result, or OOM exception.

### 3. Defensive Hardening
The Blue-Team Defender introduces minimal, surgical guards:
- Pre-condition assertions and explicit input sanitization (`ValueError` with clear diagnostics).
- Epsilon regularization ($\epsilon \mathbf{I}$) on singular matrices to prevent division-by-zero or non-invertible operators.
- Sparse matrix representations or anchor sampling when matrix size threatens memory limits.

### 4. Regression & Robustness Verification
- Run the full test suite (`pytest tests/`) to ensure legitimate inputs behave identically and no pre-existing benchmarks regressed.
- Run the new adversarial test case to confirm it now passes or fails gracefully with a handled exception.

### 5. Log & Diff Audit
Record the attack vector, reproduction script, and defensive remediation in `prompts/antigravity/logs/`.
