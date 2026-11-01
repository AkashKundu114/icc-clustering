# Multiplicity Family Specification and Error Control Plan (v2.1-RECONCILED)

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Document Reference:** `SPEC-MULTIPLICITY-v2.1`  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Branch:** `research/dami-revision`  
**Date:** November 1, 2026  
**Status:** Post-Audit Reconciled Protocol Specification (Incorporating Independent Audits)  

---

## 1. Principles of Inferential Partitioning

In complex machine learning benchmarks involving multi-algorithm grids, architectural knockouts, and exploratory data mining, uncorrected hypothesis testing leads to severe alpha inflation. Evaluating multiple algorithms or component variants without a locked family structure enables post-hoc cherry-picking.

To enforce strict Type I error rate control while preserving statistical power, this protocol partitions all confirmatory statistical tests into **distinct, non-overlapping inferential families** based on their scientific domain, stratum hierarchy, and decision impact.

### 1.1 Inferential Demarcation Matrix

| Family ID | Family Name | Primary Scientific Objective | Number of Tests ($M$) | Primary Error Metric | Multiple Testing Procedure |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Family 1** | **Primary Comparative Baselines** | Confirm superiority of Full ICC-v2 over competitive clustering pipelines | **8** | FWER ($\alpha = 0.05$) | Holm–Bonferroni Step-Down |
| **Family 2** | **Architectural Attribution** | Disentangle BGSS gating, dense attenuation, and anchor determinacy | **3** | FWER ($\alpha = 0.05$) | Holm–Bonferroni Step-Down |
| **Family 3** | **Methodological Claims** | Establish stability–accuracy decoupling and discordance gap | **2** | FWER ($\alpha = 0.05$) | Fixed-Sequence / Bonferroni-Holm |
| **Family 4** | **Sensitivity & Robustness** | Preprocessing, parameter sweeps, and LOCO leave-out checks | N/A | Exploratory | Nominal $p$-values labeled descriptive |

---

## 2. Family 1: Primary Comparative Baseline Family ($M = 8$)

### 2.1 Scope, Stratum Hierarchy, and Composition
Family 1 governs the primary benchmark claims of Full ICC-v2 against the eight competitive baselines:
- **Primary Stratum ($J_{\text{Tier A}} = 10$):** High-dimensional intrinsic tumor subtyping (B1 ground truth: GSE62254, GSE39582, GSE31210, GSE13159, GSE10846, GSE42568, GSE19188, GSE21653, GSE32894, GSE49710).
- **Secondary Stratum ($J_{\text{Total}} = 15$):** Combines Tier A with the 5 Tier B general/anatomical cohorts (GSE14520, GSE25066, GSE2034, GSE72094, GSE14333).

#### The Eight Evaluated Comparisons:
1. `BM-01`: Full ICC-v2 vs. Ambient Standard Consensus (`StdCons_All`)
2. `BM-02`: Full ICC-v2 vs. Ambient K-Means (`K-Means_All`)
3. `BM-03`: Full ICC-v2 vs. Variance-Filtered K-Means (`K-Means_VarFilt`)
4. `BM-04`: Full ICC-v2 vs. PCA K-Means (`K-Means_PCA`)
5. `BM-05`: Full ICC-v2 vs. Laplacian Score K-Means (`K-Means_LapScore`)
6. `BM-06`: Full ICC-v2 vs. Sparse K-Means (`SparseKMeans`)
7. `BM-07`: Full ICC-v2 vs. Fast Consensus Anchor Graph Spectral Baseline (`FCAG`)
8. `BM-08`: Full ICC-v2 vs. Multi-View Consensus Proxy (`FastMVC-Surrogate`)

### 2.2 Error Control: Holm–Bonferroni Step-Down Procedure
The Family-Wise Error Rate (FWER) is controlled at strong level $\alpha = 0.05$:

1. For each comparison $m \in \{1, \dots, 8\}$, compute the two-sided paired Wilcoxon signed-rank test $p$-value $p_m$ across cohort median ARIs.
2. Sort raw $p$-values in ascending order:
   $$p_{(1)} \le p_{(2)} \le p_{(3)} \le p_{(4)} \le p_{(5)} \le p_{(6)} \le p_{(7)} \le p_{(8)}$$
3. Step-down alpha thresholds:
   $$\alpha_{(k)} = \frac{\alpha}{8 - k + 1}, \quad k \in \{1, \dots, 8\}$$
   - $\alpha_{(1)} = \frac{0.05}{8} = \mathbf{0.006250}$
   - $\alpha_{(2)} = \frac{0.05}{7} \approx \mathbf{0.007143}$
   - $\alpha_{(3)} = \frac{0.05}{6} \approx \mathbf{0.008333}$
   - $\alpha_{(4)} = \frac{0.05}{5} = \mathbf{0.010000}$
   - $\alpha_{(5)} = \frac{0.05}{4} = \mathbf{0.012500}$
   - $\alpha_{(6)} = \frac{0.05}{3} \approx \mathbf{0.016667}$
   - $\alpha_{(7)} = \frac{0.05}{2} = \mathbf{0.025000}$
   - $\alpha_{(8)} = \frac{0.05}{1} = \mathbf{0.050000}$
4. Adjusted $p$-values:
   $$p_{\text{adj}, (k)} = \max_{i \le k} \min\left(1.0, (8 - i + 1) p_{(i)}\right)$$
5. **Binding Directional Superiority Rule:**  
   Rejecting a two-sided test indicates only non-zero difference ($\Delta \ne 0$). Full ICC-v2 is confirmed superior to Baseline $m$ if and only if:
   $$p_{\text{adj}, (m)} < 0.05 \quad \text{AND} \quad \text{Median}(D_{\text{BM}-m}) > 0$$

---

## 3. Family 2: Architectural Component Attribution Family ($M = 3$)

### 3.1 Scope and Scientific Role
Family 2 isolates the architectural drivers of the proposed pipeline:
1. `H2a`: **BGSS Gating Superiority over Matched Random Gating under Bipartite Consensus.**
   - Null: $\Delta_{\text{BGSS, Bip}} \le 0$; Direction: One-sided ($>0$). Primary on Tier A ($J=10$); secondary on Pooled ($J=15$).
2. `H2b`: **Dense-Consensus Attenuation Interaction.**
   - Null: $\Delta_{\text{attenuation}} \le 0$; Direction: One-sided ($>0$). Note: Severe power limitation ($<35\%$).
3. `H3`: **Core Determinacy Anchor Equivalence via TOST.**
   - Equivalence margin: $[-\delta, +\delta] = [-0.02, +0.02]$.
   - Test: Two One-Sided Tests (TOST) paired Wilcoxon / $t$-test.
   - TOST $p$-value is defined as $p_{\text{TOST}} = \max(p_{\text{lower}}, p_{\text{upper}})$.

### 3.2 Error Control and Confidence Interval Duality
1. Step-down thresholds across $M=3$ tests:
   - $\alpha_{(1)} = \frac{0.05}{3} \approx \mathbf{0.016667}$
   - $\alpha_{(2)} = \frac{0.05}{2} = \mathbf{0.025000}$
   - $\alpha_{(3)} = \frac{0.05}{1} = \mathbf{0.050000}$
2. Adjusted $p$-values: $p_{\text{adj}, (k)} = \max_{i \le k} \min\left(1.0, (3 - i + 1) p_{(i)}\right)$.
3. **Equivalence Decision Standards (H3):**
   - The primary operational standard for certifying equivalence within $[-\delta, +\delta] = [-0.02, +0.02]$ is the **$90\%$ bootstrap confidence interval** (dual to two one-sided tests at $\alpha = 0.05$).
   - If evaluated under Holm-adjusted threshold $\alpha_{(k)}$, the formal dual confidence interval is $100(1 - 2\alpha_{(k)})\%$ (up to $96.67\%$).
   - If the interval overlaps $-0.02$ or $+0.02$, the outcome is declared **INCONCLUSIVE**, and claiming an empirical null is strictly prohibited.

---

## 4. Family 3: Methodological Claims Family ($M = 2$)

### 4.1 Scope and Scientific Role
1. `H1a`: **Stability–Accuracy Decoupling.**
   - Tests whether algorithmic stability fails to predict clustering accuracy ($\rho < 0.30$ vs. $\rho \ge 0.50$).
   - One-sample Wilcoxon signed-rank test on Fisher $z$-transformed per-cohort Spearman correlations $\{z(\hat{\rho}_j)\}_{j=1}^J$. Pairwise deletion applied for aborted runs ($|\mathcal{M}_j| \ge 6$).
2. `H1b`: **Stability-Minus-Accuracy False Confidence Gap.**
   - Tests whether stability substantially exceeds empirical accuracy across non-degenerate partitions ($\Delta_{\text{gap}} > 0.20$ vs. $\Delta_{\text{gap}} \le 0.05$).
   - One-sample Wilcoxon signed-rank test on cohort-level mean gaps $\{\bar{\Delta}_j\}_{j=1}^J$.

### 4.2 Error Control: Fixed-Sequence Hierarchical Testing
1. Test H1a at nominal level $\alpha = 0.05$.
2. If and only if H1a rejects $H_{0,1\text{a}}$, proceed to test H1b at nominal level $\alpha = 0.05$.
3. If H1a fails to reject, H1b is not formally confirmed and is treated as exploratory.

---

## 5. Family 4: Sensitivity, Robustness, and Exploratory Grid (Descriptive)

The following analyses are designated as exploratory/sensitivity evaluations and do not incur multiplicity penalties:
- Preprocessing transformation ablations (E3: raw, $\log_2$, standardization, quantile normalization).
- Rule (i') cutoff grid scans (varying non-degeneracy minimum cluster thresholds from $1\%$ to $10\%$).
- Ensemble hyperparameter sweeps (varying $M \in \{5, 10, 15, 25, 50\}$ and $L \in \{20, 40, 60, 80\}$).
- Leave-One-Cohort-Out (LOCO) sensitivity trajectories.

All findings in Family 4 must be explicitly reported as **descriptive sensitivity analyses** rather than confirmatory discoveries.

---

## 6. Pseudoreplication Safeguards Across Nested Observations

1. **Algorithmic Seeds ($S=30$):** Seeds represent numerical solver initializations, NOT independent biological units. In all inferential families, seed results are collapsed to the **within-cohort median scalar** prior to entering hypothesis tests.
2. **Multiple Methods within Cohorts (H1a/H1b):** In H1a, correlation $\hat{\rho}_j$ is computed within each cohort first, yielding $J=15$ independent correlation values. In H1b, gaps are averaged within cohort across methods, yielding $J=15$ independent cohort gaps $\bar{\Delta}_j$.
3. **Clustered Bootstrap Resampling:** Bootstrap confidence intervals resample whole cohorts with replacement ($B = 10{,}000$), strictly preserving cohort independence.