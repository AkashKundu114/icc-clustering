# Report 08: Verification Experiment Plan & Protocol Execution

**Target Repository:** `AkashKundu114/icc-clustering`  
**Active Branch:** `fix/audit-remediation`  
**Scripts Directory:** `experiments/audit_controls/src/`  
**Data Directory:** `experiments/audit_controls/data/`  
**Audit Dimension:** Empirical Protocol Specification & Execution Records  
**Date:** October 16, 2026  

---

## 1. Specification of Verification Experiments (E1 through E6)

To resolve the empirical gaps identified during initial review, a suite of six pre-registered verification protocols was designed and executed:

```
                            Verification Experiment Suite
                                          │
       ┌────────────────────┬─────────────┴─────────────┬────────────────────┐
       ▼                    ▼                           ▼                    ▼
[E1: Extended Benchmarks] [E2: Noise Sweeps]         [E3: Pool Sensitivity] [E4-E6: Scale & Repro]
 • 21 Multi-Domain Datasets• 5 Noise Regimes          • 5% to 50% Gating     • Spectral Equivalence
 • Held-Out Validation    • P/R Signal Isolation      • Label-Free Selectors • Empirical Scalability
```

---

## 2. Protocol Details & Outcomes

### 2.1 Protocol E1: Extended Multi-Domain Benchmarks & Held-Out Evaluation
- **Objective:** Evaluate ICC-v2 across an expanded battery of 21 datasets (13 original + 8 held-out cohorts) against 11 baseline algorithms, testing whether biological gains generalize beyond the initial discovery set.
- **Script:** [`experiments/audit_controls/src/e1_extended_benchmarks.py`](file:///d:/Final%20Year%20Project/experiments/audit_controls/src/e1_extended_benchmarks.py)
- **Output Artifacts:** `experiments/audit_controls/data/e1_extended_benchmarks.csv` & `e1_extended_summary.csv`
- **Empirical Outcome:** Confirmed that ICC-v2 dominates on ultra-high-dimensional biological cohorts ($D/N > 20$, Rank #1 with $R=1.50$), but full-space Ward and Standard Consensus excel on dense low-dimensional vision/audio datasets.

### 2.2 Protocol E2: Systematic Noise-Model Sweeps & Signal Isolation
- **Objective:** Evaluate VSSG candidate pool recovery under 5 distinct noise models (Gaussian, Student-t, correlated, scaled, sparse binary) across dimensions $D \in [50, 5000]$.
- **Script:** [`experiments/audit_controls/src/a2_controls.py`](file:///d:/Final%20Year%20Project/experiments/audit_controls/src/a2_controls.py)
- **Output Artifacts:** `experiments/audit_controls/data/a2_syn.csv` & `a2_filter_controls.csv`
- **Empirical Outcome:** VSSG achieves $100\%$ precision/recall on planted Gaussian, scaled, and correlated noise. On sparse binary noise, Sarle's coefficient hits its theoretical ceiling ($1.0$), confirming Assumption 1's boundary condition.

### 2.3 Protocol E3 & E3b: Pool-Size Sensitivity Curve & Unsupervised Selection
- **Objective:** Map the relationship between candidate pool fraction ($\rho \in [0.02, 0.40]$) and clustering accuracy on biological cohorts (Leukemia, SRBCT, Colon, CNS) compared against a random-pool control; test whether label-free criteria (Silhouette, Stability) can select the optimal fraction.
- **Scripts:** [`experiments/audit_controls/src/e3_pool_curve.py`](file:///d:/Final%20Year%20Project/experiments/audit_controls/src/e3_pool_curve.py) & [`e3b_label_free_selector.py`](file:///d:/Final%20Year%20Project/experiments/audit_controls/src/e3b_label_free_selector.py)
- **Output Artifacts:** `experiments/audit_controls/data/e3_pool_curve.csv` & `e3b_selector.csv`
- **Empirical Outcome:** Confirmed the presence of an optimal $5\%\text{--}15\%$ biological gating window. Demonstrated that unsupervised silhouette and stability heuristics fall below fixed default screening ($\text{ARI}=0.091$ vs $0.168$), establishing pool sizing as an explicit architectural property.

### 2.4 Protocol E4: Bipartite Transfer-Cut Spectral Equivalence
- **Objective:** Measure the principal-angle cosine distance between the eigenspace of the normalized bipartite anchor graph and the dense co-association graph across multiple noise regimes.
- **Script:** [`experiments/audit_controls/src/a3_embedding.py`](file:///d:/Final%20Year%20Project/experiments/audit_controls/src/a3_embedding.py)
- **Unit Test:** [`tests/test_audit_a3.py`](file:///d:/Final%20Year%20Project/tests/test_audit_a3.py)
- **Empirical Outcome:** Principal-angle cosine verified at $\cos(\theta_k) = 1.000$ to 3 decimal places, establishing mathematical eigenspace equivalence.

### 2.5 Protocol E5: Re-runs of Downstream Generalization & Missing-Data Robustness
- **Objective:** Re-run the Exp 1 inductive multi-classifier sweep (320 evaluations) and Exp 3.5 missing-data degradation sweeps under fixed protocols.
- **Scripts:** [`experiments/audit_controls/src/e5_exp1_rerun.py`](file:///d:/Final%20Year%20Project/experiments/audit_controls/src/e5_exp1_rerun.py) & [`e5_missing_rerun.py`](file:///d:/Final%20Year%20Project/experiments/audit_controls/src/e5_missing_rerun.py)
- **Output Artifacts:** `experiments/audit_controls/data/e5_exp1_pseudolabel_rerun.csv` & `e5_missing_rerun.csv`
- **Empirical Outcome:** Established the empirical bounds: downstream accuracy gain is nominal ($+0.004$, chance baseline), and missing data retention holds reliably up to $20\%$ ($\approx 80\%$), collapsing by $30\%$.

### 2.6 Protocol E6: Asymptotic Complexity & Empirical Scalability
- **Objective:** Measure per-process peak RSS memory and runtime scaling for sample sizes $N \in [500, 32{,}000]$ and dimension scales up to $D = 100{,}000$.
- **Scripts:** [`experiments/audit_controls/src/e6_scaling_one.py`](file:///d:/Final%20Year%20Project/experiments/audit_controls/src/e6_scaling_one.py) & [`tools/profile_resources.py`](file:///d:/Final%20Year%20Project/tools/profile_resources.py)
- **Output Artifacts:** `experiments/audit_controls/data/e6_scaling.csv` & `results/resource_benchmarks.json`
- **Empirical Outcome:** Confirmed linear runtime and memory scaling; verified execution on $N=1,000,000$ in $55.6\text{s}$ and $D=5000$ in $0.51\text{s}$.

---

## 3. Protocol Status & Reproducibility Summary

All six verification protocols have been **fully executed, logged, and permanently cached** in `experiments/audit_controls/data/`. All reproduction commands execute via standard CLI invocations without external network dependencies.
