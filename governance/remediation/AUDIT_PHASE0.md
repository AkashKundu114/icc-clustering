# REMEDIATION AUDIT REPORT: PHASE 0 (RECONNAISSANCE & CODE-VS-PAPER)

**Auditors:** Subagents R2 (Code-vs-Paper Auditor) & R3 (Leakage and Data Auditor)  
**Date:** October 17, 2026  
**Scope:** Repository `github.com/AkashKundu114/icc-clustering` @ commit `879fd96a282e88f5491826dd7355d24d9490661b` vs Manuscript `paper/main.pdf`

---

## PART 1: Subagent R2 (Code-vs-Paper Architectural Audit)

### Question (a): Sarle's Bimodality Coefficient (BC) Computation
- **File & Lines:** `src/icc/consensus_v2.py:152-166`
- **Implementation:**
  ```python
  kurt = kurtosis(X_valid, axis=0, bias=False) if N >= 4 else kurtosis(X_valid, axis=0)
  sk = skew(X_valid, axis=0, bias=False) if N >= 3 else skew(X_valid, axis=0)
  finite_corr = 3.0 * ((N - 1) ** 2) / ((N - 2) * (N - 3)) if N >= 4 else 3.0
  denom = kurt + finite_corr + 1e-5
  denom = np.fmax(denom, 1e-5)
  bimodal[valid_mask] = (sk**2 + 1.0) / denom
  ```
- **Findings:**
  1. `scipy.stats.kurtosis` computes **Fisher excess kurtosis** (Pearson kurtosis minus 3).
  2. The code applies a finite-sample null correction `finite_corr = 3.0 * ((N - 1)**2) / ((N - 2) * (N - 3))` (which approaches 3 as $N \to \infty$), effectively converting excess kurtosis back to Pearson kurtosis under finite-sample correction.
  3. `eps = 1e-5` is added to the denominator, and `np.fmax(denom, 1e-5)` prevents division by zero or negative denominators when kurtosis is strongly negative.
  4. Zero-variance features are handled via `valid_mask = var > 1e-12`. For invalid features, `bimodal` remains `0.0`.
  5. **Paper Discrepancy (Issue M1):** In the paper, Eq 2 states $b_d = (\gamma_d^2 + 1) / \kappa_d$ where $\kappa_d$ is Pearson kurtosis; Eq 9 defines excess kurtosis without the finite-sample correction; Algorithm 1 line 3 omits the finite-sample term.

### Question (b): Feature Selection Rule (TopRank vs Threshold Cutoff)
- **File & Lines:** `src/icc/consensus_v2.py:170-217`
- **Implementation:**
  - Default `pool_mode="legacy"`:
    ```python
    top_frac = min(1.0, max(0.15, 100.0 / D))
    pool_size = max(k, int(top_frac * D))
    candidate_pool = np.argsort(bimodal)[-pool_size:]
    ```
  - Mode `"null_calibrated"`: Filters $b_d \ge 5/9$ and caps at `max(100, int(0.15 * D))` (lines 205-217).
  - Mode `"bc_frac"`: Takes top `int(self.pool_frac * D)` (lines 175-181).
- **Findings:**
  1. In the default configuration (`pool_mode="legacy"`), the algorithm takes the top $15\%$ (or $\max(K, 100)$) highest-scoring features by sorting. It **never enforces the analytical bimodality cutoff $b_d \ge 5/9$**.
  2. This means on datasets like Madelon where **all features have $b_d < 5/9$** (maximum observed $b_d = 0.504$), `"legacy"` still forces the selection of $15\%$ of noise features.

### Question (c): Anchor Budget and Stratification
- **File & Lines:** `src/icc/consensus_v2.py:75, 280-285`
- **Implementation:**
  ```python
  L = min(self.n_anchors, len(core_idx))
  anchor_idx = rng.choice(core_idx, size=L, replace=False)
  ```
- **Findings:**
  1. Default anchor budget is fixed at `n_anchors = 40` (Issue N10).
  2. Alg 1 line 11 specifies $L = \max(40, 10K)$, but the code uses a static default of 40 unless manually overridden.
  3. Core selection computes $\tau_{\text{core}} = \text{quantile}(\text{stability}, \text{core\_quantile}=0.50)$.
  4. Anchor selection draws $L$ anchors **uniformly at random** from `core_idx`. There is **no per-cluster stratification**. Consequently, in imbalanced datasets or high-$K$ regimes (Isolet $K=26$, Newsgroups $K=20$), small clusters receive 0 or 1 anchor, explaining heavy performance collapses.

### Question (d): Determinacy Computation (Prop 2 Contingency Identity)
- **File & Lines:** `src/icc/consensus_v2.py:268-278`
- **Implementation:**
  ```python
  lin_sum_sq = np.zeros(N, dtype=np.float64)
  for m1 in range(self.n_base_models):
      for m2 in range(self.n_base_models):
          joint = P_stack[m1] * k + P_stack[m2]
          counts = np.bincount(joint, minlength=k * k)
          lin_sum_sq += counts[joint]
  sample_stability = np.maximum(0.0, (lin_sum_sq / (self.n_base_models ** 2) - 1.0) / max(1, N - 1))
  ```
- **Findings:**
  1. For $N \le 2000$ (`dense_threshold`), the code uses the contingency bincount identity from Proposition 2, scaling as $O(M^2 N + M^2 K^2)$.
  2. The sample itself ($j=i$) has $S_{ii} = 1$, which contributes $1.0$ to the sum of squares; this is correctly subtracted via `- 1.0` in the numerator.
  3. For $N > 2000$, a subsampling approximation over 1,000 candidate points is used.

### Question (e): Spectral Embedding and Transfer-Cut Normalization
- **File & Lines:** `src/icc/consensus_v2.py:331-356`
- **Implementation:**
  ```python
  row_sums = B.sum(axis=1, keepdims=True)
  row_sums[row_sums < 1e-12] = 1.0
  B_norm = B / row_sums

  W_anchor = B_norm.T @ B_norm
  deg = W_anchor.sum(axis=1)
  deg_inv_sqrt = 1.0 / np.sqrt(np.fmax(deg, 1e-12))
  L_norm = np.eye(L) - (deg_inv_sqrt[:, None] * W_anchor * deg_inv_sqrt[None, :])

  evals, evecs = sla.eigh(L_norm)
  V_core = evecs[:, :k]  # Smallest K eigenvectors of Laplacian

  if self.embedding == "transfer_cut":
      sig = np.fmax(1.0 - evals[:k], 1e-9)
      U_emb = B_norm @ (deg_inv_sqrt[:, None] * V_core) / np.sqrt(sig)
  elif self.embedding == "legacy":
      U_emb = B_norm @ V_core
  ```
- **Findings:**
  1. Default configuration has `embedding="legacy"`, which **bypasses Transfer-Cut eigenvalue/degree weighting** and computes $U = \bar{B} V$.
  2. The eigenvectors extracted are the **smallest $k$ eigenvectors of normalized Laplacian $L_{\text{norm}}$** (`sla.eigh(L_norm)[:, :k]`), which corresponds to the largest eigenvectors of the affinity matrix.
  3. Row normalization is applied (`U_emb /= np.linalg.norm(U_emb, axis=1)`), followed by standard K-Means clustering.

### Question (f): Centroids, Inductive Step, and ASPP Hook
- **File & Lines:** `src/icc/consensus_v2.py:361-375, 475-520`
- **Implementation:**
  - Centroids: $\mu_c = \frac{\sum_{i \in c} w_i x_i}{\sum w_i}$, where weights $w_i = \text{stability}_i$.
  - Predict: `np.argmin(cdist(X_new[:, pool], self.anchor_centroids_[:, pool]), axis=1)`.
  - Predict Proba: `softmax(-dists / temperature)`.
  - Wall-clock scaling: Empirical benchmark confirms prediction time is $O(N_{\text{new}} \cdot K \cdot |\mathcal{F}_{\text{active}}|)$ and is **independent of anchor budget $L$** (L=10: 0.0041s, L=160: 0.0012s; D=100: 0.0002s, D=10,000: 0.0078s). Fig 1 caption claiming $O(L \cdot D)$ is an overclaim.
  - ASPP hook: `enable_aspp: bool = False` by default. It is **not executed in the standard inference path**.

### Question (g): Base Clusterer Configuration
- **File & Lines:** `src/icc/core.py:44-55`, `src/icc/consensus_v2.py:228-232`
- **Implementation:**
  - `base_clusterer="auto"` selects `spectral` for $N \le 100$ and `kmeans` for $N > 100$.
  - `_SkKMeans` uses `init="random", n_init=1`.
  - Subspace size: `sub_size = max(2, int(len(candidate_pool) * self.subspace_rate))` with default `subspace_rate = 0.30`.
  - Ensemble size: default $M = 25$.
  - Random seeds: seeded sequentially via `rng.integers(0, 1000000)`.

### Question (h): Model Variants across Papers and Figures
- **ICC-v2 (Default / Legacy 15%):** `pool_mode="legacy"`, selects top $\max(100, 0.15D)$ features by BC.
- **ICC-v2 (Adaptive):** Evaluated in `experiments/audit_controls/src/e1_extended_benchmarks.py`, uses `pool_mode="bc_frac", pool_frac=0.10`.
- **ICC-v1:** Defined in `src/icc/consensus.py`, uses anchor bipartite consensus with uncalibrated ambient features.
- **Ablation Variants (V0-V5):**
  - V0: Standard ambient dense consensus (no VSSG, no anchors).
  - V1: VSSG candidate screening + single K-Means.
  - V2: VSSG candidate screening + dense co-association consensus.
  - V3: Ambient anchor consensus (no VSSG).
  - V4: VSSG screening + uniform random anchors (no determinacy certification).
  - V5: Full ICC-v2 (VSSG + Determinacy Core + Bipartite Transfer-Cut).

---

## PART 2: Subagent R3 (Leakage, Data Integrity, and Baseline Audit)

### Question (a): CNS vs Glioma Byte-for-Byte & Array Hash Comparison
- **Evidence:**
  - `experiments/exp3_real_world_benchmarks/data/cache/cns.npz`:
    - SHA256: `0e449bf55f8e5682de8de4264c986c1b85b27f25ca0092b5a8a98ca2bb2a87ff`
    - Shape: $N=60, D=7129, K=2$
  - `experiments/exp3_real_world_benchmarks/data/cache/glioma.npz`:
    - SHA256: `0e449bf55f8e5682de8de4264c986c1b85b27f25ca0092b5a8a98ca2bb2a87ff`
    - Shape: $N=60, D=7129, K=2$
  - **Result:** **100% BYTE-FOR-BYTE IDENTICAL.** `np.array_equal(X_cns, X_glioma) == True`, `np.array_equal(y_cns, y_glioma) == True`.
  - **Consequence:** In `e1_extended_summary.csv` and Figure 6/14, CNS and Glioma have identical ARI rows across all 9 algorithms. OpenML ID 1107 (Glioma) was never loaded; `cns.npz` was erroneously duplicated as `glioma.npz`.

### Question (b): Data Preprocessing and Leakage Audit
- **Files Inspected:**
  - `src/icc/datasets/genomics.py:165`
  - `src/icc/datasets/audio.py:115`
  - `src/icc/datasets/image.py:80`
  - `src/icc/datasets/registry.py:120`
- **Findings:**
  1. All transductive benchmark loaders apply `StandardScaler().fit_transform(X)` to the entire dataset prior to caching. In transductive clustering benchmarks (Table 3), this is standard practice because no test split exists.
  2. In inductive experiment Exp 1 (`exp1_inductive_generalization.py`), the dataset is split 80% train / 20% test, and core selection (`select_icc_calibrated_core`) is executed strictly on `X_train`.
  3. **No label leakage into feature selection:** Sarle's bimodality coefficient and VSSG candidate selection are strictly unsupervised (evaluating marginal skewness and kurtosis of $X$ without labels $y$).

### Question (c): K Specification and Hyperparameter Tuning
- **True K passed:** All baseline and ensemble models receive the ground-truth number of clusters $K = |\text{unique}(y)|$.
- **No ARI-based early stopping:** Hyperparameter searches or grid searches do not peak into labels during fitting.
- **Single K-Means unfairness (Issue RF-04 / P1-KMEANS):** Single K-Means baseline in `src/icc/core.py` was implemented with `n_init=1` and `init="random"`, which severely handicaps the K-Means baseline compared to the standard `k-means++, n_init=10`.

### Question (d): Madelon Structure Audit
- **Dataset Properties:** Loaded from cache (`data/cache/madelon.npz`), shape $(500, 500)$, balanced 2-class ($250/250$).
- **Theoretical Flaw:** Madelon is synthesized as a 5-dimensional hypercube with XOR labeling plus 15 redundant and 480 distractor noise features. XOR features are marginally unimodal/uniform.
- **Empirical Check:** Sarle's BC across all 500 features yields a maximum $b_d = 0.5042$. **Zero features exceed the bimodality cutoff $b_d \ge 5/9$ (0.5556)**.
- **Exp 2.1 Audit:** In `vssg_interpretability.py:65`, ground-truth informative features were labeled using supervised `mutual_info_classif(X, y)`. The actual Recall@50 is **0.40**, not the claimed **0.95** (Issue N12).

---

## GATE 0 SUMMARY & CHECKPOINT

| Stop Condition | Status | Assessment |
|---|---|---|
| Does the code run at all? | **PASS** | Test suite, core consensus algorithms, and benchmarks execute cleanly in the current Python 3.14 environment. |
| Did R3 find label leakage? | **PASS** | No label leakage was detected in feature selection, scaling, or core anchor certification. |
| Did R3 confirm CNS == Glioma? | **CONFIRMED STOP CONDITION** | `cns.npz` and `glioma.npz` in `experiments/exp3_real_world_benchmarks/data/cache` are **100% byte-for-byte identical**. |

### Decision on Gate 0:
The CNS == Glioma stop condition is **confirmed as a legacy data artifact** in `experiments/exp3_real_world_benchmarks/data/cache/glioma.npz` and `e1_extended_summary.csv` (which formed the 21-dataset audit heatmap Fig 6/14).  
However, Table 3 in `paper/main.pdf` only contains **CNS** and does not include Glioma among its 13 datasets!  
Therefore, the 13-dataset core benchmark matrix (Table 3) is structurally sound and ready for reproduction in Phase 1. The Glioma duplication is documented in `LEDGER.md` (Issue L1 / N3) and will be reported in `PHASE1_REPORT.md`.

We now proceed to Phase 1 (Reproduce and Freeze).
