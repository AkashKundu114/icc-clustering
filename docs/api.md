# ICC-v2 Python API Reference

**Canonical Manuscript Title:** When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination  
**Academic Lineage:** Initial University Allotment Title: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data" (`CSE_PROJECT_68`, Faculty Mentor: Prof. Kalyan Kumar Das); Early Proposal Blueprint: "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes"  
**Target Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI), document class `sn-jnl.cls` (`sn-mathphys-num.bst`)  
**Canonical Active Release:** v2.1.0  
**Repository Package:** `icc` (v2.1.0) and `cicc` (Conformal Inductive Consensus Clustering)

The `icc` and `cicc` packages provide an unsupervised, scikit-learn compatible clustering estimator, split-conformal prediction sets, target-decoy feature selection, and episodic semantic memory for high-dimensional noise regimes ($D \gg N$).

---

## 1. Primary Estimator: `ICC` / `InvariantCoreConsensusV2`

```python
from icc import ICC
# or
from icc.consensus_v2 import InvariantCoreConsensusV2
```

### Constructor Signature

```python
ICC(
    n_clusters: int = 3,
    n_base_models: int = 25,
    n_anchors: int = 40,
    core_quantile: float = 0.50,
    subspace_rate: float = 0.30,
    beta: float = 2.0,
    pool_frac: float = 0.20,
    embedding: str = "transfer_cut",
    dense_threshold: int = 2000,
    base_clusterer: str = "auto",
    enable_aspp: bool = False,
    aspp_config: Optional[ASPPConfig] = None,
    random_state: int = 42,
    pool_mode: str = "legacy",
    pool_mad_c: float = 1.0,
    pool_alpha: float = 0.05,
)
```

### Parameters

- `n_clusters` (int, default=3): Target number of clusters ($K$).
- `n_base_models` (int, default=25): Number of ensemble base partitions ($M$).
- `n_anchors` (int, default=40): Anchor budget ($L$).
- `core_quantile` (float, default=0.50): Stability quantile threshold ($\tau_{\text{core}}$) for certifying invariant core samples.
- `subspace_rate` (float, default=0.30): Subspace draw fraction from active candidate pool.
- `embedding` (str, default="transfer_cut"): Spectral bipartite projection method (`"transfer_cut"` or `"legacy"`).
- `dense_threshold` (int, default=2000): Sample threshold below which exact co-association is used.
- `enable_aspp` (bool, default=False): Enable Anchor-Space Perturbation Profiling.
- `random_state` (int, default=42): Deterministic pseudo-random seed.
- `pool_mode` (str, default="legacy"): Feature screening mode (`"legacy"`, `"null_calibrated"`, `"robust"`, `"gauss"`).

### Methods

- `fit(X, batch_vector=None) -> ICC`: Fits the ensemble and anchor graph on feature matrix `X` of shape `(N, D)`.
- `fit_predict(X, batch_vector=None) -> np.ndarray`: Fits model and returns cluster label array of shape `(N,)` with integer labels in `[0, K-1]`.
- `predict(X_new, subspace=True) -> np.ndarray`: Inductive out-of-sample projection of unseen query matrix `(N_new, D)` onto geometry-calibrated centroids.
- `predict_proba(X_new, subspace=True, temperature=1.0) -> np.ndarray`: Soft cluster membership probabilities of shape `(N_new, K)`.
- `transform(X=None) -> np.ndarray`: Returns the low-dimensional spectral embedding coordinates of shape `(N, K)`.

### Attributes

- `labels_`: Cluster labels for training points `(N,)`.
- `stability_`: Sample-level co-association stability scores `(N,)`.
- `core_mask_`: Boolean mask indicating certified invariant core instances `(N,)`.
- `core_indices_`: Indices of certified invariant core samples.
- `anchor_indices_`: Indices of sampled anchor instances `(L,)`.
- `selected_features_`: Active feature pool selected by VSSG screening.
- `anchor_centroids_`: Geometry-calibrated cluster centroids `(K, D)`.
- `U_emb_`: Normalized spectral embedding matrix `(N, K)`.

---

## 2. Dataset Registry & Loaders

```python
from icc.datasets.registry import load_dataset, list_datasets, get_dataset_info
```

- `load_dataset(name: str, cache_dir: str = "data/cache", force_download: bool = False)`:
  Loads preprocessed feature matrix `X`, label vector `y`, and descriptor dictionary `metadata`.
- `list_datasets(enabled_only: bool = True)`:
  Returns list of registered dataset metadata containers.

---

## 3. Evaluation Metrics

```python
from icc.metrics import evaluate_all, adjusted_rand_score, normalized_mutual_info_score
```

- `evaluate_all(y_true, y_pred) -> Dict[str, float]`:
  Computes ARI, NMI, AMI, V-Measure, and Fowlkes-Mallows Index in a unified dictionary.

---

## 4. Conformal Inductive Consensus Clustering (`cicc`)

The `cicc` module provides finite-sample distribution-free uncertainty quantification, target-decoy feature selection with False Discovery Rate (FDR) control, and memory consolidation.

```python
from cicc import (
    ConformalClusterer,
    ConformalResult,
    DecoyFeatureGating,
    InductiveConsensusClusterer,
    InductiveConsensusMemory,
)
```

### `InductiveConsensusClusterer`

Unified pipeline combining decoy feature gating, anchor consensus, and split-conformal calibration.

```python
InductiveConsensusClusterer(
    n_clusters: int = 4,
    n_anchors: int = 40,
    n_base_models: int = 20,
    subspace_rate: float = 0.50,
    enable_decoy_gating: bool = True,
    fdr_target: float = 0.10,
    alpha: float = 0.10,
    random_state: int = 42,
)
```

- `fit(X, y_train=None)`: Fits anchor consensus graph and calibrates conformal prediction cutoffs on internal splits.
- `predict_conformal(X_query) -> ConformalResult`: Returns prediction set assignments, posterior probabilities, and singleton/ambiguous/abstention classifications.

### `ConformalClusterer`

General split-conformal wrapper providing finite-sample coverage guarantees ($1 - \alpha$).

- `fit_calibrate(X_disc, labels_disc, X_cal, labels_cal)`: Fits cluster prototypes on discovery set and calibrates non-conformity quantile $\hat{q}$ on calibration set.
- `predict_set(X_query, ground_truth=None) -> ConformalResult`: Evaluates query points to yield candidate prediction sets $C(x)$.

### `DecoyFeatureGating`

False Discovery Rate (FDR) controlled feature selection via target-decoy / knockoff competition:

- `fit(X, labels) -> DecoyFeatureGating`: Computes mirror statistics $W_d = |T_d| - |\tilde{T}_d|$ across true features and permuted/knockoff decoys.
- `transform(X) -> np.ndarray`: Filters feature matrix to retained candidate features at nominal FDR threshold.

### `InductiveConsensusMemory`

Dynamic episodic memory and semantic clustering buffer with instantaneous $\mathcal{O}(L)$ inductive routing and conformal novelty detection.

- `store(text, embedding, metadata=None) -> MemoryItem`: Indexes new memory item, dynamically consolidating into existing cluster or triggering novel cluster creation upon conformal abstention ($C(x) = \emptyset$).
- `query_similar(embedding, top_k=5) -> List[MemoryItem]`: Retrieves nearest indexed memory items.
