# nullconsensus

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

**Permutation-Null Calibrated Consensus Clustering for High-Dimensional Manifolds.**

---

## Overview
Consensus clustering often suffers from the **stability-accuracy trap**: under high-dimensional isotropic distractor noise ($D \gg N$), random base partitions converge stably on arbitrary noise geometries, producing falsely confident partitions with zero Adjusted Rand Index.

`nullconsensus` resolves this fundamental challenge through three coupled mechanisms:
1. **Permutation-Null Feature Saliency:** Tests empirical bimodality against an independent column-permuted reference null dataset to filter noise dimensions with finite-sample Type-I error control.
2. **Saliency-Weighted Soft Subspace Sampling:** Samples base feature subsets according to null-calibrated weights ($p_d \propto \exp(z_d / \tau)$), eliminating the seed bimodality collapse inherent to uniform random subspaces.
3. **Null-Referenced Stability for $K$ Selection:** Measures cluster consensus stability against a permutation-null baseline ($\Delta\text{PAC} = \text{PAC}_{\text{null}} - \text{PAC}_{\text{real}}$), enabling automated, data-adaptive cluster count discovery.

---

## Installation
```bash
pip install nullconsensus
# Or editable developer install:
git clone https://github.com/AkashKundu114/nullconsensus.git
cd nullconsensus
pip install -e ".[dev]"
```

---

## 10-Line Quickstart
```python
import numpy as np
from nullconsensus import NullConsensus

# 1. Generate noisy high-dimensional data (N=150, D=500, K=3)
rng = np.random.default_rng(42)
X = rng.standard_normal((150, 500))
X[:50, :15] += 3.0
X[50:100, :15] -= 3.0

# 2. Fit estimator with permutation-null calibration
model = NullConsensus(n_clusters=3, n_base_models=25, n_null_permutations=10, random_state=42)
labels = model.fit_predict(X)

# 3. Predict out-of-sample query instances
X_query = rng.standard_normal((5, 500))
X_query[:, :15] += 3.0
print("Cluster assignments:", model.predict(X_query).tolist())
```

---

## License
MIT License. Developed by Akash Kundu et al. (Techno India University).
