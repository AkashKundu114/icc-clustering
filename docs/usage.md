# Usage Guide

## Quick Start

### 1. Invariant Core Consensus (ICC)

```python
import numpy as np
from icc import ICC, evaluate_all

# Generate or load high-dimensional data (N=150, D=500, K=3)
X = np.random.randn(150, 500)
y_true = np.repeat([0, 1, 2], 50)

# Instantiate and fit ICC
model = ICC(
    n_clusters=3,
    n_base_models=25,
    n_anchors=50,
    random_state=42,
)
labels = model.fit_predict(X)

# Evaluate results
metrics = evaluate_all(y_true, labels)
print("Adjusted Rand Index (ARI):", metrics["ari"])
```

### 2. Out-of-Sample Inductive Prediction

ICC also exposes an inductive prediction method for assigning new samples using the fitted model:

```python
# Unseen query samples (N_test=20, D=500)
X_test = np.random.randn(20, 500)

# Predict cluster labels for new instances
test_labels = model.predict(X_test)
```

### 3. Stability Profiling with ASPP

```python
from icc import AnchorSpacePerturbationProfiler, ASPPConfig

config = ASPPConfig(n_bootstrap=10)
profiler = AnchorSpacePerturbationProfiler(config=config)
summary = profiler.profile(model, X, k=3, seed=42)
print("Mean PAC Stability:", summary.mean_pac)
```

## Running Benchmarks from CLI

Execute benchmarks using YAML configuration:

```bash
python scripts/run.py --config configs/default.yaml
```

Evaluate outputs:

```bash
python scripts/evaluate.py --results results/experiments/run_*.json
```
