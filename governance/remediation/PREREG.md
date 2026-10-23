# PHASE 2 PRE-REGISTRATION SPECIFICATION (PREREG.md)

**Canonical Manuscript Title**: "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue**: Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Version**: `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*  
**Authors**: Antigravity Remediation Team (Pair Programming Orchestration)  
**Date**: October 2026  
**Status**: ACTIVE / PRE-REGISTERED  
**Commit Baseline**: `results-frozen` (Tag `results-frozen` on `remediation/phase1`)  
**Target Branch**: `remediation/phase2`  

---

## 1. Scope & Scientific Intent
Phase 1 established an immutable ground truth of published results. Phase 2 conducts the necessary scientific corrections and fair evaluations to ensure all claims in the revised manuscript are defensible, statistically rigorous, and reproducible.

This pre-registration document fixes all hypotheses, metrics, baselines, seeds, and statistical procedures **prior** to generating Phase 2 results.

---

## 2. Theoretical Clarifications & Propositions

### 2.1 Proposition 1 Upper Bound & Integral Verification
- **Hypothesis**: The asymptotic upper bound on the geometry calibration factor $C(\nu)$ under Student-$t$ distributed noise with $\nu > 2$ degrees of freedom is bounded by a universal constant $C^* \approx 1.854$.
- **Verification Method**: Numerical quadrature evaluating the exact integral:
  $$I(\nu) = \int_{-\infty}^{\infty} \left[ \frac{\Gamma\left(\frac{\nu+1}{2}\right)}{\sqrt{\pi \nu} \Gamma\left(\frac{\nu}{2}\right)} \left(1 + \frac{t^2}{\nu}\right)^{-\frac{\nu+1}{2}} \right]^2 dt$$
  evaluated over $\nu \in [1, 20]$ via `scripts/verify_prop1.py`.
- **Pass Criteria**: The maximum evaluated ratio over $\nu \ge 2.1$ must not exceed $1.854 \pm 0.005$.

### 2.2 Transfer-Cut Bipartite Graph Formulation
- **Alignment**: Clarify that Transfer-Cut is formally defined over a bipartite graph $G = (V_X \cup V_A, E, W)$ between $N$ data points $V_X$ and $M$ anchors $V_A$, where the bipartite affinity matrix $B \in \mathbb{R}^{N \times M}$ has non-zero entries only between samples and anchors.
- **Spectrum Equivalence**: Prove and state that the generalized eigenvalues of the normalized bipartite graph Laplacian correspond to the Singular Value Decomposition (SVD) of the normalized bipartite matrix $\tilde{B} = D_X^{-1/2} B D_A^{-1/2}$.

### 2.3 Bimodality Coefficient & Sarle's Threshold
- **Definition**: Bimodality Coefficient is defined as:
  $$b_d = \frac{\gamma_d^2 + 1}{\kappa_d}$$
  where $\gamma_d$ is sample skewness and $\kappa_d$ is sample kurtosis (with standard Pearson definition where Gaussian kurtosis = 3, or adjusted excess kurtosis + 3).
- **Threshold**: Sarle's criterion for a uniform distribution is $b_{\text{uniform}} = 5/9 \approx 0.5556$. Values $b_d > 5/9$ indicate candidate multimodality.
- **Pre-registered Negative Scope (1D Unimodality Limitation)**:
  - VSSG filters features by calculating marginal 1D statistics ($b_d$).
  - For problems governed by multi-dimensional non-linear interactions without marginal separation (such as the XOR problem in Madelon), marginal projections are unimodal ($b_d \le 0.5042$).
  - This limitation is explicitly acknowledged and documented as an architectural boundary, not concealed.

### 2.4 Anchor Determinacy vs. Uniform Random Sampling
- **Finding**: On tiny $N$, high-$D$ regimes (Leukemia $N=72$, SRBCT $N=83$), uniform random anchors (V4) achieved comparable or slightly higher ARI than determinacy-certified anchors (V5).
- **Explanation**: Determinacy certification selects anchor points with high graph degree and localized density; in extreme $N \ll D$ regimes with severe label imbalance or outlier clusters, density-based selection can over-sample dominant classes and starve minority classes. Uniform random sampling provides unbiased coverage across the manifold.

---

## 3. Fair Baseline Formulations

To ensure a fair evaluation of high-dimensional feature selection, ICC-v2 must be benchmarked against standard, recognized feature reduction / selection pipelines applied to the baseline clusterers:

1. **Variance Filter (VarFilt)**:
   - Rank all features by sample variance: $\sigma_d^2 = \frac{1}{N} \sum_{i=1}^N (x_{id} - \bar{x}_d)^2$.
   - Retain the top $k_f = \lceil 0.15 \times D \rceil$ features (matching ICC-v2's 15% budget).
   - Cluster using K-Means and Standard Consensus.
2. **Principal Component Analysis (PCA)**:
   - Compute truncated SVD / PCA retaining top components explaining 90% variance (or $k_{\text{components}} = \min(N-1, 50)$).
   - Cluster using K-Means and Standard Consensus.
3. **Laplacian Score (LapScore)**:
   - Unsupervised graph-based feature selection (He, Cai, & Niyogi, NeurIPS 2005) evaluating feature locality preservation:
     $$L_r = \frac{\tilde{\mathbf{f}}_r^T L \tilde{\mathbf{f}}_r}{\tilde{\mathbf{f}}_r^T D \tilde{\mathbf{f}}_r}$$
   - Retain top 15% lowest Laplacian score features.
   - Cluster using K-Means.
4. **Sparse K-Means (SparseKM)**:
   - Witten & Tibshirani (JASA 2010) $L_1$-penalized feature-weighted clustering optimizing between-cluster sum of squares with sparsity parameter $s = \sqrt{D} / 2$.

---

## 4. Dataset Partition & Pre-specified Subgroups

All evaluations are conducted over the canonical 13 real-world benchmark datasets:

### 4.1 High-Dimensional Subgroup ($D/N > 20$, 6 datasets)
- `colon` ($N=62, D=2000, D/N=32.3$)
- `leukemia` ($N=72, D=7129, D/N=99.0$)
- `srbct` ($N=83, D=2308, D/N=27.8$)
- `lymphoma` ($N=62, D=4026, D/N=64.9$)
- `cns` ($N=60, D=7129, D/N=118.8$)
- `ovarian` ($N=253, D=15154, D/N=59.9$)

### 4.2 Standard / Low-Dimensional Subgroup ($D/N \le 20$, 7 datasets)
- `indian_pines` ($N=10249, D=200, D/N=0.02$)
- `isolet` ($N=7797, D=617, D/N=0.08$)
- `har` ($N=10299, D=561, D/N=0.05$)
- `newsgroups20` ($N=18846, D=2000, D/N=0.11$)
- `usps` ($N=9298, D=256, D/N=0.03$)
- `waveform` ($N=5000, D=40, D/N=0.008$)
- `yale_b` ($N=2414, D=1024, D/N=0.42$)

---

## 5. Statistical Protocols

### 5.1 Omnibus Test
- **Friedman Test**: Non-parametric repeated measures test across all $k$ models on the $N=13$ datasets.
  $$\chi_F^2 = \frac{12 N}{k(k+1)} \left[ \sum_{j=1}^k R_j^2 - \frac{k(k+1)^2}{4} \right]$$
  Significance threshold: $\alpha = 0.05$.

### 5.2 Post-Hoc Pairwise Comparisons
- **Wilcoxon Signed-Rank Test**: Two-sided paired non-parametric test between ICC-v2 and each competing model.
- **Holm-Bonferroni Correction**: Step-down adjusted $p$-values:
  $$p_{(i)}^{\text{adj}} = \min\left( \max_{j \le i} \{(k - j + 1) p_{(j)}\}, 1 \right)$$

### 5.3 Nemenyi Critical Difference Calibration
- Exact formula:
  $$\text{CD} = q_\alpha \sqrt{\frac{k(k+1)}{6N}}$$
- For $k=11$ models and $N=13$ datasets at $\alpha=0.05$:
  - Studentized range critical value $q_{0.05} = 3.219$.
  - $\sqrt{\frac{11 \times 12}{6 \times 13}} = \sqrt{\frac{132}{78}} = \sqrt{1.6923} \approx 1.3009$.
  - $\mathbf{\text{CD} = 3.219 \times 1.3009 = 4.1876 \approx 4.19}$ (locked in `paper/numbers.tex` as `\TrueNemenyiCD{4.19}`).

---

## 6. Execution Parameters & Output Destinations
- **Seeds**: Fixed 10 seeds: `[42, 101, 202, 303, 404, 505, 606, 707, 808, 909]`.
- **Output Directory**: `results/phase2/` (never overwrites `results/results.json`).
- **Target Files**:
  - `results/phase2/fair_baselines.csv`
  - `results/phase2/inductive_direct.csv`
  - `results/phase2/stats.json`
  - `results/phase2/MANIFEST.md`
