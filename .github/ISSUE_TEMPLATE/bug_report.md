---
name: Bug Report
about: Create an issue to report a software bug or unexpected behavior in ICC-v2
title: '[BUG] '
labels: bug
assignees: ''
---

## Describe the Bug
A clear and concise description of the bug encountered.

## Steps to Reproduce
Steps to reproduce the behavior:
1. Initialize the estimator: `model = ICC(n_clusters=..., n_base_models=25, ...)`
2. Call `labels = model.fit_predict(X)` with dimensions `N=..., D=...`
3. Execute out-of-sample prediction: `pred = model.predict(X_query)`
4. Encountered error, exception, or unexpected clustering partition.

## Minimal Reproducible Example (MRE)
```python
import numpy as np
from icc import ICC

# Generate minimal synthetic high-dimensional array
rng = np.random.default_rng(42)
X = rng.standard_normal((60, 200))

# Instantiate and fit estimator
model = ICC(n_clusters=3, n_base_models=25, random_state=42)
labels = model.fit_predict(X)

# Out-of-sample projection
X_query = rng.standard_normal((10, 200))
pred = model.predict(X_query)
```

## Expected Behavior
A concise description of what you expected to happen according to documentation or mathematical derivations.

## Environment & System Information
- OS: [e.g., Ubuntu 22.04 LTS / Windows 11 / macOS Sonoma]
- Python Version: [e.g., 3.10.12, 3.11.8, 3.12.3]
- NumPy Version: [e.g., 1.26.4]
- SciPy Version: [e.g., 1.12.0]
- Scikit-Learn Version: [e.g., 1.4.1]
- Single-Thread Environment Flags: `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`
- Hardware Architecture: [e.g., x86_64, Apple Silicon M2, 16 GB RAM]

## Additional Context & Stack Trace
Add any additional context, error logs, or full stack traces below:
```
<paste stack trace here>
```
