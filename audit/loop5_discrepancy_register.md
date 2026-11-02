# Loop 5: Discrepancy Register and Conflict Adjudication

**Author:** Lead Scientific Auditor & Principal Review Adjudicator  
**Adjudication Date:** November 2, 2026  
**Repository:** `AkashKundu114/icc-clustering` (`D:\icc-clustering`)  
**Target Manuscript:** `paper/manuscript/main.tex`  

---

## Executive Summary

This register formally adjudicates the ten mandatory discrepancy items (D1 through D10) identified across Loops 0 through 4. It synthesizes findings from Agent A (Provenance), Agent B (Theory), Agent C (Statistics), Agent D (Manuscript), and Agent E (Falsification), establishing definitive, mathematically grounded resolutions.

---

## 1. Item-by-Item Discrepancy Adjudications

### D1: Experiment Suite Identity (Loop 2 vs. Loop 4 / Manuscript)
- **The Discrepancy:** Loop 2 reports an adversarial evaluation across 10 datasets, 8 methods, and 5 seeds (400 runs). Loop 4 / Manuscript reports an omnibus evaluation across 13 datasets, 12 pipelines, and 3,000 model fits. In Loop 4 Claim 21, the author cited `results/loop2/raw/exp5_benchmark_suite.csv` as the raw evidence for Table 6, and claimed GAC ranked 1st with mean ARI = 0.320.
- **Forensic Resolution:**
  1. The two experiment suites are completely distinct physical entities designed for different purposes:
     - **Suite 1 (Omnibus Benchmark):** Executed during the primary benchmarking phase, recorded in `results/evidence_recovery/recovered/results.json` (`exp3_1`, 3,430 total records) and `stats.json`. Evaluates 13 real-world datasets across 12 clustering pipelines and 30/10 seeds (3,000 fits). Forms the exact basis of Table 6 in `main.tex`.
     - **Suite 2 (Adversarial Stress Test):** Executed in Loop 2, recorded in `results/loop2/raw/exp5_baseline_comparison.csv` (400 runs) and `.json`. Evaluates 10 datasets (including synthetic manifolds `two_moons` and `concentric_circles`) across 8 algorithms and 5 seeds.
  2. The citation in Loop 4 Claim 21 was an internal reporting error. The path `exp5_benchmark_suite.csv` was a conflated name.
  3. The claim that GAC achieved mean ARI = 0.320 ranking 1st across 13 datasets is **CONTRADICTED**. GAC's grand mean ARI across all 13 benchmarks is **0.152** with an omnibus rank of **5.62** (ranking 4th behind K-Means 5.15, DEC 5.23, and Standard Consensus 5.23, Friedman $p = 0.40$). The mean of **0.217** and 1st rank (**2.17**) apply strictly to the 6 high-$D$ microarray cohorts (`HighD_N6`).
- **Disposition:** Reconciled. The manuscript correctly reports Table 6; the erroneous Loop 4 claim is formally withdrawn.

---

### D2: Manuscript Availability and Local vs. Remote Git Tracking
- **The Discrepancy:** Are `paper/` and `results/` tracked in Git, ignored, or missing? Can an external researcher reproduce the paper from the public repository?
- **Forensic Resolution:**
  1. `paper/` (226 files) and `results/` (130 files) exist locally on disk and match all cryptographic manifests (`02_manuscript_asset_manifest.csv` and `artifact_manifest.csv`) with 100% precision.
  2. However, both directories are actively ignored by `.gitignore` (`/results/` on line 2, `paper/` on line 102). Consequently, they are **NOT tracked in the GitHub remote repository**.
  3. A researcher cloning `https://github.com/AkashKundu114/icc-clustering.git` will receive the complete source code (`src/`), tests, scripts, and audit reports, but `paper/` and `results/` will be empty.
- **Disposition:** Reconciled. The authors must ensure the raw results archive and manuscript source are hosted on Zenodo (as declared in the manuscript's Data Availability section).

---

### D3: SRBCT and Factorial Wilcoxon P-Value Clarifications
- **The Discrepancy:** Loop 2 reports SRBCT with 5 seeds, 5 wins, and $p = 0.03125$. Loop 4 reports a factorial result on $n = 6$ cohorts with $p = 0.031$. Are these one-sided or two-sided p-values? Do they survive multiple testing?
- **Forensic Resolution:**
  1. **Loop 2 SRBCT ($n = 5$ seeds):** The exact probability of 5 positive ranks under $H_0$ is $(1/2)^5 = 1/32 = 0.03125$. This is strictly a **one-sided p-value**. The standard **two-sided p-value is $2 \times (1/32) = 0.0625$**, which does not reach statistical significance at $\alpha = 0.05$. Furthermore, testing across 5 seeds on a single dataset represents seed pseudoreplication.
  2. **Loop 4 Factorial ($n = 6$ cohorts):** For $n = 6$ cohorts, if a method wins on all 6 cohorts ($W = 0$), the exact two-sided p-value is $2 \times (1/2)^6 = 2/64 = 0.03125 \approx 0.031$. This is indeed a valid two-sided test on independent biological cohorts.
  3. However, across the 3 factorial comparisons, Bonferroni correction yields $p_{\text{adj}} = 3 \times 0.03125 = 0.0938 > 0.05$. Across the 11 baseline comparisons in `stats.json`, Holm-Bonferroni correction yields $p_{\text{adj}} \ge 0.25$.
- **Disposition:** Reconciled. All p-values must be explicitly labeled as one-sided or two-sided, and the uncorrected nature of the factorial p-value must be maintained.

---

### D4: Bounded Metric Violations in Confidence Intervals
- **The Discrepancy:** In `results/loop2/raw/exp5_baseline_comparison.json`, ICC-v2 on Leukemia is assigned an ARI confidence interval of `[-0.1048, 1.0397]`.
- **Forensic Resolution:**
  1. This interval was produced by blindly evaluating a Student-t formula ($\bar{x} \pm t_{0.025, 4} \cdot \frac{s}{\sqrt{5}}$) on 5 Monte Carlo seeds ($\bar{x} = 0.4675, s = 0.4609, t = 2.7764$).
  2. The Adjusted Rand Index is mathematically bounded by $1.0$. An upper bound of $1.0397$ violates the mathematical support of the metric.
  3. The distribution of ARI across seeds on Leukemia is discretely bimodal (seeds either hit the AML/ALL features and achieve $\approx 0.9$ or miss and get $\approx 0.0$), violently violating the normality assumption.
  4. The valid interval must be computed via non-parametric percentile bootstrapping clipped to $[-1, 1]$, yielding $[0.0076, 0.8879]$.
- **Disposition:** Reconciled. Naive Student-t intervals on bounded clustering metrics are invalid. The manuscript correctly uses clustered bootstrapping across cohorts for Table 2.

---

### D5: Adaptive Anchor Guarantee Under Cluster Imbalance
- **The Discrepancy:** Loop 3 proposed $L^*(K) = \max(40, \lceil 3 K \ln K \rceil)$ as a guarantee for minority cluster coverage.
- **Forensic Resolution:**
  1. The coupon-collector bound $O(K \ln K)$ holds strictly when cluster proportions are perfectly balanced ($\pi_k = 1/K$).
  2. Under arbitrary cluster imbalance with minority proportion $\pi_{\min}$, the probability that a minority cluster receives zero anchors from $L$ uniform draws is $(1 - \pi_{\min})^L$.
  3. For $\pi_{\min} = 0.01$ and $K = 4$, $L^*(4) = 40$ gives a failure probability of $(1 - 0.01)^{40} \approx 66.9\%$.
  4. Guaranteeing minority coverage with failure probability $\le \delta$ requires:
     $$L = \Omega\left(\frac{\ln(K/\delta)}{\pi_{\min}}\right).$$
- **Disposition:** Reconciled. The claim that $3 K \ln K$ provides a general minority coverage guarantee is mathematically false and must not appear in any publication.

---

### D6: Preprocessing Transformations and Symmetry
- **The Discrepancy:** Loop 4 suggested that data standardization or log-transformation guarantees the symmetric density condition required for Proposition 1.
- **Forensic Resolution:**
  1. **Standardization ($z = (x - \mu)/\sigma$) is an affine transformation.** Skewness and kurtosis are strictly scale- and location-invariant. Standardization leaves Sarle's Bimodality Coefficient 100% unchanged!
  2. **Log-transformation ($y = \log(1 + x)$)** reduces right skewness for positive continuous variables, but can induce severe left-skewness if overcorrected, or create a spike at zero in zero-inflated count data (scRNA-seq). It does not guarantee mathematical symmetry.
- **Disposition:** Reconciled. The manuscript must state that Proposition 1 holds for symmetric unimodal distributions, without claiming that standard scalers guarantee symmetry.

---

### D7: Theoretical Consensus Graph Storage vs. Total Process Memory
- **The Discrepancy:** Does GAC require $160\text{ MB}$ at $N = 10^6$, or does it require $3.84\text{ GB}$?
- **Forensic Resolution:**
  1. The auxiliary bipartite consensus graph array $B \in \mathbb{R}^{10^6 \times 40}$ in `float32` requires exactly $10^6 \times 40 \times 4\text{ bytes} = 160.0\text{ MB}$.
  2. Dense consensus would require an $N \times N$ matrix: $10^{12} \times 8\text{ bytes} \approx 8\text{ Terabytes of RAM}$ (impossible on a workstation).
  3. However, total peak process heap memory (measured via `tracemalloc`) reached $3.84\text{ GB}$ during the $N = 10^6$ run due to intermediate array allocations in K-Means base clustering and Scikit-learn workspace buffers.
- **Disposition:** Reconciled. Graph array memory reduction ($99.6\%$ at $N=10^4$; $160\text{ MB}$ at $N=10^6$) must be distinguished from total process heap memory ($68.8\text{ MB}$ at $N=10^4$; $3.84\text{ GB}$ at $N=10^6$).

---

### D8: CCAA Conformal Coverage Target
- **The Discrepancy:** What does conformal prediction in clustering actually guarantee?
- **Forensic Resolution:**
  1. Conformal prediction in supervised learning guarantees coverage of unobserved ground-truth labels $Y_{n+1}$.
  2. In unsupervised clustering, true biological labels are latent. Calibrating against transductive pseudo-labels $\hat{y}_i$ guarantees coverage only of the *algorithm's own cluster model*, not the underlying biological truth.
  3. If the transductive clustering is biologically wrong (e.g., Prostate $\text{ARI} \approx 0.01$), achieving $90\%$ coverage of the wrong cluster provides zero clinical validity.
- **Disposition:** Reconciled. Conformal clustering claims must remain strictly confined to Future Work as an algorithmic open problem.

---

### D9: Independent Traceability of Experimental Evidence
- **The Discrepancy:** Are any claimed raw results missing?
- **Forensic Resolution:**
  1. All 14 recovered artifacts in `artifact_manifest.csv` are present and verified by SHA-256.
  2. All 226 manuscript assets in `02_manuscript_asset_manifest.csv` are present and verified by SHA-256.
  3. All 13 benchmark datasets exist in `data/cache/` (110.8 MB).
  4. All 3,430 model fit records exist in `results/evidence_recovery/recovered/results.json`.
  5. All 6 adversarial experiment logs and CSVs exist in `results/loop2/`.
- **Disposition:** Reconciled. Traceability is 100% complete on local disk.

---

### D10: Definitive Technical Novelty Characterization
- **The Discrepancy:** Is GAC a breakthrough algorithm, or an empirical warning vehicle?
- **Forensic Resolution:**
  1. The GAC pipeline itself is a **new combination of established methods** (Sarle's BC from 1983, random subspace K-Means from 2003, and bipartite anchor cuts from 2015).
  2. Proposition 2 (Linear Determinacy Identity) is a **genuinely novel, exact algorithmic identity**.
  3. The primary scientific contribution of the paper is an **empirical and methodological falsification**: proving that high stability does not imply correctness in high-$D$ genomics, and establishing null controls and non-degeneracy audits as mandatory safeguards.
- **Disposition:** Reconciled. Framing GAC as an *experimental vehicle* for component attribution is scientifically defensible and appropriate for DMKD.
