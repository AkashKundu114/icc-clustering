# ICC Test Suite Documentation

This directory contains the unit, integration, and mathematical verification test suite for the Invariant Core Consensus (ICC-v2) clustering framework and its conformal extension (CICC).

## Quickstart

Run the full test suite with coverage reporting:

```powershell
python -m pytest tests/
```

Run a specific test module:

```powershell
python -m pytest tests/test_consensus.py -v
```

Run tests matching a keyword:

```powershell
python -m pytest tests/ -k "inductive"
```

---

## Test Module Catalog

| Test File | Former Legacy Name | Primary Focus & Verification Scope |
| :--- | :--- | :--- |
| [`test_consensus.py`](file:///D:/icc-clustering/tests/test_consensus.py) | `test_consensus_v2.py` | Full ICC-v2 consensus clustering lifecycle: hyperparameter initialization, alias mappings, fit/predict execution, bipartite sample-anchor graph construction, spectral embedding properties, candidate feature pool modes, and backward-compatible option handling. |
| [`test_core.py`](file:///D:/icc-clustering/tests/test_core.py) | `test_core_and_generators.py` | Foundational algorithmic primitives: synthetic dataset generation across 5 noise models (Gaussian, Student's t, correlated, scaled, sparse), pairwise co-association matrix axioms (symmetry, unit diagonal, $[0, 1]$ bounds), base clustering engines (K-Means, Ward, Spectral, FCM), canonical relabeling, and legacy ICC-v1 execution. |
| [`test_projection.py`](file:///D:/icc-clustering/tests/test_inductive_projection.py) | `test_inductive_projection.py` | Geometry-calibrated out-of-sample inductive projection: anchor centroid computation, fail-fast uncalibrated model errors, discrete cluster prediction, posterior probability calibration ($\sum_k P(c_k \mid x) = 1$), temperature scaling entropy modulation, and noise resilience of invariant subspace gating ($d_{\text{noise}} \gg d_{\text{signal}}$). |
| [`test_anchors.py`](file:///D:/icc-clustering/tests/test_anchor_fidelity.py) | `test_anchor_fidelity.py` | Anchor approximation fidelity: exact $N \times N$ consensus execution, bounded spectral approximation discrepancy ($|\Delta \text{ARI}| < 0.25$), and end-to-end sample size scaling sweep verification. |
| [`test_multiclassifier.py`](file:///D:/icc-clustering/tests/test_exp1_multiclassifier.py) | `test_exp1_multiclassifier.py` | Multi-classifier inductive generalization: parameter configuration across downstream classifiers (SVM, RF, MLP, KNN), balanced core subset distillation, and generalization benchmark sweep validation. |
| [`test_conformal.py`](file:///D:/icc-clustering/tests/test_cicc.py) | `test_cicc.py` | Conformal Inductive Core Consensus (CICC): non-parametric False Discovery Rate (FDR) control via knockoff/decoy feature gating, finite-sample split-conformal cluster coverage guarantees ($1 - \alpha$), and dynamic consensus memory consolidation. |
| [`test_profiling.py`](file:///D:/icc-clustering/tests/test_aspp.py) | `test_aspp.py` | Anchor-Space Perturbation Profiling (ASPP): configuration defaults and overrides, Perturbation Stability Index (PSI) calculation, categorical reliability classification (`globally_invariant`, `conditionally_invariant`, `perturbation_fragile`, `ambiguous`), inductive stability-weighted confidence ($C = M \cdot (1 - \text{PSI})$), and technical batch perturbation profiling. |
| [`test_baselines.py`](file:///D:/icc-clustering/tests/test_baselines.py) | *(Retained)* | Central baseline model registry and dispatcher: category categorization (single, consensus, deep, anchor), dynamic dispatch, FCAG and FastMVC anchor graph baselines, Deep Embedded Clustering (DEC) autoencoders, and `ModelMetadata` hybrid integer/dictionary encapsulation. |
| [`test_datasets.py`](file:///D:/icc-clustering/tests/test_datasets.py) | *(Retained)* | Benchmark dataset registry and loaders: enumeration of all 13 canonical datasets across genomics, text, audio, hyperspectral, vision, and scRNA-seq; metadata verification against `configs/datasets.yaml`; tensor loading; missing value imputation; and z-score standardization. |
| [`test_edge_cases.py`](file:///D:/icc-clustering/tests/test_edge_cases.py) | *(Retained)* | Boundary condition and numerical stability tests: zero-variance / constant features, identical duplicate samples, micro sample sizes ($N=10, K=2$), extreme aspect ratios ($D/N = 250$), degenerate metric edge cases (all-one or all-distinct clusters), and MCAR missing data injection. |
| [`test_metrics.py`](file:///D:/icc-clustering/tests/test_metrics.py) | *(Retained)* | Consensus clustering evaluation metrics: bijective label permutation invariance, null-model statistical independence ($ARI \approx 0$), dual-backend numerical parity between scikit-learn and pure NumPy/SciPy fallbacks, and bootstrap percentile confidence intervals. |

---

## Detailed Test Logic & Mathematical Rationale

### 1. `test_consensus.py`
- **Ensemble Aggregation:** Validates that $M$ base partitions $\Pi = \{\pi_1, \dots, \pi_M\}$ are mapped onto $L$ selected anchor points rather than the dense $N \times N$ co-association matrix.
- **Subspace Gating:** Verifies that feature variance and stability-weighted scores rank dimensions so that uninformative noise channels are filtered out prior to spectral embedding.
- **Embedding Invariance:** Checks that spectral coordinates derived from both the normalized symmetric Laplacian and bipartite transfer-cut formulations are strictly finite.

### 2. `test_core.py`
- **Noise Generator Invariants:** Validates synthetic clustering across isotropic Gaussian, Student's $t$ ($\nu=3$ heavy tails), AR(1) correlated, heteroscedastic scaled, and high-kurtosis sparse noise distributions.
- **Algebraic Axioms of Co-association:** Explicitly verifies:
  $$\forall i, \; S_{ii} = 1.0, \quad S_{ij} = S_{ji}, \quad 0.0 \le S_{ij} \le 1.0$$
- **Canonical Labeling:** Verifies relabeling functions eliminate cluster index permutation symmetries by assigning labels based on the first occurrence in the observation vector.

### 3. `test_projection.py`
- **Closed-Form Inductive Inference:** Tests out-of-sample projection without retraining:
  $$c^*(x_{\text{new}}) = \arg\min_{k} \|x_{\text{new}}[\mathcal{S}] - \mu_k[\mathcal{S}]\|_2^2$$
- **Softmax Posterior Calibration:** Validates probability simplex mapping:
  $$P(c_k \mid x_{\text{new}}) = \frac{\exp(-\|x_{\text{new}}[\mathcal{S}] - \mu_k[\mathcal{S}]\|_2^2 / T)}{\sum_{j=1}^K \exp(-\|x_{\text{new}}[\mathcal{S}] - \mu_j[\mathcal{S}]\|_2^2 / T)}$$
- **Noise Accumulation Prevention:** Demonstrates that gating on selected features $\mathcal{S}$ achieves higher or equal Adjusted Rand Index compared to unguided full-space Euclidean projection when $D_{\text{noise}} \gg D_{\text{signal}}$.

### 4. `test_anchors.py`
- **Approximation Bound:** Validates that anchor-based bipartite spectral clustering closely approximates exact dense co-association spectral clustering within a bounded tolerance ($|\text{ARI}_{\text{exact}} - \text{ARI}_{\text{reduced}}| < 0.25$).
- **Complexity Advantage:** Verifies that anchor clustering completes in $O(N \cdot L)$ time rather than $O(N^2)$ time.

### 5. `test_conformal.py`
- **Finite-Sample Marginal Coverage:** Validates split conformal prediction calibration, verifying empirical test coverage:
  $$\mathbb{P}(Y_{n+1} \in \mathcal{C}(X_{n+1})) \ge 1 - \alpha$$
- **Decoy Feature Gating:** Verifies knockoff-style decoy features control empirical False Discovery Rate below target $q=0.15$.

### 6. `test_profiling.py`
- **Perturbation Stability Index (PSI):** Measures mean cluster retention under multi-family perturbations:
  $$\text{PSI}_k = \frac{1}{|\mathcal{F}|} \sum_{f \in \mathcal{F}} \text{Stability}_f(k)$$
- **Modulated Prediction Confidence:** Confirms that inductive prediction confidence is strictly bounded by raw classification margin:
  $$\text{Confidence}(x) = \text{Margin}(x) \cdot (1 - \text{PSI}_{c^*(x)}) \le \text{Margin}(x)$$
