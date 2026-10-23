# Loop: Data Pipeline Integrity & Leakage Detection Loop

Use this loop to rigorously audit data ingestion, cross-validation boundaries, and feature transformations across all benchmark suites to guarantee complete scientific validity and prevent optimistic evaluation bias.

---

## Operating Budget & Setup
- **Maximum Iterations:** 3 iterations per run.
- **Assigned Subagent Personas:**
  - `Leakage Auditor (roo_reviewer)`: Inspects train/test split points, transformer pipelines, and label access.
  - `Data Governance Specialist (roo_ask)`: Audits raw benchmark licenses, sources, and SHA-256 hashes.
  - `Pipeline Engineer (roo_coder)`: Implements strict scoping and split verification assertions.

---

## Iteration Protocol

### 1. Split Isolation Verification
For every benchmark experiment (`experiments/`):
- Verify that test data partitions are created before any feature normalization, graph construction, or anchor selection:
  ```python
  # CORRECT: Transformers fit ONLY on train split
  scaler.fit(X_train)
  X_train_scaled = scaler.transform(X_train)
  X_test_scaled = scaler.transform(X_test)
  ```
- **Fail condition:** Any call to `scaler.fit(X)` or `pca.fit(X)` prior to splitting is flagged as a critical leakage violation.

### 2. Unsupervised Label Boundary Audit
- Audit consensus clustering pipelines to guarantee that ground-truth labels ($y$) are never accessed during:
  - Consensus matrix construction.
  - Adaptive spectral projection (ASPP).
  - Out-of-sample inductive projection.
- Labels may only be accessed at the final evaluation step when computing external cluster validity indices (ARI, NMI).

### 3. Raw Data Immutability Check
- Inspect `data/raw/` files:
  - Verify file modification timestamps and check SHA-256 hashes against canonical manifests (`docs/DATA.md`).
  - Guarantee that no preprocessing script writes back into `data/raw/`.

### 4. Automated Split Integrity Test
- Run a targeted leakage regression test:
  - Introduce synthetic probe features with known correlations on test sets and assert that the trained model gains zero predictive advantage from them during training.

### 5. Final Report & Audit Certification
Log all examined datasets, transformations, and isolation verification results in `prompts/antigravity/logs/`.
