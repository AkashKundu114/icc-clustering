# ICC-v2 Python API Reference

The `icc` package provides an unsupervised, scikit-learn compatible clustering estimator for high-dimensional noise regimes ($D \gg N$).

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
