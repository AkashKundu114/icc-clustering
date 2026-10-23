# Goal: Baseline Fairness, Tuning Parity & Statistical Significance Audit

Deploy this goal to eliminate benchmark bias, prevent strawman comparator implementations, and verify statistical rigor across all experimental evaluations.

---

## Assigned Subagent Personas
1. **Methodological Auditor (`roo_reviewer`)**: Scrutinizes baseline algorithms, parameter sweeps, and objective evaluation parity.
2. **Statistical Testing Specialist (`roo_ask`)**: Executes multi-dataset non-parametric hypothesis tests (Friedman, Nemenyi CD, Wilcoxon signed-rank).
3. **Benchmark Engineer (`roo_coder`)**: Standardizes input interfaces and harmonizes execution seeds.

---

## Audit Checklist & Fairness Rules

### 1. Baseline Implementation Parity
- **Non-Degenerate Configurations:** Ensure baseline models are not crippled with inadequate iterations, suboptimal defaults, or inappropriate distance metrics.
- **Fair Preprocessing:** If the proposed method receives dimension-reduced or normalized features, ensure baseline methods are evaluated on identical preprocessed inputs.
- **Tuning Budget Equality:** Give baselines equal hyperparameter search budgets (e.g. grid search / cross-validation iterations).

### 2. Multi-Seed Replication
- Single-seed evaluation is strictly prohibited for non-deterministic algorithms (e.g., $k$-means random initializations, neural embeddings).
- All reported metric points (ARI, NMI, ACC) must report sample means and standard deviations over at least $10$ independent random seeds:
  $$\mu \pm \sigma \quad \text{or} \quad \text{95\% Confidence Intervals}$$

### 3. Rigorous Statistical Significance
- For multiple datasets across competing algorithms:
  - Run the **Friedman test** across all benchmarks to establish rank differences:
    $$F_F = \frac{(N-1)\chi_F^2}{N(k-1) - \chi_F^2}$$
  - If $p < 0.05$, compute the **Nemenyi Critical Difference (CD)**:
    $$CD = q_\alpha \sqrt{\frac{k(k+1)}{6N}}$$
  - Produce critical difference diagrams and radar plots verifying significant outperformance boundaries.
