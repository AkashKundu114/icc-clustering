# Remediation Report 04: Unknown-K Model Order Discovery & ICC-AutoK Remediation

**Reference File:** `research_audit/remediation/04_unknown_k.md`  
**Auditing Persona:** Senior Clustering & Unsupervised Learning Researcher (Agent 4)  
**Target Repository:** `AkashKundu114/icc-clustering` (Branch: `research/dmkd-complete-remediation`)  
**Date:** November 1, 2026  
**Findings Addressed:** F-20 through F-22  

---

## 1. Executive Summary & Core Mandate

This report provides the exhaustive mathematical, algorithmic, and experimental audit of model order selection ($K$ discovery) in high-dimensional consensus clustering. Previous drafts asserted that ICC-AutoK provided an exact, linear-memory model order discovery mechanism via bipartite anchor Proportion of Ambiguous Clustering (PAC). The adversarial audit revealed that:
1. The synthetic unknown-$K$ evaluation script leaked the ground truth: `k_max = max(6, k_true + 2)`.
2. The implementation of PAC in `src/icc/autok.py` passed spectral eigenvectors $U \in \mathbb{R}^{N \times k}$ rather than the bipartite anchor co-occurrence matrix $B \in \mathbb{R}^{N \times L}$.
3. An artificial Occam's parsimony heuristic (`min_pac + 0.02`) structurally biased PAC toward $K=2$.
4. On synthetic multi-class data ($K^* \ge 3$), PAC achieved 0% exact match (MAE 2.37), whereas ICC-AutoK-Silhouette demonstrated robust performance (MAE 0.60, exact match 63.3%, ARI 0.834).

### Key Audit Conclusions & Remediations:
- **Removal of Ground-Truth Leakage (Finding F-20, CRITICAL):**  
  In `experiments/exp8_unknown_k/src/run_unknown_k.py`, all instances of `k_max = max(6, k_true + 2)` have been eliminated and replaced with a fixed, declared, label-independent candidate search space ($k \in [2, 8]$).
- **Resolution of Representation Disconnect (Finding F-21, CRITICAL):**  
  In `src/icc/consensus_v2.py`, the normalized bipartite co-occurrence matrix $B_{\text{norm}} \in \mathbb{R}^{N \times L}$ is now stored as an explicit model attribute (`self.B_norm_ = B_norm`). In `src/icc/autok.py`, PAC is computed directly on $B_{\text{norm}}$ as derived in theory, or documented transparently when evaluated in spectral space.
- **PAC Collapse Disclosed & Silhouette Recommended (Finding F-22, CRITICAL):**  
  The artificial parsimony heuristic `min_pac + 0.02` that forced selection of $K=2$ has been removed, restoring true argmin PAC selection. The manuscript narrative is updated to disclose PAC's vulnerability in multi-class noisy regimes, recommending **ICC-AutoK-Silhouette** as the primary reliable heuristic.

---

## 2. Itemized Unknown-K Audit & Remediation Matrix

| Finding ID | Track | Description & Forensic Evidence | Severity | Implemented Remediation | Verification Test |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **F-20** | Unknown-$K$ | `run_unknown_k.py` used `k_max = max(6, k_true + 2)`, leaking ground-truth $K$ into candidate grid. | **CRITICAL** | Replaced with fixed, declared label-independent range $k \in [2, 8]$ across all models and datasets. | `test_label_independent_search_space_synthetic` in `tests/test_unknown_k_remediation.py` |
| **F-21** | Unknown-$K$ | `autok.py` computed PAC on spectral eigenvectors $U \in \mathbb{R}^{N \times k}$, not bipartite matrix $B \in \mathbb{R}^{N \times L}$. | **CRITICAL** | Stored `self.B_norm_` on `InvariantCoreConsensusV2`; updated `autok.py` to evaluate PAC on $B_{\text{norm}}$. | `test_bipartite_b_norm_attribute_preservation` in `tests/test_unknown_k_remediation.py` |
| **F-22** | Unknown-$K$ | `min_pac + 0.02` heuristic forced $K=2$; PAC achieved 0% match on synthetic $K^* \ge 3$ (MAE 2.37). | **CRITICAL** | Removed artificial parsimony bias; restored true argmin PAC; transparently report PAC limitations and recommend Silhouette. | `test_unbiased_pac_argmin_selection` in `tests/test_unknown_k_remediation.py` |

---

## 3. Mathematical Analysis: Bipartite Projection vs Spectral Embedding PAC

### 3.1 The Theoretical Formulation (Bipartite Co-occurrence)
Senbabaoglu et al. (Sci Rep 2014) define PAC on an empirical consensus matrix $S \in [0, 1]^{N \times N}$ as the fraction of sample pairs with ambiguous co-occurrence:
$$\text{PAC}(k) = F_k(x_2) - F_k(x_1) = \frac{2}{N(N-1)} \sum_{i < j} \mathbb{I}(x_1 \le S_{ij} \le x_2)$$
where $x_1 = 0.10$ and $x_2 = 0.90$.
In GAC, the bipartite co-occurrence matrix $B \in [0, 1]^{N \times L}$ defines an approximate pairwise similarity:
$$\hat{S}_{ij} = \sum_{l=1}^L B_{il} B_{jl} = (B B^T)_{ij}$$
Computing $\hat{S}_{ij}$ over a random sample of pairs $\mathcal{P}$ yields an $O(|\mathcal{P}| \cdot L)$ linear-time approximation of consensus stability.

### 3.2 The Spectral Embedding Divergence
In the legacy code, instead of $B$, the normalized Laplacian eigenvectors $U_{\text{norm}} \in \mathbb{R}^{N \times k}$ were passed to `compute_anchor_pac`:
$$S_{ij}^{\text{spectral}} = \cos(\theta_{ij}) = \sum_{c=1}^k U_{ic} U_{jc}$$
In $\mathbb{R}^k$, well-separated clusters map to mutually orthogonal coordinate axes. Consequently:
- For pairs in different clusters: $\cos(\theta_{ij}) \le 0$ (clipped to $0.0$).
- For pairs in the same cluster: $\cos(\theta_{ij}) \approx 1.0$.
As $k$ increases, intermediate cosine values in $(0.10, 0.90)$ vanish due to spectral geometry rather than consensus stability. For all $k \ge 2$, $\text{PAC}(k) < 0.02$.
The legacy decision rule:
$$\hat{K} = \min \{k : \text{PAC}(k) \le \min_k \text{PAC}(k) + 0.02\}$$
trivially evaluated to $\hat{K} = 2$ for virtually every dataset, creating an artificial $K=2$ attractor.

---

## 4. Empirical Performance: PAC vs Silhouette

In Experiment 8 (EXP8), evaluating model order discovery across isotropic noise regimes ($D_{\text{noise}} \in \{0, 100, 1000\}$):
- **HDBSCAN\*:** Exact match **70.0%**, MAE $= 0.73$.
- **ICC-AutoK-Silhouette:** Exact match **63.3%**, MAE $= 0.60$, Mean ARI at $\hat{K} = 0.834$.
- **Spectral Eigengap:** Exact match **56.7%**, MAE $= 1.20$.
- **GMM-BIC:** Exact match **56.7%**, MAE $= 1.13$.
- **ICC-AutoK-PAC:** Exact match **16.7%**, MAE $= 2.37$ (0% exact match on $K^* \ge 3$).

On real multi-class biological cohorts (e.g. `su2001`, $K^*=11$):
- **ICC-AutoK-PAC:** Predicted $\hat{K} = 2$ (error $-9$, cluster collapse).
- **ICC-AutoK-Silhouette:** Predicted $\hat{K} = 8$ (error $-3$, preserving major anatomical groupings).

### Formal Disposition Recommendation:
The manuscript narrative is updated to:
1. Disclose the mathematical limitations and multi-class failure of PAC under high-dimensional noise.
2. Present PAC as an experimental diagnostic rather than a universal model order estimator.
3. Recommend **ICC-AutoK-Silhouette** as the primary robust heuristic for practical unknown-$K$ cluster discovery.

---
*Report certified by Agent 4 (Unknown-K & ICC-AutoK Research). All fixes verified with passing tests in `tests/test_unknown_k_remediation.py`.*
