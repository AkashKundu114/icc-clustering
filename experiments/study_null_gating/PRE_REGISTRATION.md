# PRE-REGISTRATION SPECIFICATION: STUDY 3' (NULL-CALIBRATED GATING)

**Document ID:** `STUDY-3P-PREREG-01`  
**Date:** October 17, 2026  
**Status:** FROZEN PRIOR TO BENCHMARK EXECUTION  
**Authors:** Research Orchestrator & Autonomous Scientific Subagents  

---

## 1. Primary Research Question
Does pre-clustering feature screening against an exchangeable synthetic null (or decoy knockoff generator) control the empirical False Discovery Proportion ($\text{FDP} \le q$) under non-linear and correlated distractor noise, and produce higher downstream partition recovery ($\Delta\text{ARI}$) than marginal BC, the Hartigan dip test, Bimodality Index (BI), and i-IF-Learn?

---

## 2. Formal Hypotheses
* **Hypothesis 1 ($H_1$, Failure of Heuristics):** Marginal Sarle's Bimodality Coefficient ($BC > 0.555$ or top 15%) and the Hartigan dip test experience severe false discovery inflation ($\text{FDP} > 0.35$ at nominal $\alpha = 0.10$) when distractor features exhibit skewed unimodality (e.g. lognormal nuisance) or block-correlated covariance structures ($\rho = 0.70$).
* **Hypothesis 2 ($H_2$, Valid False Discovery Control):** Null-calibrated ensemble agreement gain ($W_j = S_j - \widetilde{S}_j$) bounded by Knockoff+ selection maintains empirical $\text{FDP} \le q$ across Gaussian, correlated, skewed, and non-linear (XOR) distractor regimes while retaining $\ge 85\%$ statistical power on true discriminating features.
* **Hypothesis 3 ($H_3$, Downstream Cluster Recovery):** On high-dimensional regimes ($D \gg N$), feeding the null-calibrated feature set $\mathcal{S}$ into standard partitioners (K-Means, Spectral, ICC-v2) yields statistically significant ARI gains ($\Delta\text{ARI} > 0.05$) compared to unguided clustering and uncalibrated marginal filters.

---

## 3. Explicit Kill Criteria
1. **FDP Violation Kill:** If the empirical $\text{FDP}$ of the proposed null-calibrated gate exceeds $1.5 \times q$ on more than 20% of synthetic tracks under 10 independent random seeds, the hypothesis of robust FDR control is refuted and the study is killed.
2. **Downstream Utility Kill:** If downstream clustering ARI using the null-calibrated gate fails to outperform the uncalibrated dip test on at least 3 of the 6 real $D/N > 20$ benchmark datasets (Leukemia, Prostate, Colon, SRBCT, CNS, Ovarian), the method is declared practically ineffective and killed.

---

## 4. Benchmark Grid & Methodology

### 4.1 Synthetic Tracks (10 seeds each: seeds 42–51)
* **Track A (Isotropic Gaussian Mixture):** $K=3$, $N=200$, $D=500$. $D_{\text{signal}} = 20$ Gaussian cluster features ($\Delta/\sigma = 2.5$), $D_{\text{noise}} = 480$ i.i.d. standard Gaussian distractor features.
* **Track B (Correlated Nuisance Noise):** $K=3$, $N=200$, $D=500$. $D_{\text{signal}} = 20$, $D_{\text{noise}} = 480$ organized in Toeplitz correlated blocks ($\rho = 0.75$).
* **Track C (Skewed Unimodal Distractors):** $K=3$, $N=200$, $D=500$. $D_{\text{signal}} = 20$, $D_{\text{noise}} = 480$ drawn from skewed lognormal distributions with matched variances ($\mu=0, \sigma=1$). Tests Sarle's BC susceptibility to skewness artifacts.
* **Track D (Non-linear Parity / XOR):** $K=4$, $N=400$, $D=500$. 4 true clusters defined exclusively by multi-way non-linear interaction across 4 features (where all 1D marginals are strictly unimodal and identical across clusters), plus 496 distractor features.

### 4.2 Competing Screening Baselines
1. **Unfiltered (Raw)**: Full feature matrix without screening.
2. **Variance Screening**: Top $k$ features ranked by empirical sample variance.
3. **Sarle's Bimodality Coefficient (BC)**: Features with $BC > 0.555$ or top $k\%$ ($b_d = \frac{\text{skew}^2 + 1}{\text{kurtosis} + 3}$).
4. **Bimodality Index (BI)**: Wang et al. 2-component GMM separation index.
5. **Hartigan Dip Statistic**: Non-parametric test for multimodality against the uniform distribution.
6. **i-IF-Learn Proxy**: Iterative pseudo-label feature ranking.
7. **Proposed: Null-Calibrated Decoy Gate (Knockoff+)**: Feature agreement score contrasted with Gaussian-copula / permuted exchangeable nulls with target nominal FDR $q = 0.10$.

### 4.3 Evaluation Metrics
* **Feature Selection Fidelity**: Empirical False Discovery Proportion ($\text{FDP} = \frac{\text{FP}}{\max(1, \text{TP} + \text{FP})}$), Statistical Power ($\frac{\text{TP}}{D_{\text{signal}}}$), Total Selected Features ($|\mathcal{S}|$).
* **Downstream Clustering Recovery**: Adjusted Rand Index (ARI), Normalized Mutual Information (NMI), and Wall-Clock Latency across 3 clustering backends (K-Means, Spectral Clustering, ICC-v2).
