# ADVERSARIAL AUDIT REPORT: ICC-AutoK & UNKNOWN-$K$ MODEL ORDER DISCOVERY
**Target Venue:** Springer *Data Mining and Knowledge Discovery* (DMKD)  
**Auditor Persona:** `roo_reviewer` (Adversarial Scientific Peer Reviewer & Code Auditor)  
**Target Repository:** `d:/Final Year Project` (`AkashKundu114/icc-clustering`)  
**Investigation Track:** Mandatory Investigation D — ICC-AutoK & Unknown-$K$ Model Order Discovery  
**Audit Date:** November 1, 2026  

---

### EXECUTIVE AUDIT DISPOSITION: **MAJOR REVISION / CONDITIONAL REJECTION**
The claim that **ICC-AutoK** provides a "genuinely unsupervised, mathematically rigorous model order selection mechanism via linear-memory anchor PAC" cannot be accepted in its current form. While the companion heuristic (**ICC-AutoK-Silhouette**) demonstrates resilience in high-dimensional noise regimes, the primary advertised mathematical framework (**ICC-AutoK-PAC**) suffers from:
1. **Critical Theoretical-Implementation Disconnect:** The code in [`src/icc/autok.py`](file:///d:/Final%20Year%20Project/src/icc/autok.py#L165-L175) does **not** evaluate PAC on the row-projected bipartite anchor graph $B \in \mathbb{R}^{N \times L}$ as claimed in the text and protocol; it computes cosine similarities on the unit-normalized spectral eigenvectors $U \in \mathbb{R}^{N \times k}$.
2. **Pathological $K=2$ Stability Attractor:** The combination of spectral eigenvector cosine distribution, the $K=1$ blind spot (Senbabaoglu et al., 2014), and an explicit `min(k)` tie-breaking tolerance (`min_pac + 0.02`) turns ICC-AutoK into an aggressive $K=2$ attractor. It predicted $K=2$ for 100% of runs on high-noise synthetic benchmarks ($K^*=5$) and 100% of runs on the multi-class biological cohort Su2001 ($K^*=11$, error $-9$).
3. **Severe Experimental Protocol Vulnerability (Ground-Truth Leakage):** In [`experiments/exp8_unknown_k/src/run_unknown_k.py`](file:///d:/Final%20Year%20Project/experiments/exp8_unknown_k/src/run_unknown_k.py#L161-L230), the upper bound of the candidate search space is explicitly set as a function of the ground truth: `k_max = max(6, k_true + 2)`. This artificially truncates over-estimation error for larger $K^*$, violating the fundamental premise of unsupervised model order discovery.
4. **Catastrophic PAC Synthetic Failure:** On synthetic benchmark grids, ICC-AutoK-PAC achieves an exact match rate of only **16.7%** (MAE $= 2.37$), significantly underperforming standard classical baselines: HDBSCAN\* (**70.0%**, MAE $= 0.73$), GMM-BIC (**56.7%**, MAE $= 1.13$), and Spectral Eigengap (**56.7%**, MAE $= 1.20$).

---

## 1. MATHEMATICAL FORMULATION & IMPLEMENTATION AUDIT

### 1.1 Divergence Between Protocol, Claims, and Code
In [`research_audit/13_unknown_k_protocol.md`](file:///d:/Final%20Year%20Project/research_audit/13_unknown_k_protocol.md#L36-L39), the manuscript claims:
> *"In ICC-AutoK, we exploit the bipartite anchor representation $\tilde{B} \in \mathbb{R}^{N \times L}$... Approximate co-association in $O(L)$ time: $\hat{S}_{ij} = \sum_{l=1}^L \tilde{B}_{il} \tilde{B}_{jl}$... Compute $\widehat{\text{PAC}}(k)$ in $O(|\mathcal{P}| \cdot L)$ time."*

However, in [`src/icc/autok.py`](file:///d:/Final%20Year%20Project/src/icc/autok.py#L164-L175):
```python
# autok.py lines 164-175:
if model.U_emb_ is not None and model.U_emb_.shape[0] == N:
    # Normalized spectral embedding in R^k
    U = model.U_emb_
    U_norm = U / (np.linalg.norm(U, axis=1, keepdims=True) + 1e-12)
    pac, area = compute_anchor_pac(U_norm, n_pairs=n_pairs, random_state=seed)
else:
    # Fallback to one-hot assignment co-association
    one_hot = np.zeros((N, k), dtype=np.float64)
    one_hot[np.arange(N), labels] = 1.0
    pac, area = compute_anchor_pac(one_hot, n_pairs=n_pairs, random_state=seed)
```
**Audit Findings:**
1. **Wrong Object Passed:** The matrix passed to [`compute_anchor_pac`](file:///d:/Final%20Year%20Project/src/icc/autok.py#L46) is `model.U_emb_`, which is the $N \times k$ matrix of Laplacian eigenvectors (the low-dimensional spectral embedding), **not** the bipartite co-association matrix $B \in \mathbb{R}^{N \times L}$.
2. **Dimension-Dependent Dot Product Contraction:** For candidate $k$, $U_{\text{norm}} \in \mathbb{R}^{N \times k}$. The inner product $U_i \cdot U_j = \cos(\theta_{ij})$ occurs in $\mathbb{R}^k$. As $k$ increases, orthogonal cluster poles cause between-cluster pairs to have inner products $\le 0$ (clipped to $0$ by `np.clip(co_assoc, 0.0, 1.0)`), while within-cluster pairs have inner products $\approx 1$. Consequently, intermediate ambiguous values in $(0.1, 0.9)$ disappear by spectral geometric construction, not by empirical resampling consensus!
3. **Catastrophic Fallback Degeneracy:** If `model.U_emb_` is `None`, the code falls back to `one_hot \in \mathbb{R}^{N \times k}`. For one-hot vectors, $S_{ij} = \mathbf{e}_{c_i}^T \mathbf{e}_{c_j} \in \{0.0, 1.0\}$ identically for all pairs. The condition `(co_assoc >= 0.10) & (co_assoc <= 0.90)` evaluates to **identically zero** for all $k$, yielding $\text{PAC}(k) = 0.0$ uniformly.

### 1.2 Decision Rule Flaw: Hardcoded Bias Toward Smallest $K$
Look at [`src/icc/autok.py`](file:///d:/Final%20Year%20Project/src/icc/autok.py#L206-L208):
```python
# autok.py lines 206-208:
min_pac = min(pac_scores.values())
best_k_pac = min(k for k, p in pac_scores.items() if p <= min_pac + 0.02)
```
**Mechanism of Bias:**
- The author introduced an *"Occam's parsimony tolerance (+0.02)"*.
- In spectral embedding space, PAC values across all $k$ are frequently $< 0.02$.
- If $\text{PAC}(2) = 0.015$, $\text{PAC}(3) = 0.008$, $\text{PAC}(4) = 0.002$, then `min_pac = 0.002` and `min_pac + 0.02 = 0.022`.
- Since $0.015 \le 0.022$, the expression `min(k for k ...)` selects **$k = 2$**, completely ignoring the fact that $k=4$ has an 87% lower ambiguity rate!
- This mathematical heuristic structurally forces the model to choose $k_{\min} = 2$.

### 1.3 Theoretical Invalidation: Anchor Graph Projection vs. Resampling PAC
Senbabaoglu et al. (Sci Rep 2014) formulated PAC on the empirical consensus matrix $M_{ij} \in [0, 1]$, where entries represent the true fraction of subsampled base runs where $i$ and $j$ clustered together.
- In bipartite anchor graphs ($B = Z \Delta^{-1/2} \in \mathbb{R}^{N \times L}$), the projection $W_{ij} = (B B^T)_{ij} = \sum_l \frac{Z_{il} Z_{jl}}{\Delta_{ll}}$ is a **static topological kernel smoother**.
- If two clusters are adjacent, boundary points naturally share intermediate anchor connections. The anchor graph dot product distributes values continuously between $0$ and $1$, reflecting local graph density rather than partition ambiguity across stochastic draws.
- Furthermore, Senbabaoglu et al. established that consensus clustering possesses an intrinsic mathematical bias toward $K=2$ on unclustered unimodal distributions. Projecting onto bipartite anchor graphs does not eliminate this bias; it exacerbates it.

---

## 2. FAIRNESS & METHODOLOGICAL AUDIT OF EXP8 SETUP

### 2.1 Ground-Truth Leakage in Search Range
In [`experiments/exp8_unknown_k/src/run_unknown_k.py`](file:///d:/Final%20Year%20Project/experiments/exp8_unknown_k/src/run_unknown_k.py#L161-L230):
```python
# Lines 161, 194, 212, 230:
res = run_icc_autok(X, k_min=2, k_max=max(6, k_true + 2), seed=seed)
k_bic, y_bic = estimate_k_gmm(X, k_min=2, k_max=max(6, k_true + 2), ...)
k_eigen, y_eigen = estimate_k_spectral_eigengap(X, k_min=2, k_max=max(6, k_true + 2), ...)
```
**Critical Violation:**
- The candidate upper bound $K_{\max}$ is **dynamically parameterized by $K_{\text{true}}$**!
  - When $K_{\text{true}} = 2$, range is $[2, 6]$.
  - When $K_{\text{true}} = 5$, range is $[2, 7]$.
  - When $K_{\text{true}} = 8$, range is $[2, 10]$.
- This violates the explicit claim in [`research_audit/overnight/UNKNOWN_K_DESIGN.md`](file:///d:/Final%20Year%20Project/research_audit/overnight/UNKNOWN_K_DESIGN.md#L21-L25):
  > *"Zero Access to Ground-Truth Labels: True class labels and true $K^*$ are strictly isolated... All candidate algorithms explore candidate cluster counts $K \in \{2, 3, 4, 5, 6, 7, 8, 9, 10\}$."*
- **Impact of Leakage:** For $K_{\text{true}} = 8$, the maximum possible over-estimation error is artificially capped at $+2$ (since $K_{\max} = 10$). Yet the lower bound remains $K_{\min} = 2$, allowing an under-estimation error of $-6$. This asymmetric bounding hides potential runaway over-clustering.

### 2.2 Benchmark Cohort Composition Bias
In [`experiments/exp8_unknown_k/src/run_unknown_k.py`](file:///d:/Final%20Year%20Project/experiments/exp8_unknown_k/src/run_unknown_k.py#L275), the real cohorts evaluated are:
- `colon` ($K^* = 2$)
- `srbct` ($K^* = 4$)
- `cns` ($K^* = 2$)
- `leukemia` ($K^* = 2$)
- `prostate` ($K^* = 2$)
- `ovarian` ($K^* = 2$)

**5 out of 6 cohorts have $K^* = 2$!**  
In the overnight audit benchmark ([`results/overnight/unknown_k/unknown_k_real_results.csv`](file:///d:/Final%20Year%20Project/results/overnight/unknown_k/unknown_k_real_results.csv)), cohorts were `colon` ($K^*=2$), `srbct` ($K^*=4$), `cns` ($K^*=2$), `leukemia` ($K^*=2$), `dlbcl` ($K^*=2$), `breast` ($K^*=2$), and `su2001` ($K^*=11$). Again, **5 out of 7 cohorts have $K^* = 2$**.
- Because ICC-AutoK has a strong propensity to select $K = 2$, evaluating on a cohort suite dominated by binary classifications creates a **false appearance of model order discovery accuracy** (reported as "54.3% exact match" in [`UNKNOWN_K_RESULTS.md`](file:///d:/Final%20Year%20Project/research_audit/overnight/UNKNOWN_K_RESULTS.md#L37)).
- The moment a non-binary cohort is tested (`su2001`, $K^* = 11$), ICC-AutoK predicts $\hat{K} = 2$ across all 5 random seeds (error $-9$).

### 2.3 Discrepancy Between Protocol Manifest and Executed Code
- [`research_audit/13_unknown_k_protocol.md`](file:///d:/Final%20Year%20Project/research_audit/13_unknown_k_protocol.md#L55) claims a *"560-Run Phase Grid across 5 independent seeds"*.
- In [`experiments/exp8_unknown_k/src/run_unknown_k.py`](file:///d:/Final%20Year%20Project/experiments/exp8_unknown_k/src/run_unknown_k.py#L358), execution is called with `n_reps=2` (seeds 42, 52 only).
- Missing Comparators: The protocol promised **Gap Statistic**, **X-Means**, and **Hierarchical Dynamic Tree Cut**. None of these are implemented in [`run_unknown_k.py`](file:///d:/Final%20Year%20Project/experiments/exp8_unknown_k/src/run_unknown_k.py).

---

## 3. DEGENERATE PARTITIONS & EDGE CASE STRESS AUDIT

| Edge Case / Degime | Theoretical Vulnerability | Executed Behavior in Codebase | Severity |
| :--- | :--- | :--- | :---: |
| **$K = 1$ (Null Noise Distribution)** | Consensus clustering cannot evaluate $K=1$; Silhouette, CH, and DB indices are undefined for $K=1$. | `k_min` is hardcoded to $2$. When pure Gaussian noise is presented, ICC-AutoK cannot predict $K=1$ and defaults to $K=2$. | **Critical** |
| **High Cluster Imbalance (e.g. 90% / 10%)** | Uniform anchor sampling from certified core points ($L=40$) starves the minority cluster of anchors. | In `SYN-K4-IMB` (200:100:60:40), ICC-AutoK collapsed to $\hat{K}=2$ or $3$ on 4/5 seeds; on seed 202, recovered $\text{ARI} = -0.0006$. | **Critical** |
| **High Distractor Overlap ($D_{\text{noise}} \gg D_{\text{signal}}$)** | Uninformative features flatten variance-guided gating, reducing sample stability contrast. | In `SYN-K5-NOISE` ($D=500, K^*=5$), ICC-AutoK predicted $\hat{K}=2$ across **100% of seeds** (42, 101, 202, 303, 404). | **Critical** |
| **Distance Concentration ($D \to \infty$)** | Ratio $(d_{\max} - d_{\min})/d_{\min} \to 0$, destroying spectral contrast. | In Prostate ($D=12,600$), Ovarian ($D=15,154$), Breast ($D=24,481$), ICC-AutoK predicted $\hat{K}=2$, but post-hoc ARI was $\approx 0.005\text{--}0.026$. Correct $K$ for uninformative partition. | **Major** |

---

## 4. QUANTITATIVE BENCHMARK RECONCILIATION

### 4.1 Synthetic Phase Grid Performance Matrix
*(Compiled directly from [`experiments/exp8_unknown_k/data/unknown_k_synthetic_results.csv`](file:///d:/Final%20Year%20Project/experiments/exp8_unknown_k/data/unknown_k_synthetic_results.csv); 30 runs per method across $K^* \in \{2, 3, 4, 5, 8\}$ and $D_{\text{noise}} \in \{0, 100, 1000\}$)*

| Model Order Selector | Exact $K$ Hit Rate | Mean Absolute Error $|\hat{K} - K^*|$ | Mean Post-Hoc ARI | Mean Post-Hoc NMI | Mean Runtime (s) | Rank (Accuracy) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **HDBSCAN\*** | **70.0%** (21/30) | $0.73 \pm 1.28$ | $0.787 \pm 0.35$ | $0.859 \pm 0.27$ | **0.017 s** | **1** |
| **GMM-BIC** | 56.7% (17/30) | $1.13 \pm 1.57$ | $0.781 \pm 0.34$ | $0.866 \pm 0.25$ | 0.039 s | 2 |
| **GMM-ICL** | 56.7% (17/30) | $1.13 \pm 1.57$ | $0.781 \pm 0.34$ | $0.866 \pm 0.25$ | 0.040 s | 2 |
| **Spectral-Eigengap** | 56.7% (17/30) | $1.20 \pm 1.58$ | $0.716 \pm 0.34$ | $0.839 \pm 0.25$ | 0.040 s | 4 |
| **ICC-AutoK-Silhouette** | 53.3% (16/30) | **$0.60 \pm 0.81$** | **$0.834 \pm 0.23$** | **$0.901 \pm 0.16$** | 0.613 s | 5 |
| **ICC-AutoK-PAC (Proposed)**| **16.7%** (5/30) | **$2.37 \pm 2.06$** | $0.639 \pm 0.30$ | $0.752 \pm 0.23$ | 0.613 s | **6 (Dead Last)** |

#### Detailed Failure Pattern of ICC-AutoK-PAC on Synthetic Data:
- For $K^* = 2$: 5 / 6 exact matches.
- For $K^* = 3$: **0 / 6** exact matches (predicted $K \in \{5, 6\}$).
- For $K^* = 4$: **0 / 6** exact matches (predicted $K \in \{2, 5, 6\}$).
- For $K^* = 5$: **0 / 6** exact matches (predicted $K \in \{2, 7\}$).
- For $K^* = 8$: **0 / 6** exact matches (bounced between $K = 2$ and $K = 10$).
- Across all multi-class settings ($K^* \ge 3$), **ICC-AutoK-PAC had a 0.0% exact recovery rate**.

---

### 4.2 Real Oncology Cohort Performance Matrix
*(Compiled from [`experiments/exp8_unknown_k/data/unknown_k_real_results.csv`](file:///d:/Final%20Year%20Project/experiments/exp8_unknown_k/data/unknown_k_real_results.csv))*

| Dataset | $N$ | $D$ | True $K^*$ | ICC-AutoK-PAC ($\hat{K}$, ARI) | ICC-AutoK-Silh ($\hat{K}$, ARI) | GMM-BIC ($\hat{K}$, ARI) | Spectral Eigengap ($\hat{K}$, ARI) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Colon** | 62 | 2,000 | 2 | $\hat{K}=7$ (ARI=0.055) | $\hat{K}=6$ (ARI=0.066) | **$\hat{K}=2$** (ARI=-0.018) | **$\hat{K}=2$** (ARI=-0.023) |
| **SRBCT** | 83 | 2,308 | 4 | $\hat{K}=2$ (ARI=0.200) | $\hat{K}=6$ (**ARI=0.564**) | **$\hat{K}=4$** (ARI=0.041) | $\hat{K}=2$ (ARI=0.107) |
| **CNS** | 60 | 7,129 | 2 | **$\hat{K}=2$** (ARI=0.006) | $\hat{K}=3$ (ARI=-0.021) | $\hat{K}=8$ (ARI=-0.017) | $\hat{K}=6$ (ARI=0.030) |
| **Leukemia** | 72 | 7,129 | 2 | $\hat{K}=7$ (ARI=0.189) | $\hat{K}=3$ (**ARI=0.391**) | $\hat{K}=8$ (ARI=0.110) | **$\hat{K}=2$** (ARI=0.139) |
| **Prostate** | 102 | 12,600 | 2 | **$\hat{K}=2$** (ARI=0.026) | **$\hat{K}=2$** (ARI=0.026) | $\hat{K}=8$ (ARI=0.021) | $\hat{K}=8$ (ARI=0.075) |
| **Ovarian** | 253 | 15,154 | 2 | **$\hat{K}=2$** (**ARI=0.433**) | $\hat{K}=4$ (ARI=0.216) | $\hat{K}=8$ (ARI=0.020) | $\hat{K}=3$ (ARI=-0.000) |
| **Aggregate Mean**| — | — | — | **MAE = 2.00, ARI = 0.152** | **MAE = 1.67, ARI = 0.207** | **MAE = 4.00, ARI = 0.026** | **MAE = 2.17, ARI = 0.055** |

#### Real Cohort Findings:
1. **Silhouette vs. PAC:** ICC-AutoK-Silhouette achieved superior cluster partition quality (Mean ARI $= 0.207$, Mean NMI $= 0.282$) compared to ICC-AutoK-PAC (Mean ARI $= 0.152$, Mean NMI $= 0.233$).
2. **Biological Subtyping Reality:** On Leukemia ($K^*=2$, AML vs ALL), ICC-AutoK-Silhouette predicted $\hat{K}=3$ with high partition accuracy ($\text{ARI} = 0.391$, $\text{NMI} = 0.457$), reflecting the true biological tri-lineage separation (AML, B-cell ALL, T-cell ALL). Conversely, PAC overestimated $\hat{K}=7$.
3. **Parametric Model Degeneracy:** Classical parametric GMM-BIC deteriorated to the upper boundary $\hat{K}=8$ on 4 out of 6 cohorts, yielding a near-zero mean ARI of $0.026$.

---

## 5. AUDIT FINDINGS CATEGORIZED BY SEVERITY

### CRITICAL SEVERITY (Must be remediated before DMKD submission)
1. **[CRIT-01] Ground-Truth Leakage in Candidate Grid:** [`run_unknown_k.py`](file:///d:/Final%20Year%20Project/experiments/exp8_unknown_k/src/run_unknown_k.py#L161) bounds $K_{\max} = \max(6, K_{\text{true}} + 2)$. Any peer reviewer will reject the paper upon inspecting the execution scripts. Search grids must be fixed across all datasets (e.g. $K \in [2, 10]$ or $K \in [2, \min(15, \lfloor N/5 \rfloor)]$).
2. **[CRIT-02] Disconnect Between PAC Theory and Code Implementation:** [`autok.py`](file:///d:/Final%20Year%20Project/src/icc/autok.py#L167) passes unit-normalized spectral eigenvectors $U \in \mathbb{R}^{N \times k}$ to [`compute_anchor_pac`](file:///d:/Final%20Year%20Project/src/icc/autok.py#L46), while the paper claims PAC is evaluated on the row-projected bipartite anchor graph $\tilde{B} \in \mathbb{R}^{N \times L}$. Either the text must be corrected to acknowledge spectral embedding PAC, or the implementation must be rewritten to evaluate $\tilde{B} \tilde{B}^T$.
3. **[CRIT-03] Catastrophic Failure of Advertised PAC Metric:** In synthetic multi-class experiments ($K^* \ge 3$), ICC-AutoK-PAC achieved a **0.0% exact match rate**, ranking last among all tested methods. The paper cannot claim PAC as a primary algorithmic contribution without honestly disclosing this failure.
4. **[CRIT-04] Degeneracy on Null and Imbalanced Data:** $K=1$ is mathematically inaccessible to ICC-AutoK. On imbalanced clusters, uniform anchor sampling starves minority groups.

### MAJOR SEVERITY (Scientific validity & reproducibility)
1. **[MAJ-01] Deceptive Cohort Balance:** 5 of 6 real oncology cohorts have $K^*=2$. In multi-class cohorts (`su2001`, $K^*=11$), the algorithm collapsed completely to $\hat{K}=2$ across all seeds.
2. **[MAJ-02] Missing Promised Baseline Algorithms:** Gap Statistic, X-Means, and Dynamic Tree Cut were specified in [`13_unknown_k_protocol.md`](file:///d:/Final%20Year%20Project/research_audit/13_unknown_k_protocol.md#L60-L69) and [`experiments/exp8_unknown_k/README.md`](file:///d:/Final%20Year%20Project/experiments/exp8_unknown_k/README.md#L15-L21), but omitted from [`run_unknown_k.py`](file:///d:/Final%20Year%20Project/experiments/exp8_unknown_k/src/run_unknown_k.py).
3. **[MAJ-03] Discrepancy in Seed Count:** [`14_unknown_k_results.md`](file:///d:/Final%20Year%20Project/research_audit/14_unknown_k_results.md#L22) claims 5 random seeds (180 evaluations), but [`run_unknown_k.py`](file:///d:/Final%20Year%20Project/experiments/exp8_unknown_k/src/run_unknown_k.py#L358) executed only 2 seeds (`n_reps=2`).

### MINOR SEVERITY (Code quality & hygiene)
1. **[MIN-01] Fallback Triviality:** If `U_emb_` is None, fallback one-hot dot product evaluates identically to 0 or 1, making $\text{PAC} = 0.0$ uniformly for all $k$.
2. **[MIN-02] Occam's Heuristic Bias:** The hardcoded `min_pac + 0.02` threshold systematically favors lower $k$ whenever PAC values are small.

---

## 6. ACTIONABLE REMEDIATION RECOMMENDATIONS FOR DMKD

1. **Reposition Model Selection around Consensus Silhouette:**  
   Reframe the manuscript's narrative: acknowledge that while resampling PAC is historically popular, **Consensus Silhouette on the bipartite anchor graph is significantly more robust** in high-dimensional genomic regimes ($\text{ARI} = 0.834$ vs $0.639$; $\text{MAE} = 0.60$ vs $2.37$). Present PAC transparently as a comparator that over-clusters when local density plateaus occur.
2. **Fix the Leak-Free Search Space:**  
   Update [`experiments/exp8_unknown_k/src/run_unknown_k.py`](file:///d:/Final%20Year%20Project/experiments/exp8_unknown_k/src/run_unknown_k.py) immediately: set candidate grid to a fixed $K \in [2, 10]$ across all datasets and models, completely removing `k_true` from the loop.
3. **Correct the Mathematical Formulation:**  
   In [`src/icc/autok.py`](file:///d:/Final%20Year%20Project/src/icc/autok.py), store $B_{\text{norm}} \in \mathbb{R}^{N \times L}$ on `InvariantCoreConsensusV2` (e.g. `self.B_norm_ = B_norm`), and compute anchor PAC directly from sample pairs in anchor space as originally claimed, or explicitly document that PAC is computed in the normalized spectral embedding space $\mathbb{R}^k$.
4. **Expand Multi-Class Real Cohort Evaluations:**  
   Add more multi-class real cohorts to the primary results table (e.g., `su2001` with $K^*=11$, `novartis` with $K^*=4$, `endometrium` with $K^*=3$) so the evaluation is not artificially dominated by binary datasets.
5. **Add Explicit Limitations Section in DMKD Submission:**  
   Explicitly acknowledge the $K=1$ null-hypothesis boundary and minority-cluster collapse under uniform anchor sampling. Peer reviewers in DMKD will respect this intellectual honesty, whereas hiding it will trigger an immediate rejection.

---
*Report submitted by `roo_reviewer` to Lead Coordinator Agent (`75860bdd-4d81-446c-a143-6e73f3804f09`).*