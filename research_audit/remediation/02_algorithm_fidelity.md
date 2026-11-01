# Remediation Report 02: Algorithm Implementation Fidelity & Baseline Engineering

**Reference File:** `research_audit/remediation/02_algorithm_fidelity.md`  
**Auditing Persona:** Senior Clustering Researcher & Baseline Engineering Agent (Agent 2)  
**Target Repository:** `AkashKundu114/icc-clustering` (Branch: `research/dmkd-complete-remediation`)  
**Date:** November 1, 2026  
**Findings Addressed:** F-07 through F-13  

---

## 1. Executive Summary & Core Mandate

This report provides the exhaustive engineering audit, mathematical reconciliation, and code remediation for the benchmark baselines evaluated across Experiments 6, 7, and 8. Previous audits revealed that multiple classical and modern baselines suffered from hidden switching, uncredited surrogate stubs, silent library fallbacks, parameter discrepancies, and ground-truth leakage.

### Key Audit Conclusions & Remediations:
1. **Base Clusterer Switching Resolved (Finding F-07, CRITICAL):**  
   The hidden switching logic in `src/icc/consensus_v2.py` (lines 244-254) which automatically switched between Spectral Clustering ($N \le 100$) and K-Means ($N > 100$) has been exposed as an explicit configurable parameter `base_clusterer`. For strict apples-to-apples comparisons against Standard Consensus (which employs K-Means voters), `base_clusterer="kmeans"` is formally supported and benchmarked.
2. **Authentic GMM-BIC Unsupervised Grid Search (Finding F-08, CRITICAL):**  
   In `src/icc/baselines/probabilistic.py`, `run_gmm_bic` previously aliased `run_gmm` directly with ground-truth $k$. The code has been rewritten to implement an authentic unsupervised model order selection pipeline: candidate grid $k \in [k_{\min}, k_{\max}]$ (default $[2, 10]$) independent of true labels, fitting models with diagonal covariance to combat high-dimensional singularity, and selecting $k^* = \arg\min_k \text{BIC}(k)$.
3. **Leiden SNN Library Fallback Handled (Finding F-09, CRITICAL):**  
   In `src/icc/baselines/leiden_snn.py`, the code silently caught `ImportError` when `igraph`/`leidenalg` were missing and executed Spectral Clustering on the SNN graph using ground-truth $k$. The baseline now explicitly reports `status="UNAVAILABLE: No module named 'igraph'"` by default, preventing silent algorithm substitution. A separate, transparently named baseline `run_spectral_snn` has been introduced.
4. **HDBSCAN* Noise & Coverage Protocol (Finding F-10, MAJOR):**  
   In `src/icc/baselines/density.py`, HDBSCAN* evaluated on raw ambient high-dimensional matrices ($D = 15,154$) suffered catastrophic distance concentration, assigning large proportions of instances to noise (label `-1`). A standardized evaluation function `evaluate_hdbscan_metrics` now reports both full-sample ARI (treating noise as a distinct cluster) and conditional core ARI (computed only on non-noise points), alongside exact coverage ($1 - \text{noise\_ratio}$).
5. **Sparse K-Means Scaling Formula Harmonized (Finding F-11, MAJOR):**  
   In `src/icc/baselines/sparse_kmeans.py`, the code defaulted to $s = 0.15\sqrt{D} + 1.0$, whereas Table 2 in the manuscript specified $s = 1.1 + 0.5(\sqrt{D} - 1.1)$ (a $3\times$ difference in $L_1$ penalty). The implementation now supports an explicit `s_rule` parameter (`"witten_scaled"` vs `"table2"`), recording the exact value and formula in model metadata.
6. **Ensemble Voter Initialization Documented (Finding F-12, MAJOR):**  
   The methodological rationale for using single-restart K-Means ($n_{\text{init}} = 1$) within consensus ensembling versus multi-restart ($n_{\text{init}} = 10$) in standalone K-Means is established: ensembling relies on voter diversity induced across random subspaces, whereas standalone K-Means seeks local-minima avoidance on the full ambient space.
7. **Fuzzy C-Means Hard Defuzzification Documented (Finding F-13, MINOR):**  
   Documented standard default fuzzifier $m = 2.0$ and deterministic `argmax` membership defuzzification for partition evaluation.

---

## 2. Itemized Baseline Remediation Scorecard

The table below summarizes the exact audit status, code changes, and test verifications across all 10 baseline implementations:

| Baseline Algorithm | Original Code File | Identified Deficiency | Severity | Implemented Remediation | Verification Test |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GAC (ICC-v2)** | `src/icc/consensus_v2.py` | Hidden `base_clusterer="auto"` switched based on $N \le 100$. | **CRITICAL** | Added explicit `base_clusterer` parameter; documented behavior; enabled `base_clusterer="kmeans"` comparison. | `test_base_clusterer_parameterization` in `tests/test_algorithm_fidelity.py` |
| **GMM-BIC** | `src/icc/baselines/probabilistic.py` | Aliased to `run_gmm(k=k_true)`; no BIC grid search. | **CRITICAL** | Implemented authentic unsupervised grid search over $k \in [2, 10]$ returning $\arg\min \text{BIC}$. Fixed-$K$ baseline renamed to `GMM (Fixed-K)`. | `test_gmm_fixed_k_vs_bic_grid_search` in `tests/test_algorithm_fidelity.py` |
| **Leiden SNN** | `src/icc/baselines/leiden_snn.py` | Silently fell back to Spectral Clustering on SNN with target $k$ when C++ libraries missing. | **CRITICAL** | When `igraph`/`leidenalg` missing, reports `UNAVAILABLE` by default. Introduced distinct, accurately named `run_spectral_snn`. | `test_leiden_snn_unavailability_and_spectral_snn` in `tests/test_algorithm_fidelity.py` |
| **HDBSCAN*** | `src/icc/baselines/density.py` | Ambient distance concentration; noise `-1` penalized in ARI without coverage context. | **MAJOR** | Added `evaluate_hdbscan_metrics` returning both full ARI and core ARI; records noise ratio and coverage. | `test_hdbscan_core_and_full_metrics` in `tests/test_algorithm_fidelity.py` |
| **Sparse K-Means** | `src/icc/baselines/sparse_kmeans.py` | Code used $s = 0.15\sqrt{D} + 1.0$; Table 2 specified $s = 1.1 + 0.5(\sqrt{D} - 1.1)$. | **MAJOR** | Parameterized `s_rule` (`'witten_scaled'` vs `'table2'`); recorded $s$ parameter and active feature counts. | `test_sparse_kmeans_formula_options` in `tests/test_algorithm_fidelity.py` |
| **FastMVC** | `src/icc/baselines/anchor.py` | Uncredited surrogate proxy for FastMICE (Huang et al., IEEE TKDE 2023). | **CRITICAL** | Renamed method metadata to `FastMVC-Surrogate`; added reference to Huang et al. (2023) in docstrings and bib. | `test_fastmvc_surrogate_attribution` in `tests/test_algorithm_fidelity.py` |
| **FCAG** | `src/icc/baselines/anchor.py` | Re-implementation uses k-means++ anchors rather than PGD/IRW solvers. | **MINOR** | Explicitly documented k-means++ anchor spectral re-implementation in docstring. | Existing unit tests in `tests/test_baselines.py` |
| **Standard Consensus** | `src/icc/baselines/consensus.py` | Uses Fred & Jain (2005) dense co-association matrix with single-restart K-Means. | **MAJOR** | Confirmed authentic $O(N^2)$ EAC implementation; documented single-restart ensembling diversity. | Existing tests in `tests/test_consensus.py` |
| **FCM** | `src/icc/baselines/classical.py` | Evaluated strictly via `argmax` membership defuzzification. | **MINOR** | Documented standard $m=2.0$ fuzzifier and hard partition conversion protocol. | Existing tests in `tests/test_baselines.py` |
| **CoHiRF** | `src/icc/baselines/cohirf.py` | Heavy cluster collapse on high-dimensional noisy data. | **MINOR** | Documented strict unanimity filtering causes singleton collapse when noise is extreme. | Existing tests in `tests/test_cohirf.py` |

---

## 3. Detailed Algorithmic Fixes & Implementations

### 3.1 Base Clusterer Parameterization in GAC
In `src/icc/consensus_v2.py`:
```python
if self.base_clusterer == "auto":
    base_engine = "spectral" if N <= 100 else "kmeans"
else:
    base_engine = self.base_clusterer
```
When running on the 6 classic cohorts:
- `colon` ($N=62$), `srbct` ($N=83$), `cns` ($N=60$), `leukemia` ($N=72$) used Spectral Clustering base voters.
- `prostate` ($N=102$), `ovarian` ($N=253$) used K-Means base voters.

Under our updated protocol:
1. `base_clusterer` can be explicitly fixed to `"kmeans"`, ensuring exact base-voter parity with Standard Consensus (`Standard_Consensus`).
2. The hybrid configuration `base_clusterer="auto"` is retained and transparently reported as an adaptive ensemble strategy.

### 3.2 Authentic GMM-BIC Grid Search
In `src/icc/baselines/probabilistic.py`:
- `run_gmm(X, k, ...)`: Fixed-$K$ baseline.
- `run_gmm_bic(X, k_min=2, k_max=10, ...)`: Unsupervised grid search fitting Gaussian mixtures with diagonal covariance:
  $$\text{BIC}(k) = -2 \ln \hat{L} + d_k \ln N$$
  where $d_k$ is the number of free parameters for $k$ diagonal Gaussians in $D$ dimensions:
  $$d_k = (k - 1) + k \cdot D + k \cdot D = k(2D + 1) - 1$$
  The model returning minimum $\text{BIC}(k)$ is chosen without access to reference labels.

### 3.3 Leiden SNN Availability & Spectral-SNN Separation
In `src/icc/baselines/leiden_snn.py`:
- `run_leiden_snn`: Requires `igraph` and `leidenalg`. When missing in the environment (e.g. pure Python Windows without C++ compilers), it returns `metadata.status = "UNAVAILABLE: No module named 'igraph'"` rather than silently executing another algorithm.
- `run_spectral_snn`: Defined as a standalone baseline executing normalized spectral clustering on the SNN graph, accurately documented in all output files.

---
*Report certified by Agent 2 (Algorithm Fidelity & Baseline Engineering). All fixes covered by passing unit tests.*
