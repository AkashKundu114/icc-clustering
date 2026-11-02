# Minimum Public Reproduction Package Specification for Zenodo Deposit

**Phase:** Loop 5.4 — Final Adversarial Statistical Validation & Manuscript Claim Adjudication  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Target Archive Name:** `icc_v2_dmkd_reproduction_bundle.tar.gz` (Estimated size: $\approx 118\text{ MB}$)  
**Target DOI Service:** Zenodo (CERN / OpenAIRE)  
**Date:** November 2026  
**Auditor:** Agent C — Data & Provenance Specialist  
**Deliverable Associated:** [minimum_public_reproduction_package.md](file:///d:/icc-clustering/audit/loop5_4/minimum_public_reproduction_package.md)

---

## 1. Package Architecture & Archive Layout

Because the Git repository excludes large data caches and raw result arrays via `.gitignore`, this specification defines the self-contained archive to be deposited on Zenodo. Unpacking this archive into the root of a cloned repository restores 100% of the inputs required for Tier 1 (push-button table generation) and Tier 2 (live benchmark re-execution).

```text
icc_v2_dmkd_reproduction_bundle/
├── README_REPRODUCTION.md                  <- Comprehensive push-button verification guide
├── LICENSE.md                              <- Dual-licensing legal specification
├── checksums.sha256                        <- Cryptographic integrity manifest
├── data/
│   └── cache/                              <- 14 preprocessed benchmark datasets (115.8 MB)
│       ├── breast_cancer.npz
│       ├── cns.npz
│       ├── colon.npz
│       ├── indian_pines.npz
│       ├── isolet.npz
│       ├── leukemia.npz
│       ├── madelon.npz
│       ├── newsgroups20.npz
│       ├── ovarian.npz
│       ├── prostate.npz
│       ├── sonar.npz
│       ├── srbct.npz
│       ├── yale_b.npz                      <- Licensed under CC-BY-NC 4.0
│       └── zheng68k.npz
└── results/
    └── evidence_recovery/
        └── recovered/                      <- 14 canonical recovered evidence artifacts (2.4 MB)
            ├── results.json                <- Master trial archive (1,430 core exp3_1 fits)
            ├── stats.json                  <- Omnibus summary tables & rank records
            ├── subsample_stability_summary.csv <- 72-cell discordance matrix
            ├── exp2_real_high_d_factorial.csv  <- 420-run factorial ablation logs
            ├── adversarial_autok_raw_results.csv <- 510-trial AutoK collapse logs
            ├── exp1_generalization_summary.json
            ├── exp4_anchor_budget_summary.json
            ├── exp7_extreme_scaling_summary.json
            ├── exp8a_distance_geometries_summary.json
            ├── exp8b_spectral_anchor_budget_summary.json
            ├── exp8c_matched_feature_budget_summary.json
            ├── exp8d_non_euclidean_distance_summary.json
            ├── exp8e_large_k_anchor_budget_summary.json
            └── table02_real_data_stability.csv
```

---

## 2. Inventory of Included Artifacts and Cryptographic Checksums

### 2.1 Recovered Experimental Evidence Artifacts (`results/evidence_recovery/recovered/`)

| File Name | Exact Size (Bytes) | Cryptographic SHA-256 Digest | Role in Reproduction |
|:---|:---:|:---|:---|
| `results.json` | 1,627,258 | `0e5d2c10343ba077ff109e5f6554ecc191d89a590dfaf28bec2ef3e950e3ba27` | Master benchmark run logs; generates Table 6 & scaling figures |
| `stats.json` | 11,858 | `83858600000b0d02fbad9742c333d634621f2fc1c64fdcd848c689ea952c4761` | Table 6 summary moments and rank comparisons |
| `subsample_stability_summary.csv` | 10,622 | `577cbab79913020ce362b8280ccb8c7ef62952d28ea47a45950f75cca2ff4b4f` | Core discordance matrix; generates Table 2 & cluster bootstrap |
| `exp2_real_high_d_factorial.csv` | 43,385 | `50bc54c6855fd50d3cd61329d776aa2d998238a232b339075fe588800745c458` | Generates Table 12 / 14 factorial ablation analysis |
| `adversarial_autok_raw_results.csv` | 104,264 | `b61898c371e6e5c7dd1a72de560a257e6c184f59860804d716d4b0c58bbe402a` | Generates Section 3.3 AutoK adversarial collapse evaluation |
| `exp1_generalization_summary.json` | 8,921 | `d289115b0266f81a7071eb329a21e4ea470f1190bc1f9b3117b4ab36a3f908e2` | Generates Table 3 inductive generalization bounds |
| `exp4_anchor_budget_summary.json` | 7,419 | `ac12411516bf1480cfb7a8ee1b75c87bc00e1273950af3dfc8ae1fb5c9cb6b62` | Generates anchor budget scaling figures |
| `exp7_extreme_scaling_summary.json` | 6,512 | `9815ea71a931cb7f1262dca9ee127b8af5c719e7ae9251f7bb8ce2c18ab2cb1e` | Generates Table 5 extreme sample scaling |
| `table02_real_data_stability.csv` | 7,137 | `da745ed9ce810620d3ec639260f4cbeea82355ae8fd5c067a00b38aba8cbf641` | Tabular export of manuscript Table 2 |

### 2.2 Benchmark Dataset Cache (`data/cache/`)

| Dataset Name | File Format | Samples ($N$) | Features ($D$) | Size (Bytes) | Cryptographic SHA-256 Digest |
|:---|:---:|:---:|:---:|:---:|:---|
| `cns.npz` | NumPy Archive | 60 | 7,129 | 1,712,410 | `38b4d8ec5611488c9cf0b04e6bbaf22c36a445e3ea1e0abf90c4d8ce8e5c1d68` |
| `colon.npz` | NumPy Archive | 62 | 2,000 | 497,212 | `6062fec2eb57f86f7b949c51c3ec6620ca533b664d0fe2c47a3e2a050f2aece0` |
| `leukemia.npz` | NumPy Archive | 72 | 7,129 | 2,054,784 | `2a84e91fc64b4c7349942a0336cebf9f2c253245bbef2c569fffa361abef2322` |
| `ovarian.npz` | NumPy Archive | 253 | 15,154 | 15,338,412 | `4e80bb3b37996ac6c87cfef7414bcda9a5a7dfc0eeff7a7ae4f3f1e9447473a5` |
| `prostate.npz` | NumPy Archive | 102 | 12,600 | 5,142,884 | `b09f427f711204cfbf65c1920786cf88ab94f7d23d8c4749f7ba3043818e9505` |
| `srbct.npz` | NumPy Archive | 83 | 2,308 | 768,418 | `132af2927ea9fc512017361a9953934d40bc43a123ee9099df2f62363152be33` |
| `yale_b.npz` | NumPy Archive | 2,414 | 1,024 | 11,842,670 | `f280cb02ee960aa460dc1d054238e8ec2ebf1a30f30c6a3861a1290326d95397` |
| `zheng68k.npz` | NumPy Archive | 68,579 | 1,000 | 68,610,412 | `a9117c2f0b7415ee516bb59fa99178de34af100c6d36e2f69842a170564e9a4f` |

---

## 3. Push-Button Verification Instructions for External Reviewers

### Step 1: Environment Setup
```bash
git clone https://github.com/AkashKundu114/icc-clustering.git
cd icc-clustering
pip install -r requirements.txt
```

### Step 2: Extract Reproduction Bundle
```bash
tar -xzf icc_v2_dmkd_reproduction_bundle.tar.gz -C .
sha256sum -c checksums.sha256
```

### Step 3: Tier 1 Reproduction (Regenerate All Manuscript Tables)
```bash
python audit/loop5_4/clustered_bootstrap_independent_verification.py
python audit/loop5_4/generate_friedman_validation.py
```
- Output: Validates Table 2 discordance metrics, clustered bootstrap CIs, and Table 6 Friedman ranks.

### Step 4: Tier 2 Reproduction (Re-Run GAC on Leukemia Benchmark)
```bash
python scripts/run_single_benchmark.py --dataset leukemia --method icc_v2 --seeds 10
```

---

## 4. Legal & Licensing Notice (`LICENSE.md`)

```markdown
# Replication Package Licensing Agreement

This replication bundle contains multiple research assets subject to the following terms:

1. Software Code and Derived Summary Data:
   Copyright (c) 2026 Akash Kundu and Project Contributors.
   Licensed under the Creative Commons Attribution 4.0 International (CC-BY 4.0).
   You are free to share and adapt the material for any purpose, with appropriate credit.

2. Third-Party Academic Datasets:
   - Leukemia, Colon, SRBCT, CNS, Prostate, Ovarian datasets: Public domain open access.
   - Extended Yale B Database (yale_b.npz):
     Copyright (c) 2001 Yale University.
     DISTRIBUTED EXCLUSIVELY UNDER CREATIVE COMMONS ATTRIBUTION-NONCOMMERCIAL (CC-BY-NC 4.0).
     Academic research and non-commercial educational use only. Commercial use is strictly prohibited.
```

---

## 5. Zenodo Metadata & Deposit Specification

- **Title:** Replication Package for: *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*
- **Creators:** Kundu, Akash; et al.
- **Description:** Complete independent replication archive containing preprocessed microarray benchmarks, single-cell cohorts, consensus partition outputs, bootstrap verification scripts, and raw execution logs for Springer Nature DMKD submission.
- **Keywords:** Consensus Clustering, Clustering Stability, High-Dimensional Genomics, Microarray, Bipartite Graphs, Reproducibility.
- **Access Rights:** Open Access (with dual-licensed Non-Commercial restriction on `yale_b.npz`).
