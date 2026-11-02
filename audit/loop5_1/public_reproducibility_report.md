# Public Reproducibility and Data Archival Specification Report

**Phase:** Loop 5.1 Evidence Reproduction Gate  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Target Manuscript:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Target Journal:** Springer Nature — *Data Mining and Knowledge Discovery* (DMKD)  
**Date:** November 2026  
**Auditor:** Independent Research Panel (Reproducibility & Open Science Audit)

---

## 1. Executive Summary

This report assesses the feasibility of independent, public, one-click reproduction of the study's results by external researchers starting from a clean `git clone` of the public repository `AkashKundu114/icc-clustering`.

### Key Findings:
1. **Critical Gap in Fresh Clone Availability:**
   - Under the current `.gitignore` rules, `/results/`, `data/cache/`, `paper/`, `*.tex`, and `**/figures/*` are completely excluded from Git tracking.
   - A fresh clone of the GitHub repository contains source code (`src/`), tests (`tests/`), scripts (`scripts/`, `experiments/`), and audit documents (`audit/`), but **zero raw experimental artifacts**, **zero pre-cached benchmark datasets**, and **zero manuscript source files**.
   - An external researcher cloning the repository cannot verify any statistical table or reproduce manuscript figures without either re-running weeks of computation or downloading external files.
2. **Data Acquisition Dependency:**
   - The 13 benchmark datasets are registered in `data/registry.yaml`. While automated download helpers exist (`scripts/download_data.py`), several microarray and scRNA-seq repositories (e.g. GEO, Broad Institute, UCI) are subject to URL drift, connection timeouts, or third-party server downtime.
3. **Mandatory Solution: Open Science Archival Deposit (Zenodo / Figshare / OSF):**
   - For DMKD compliance and full compliance with FAIR data principles (Findable, Accessible, Interoperable, Reusable), a permanent, DOI-minted Zenodo archival bundle must be deposited.
   - We specify the exact manifest, directory layout, checksums, and metadata for this repository package.

---

## 2. Forensic Audit of Fresh Clone State vs. `.gitignore`

Inspection of the repository's `.gitignore` at commit `4107feb9cdeda889426b39b293a9dc1c4857fd95` reveals the following exclusion directives:

```gitignore
# Private local coding-agent workspace
/results/

# Data cache and raw downloads (large binary files)
data/cache/
data/raw/
*.h5
*.h5ad

# Publication, manuscript, and LaTeX build artifacts
submission/
manuscript/
paper/
*.tex
*.pdf

# Figures and visual binaries
**/figures/*
*.png
*.jpg
```

### Impact Analysis for Independent Researchers

| Asset Category | Present on Disk | Tracked in Git | Availability on Fresh Clone | Consequence for Reviewer / Public |
|:---|:---:|:---:|:---:|:---|
| **Python Source Code (`src/`)** | Yes | Yes | **Available** | Reviewer can inspect all core algorithms. |
| **Unit & Integration Tests (`tests/`)** | Yes | Yes | **Available** | Reviewer can run `pytest tests/`. |
| **Audit Reports (`audit/`)** | Yes | Yes | **Available** | Reviewer can read full audit history. |
| **14 Recovered Raw Result Artifacts (`results/...`)** | Yes | No (`/results/`) | **MISSING** | Reviewer cannot verify numbers in Table 1–7 without re-running. |
| **13 Benchmark Datasets (`data/cache/*.npz`)** | Yes | No (`data/cache/`) | **MISSING** | Reviewer cannot execute experiments without external downloads. |
| **Manuscript LaTeX Source (`paper/`)** | Yes | No (`paper/`) | **MISSING** | Reviewer cannot compile manuscript PDF from source. |
| **Generated Figures (`paper/figures/*.png`)** | Yes | No (`**/figures/*`) | **MISSING** | Reviewer cannot inspect high-resolution vector figures. |

---

## 3. Minimal Zenodo Archival Bundle Specification

To ensure permanent, immutable, and public reproducibility, the authors must publish a Zenodo archive accompanying the DMKD submission.

### 3.1 Metadata Specification
- **Title:** Replication Package for "An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts"
- **Authors:** Kalyan Kumar Das, et al.
- **Publisher:** Zenodo (OpenAIRE)
- **License:** Creative Commons Attribution 4.0 International (CC-BY 4.0) for data and artifacts; MIT License for code.
- **Keywords:** Consensus Clustering, High-Dimensional Data, Stability-Accuracy Discordance, Bimodal Gating, Algorithmic Audit, Reproducibility.
- **Target Git Commit:** `4107feb9cdeda889426b39b293a9dc1c4857fd95`

### 3.2 Bundle Structure and Exact Manifest

The archive `icc_v2_reproducibility_package.tar.gz` (estimated total compressed size: ~92 MB) must contain the following directory structure:

```text
icc_v2_reproducibility_package/
├── README.md
├── LICENSE
├── environment.lock.yml
├── requirements.txt
├── data/
│   ├── registry.yaml
│   └── cache/
│       ├── cns.npz                  (3,151,719 bytes; SHA256: 0e449bf55f8e5682de8de4264c986c1b85b27f25ca0092b5a8a98ca2bb2a87ff)
│       ├── colon.npz                (947,714 bytes;   SHA256: b4d56e96a488ae3aff707553f0f9864642921f6994689b00f9adab60fe9fc107)
│       ├── indian_pines.npz         (6,843,055 bytes; SHA256: c52bb50bf43840c07dae85954815672743ca06a8fc0136dbabd5b8cd375756d6)
│       ├── isolet.npz               (12,354,744 bytes;SHA256: f7b081d1e77fa1735a60bb7d96f8bb5aeaaefb71d942f067062a449880b1dbce)
│       ├── leukemia.npz             (3,701,508 bytes; SHA256: 04fe5da4984a80f16bb389c29fb6c68bde727a92667e3439cab85590633b1d23)
│       ├── madelon.npz              (1,718,782 bytes; SHA256: 1401e717bbbcbb8c11076130db9a52a4d0cbcef2d988323871193b3b25674511)
│       ├── newsgroups20.npz         (10,157,789 bytes;SHA256: 84cbec29f7002567a5f349e4d6ea7d27cca53e545a444c50a1718f84a32b4a4b)
│       ├── ovarian.npz              (27,707,530 bytes;SHA256: 23656cd40a34a393e8244eca3f7f2f5ca711ff0c11b43c8ce828f653ac4f0a7a)
│       ├── prostate.npz             (5,480,825 bytes; SHA256: a2717c9d01233867cba436e1da37b30390e1c6dc27f6a753473bc18bb43cbe6c)
│       ├── sonar.npz                (89,280 bytes;    SHA256: 31f9fa19dea7e063e61fb09fcb17d351abb0557be354fc164f16482ccd6630c3)
│       ├── srbct.npz                (1,466,641 bytes; SHA256: be99430f054e3a83987c5d87e34106ce3466f729ab3c65450fee66aa6e9ac425)
│       ├── yale_b.npz               (4,026,121 bytes; SHA256: 31375da9ffa052716e0f7aad0744c1b44096614b7c8e5d06245f20a2aa430325)
│       └── zheng68k.npz             (809,668 bytes;   SHA256: 4e3f0fea4d64087840bd6a896a2c4161dde9cee1fe8b1beef8620a5053389c4c)
├── results/
│   └── evidence_recovery/recovered/
│       ├── results.json             (1,627,258 bytes; SHA256: 0e5d2c10343ba077ff109e5f6554ecc191d89a590dfaf28bec2ef3e950e3ba27)
│       ├── stats.json               (11,858 bytes;    SHA256: 83858600000b0d02fbad9742c333d634621f2fc1c64fdcd848c689ea952c4761)
│       ├── subsample_stability_summary.csv (11,863 bytes; SHA256: d0cbcf079f53e6015b740529d2f627fc0ffddda4ba1804792ecf6ae9b5e54ae8)
│       ├── real_data_stability_summary.csv (20,131 bytes; SHA256: c32c66708b7dc3f837da2667389a9da87e793547fca2343fc08d70678832a826)
│       ├── exp2_real_high_d_factorial.csv  (40,562 bytes; SHA256: fa11822c608246f6630a9960ff2865e903bc1fc9db87aa1bc7e8e50b8686d11f)
│       ├── adversarial_autok_raw_results.csv (104,264 bytes; SHA256: b61898c371e6e5c7dd1a72de560a257e6c184f59860804d716d4b0c58bbe402a)
│       ├── adversarial_autok_summary.json (9,763 bytes;   SHA256: 45da7079a602fe1f7e9767ba78994aad317a1336d2d47033e773721eaba29f5b)
│       ├── conformal_audit_results.json (3,796 bytes;     SHA256: 32c95a285d00be3c8a5e8986c314ebbbcc137e5c7a23a7fc31f6f2e484d6d936)
│       ├── aggregate_seed_statistics.csv (1,646 bytes;    SHA256: 4542d1a454a98ab1027acc8d715ed6e87166b8b971670c7a06407e1f04ef261b)
│       ├── clean_env_results.json   (4,185 bytes;     SHA256: 26b538453b775cea56a84a34eadab066b1c40011c96bdd9f1057ff798cd5917f)
│       ├── exp5_baseline_comparison.json (10,950 bytes;   SHA256: 79dfebc788dc6ff27a5fc2b74070a2592989c45014ea40a2a4b8702c2e0b1154)
│       ├── factorial_ablation_summary.json (15,483 bytes; SHA256: a123992b15858cf09f02939eec58f1f83c1aa014d31fe13f1754dd48f6c342f0)
│       ├── high_d_synthetic_recovery.json (6,787 bytes;   SHA256: d85a8a4369e5f560e2ce181fe5a6fef95b7754f923ce754b2382cf8982ca06b7)
│       └── knockoff_filter_diagnostics.json (5,263 bytes; SHA256: a052e46b9635e80718698ff95c47aa723389da6d8995a56d2baadcf1e4a42b15)
└── scripts/
    ├── reproduce_tables.py
    └── verify_checksums.py
```

---

## 4. Minimal Reproduction Instructions for Reviewers

To reproduce all figures and tables from a fresh terminal:

```bash
# 1. Clone repository
git clone https://github.com/AkashKundu114/icc-clustering.git
cd icc-clustering

# 2. Extract Zenodo package into workspace
tar -xzf icc_v2_reproducibility_package.tar.gz

# 3. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 4. Verify artifact and dataset checksums
python scripts/verify_checksums.py

# 5. Recompute all manuscript tables from raw data
python scripts/reproduce_tables.py
```

---

## 5. Summary Recommendation

1. **Un-ignore Recovered Results in Git or Add Zenodo Hook:** Add an explicit `.gitignore` negation (`!results/evidence_recovery/recovered/`) to ensure the recovered evidence is permanently tracked in Git history.
2. **Deposit Zenodo Archive Prior to Resubmission:** Generate the tarball according to Section 3.2, deposit it on Zenodo under a CC-BY 4.0 license, and include the minted DOI in the manuscript's Data Availability Statement.
