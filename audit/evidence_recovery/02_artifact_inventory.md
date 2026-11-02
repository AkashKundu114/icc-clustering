# 02 Raw Experimental Artifact Inventory and Recovery Report

**Audit Target:** ICC-Clustering (`D:\icc-clustering`)  
**Auditor:** Senior Research Software Auditor & Reproducibility Specialist  
**Audit Timestamp:** 2026-11-01T23:05:00+05:30  
**Recovery Locations Audited:**
- Local Active Workspace: `D:\icc-clustering\results\post_refactor_verification\`
- Historical Git Tree: Commit `e3f54cc0951d173f0e13a4b524628328f318e746`
- Local Private Archive: `D:\icc-clustering-private-archive\`
- Local Mirror Backups: `D:\icc-clustering-backup\`

---

## 1. Executive Summary

This forensic evidence recovery operation identified, verified, and secured critical raw experimental artifacts supporting the scientific claims of the ICC-Clustering project and its upcoming submission to *Data Mining and Knowledge Discovery* (DMKD).

### Key Recovery Outcomes:
1. **Full Recovery of Core Audit Artifacts:**
   The primary raw artifacts queried by the mandate—including `adversarial_autok_raw_results.csv` (104 KB, 510 trials), `conformal_audit_results.json` (3.8 KB), `knockoff_audit_results.json` (8.1 KB), and `reproduction_benchmarks.csv` (14.8 KB)—were located in `results/post_refactor_verification/`, verified, and archived into `results/evidence_recovery/recovered/`.
2. **Discovery of Master Manuscript Results Database:**
   In `D:\icc-clustering-private-archive\`, we discovered the master results database `results.json` (1.63 MB), the exact manuscript LaTeX macro specification `numbers.tex` (4.1 KB), the complete statistical metrics repository `stats.json` (11.9 KB), and the raw factorial ablation data `exp2_real_high_d_factorial.csv` (43.4 KB).
3. **Recovery of Stability-Accuracy Discordance Microdata:**
   The raw tabular observations supporting the manuscript's headline stability–accuracy discordance gap (`+0.485`, 95% CI `[+0.379, +0.662]`) were recovered in `subsample_stability_summary.csv` and `real_data_stability_summary.csv`.
4. **Identification of Irrecoverable / Missing Data:**
   The raw execution trace for the claimed 1,000,000-cell transcriptomics benchmark (55.6 s, 240 MB RAM) and the driver gene overlap database for Leukemia/SRBCT remain unrecovered, confirming that these claims lack empirical backing in the repository.

---

## 2. Inventory of Recovered Raw Artifacts

All recovered artifacts have been copied into `results/evidence_recovery/recovered/` without modifying tracked source files. Complete SHA-256 hashes and metadata are recorded in `audit/evidence_recovery/artifact_manifest.csv`:

### Table 1: Recovered Raw Evidence Manifest

| Artifact Name | Size (Bytes) | SHA-256 Checksum (Prefix) | Originating Source Path | Scientific Role / Claim Supported |
|---|:---:|:---:|---|---|
| `adversarial_autok_raw_results.csv` | 104,264 | `3ecf3460...` | `results/post_refactor_verification/auto_k/` | 510-trial adversarial AutoK evaluation proving 100% collapse to $K_{min}$ |
| `adversarial_autok_summary.json` | 9,763 | `64966606...` | `results/post_refactor_verification/auto_k/` | Scenario-level aggregations and collapse rates across 17 regimes |
| `conformal_audit_results.json` | 3,796 | `3d51f2bc...` | `results/post_refactor_verification/conformal/` | Monte Carlo calibration data; true pathology coverage collapse (37%–62%) |
| `knockoff_audit_results.json` | 8,125 | `5d848792...` | `results/post_refactor_verification/knockoff/` | Decoy exchangeability errors; 100% empirical FDR under pure null |
| `reproduction_benchmarks.csv` | 14,849 | `f172776c...` | `results/post_refactor_verification/benchmark_logs/` | 5-repeat timing and memory profiling falsifying Seed 101 speedup claim |
| `aggregate_seed_statistics.csv` | 1,646 | `97d519b5...` | `results/post_refactor_verification/benchmark_logs/` | 10-seed aggregate performance (Standard Consensus 1.0 vs ICC-v2 0.652) |
| `leakage_audit_results.json` | 2,684 | `27096e57...` | `results/post_refactor_verification/leakage/` | 5-fold CV comparisons proving $0.25\sigma$ mean shift from pre-split scaling |
| `clean_env_results.json` | 4,185 | `271638ae...` | `results/post_refactor_verification/packaging/` | Isolated virtual environment test tracebacks (`ModuleNotFoundError`) |
| `exp2_real_high_d_factorial.csv` | 43,385 | `515b133b...` | `private-archive/results/exp2_ablation/` | Factorial ablation matrix across 6 high-D datasets (V0 through V5) |
| `subsample_stability_summary.csv` | 10,622 | `b542df98...` | `private-archive/results/stability/` | Subsample stability microdata establishing the non-degenerate $+0.485$ gap |
| `real_data_stability_summary.csv` | 16,630 | `f28eebe0...` | `private-archive/results/stability/` | Full-cohort stability vs. accuracy metrics across 13 benchmark cohorts |
| `stats.json` | 11,858 | `36fe4c3c...` | `private-archive/results/` | Master statistical store (Friedman $p=0.40$, Nemenyi $CD=4.62$, bootstrap CIs) |
| `results.json` | 1,627,258 | `9c9b5f54...` | `private-archive/results/` | Comprehensive raw baseline benchmark database (1.63 MB JSON) |
| `numbers.tex` | 4,087 | `4f326a0b...` | `private-archive/springer_manuscript/` | LaTeX macro definitions generated from `stats.json` for DMKD manuscript |

---

## 3. Classification of Missing and Unsubstantiated Evidence

The investigation cross-referenced published claims against recovered microdata. Missing items are logged in `audit/evidence_recovery/missing_artifacts.csv`:

### Table 2: Missing or Irrecoverable Artifact Manifest

| Missing Artifact | Category | Claimed Location in Text | Research Impact | Verification Status |
|---|---|---|---|:---:|
| `million_cell_scrnaseq_scaling_raw.csv` | Scalability | `docs/theory.md Sec 10` | Claimed $10^6$ cells clustered in 55.6 s with 240 MB memory. | **IRRECOVERABLE** (No raw run log found; theoretical estimate) |
| `driver_gene_overlap_validation.json` | Cancer Genomics | `docs/theory.md Sec 10`, `numbers.tex` | Claimed 54.0% recovery of top oncogenic driver genes on Leukemia/SRBCT. | **REFERENCED BUT MISSING** (No driver database or overlap script exists) |
| `model_x_knockoff_exact_matrices.npz` | Multiple Testing | `docs/theory.md Sec 9.2` | Claimed finite-sample Model-X FDR control under arbitrary covariance. | **IRRECOVERABLE** (Implementation uses independent MVN draws) |
| `unfrozen_seed_synthetic_benchmarks.csv` | Reproducibility | `README.md`, `docs/theory.md` | Historical synthetic benchmark used frozen `seed=42` in `make_signal`. | **REPRODUCIBLE ONLY BY RERUN** (Requires unfreezing dataset seed) |
| `clean_train_scaler_clinical_cv.json` | Leakage Remediation | `examples/leukemia_inductive.py` | Published clinical ARI values evaluated on pre-standardized matrices. | **REPRODUCIBLE ONLY BY RERUN** (Requires strict train-only scaling) |

---

## 4. Evidence Integrity and Preservation Protocol

To maintain complete scientific and forensic integrity:
1. **Zero Overwrite Policy:** No original file in `results/post_refactor_verification/` or `D:\icc-clustering-private-archive\` was overwritten or modified.
2. **Explicit Directory Partitioning:**
   - `results/evidence_recovery/recovered/`: Holds bitwise identical copies of original raw artifacts discovered during the audit.
   - `results/evidence_recovery/reconstructed/`: Reserved strictly for newly generated or recalculated outputs, clearly segregated from historical evidence.
