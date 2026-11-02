# 01 Experimental Artifact Integrity Report and Forensics Audit

**Target Repository:** `D:\icc-clustering`  
**Audit Scope:** Verification of Recovered Experimental Artifacts against Physical Filesystem  
**Phase:** LOOP 0 ?" Research Workspace Initialization and Evidence Integrity Gate  
**Timestamp:** 2026-11-01T23:45:00+05:30  
**Auditor:** Independent Research Integrity Auditor  

---

## 1. Executive Summary

This report performs an exhaustive, independent verification of all experimental artifacts reported as recovered or missing in previous forensic audit phases. 

### Key Integrity Findings:
1. **14 Recovered Files Physically Verified:** All 14 artifacts recorded in `audit/evidence_recovery/artifact_manifest.csv` physically exist in `results\evidence_recovery\recovered\`.
2. **Bitwise Match with Manifest:** SHA-256 checksums calculated directly from the filesystem for all 14 recovered files **match `artifact_manifest.csv` with zero discrepancies**.
3. **Critical Documentation Discrepancy in `02_artifact_inventory.md`:** Table 1 of `audit/evidence_recovery/02_artifact_inventory.md` listed hallucinated / erroneous checksum prefixes (e.g. `3ecf3460...` for `adversarial_autok_raw_results.csv`, `64966606...` for `adversarial_autok_summary.json`). This report explicitly documents and reconciles this documentation defect against the real filesystem.
4. **Origin Path Discrepancy:** While 8 audit artifacts exist at their claimed original paths within `results/post_refactor_verification/`, 6 historical artifacts (`exp2_real_high_d_factorial.csv`, `numbers.tex`, `real_data_stability_summary.csv`, `results.json`, `stats.json`, `subsample_stability_summary.csv`) do not exist at their original paths in the active repository, but exist in `D:\icc-clustering-private-archive\`, from which they were recovered.
5. **5 Missing Artifacts Confirmed Absent:** The 5 missing artifacts logged in `missing_artifacts.csv` (including the 1,000,000-cell scaling log and cancer driver gene overlap data) are confirmed absent from both the working repository and the private archive.
6. **Aggregated Outputs Without Raw Microdata:** The manuscript claims for 1M cell scaling ($55.6\,\text{s}$) and 54.0% oncogenic driver recovery represent aggregated claims without raw execution microdata.

---

## 2. Exhaustive Verification of Recovered Artifacts

Every artifact recorded in `audit/evidence_recovery/artifact_manifest.csv` was verified on disk. SHA-256 hashes were calculated independently using standard cryptographically secure SHA-256 implementations.

### Table 1: Independent Verification of Recovered Artifacts

| # | Artifact Name | Exact Filesystem Path | Size (Bytes) | Calculated SHA-256 Checksum | Manifest SHA-256 Match | `02_inventory` Table 1 Check | Classification | Generating Script | Originating Commit / Context |
|:---:|---|---|:---:|---|:---:|:---:|---|---|---|
| 1 | `adversarial_autok_raw_results.csv` | `results\evidence_recovery\recovered\adversarial_autok_raw_results.csv` | 104,264 | `b61898c371e6e5c7dd1a72de560a257e6c184f59860804d716d4b0c58bbe402a` | **MATCH** | MISMATCH (`3ecf3460`) | Raw observations | `run_adversarial_autok_benchmarks.py` | `83728a44` (AutoK audit) |
| 2 | `adversarial_autok_summary.json` | `results\evidence_recovery\recovered\adversarial_autok_summary.json` | 9,763 | `45da7079a602fe1f7e9767ba78994aad317a1336d2d47033e773721eaba29f5b` | **MATCH** | MISMATCH (`64966606`) | Aggregated metrics | `run_adversarial_autok_benchmarks.py` | `83728a44` (AutoK audit) |
| 3 | `aggregate_seed_statistics.csv` | `results\evidence_recovery\recovered\aggregate_seed_statistics.csv` | 1,646 | `4542d1a454a98ab1027acc8d715ed6e87166b8b971670c7a06407e1f04ef261b` | **MATCH** | MISMATCH (`97d519b5`) | Aggregated metrics | `reproduce_benchmarks.py` | `83728a44` (Seed sensitivity) |
| 4 | `clean_env_results.json` | `results\evidence_recovery\recovered\clean_env_results.json` | 4,185 | `26b538453b775cea56a84a34eadab066b1c40011c96bdd9f1057ff798cd5917f` | **MATCH** | MISMATCH (`271638ae`) | Execution log / Trace | `test_clean_install.py` | `83728a44` (Packaging audit) |
| 5 | `conformal_audit_results.json` | `results\evidence_recovery\recovered\conformal_audit_results.json` | 3,796 | `32c95a285d00be3c8a5e8986c314ebbbcc137e5c7a23a7fc31f6f2e484d6d936` | **MATCH** | MISMATCH (`3d51f2bc`) | Aggregated metrics | `audit_conformal.py` | `83728a44` (Coverage audit) |
| 6 | `exp2_real_high_d_factorial.csv` | `results\evidence_recovery\recovered\exp2_real_high_d_factorial.csv` | 43,385 | `50bc54c6855fd50d3cd61329d776aa2d998238a232b339075fe588800745c458` | **MATCH** | MISMATCH (`515b133b`) | Raw observations | `exp2_ablation/run.py` (archive) | `e3f54cc0` (Historical) |
| 7 | `knockoff_audit_results.json` | `results\evidence_recovery\recovered\knockoff_audit_results.json` | 8,125 | `fd0aaba191a4b09dc711f6e666ef4b035e11802077caeea6dbb2a5c948f8c010` | **MATCH** | MISMATCH (`5d848792`) | Aggregated metrics | `audit_knockoff.py` | `83728a44` (Knockoff audit) |
| 8 | `leakage_audit_results.json` | `results\evidence_recovery\recovered\leakage_audit_results.json` | 2,684 | `2c33dd40c1bd611a3876b9b4be6e4c3eb16e33eac5e8c1f809ca759af1f0c46d` | **MATCH** | MISMATCH (`27096e57`) | Aggregated metrics | `audit_leakage.py` | `83728a44` (Leakage audit) |
| 9 | `numbers.tex` | `results\evidence_recovery\recovered\numbers.tex` | 4,087 | `10265f3d68da1985938382a9601c258193cc35a24579aa505133d480bb9493f7` | **MATCH** | MISMATCH (`4f326a0b`) | LaTeX Macro Registry | `scripts/make_numbers.py` (archive) | Historical export from `stats.json` |
| 10 | `real_data_stability_summary.csv` | `results\evidence_recovery\recovered\real_data_stability_summary.csv` | 16,630 | `7720e038ad46a6cb399b02f989ec7ba16fc93025ff7d38ece6064d90e7ed49d0` | **MATCH** | MISMATCH (`f28eebe0`) | Derived Summary | `experiments/stability/run.py` (archive) | Historical stability study |
| 11 | `reproduction_benchmarks.csv` | `results\evidence_recovery\recovered\reproduction_benchmarks.csv` | 14,849 | `23f2c804f8d7298bd49f681e2b6105899543b848ada058372605f859ad6f9312` | **MATCH** | MISMATCH (`f172776c`) | Raw observations | `reproduce_benchmarks.py` | `83728a44` (Runtime profile) |
| 12 | `results.json` | `results\evidence_recovery\recovered\results.json` | 1,627,258 | `0e5d2c10343ba077ff109e5f6554ecc191d89a590dfaf28bec2ef3e950e3ba27` | **MATCH** | MISMATCH (`9c9b5f54`) | Master Benchmark DB | `results/overnight/run_all.py` (archive) | `e3f54cc0` (Baseline suite) |
| 13 | `stats.json` | `results\evidence_recovery\recovered\stats.json` | 11,858 | `83858600000b0d02fbad9742c333d634621f2fc1c64fdcd848c689ea952c4761` | **MATCH** | MISMATCH (`36fe4c3c`) | Derived Statistical Store | `scripts/evaluate.py` (archive) | `e3f54cc0` (Friedman/Nemenyi) |
| 14 | `subsample_stability_summary.csv` | `results\evidence_recovery\recovered\subsample_stability_summary.csv` | 10,622 | `577cbab79913020ce362b8280ccb8c7ef62952d28ea47a45950f75cca2ff4b4f` | **MATCH** | MISMATCH (`b542df98`) | Derived Summary | `experiments/stability/run.py` (archive) | Historical discordance study |

---

## 3. Discrepancy Analysis and Audit Defect Reconciliation

### 3.1 Documentation Defect in `02_artifact_inventory.md` Table 1
A critical discrepancy was discovered during physical verification:
- In `audit/evidence_recovery/02_artifact_inventory.md`, Table 1 listed checksum prefixes such as `3ecf3460...`, `64966606...`, `3d51f2bc...`, `5d848792...`, etc.
- In `audit/evidence_recovery/artifact_manifest.csv`, the recorded checksums are completely different: `b61898c3...`, `45da7079...`, `32c95a28...`, `fd0aaba1...`.
- Direct cryptographic calculation (`Get-FileHash -Algorithm SHA256`) of the physical files in `results\evidence_recovery\recovered\` confirms that **the manifest values in `artifact_manifest.csv` are 100% correct**, while the prefixes in Table 1 of `02_artifact_inventory.md` were inaccurate or hallucinated in the prior report.
- **Finding:** The physical artifacts are completely authentic and undamaged; the error was strictly clerical within `02_artifact_inventory.md`.

### 3.2 Dual-Location vs Archive-Only Artifacts
Verification of the `original_path` column in `artifact_manifest.csv` revealed two categories of recovered evidence:

1. **Active Repository Artifacts (8 files):**
   These files exist in both `results/post_refactor_verification/` and `results/evidence_recovery/recovered/`. The hashes in both directories are identical bit-for-bit:
   - `adversarial_autok_raw_results.csv`
   - `adversarial_autok_summary.json`
   - `aggregate_seed_statistics.csv`
   - `clean_env_results.json`
   - `conformal_audit_results.json`
   - `knockoff_audit_results.json`
   - `leakage_audit_results.json`
   - `reproduction_benchmarks.csv`

2. **Private Archive Artifacts (6 files):**
   These files were deleted from the active repository during confidentiality sanitization and do not exist at their claimed original paths in `D:\icc-clustering\`. However, bitwise identical copies exist in `D:\icc-clustering-private-archive\`:
   - `exp2_real_high_d_factorial.csv` (Source: `D:\icc-clustering-private-archive\results\exp2_ablation\`)
   - `numbers.tex` (Source: `D:\icc-clustering-private-archive\springer_manuscript\`)
   - `real_data_stability_summary.csv` (Source: `D:\icc-clustering-private-archive\results\stability\`)
   - `results.json` (Source: `D:\icc-clustering-private-archive\results\`)
   - `stats.json` (Source: `D:\icc-clustering-private-archive\results\`)
   - `subsample_stability_summary.csv` (Source: `D:\icc-clustering-private-archive\results\stability\`)

---

## 4. Verification of Missing and Unsubstantiated Evidence

An independent search was conducted across `D:\icc-clustering` and `D:\icc-clustering-private-archive` to determine if any of the 5 missing artifacts logged in `missing_artifacts.csv` could be recovered.

### Table 2: Missing Artifact Audit

| Missing Artifact | Category | Claimed Reference in Manuscript / Docs | Search Result | Verification Status | Research Impact |
|---|---|---|---|:---:|---|
| `million_cell_scrnaseq_scaling_raw.csv` | Scalability | `docs/theory.md Sec 10`, `numbers.tex` (`\DefExtremeScaleOneMillionTime{55.6}`) | Not found on filesystem | **IRRECOVERABLE** | Claim of 1,000,000 cells clustered in 55.6 s with 240 MB memory is completely unbacked by raw run logs. It is a theoretical extrapolation presented as empirical data. |
| `driver_gene_overlap_validation.json` | Cancer Genomics | `docs/theory.md Sec 10`, `numbers.tex` (`\DefAblationLeukemiaMarkerFiftyFraction{0.540}`) | Not found on filesystem | **REFERENCED BUT MISSING** | Claim of 54.0% recovery of top oncogenic driver genes on Leukemia/SRBCT lacks any reference gene list (COSMIC/OncoKB) or generating script. |
| `model_x_knockoff_exact_matrices.npz` | Multiple Testing | `docs/theory.md Sec 9.2` | Not found on filesystem | **IRRECOVERABLE** | Theoretical claim of exact second-order Model-X FDR control is contradicted by implementation, which samples independent standard normal noise. |
| `unfrozen_seed_synthetic_benchmarks.csv` | Reproducibility | `README.md`, `docs/theory.md Sec 10` | Not found on filesystem | **REPRODUCIBLE ONLY BY RERUN** | Historical synthetic benchmarks evaluated noise variations on a single frozen signal manifold (`seed=42`). Requires unfreezing seed in `make_signal`. |
| `clean_train_scaler_clinical_cv.json` | Leakage Remediation | `examples/leukemia_inductive.py`, `realtime_patient_projection.py` | Not found on filesystem | **REPRODUCIBLE ONLY BY RERUN** | Reported clinical ARI was evaluated on pre-split standardized matrices. Requires clean 5-fold CV fitting scalers strictly on training folds. |

---

## 5. Evidence Classification and Traceability Matrix

### 5.1 Aggregated Outputs Without Raw Supporting Data
1. **Million-Cell Benchmark:** Macro `\DefExtremeScaleOneMillionTime{55.6}` in `numbers.tex` reports $55.6\,\text{s}$ runtime. There is no raw benchmark log, timing trace, or system memory log supporting this number.
2. **Oncogenic Driver Gene Overlap:** Macro `\DefAblationLeukemiaMarkerFiftyFraction{0.540}` in `numbers.tex` reports $54.0\%$ recovery of driver genes. There is no underlying JSON, CSV, or script matching feature indices to biological gene symbols.

### 5.2 Raw Data Without Reproducible Generating Scripts
1. **Factorial Ablation (`exp2_real_high_d_factorial.csv`):** Contains raw ARI/NMI measurements across V0-V5 ablation variants. The original generating script in `scripts_original/` was written against pre-refactor monolithic class structures and cannot be executed directly against modern `src/icc/` without an adapter.
2. **Master Baseline Database (`results.json`):** 1.63 MB of baseline runs. Generated by historical overnight runners (`results/overnight/run_all.py`) that are not present in current `scripts/`.

### 5.3 Fully Verified & Reproducible Microdata
1. **AutoK Adversarial Trials (`adversarial_autok_raw_results.csv`):** 510 raw trials generated deterministically by `results/post_refactor_verification/auto_k/run_adversarial_autok_benchmarks.py`.
2. **Timing & Memory Profiling (`reproduction_benchmarks.csv`):** 5-repeat profiles generated deterministically by `results/post_refactor_verification/benchmark_logs/reproduce_benchmarks.py`.
3. **Conformal Coverage Collapse (`conformal_audit_results.json`):** Generated deterministically by `results/post_refactor_verification/conformal/audit_conformal.py`.
4. **Decoy Feature FDR Inflation (`knockoff_audit_results.json`):** Generated deterministically by `results/post_refactor_verification/knockoff/audit_knockoff.py`.
5. **Data Leakage Shift (`leakage_audit_results.json`):** Generated deterministically by `results/post_refactor_verification/leakage/audit_leakage.py`.

---

## 6. Integrity Gate Conclusion

The physical evidence verification establishes that:
- 14 recovered artifacts are physically intact and verified against `artifact_manifest.csv`.
- The clerical checksum mismatch in `02_artifact_inventory.md` is resolved.
- Core audit findings (AutoK collapse, Knockoff FDR inflation, conformal coverage loss, frozen seed leakage) are backed by authentic raw microdata.
- Key empirical claims regarding 1M cell scaling and cancer driver gene recovery are unsubstantiated and must be remediated or retracted prior to submission.
