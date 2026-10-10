---
name: Bug Report
about: Create a report to help us improve ICC-v2
title: '[BUG] '
labels: bug
assignees: ''
---

## Describe the Bug
A clear and concise description of what the bug is.

## Steps to Reproduce
Steps to reproduce the behavior:
1. Call `model = InvariantCoreConsensusV2(...)`
2. Execute `labels = model.fit_predict(X)` with dimensions `N=..., D=...`
3. See error or unexpected output

## Minimal Reproducing Example
```python
import numpy as np
from icc import InvariantCoreConsensusV2

X = np.random.randn(50, 100)
model = InvariantCoreConsensusV2(n_clusters=3)
model.fit_predict(X)
```

## Expected Behavior
A clear and concise description of what you expected to happen.

## Environment & System Information
- OS: [e.g. Linux Ubuntu 22.04 / Windows 11 / macOS Sonoma]
- Python Version: [e.g. 3.10.12, 3.12.3]
- NumPy Version: [e.g. 1.26.4]
- Scikit-Learn Version: [e.g. 1.4.1]
- Hardware (CPU, RAM): [e.g. 16 GB RAM, 8-core CPU]

## Additional Context
Add any other context about the problem here (e.g., stack trace).
