# Custom Prompt: Data Split Hygiene & Preprocessing Leakage Audit

- **Target Systems:** Data loaders (`src/*/datasets/`), benchmark suites (`experiments/`), and evaluation metrics.
- **Assigned Persona:** `roo_reviewer` (Leakage Inspection), `roo_coder` (Refactoring).

---

## Technical Instructions
1. Inspect all train/test partitioning mechanisms across `experiments/`:
   - Verify that test indices are strictly held out before any unsupervised feature selection or graph construction.
   - For inductive out-of-sample projection, confirm the projection operator is computed **only** on the anchor/discovery set.
2. Check feature transformers (standardization, PCA, min-max scaling):
   - Confirm transformers use `.fit()` exclusively on the discovery partition.
   - Confirm test partitions are transformed strictly via `.transform()` with zero re-centering.
3. Verify test label isolation:
   - Ground-truth cluster labels must never be accessed by the unsupervised consensus pipeline during model fitting, anchor selection, or hyperparameter tuning.

## Acceptance Criteria
- Zero data leakage detected across all benchmark pipelines.
- Unit test verifying split isolation passes cleanly.
