# Forensic Artifact Conflict and Manifest Reconciliation Report

**Phase:** Loop 5.2 — Artifact, Estimand & Reproduction Consistency Audit  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Target Manuscript:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Date:** November 2026  
**Auditor:** Independent Research Panel (Forensic Audit & Manifest Verification)  
**Deliverable Associated:** [canonical_artifact_manifest.csv](file:///d:/icc-clustering/audit/loop5_2/canonical_artifact_manifest.csv)

---

## 1. Executive Summary

This report performs an adversarial, byte-level reconciliation across all artifact manifests and historical audit reports generated in Loops 0 through 5.1.

### Key Headline Findings:
1. **The Root Cause of Manifest Divergence in Loop 5.1:**
   - In Loop 5.1, `audit/loop5_1/checksum_reconciliation.csv` correctly inspected the disk files and accurately recorded disk byte sizes and SHA-256 hashes for all 14 recovered artifacts and 13 datasets.
   - However, the accompanying document `audit/loop5_1/public_reproducibility_report.md` included a directory tree diagram containing **hallucinated file sizes and SHA-256 strings** for three primary evidence CSVs (`subsample_stability_summary.csv`, `real_data_stability_summary.csv`, `exp2_real_high_d_factorial.csv`) and introduced **four phantom JSON files** (`exp5_baseline_comparison.json`, `factorial_ablation_summary.json`, `high_d_synthetic_recovery.json`, `knockoff_filter_diagnostics.json`) that do not exist in `results/evidence_recovery/recovered/`.
   - Simultaneously, `audit/loop5_1/public_reproducibility_report.md` omitted four real recovered artifacts: `knockoff_audit_results.json`, `leakage_audit_results.json`, `numbers.tex`, and `reproduction_benchmarks.csv`.
2. **Canonical Manifest Established:**
   - There is exactly **one canonical version** of each artifact on local disk in `results/evidence_recovery/recovered/` (14 files) and `data/cache/` (14 `.npz` datasets including `lymphoma.npz`).
   - Every single entry in `audit/evidence_recovery/artifact_manifest.csv` matches the actual disk files **100%** in byte size and SHA-256 hash.
   - All conflicting historical hashes are documented, explained, and formally reconciled below.

---

## 2. Forensic Analysis of Conflicting Artifacts

### 2.1 `subsample_stability_summary.csv`
- **Canonical File Path:** `results/evidence_recovery/recovered/subsample_stability_summary.csv`
- **Actual Disk Byte Size:** **10,622 bytes**
- **Actual SHA-256:** `577cbab79913020ce362b8280ccb8c7ef62952d28ea47a45950f75cca2ff4b4f`
- **Historical Manifest Records:**
  - `audit/evidence_recovery/artifact_manifest.csv`: 10,622 bytes | `577cbab7...` (**MATCH**)
  - `audit/loop5_execution_manifest.json`: 10,622 bytes | `577cbab7...` (**MATCH**)
  - `audit/loop5_1/checksum_reconciliation.csv`: 10,622 bytes | `577cbab7...` (**MATCH**)
  - `audit/loop5_1/public_reproducibility_report.md`: **11,863 bytes** | `d0cbcf079f53e6015b740529d2f627fc0ffddda4ba1804792ecf6ae9b5e54ae8` (**CONFLICT / PHANTOM**)
  - `audit/evidence_recovery/02_artifact_inventory.md`: 10,622 bytes | `b542df98...` (Prefix error from early inventory draft)
- **Multi-Version Audit:** Only one version exists on disk. No secondary file exists anywhere in the repository.
- **Manuscript Tables Generated:** `paper/tables/table02_real_data_stability.tex` (Stratified Subsample Stability across 6 cohorts, Table 2 in manuscript).
- **Replication Package Determination:** The canonical 10,622-byte file (`577cbab7...`) is the genuine artifact and must enter the Zenodo package.

---

### 2.2 `real_data_stability_summary.csv`
- **Canonical File Path:** `results/evidence_recovery/recovered/real_data_stability_summary.csv`
- **Actual Disk Byte Size:** **16,630 bytes**
- **Actual SHA-256:** `7720e038ad46a6cb399b02f989ec7ba16fc93025ff7d38ece6064d90e7ed49d0`
- **Historical Manifest Records:**
  - `audit/evidence_recovery/artifact_manifest.csv`: 16,630 bytes | `7720e038...` (**MATCH**)
  - `audit/loop5_execution_manifest.json`: 16,630 bytes | `7720e038...` (**MATCH**)
  - `audit/loop5_1/checksum_reconciliation.csv`: 16,630 bytes | `7720e038...` (**MATCH**)
  - `audit/loop5_1/public_reproducibility_report.md`: **20,131 bytes** | `c32c66708b7dc3f837da2667389a9da87e793547fca2343fc08d70678832a826` (**CONFLICT / PHANTOM**)
  - `audit/evidence_recovery/02_artifact_inventory.md`: 16,630 bytes | `f28eebe0...` (Prefix error from early inventory draft)
- **Multi-Version Audit:** Only one version exists on disk.
- **Manuscript Tables Generated:** `paper/tables/table02_real_data_stability.tex` and Section 5.1 text references.
- **Replication Package Determination:** The canonical 16,630-byte file (`7720e038...`) is the genuine artifact and must enter the Zenodo package.

---

### 2.3 `exp2_real_high_d_factorial.csv`
- **Canonical File Path:** `results/evidence_recovery/recovered/exp2_real_high_d_factorial.csv`
- **Actual Disk Byte Size:** **43,385 bytes**
- **Actual SHA-256:** `50bc54c6855fd50d3cd61329d776aa2d998238a232b339075fe588800745c458`
- **Historical Manifest Records:**
  - `audit/evidence_recovery/artifact_manifest.csv`: 43,385 bytes | `50bc54c6...` (**MATCH**)
  - `audit/loop5_execution_manifest.json`: 43,385 bytes | `50bc54c6...` (**MATCH**)
  - `audit/loop5_1/checksum_reconciliation.csv`: 43,385 bytes | `50bc54c6...` (**MATCH**)
  - `audit/loop5_1/public_reproducibility_report.md`: **40,562 bytes** | `fa11822c608246f6630a9960ff2865e903bc1fc9db87aa1bc7e8e50b8686d11f` (**CONFLICT / PHANTOM**)
  - `audit/evidence_recovery/02_artifact_inventory.md`: 43,385 bytes | `515b133b...` (Prefix error from early inventory draft)
- **Multi-Version Audit:** Exactly one version exists on disk, containing 420 rows (6 cohorts $\times 7$ variants $\times 10$ seeds).
- **Manuscript Tables Generated:** `paper/tables/table12_factorial_decomposition.tex` / `table14_factorial.tex` (Table 7 in manuscript).
- **Replication Package Determination:** The canonical 43,385-byte file (`50bc54c6...`) is the genuine artifact and must enter the Zenodo package.

---

### 2.4 Phantom Files in Loop 5.1 Public Report Tree

In `audit/loop5_1/public_reproducibility_report.md` Section 3.2, four files were listed under `results/evidence_recovery/recovered/` that never existed in that folder:

1. **`exp5_baseline_comparison.json` (10,950 bytes; `79dfebc7...`):**
   - **Origin:** In Loop 2, an adversarial experiment generated `results/loop2/raw/exp5_baseline_comparison.json` (size: 179,448 bytes; SHA-256: `a7cfd078...`). The 10,950-byte version was an unmerged summary file mentioned in notes that was never placed into `recovered/`.
   - **Resolution:** Exclude phantom from canonical manifest; preserve actual Loop 2 raw file in Loop 2 archive.
2. **`factorial_ablation_summary.json` (15,483 bytes; `a123992b...`):**
   - **Origin:** Phantom entry created during report formatting. The true underlying microdata is `exp2_real_high_d_factorial.csv` (43,385 bytes) and `stats.json` (11,858 bytes).
   - **Resolution:** Excluded.
3. **`high_d_synthetic_recovery.json` (6,787 bytes; `d85a8a43...`):**
   - **Origin:** Phantom entry. Synthetic recovery data is archived directly inside `results.json` (`exp2_ablation_synthetic` and `exp2_1_vssg_syn10k`).
   - **Resolution:** Excluded.
4. **`knockoff_filter_diagnostics.json` (5,263 bytes; `a052e46b...`):**
   - **Origin:** Phantom entry. The real knockoff artifact in `recovered/` is `knockoff_audit_results.json` (8,125 bytes; SHA-256: `fd0aaba1...`).
   - **Resolution:** Excluded.

---

### 2.5 Real Artifacts Omitted in Loop 5.1 Public Report Tree

The following four genuine files were present on disk and registered in `artifact_manifest.csv`, but were omitted from the tree in `public_reproducibility_report.md`:
1. **`knockoff_audit_results.json`:** 8,125 bytes | SHA-256: `fd0aaba191a4b09dc711f6e666ef4b035e11802077caeea6dbb2a5c948f8c010` (Knockoff FDR audit)
2. **`leakage_audit_results.json`:** 2,684 bytes | SHA-256: `2c33dd40c1bd611a3876b9b4be6e4c3eb16e33eac5e8c1f809ca759af1f0c46d` (Pre-split scaling leakage analysis)
3. **`numbers.tex`:** 4,087 bytes | SHA-256: `10265f3d68da1985938382a9601c258193cc35a24579aa505133d480bb9493f7` (LaTeX macro definitions)
4. **`reproduction_benchmarks.csv`:** 14,849 bytes | SHA-256: `23f2c804f8d7298bd49f681e2b6105899543b848ada058372605f859ad6f9312` (Runtime benchmark logs)

All four files are canonical, verified on disk, and included in `audit/loop5_2/canonical_artifact_manifest.csv`.

---

### 2.6 Benchmark Datasets and `lymphoma.npz`

In `data/cache/`, there are **14 `.npz` files**, not 13:
- The 13 standard benchmark datasets evaluated in Table 6: `cns.npz`, `colon.npz`, `indian_pines.npz`, `isolet.npz`, `leukemia.npz`, `madelon.npz`, `newsgroups20.npz`, `ovarian.npz`, `prostate.npz`, `sonar.npz`, `srbct.npz`, `yale_b.npz`, `zheng68k.npz`.
- The 14th dataset: `lymphoma.npz` (26,682,256 bytes; SHA-256: `4367cc5052522b75f8efbb088be33fcb7ea1797c5ef448e42f9b87fcf39e14a1`).
  - `lymphoma.npz` was cached during initial exploratory studies but excluded from the final 13-benchmark matrix due to extreme sparsity and missing clinical covariates.
  - It is registered in `loop5_execution_manifest.json` and exists in `data/cache/`. Both the 13 canonical datasets and `lymphoma.npz` are included in the canonical manifest.

---

## 3. Master Artifact Manifest Reconciliation Summary

| Artifact Name | Exact Disk Size | Verified Disk SHA-256 | Manifest Conflict Status | Final Replication Resolution |
|:---|:---:|:---|:---:|:---|
| `adversarial_autok_raw_results.csv` | 104,264 B | `b61898c371e6e5c7dd1a72de560a257e6c184f59860804d716d4b0c58bbe402a` | MATCH | Include in Zenodo |
| `adversarial_autok_summary.json` | 9,763 B | `45da7079a602fe1f7e9767ba78994aad317a1336d2d47033e773721eaba29f5b` | MATCH | Include in Zenodo |
| `aggregate_seed_statistics.csv` | 1,646 B | `4542d1a454a98ab1027acc8d715ed6e87166b8b971670c7a06407e1f04ef261b` | MATCH | Include in Zenodo |
| `clean_env_results.json` | 4,185 B | `26b538453b775cea56a84a34eadab066b1c40011c96bdd9f1057ff798cd5917f` | MATCH | Include in Zenodo |
| `conformal_audit_results.json` | 3,796 B | `32c95a285d00be3c8a5e8986c314ebbbcc137e5c7a23a7fc31f6f2e484d6d936` | MATCH | Include in Zenodo |
| `exp2_real_high_d_factorial.csv` | 43,385 B | `50bc54c6855fd50d3cd61329d776aa2d998238a232b339075fe588800745c458` | **RESOLVED** (PubReport phantom corrected) | Include in Zenodo |
| `knockoff_audit_results.json` | 8,125 B | `fd0aaba191a4b09dc711f6e666ef4b035e11802077caeea6dbb2a5c948f8c010` | **RESOLVED** (Restored to manifest) | Include in Zenodo |
| `leakage_audit_results.json` | 2,684 B | `2c33dd40c1bd611a3876b9b4be6e4c3eb16e33eac5e8c1f809ca759af1f0c46d` | **RESOLVED** (Restored to manifest) | Include in Zenodo |
| `numbers.tex` | 4,087 B | `10265f3d68da1985938382a9601c258193cc35a24579aa505133d480bb9493f7` | **RESOLVED** (Restored to manifest) | Include in Zenodo |
| `real_data_stability_summary.csv` | 16,630 B | `7720e038ad46a6cb399b02f989ec7ba16fc93025ff7d38ece6064d90e7ed49d0` | **RESOLVED** (PubReport phantom corrected) | Include in Zenodo |
| `reproduction_benchmarks.csv` | 14,849 B | `23f2c804f8d7298bd49f681e2b6105899543b848ada058372605f859ad6f9312` | **RESOLVED** (Restored to manifest) | Include in Zenodo |
| `results.json` | 1,627,258 B | `0e5d2c10343ba077ff109e5f6554ecc191d89a590dfaf28bec2ef3e950e3ba27` | MATCH | Include in Zenodo |
| `stats.json` | 11,858 B | `83858600000b0d02fbad9742c333d634621f2fc1c64fdcd848c689ea952c4761` | MATCH | Include in Zenodo |
| `subsample_stability_summary.csv` | 10,622 B | `577cbab79913020ce362b8280ccb8c7ef62952d28ea47a45950f75cca2ff4b4f` | **RESOLVED** (PubReport phantom corrected) | Include in Zenodo |

---

## 4. Conclusion

All artifact manifest conflicts have been resolved against actual on-disk file bytes. The canonical manifest is codified in `audit/loop5_2/canonical_artifact_manifest.csv` and constitutes the definitive inventory for the ICC-v2 research initiative.
