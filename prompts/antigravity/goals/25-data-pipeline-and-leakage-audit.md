# Goal: Data Pipeline Integrity, Provenance & Leakage Audit

Deploy this goal to audit all data pipelines, ensuring strict split isolation, mathematical immutability of raw datasets, and zero contamination between training, tuning, and evaluation partitions.

---

## Assigned Subagent Personas
1. **Data Leakage Auditor (`roo_reviewer`)**: Analyzes feature engineering and cross-validation pipelines for information seepage.
2. **Provenance Specialist (`roo_ask`)**: Validates dataset licenses, download URLs, and SHA-256 integrity checksums.
3. **Pipeline Engineer (`roo_coder`)**: Implements strict `fit()` / `transform()` separation and automated download scripts.

---

## Audit Checklist & Verification Rules

### 1. Train / Test Split Hygiene
- **Preprocessing Seepage:** Verify that data scaling (e.g. `StandardScaler`, min-max, PCA) is fitted **strictly on training partitions** and only applied to test sets via `.transform()`.
- **Feature Selection Leakage:** Confirm that feature selection, variance thresholding, or anchor selection does not observe test partition labels or distributions.
- **Cross-Validation Leakage:** Ensure CV folds re-run the entire pipeline from scratch inside each fold.

### 2. Dataset Immutability & Checksum Protocol
- **Raw Data Boundary:** Confirm that raw downloaded files in `data/raw/` are read-only and never modified in-place by preprocessing scripts.
- **Deterministic Checksums:** All automated download scripts (`scripts/fetch_data.py`) must compute and verify SHA-256 hashes against a frozen reference manifest before staging into `data/cache/`.

### 3. Git Exclusion & Anonymity
- Run `git status -u` and `git check-ignore` to confirm no raw datasets (`*.csv`, `*.npz`, `*.mat`, `*.h5ad`) or patient identifiers are tracked in Git.
- Confirm only `.gitkeep` and `README.md` files are version-controlled in data directories.

---

## Deliverables
- **Data Leakage Audit Report:** Documentation of audited split pipelines and verification of zero information leakage.
- **Dataset Provenance Table:** Manifest detailing origin endpoints, licenses, SHA-256 hashes, and preprocessing parameters.
