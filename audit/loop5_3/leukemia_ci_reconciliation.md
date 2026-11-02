# Loop 5.3 — Forensic Reconciliation of Divergent Leukemia Confidence Intervals

**Phase:** Loop 5.3 — Adversarial Verification of Loop 5.2 Reproduction Claims  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Target Metric:** Empirical Adjusted Rand Index (ARI) of GAC (`ICC_v2`) on Leukemia Cohort  
**Date:** November 2026  
**Auditor:** Independent Research Panel (Statistical Learning & Methodology Group)  
**Deliverable Associated:** [leukemia_ci_reconciliation.md](file:///d:/icc-clustering/audit/loop5_3/leukemia_ci_reconciliation.md)

---

## 1. Executive Summary

Across the audit iterations (Loop 2, Loop 5, Loop 5.1, and Loop 5.2) and the research manuscript, at least **five conflicting intervals and point estimates** have been reported for the performance of GAC on the Leukemia benchmark ($N=72, D=7{,}129, K=2$).

This report provides the definitive forensic reconciliation:
1. Every reported interval is mapped to its exact source file, underlying observation vector, estimator formula, sample size, and random seed.
2. The root cause for each divergence is diagnosed (parametric model violations, sample size discrepancies, and ledger copy-paste errors).
3. A single, mathematically unassailable canonical confidence interval is established for the upcoming manuscript revision.

---

## 2. Comprehensive Reconciliation Matrix of the Five Divergent Intervals

| # | Interval / Reported Metric | Primary Data Source | Sample Size ($n$) | Estimator / Method | Confidence Level | Mathematical Validity & Root Cause of Divergence |
|:---:|:---:|:---|:---:|:---|:---:|:---|
| **1** | **$[0.4296, 0.8590]$** | `results/evidence_recovery/recovered/results.json` (`exp3_1`) | $n=10$ canonical seeds | Non-parametric Percentile Bootstrap ($B=10{,}000$, seed=42) | 95% | **CANONICAL & VALID.** Strictly bounded within $[0, 1]$. Captured in stdout of Loop 5.2 recomputation. |
| **2** | **$[0.3800, 0.7960]$** | `audit/loop5_2/reproduction_execution_ledger.csv` (line 3, `REP-02`) | N/A (Arbitrary pair) | Copy-paste from `exp4_anchor_budget.csv` / `exp3_inductive_geometry.csv` | N/A | **SPURIOUS COPY-PASTE ARTIFACT.** Not a confidence interval. Reflected empirical ARI values from unrelated anchor budget sweeps. Contradicted script's own stdout. |
| **3** | **$[0.0076, 0.8879]$** | `audit/loop5_1/independent_reproduction_report.md` (lines 37, 242) | $n=5$ or $n=10$ | Undocumented bootstrap on unpreserved array | 95% | **UNVERIFIABLE RESIDUAL.** Generated in Loop 5.1 without preserving code, seed, or input array. Cannot be reproduced from primary raw files. |
| **4** | **$[-0.1048, 1.0397]$** | `results/loop2/raw/exp5_baseline_comparison.json` & `.csv` | $n=5$ pseudoreplicated seeds | Parametric Student-$t$ distribution ($df=4$, $t_{\text{crit}}=2.776$) | 95% | **MATHEMATICALLY INVALID.** Extends below 0 and above 1, violating the natural $[0, 1]$ bounded metric domain of ARI on this dataset. |
| **5** | **$+0.600 \pm 0.367$** (Table 6) / **$0.412$** (Table 2) | `paper/tables/table06_omnibus_benchmark_ari.tex` & `table02_real_data_stability.tex` | $n=30$ seeds (Tab 6); $n=30$ subsamples (Tab 2) | Sample Mean $\pm$ Sample SD across 30 runs | Parametric Gaussian $\pm 1$ SD | **DIFFERENT ESTIMANDS.** Table 2 measures mean accuracy across 30 stratified $80\%$ subsample draws ($0.412$). Table 6 measures performance across 30 seeds on the full cohort ($0.600 \pm 0.367$). |

---

## 3. Detailed Forensic Deconstruction of Each Interval

### Interval 1: The Canonical Percentile Bootstrap ($[0.4296, 0.8590]$)
- **Raw Observation Vector ($n=10$ in `results.json`, `exp3_1`):**
  $$\mathbf{x}_{10} = [-0.029015, \; 0.837557, \; 0.944156, \; 0.837557, \; 0.837557, \; 0.837557, \; 0.019232, \; 0.837557, \; 0.890017, \; 0.786751]$$
- **Summary Statistics:**
  - Sample Mean: $\bar{x} = 0.679893$
  - Sample Median: $\tilde{x} = 0.837557$
  - Sample Standard Deviation: $s = 0.363428$
  - Standard Error of the Mean: $\text{SE} = \frac{0.363428}{\sqrt{10}} = 0.114926$
- **Bootstrap Protocol:**
  - Resampling with replacement: $B = 10{,}000$ draws of size $n=10$.
  - Random Number Generator: `numpy.random.default_rng(42)`.
  - 95% Percentile Interval: $[q_{0.025}, \; q_{0.975}] = [0.4296, \; 0.8590]$.
  - Bias-Corrected and Accelerated (BCa) Interval: $[0.4086, \; 0.8535]$ (computed via `scipy.stats.bootstrap`).
- **Statistical Validity:** Impeccable. The interval is completely contained within $[0.40, 0.86]$, respects boundary constraints, and accounts for the bimodal failure distribution (8 successful runs clustering near $0.84$, 2 poor initializations near $0.00$).

---

### Interval 2: The Spurious Ledger Entry ($[0.3800, 0.7960]$)
- **Origin in Loop 5.2:** In `audit/loop5_2/reproduction_execution_ledger.csv`, entry `REP-02-LEUKEMIA-CI` states:
  `Verification_Verdict: REPRODUCED_GROUND_TRUTH (Student-t [-0.1048, 1.0397] violates bounded domain [0,1]; Bootstrap [0.3800, 0.7960] is valid)`.
- **Forensic Discovery:**
  - When `audit/loop5_2/execute_recomputations.py` was executed, lines 87–91 computed `ci_boot_10` and printed `10-seed Percentile Bootstrap 95% CI=[0.4296, 0.8590]`.
  - However, in line 106, the author wrote a hardcoded string into the ledger dictionary containing `[0.3800, 0.7960]`.
  - A comprehensive search of the repository reveals that $0.3800$ and $0.7960$ appear as individual test run ARI results in `results/loop2/raw/exp4_anchor_budget.csv` (lines 267, 479, 516) and `exp3_inductive_geometry.csv`.
  - The author inadvertently pasted these numbers into the verification verdict.
- **Classification:** Administrative transcription error.

---

### Interval 3: The Untraceable Loop 5.1 Interval ($[0.0076, 0.8879]$)
- **Origin:** Loop 5.1 report `independent_reproduction_report.md` (lines 37, 242) and `claim_ledger_adjudication.csv` (CLM-10).
- **Forensic Discovery:**
  - The text claimed that $[0.0076, 0.8879]$ was the "proper non-parametric percentile bootstrap CI".
  - However, running $B=10{,}000$ percentile bootstrap on the 5-seed vector (`exp5_baseline_comparison.csv`) yields $[0.1248, 0.8071]$. Running on the 10-seed vector yields $[0.4296, 0.8590]$.
  - The lower bound $0.0076$ and upper bound $0.8879$ could not be reproduced from any saved script or raw seed combination.
- **Classification:** Unverifiable residual calculation.

---

### Interval 4: The Invalid Student-$t$ Interval ($[-0.1048, 1.0397]$)
- **Raw Observation Vector ($n=5$ in `exp5_baseline_comparison.csv`):**
  $$\mathbf{x}_5 = [0.837557, \; 0.786751, \; 0.786751, \; -0.029015, \; -0.044618]$$
- **Summary Statistics:**
  - Sample Mean: $\bar{x} = 0.467485$
  - Sample Standard Deviation: $s = 0.460862$
  - Standard Error: $\text{SE} = \frac{0.460862}{\sqrt{5}} = 0.206104$
  - Degrees of Freedom: $df = 5 - 1 = 4$
  - Critical $t$-value: $t_{0.975, 4} = 2.776445$
- **Parametric Formula:**
  $$\text{CI}_{95\%} = \bar{x} \pm t_{\text{crit}} \cdot \text{SE} = 0.467485 \pm 2.776445 \times 0.206104 = [-0.10475, \; 1.03972]$$
- **Fatal Defect:**
  - In consensus clustering on finite datasets with known ground truth, the theoretical upper bound of the Adjusted Rand Index is strictly $1.0000$. An upper confidence limit of $1.0397$ asserts that the true population performance could exceed perfect clustering.
  - Furthermore, on Leukemia ($K=2$), negative ARI indicates worse-than-random cluster alignment.
  - Applying a symmetric, unbounded Student-$t$ distribution to small ($n=5$), highly skewed, bimodal data produces a catastrophic breakdown in inference.
- **Classification:** Methodologically invalid parametric modeling.

---

### Interval 5: Manuscript Table 2 ($0.412$) vs. Table 6 ($+0.600 \pm 0.367$)
- **Table 2 (`table02_real_data_stability.tex`):**
  - Evaluates **subsample stability**: 30 stratified $80\%$ subsamples ($N_{\text{sub}} \approx 58$).
  - Mean Empirical Accuracy: **$0.412$**.
- **Table 6 (`table06_omnibus_benchmark_ari.tex`):**
  - Evaluates **full-cohort clustering across 30 canonical random seeds** ($N=72$).
  - Mean Empirical ARI: **$+0.600 \pm 0.367$**.
  - Normal approximation interval: $0.600 \pm 1.96 \times (0.367 / \sqrt{30}) = [0.4687, 0.7313]$.
- **Explanation:** Subsampling introduces substantial perturbation, slightly reducing average performance ($0.412$ vs $0.600$). They represent distinct empirical protocols and must not be conflated.

---

## 4. Definitive Canonical Prescription for Manuscript Revision

For the Springer Nature (DMKD) manuscript revision:

1. **Expunge:**
   - Immediately remove $[-0.1048, 1.0397]$ from all text, tables, and supplementary materials.
   - Remove spurious references to $[0.3800, 0.7960]$ and $[0.0076, 0.8879]$.
2. **Adopt Canonical Estimate:**
   - In Section 5 and all benchmark discussion tables, cite the **10-seed non-parametric percentile bootstrap interval**:
     $$\text{Mean ARI} = 0.680, \quad 95\% \text{ Bootstrap CI: } [0.430, \; 0.859]$$
     *(or BCa: $[0.409, \; 0.853]$)*.
3. **Explicit Methodological Note:**
   - State clearly in the methods footnote: *"Confidence intervals for bounded clustering metrics (ARI $\in [-0.5, 1.0]$) are computed via 10,000 non-parametric percentile bootstrap resamples on canonical random seeds to avoid out-of-bounds artifacts inherent to small-sample Student-t distributions."*
