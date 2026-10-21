# Loop: Systematic Component Ablation & Hypothesis Verification

Use this loop to rigorously verify scientific hypotheses ($H_1, H_2, \dots$) by isolating individual algorithmic modules and measuring performance degradation when components are ablated.

---

## Operating Budget & Setup
- **Maximum Iterations:** 5 iterations per run.
- **Assigned Subagent Personas:**
  - `Hypothesis Evaluator (roo_ask / Domain Specialist)`: Formulates ablation variants and defines null hypotheses.
  - `Experimentalist (roo_coder)`: Implements modular toggle flags and executes benchmarking sweeps across seeds.
  - `Statistical Analyst (roo_reviewer)`: Analyzes metric drops, computes p-values/confidence intervals, and verifies statistical significance.

---

## Iteration Protocol

### 1. Component Isolation & Null Hypothesis
Select one core architectural component to ablate:
- **Variant A (Full Proposed System):** Complete algorithm with all enhancements enabled.
- **Variant B (Ablated Component):** Algorithm with the target module disabled, bypassed, or replaced with a naive baseline (e.g., identity weighting, uniform sampling, or uncalibrated gating).
- **Hypothesis Check:** What is the predicted empirical degradation? (e.g., "Removing anchor-fidelity gating decreases ARI by $\ge 0.05$ on noisy manifolds").

### 2. Multi-Seed Replication Run
- Run both variants across a minimum of $5-10$ independent random seeds over identical benchmark splits.
- Capture raw metric matrices (ARI, NMI, runtime, memory).
- Ensure baseline comparators and ablation variants share identical random seeds to eliminate variance confounding.

### 3. Statistical Significance Testing
- Compute paired difference tests (paired Wilcoxon signed-rank test or paired t-test):
  $$t = \frac{\bar{d}}{s_d / \sqrt{n}}$$
- Verify whether the component provides a statistically significant improvement at $\alpha = 0.05$.

### 4. Waterfall & Table Generation
- Automatically emit ablation delta tables (`results/exp2_ablation/`):
  - Component contribution ($\Delta \text{ARI}$, $\Delta \text{NMI}$).
  - Waterfall chart data and LaTeX tabular rows.

### 5. Termination & Evidence Audit
Log the outcome: confirm whether the hypothesis was **supported**, **partially supported**, or **falsified**. Never hide negative results—document anomalies honestly.
