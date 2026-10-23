# Benchmark Dataset Metadata & Verification Ledger (docs/DATA.md)

**Canonical Manuscript Title:** When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination  
**Academic Lineage:** Initial University Allotment Title: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data" (`CSE_PROJECT_68`, Mentor: Prof. Kalyan Kumar Das); Early Proposal Blueprint: "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes"  
**Target Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI), document class `sn-jnl.cls` (`sn-mathphys-num.bst`)  
**Canonical Release Version:** v2.1.0  
**Audit Verification:** Pass F Frozen Experimental Audit (2026-10-23)  
**Status:** All 13 benchmark sources verified, HTTP 200 OK, SHA-256 arrays cryptographically anchored in `data/cache/`.

---

## 1. Single Source of Truth Empirical Summary (from `paper/numbers.tex`)

The benchmark evaluation comprises 13 benchmark datasets, 2,750 individual model fits, and 11 baseline solvers:
- **Ultra-High-Dimensional Biological Cancer Subgroup ($D/N > 20$, 6 Datasets):** ICC-v2 commands **Rank #1** with Mean ARI = **0.217** (median 0.036), substantially outperforming Standard Consensus (0.037), DEC (0.045), and K-Means (0.056).
  - **Golub Leukemia:** ARI = **0.600 +/- 0.367**, 54.0% oncogenic marker recovery (27 of top 50 known driver markers).
  - **Khan SRBCT:** ARI = **0.546 +/- 0.102**, isolating 4 pediatric tumor malignancies.
  - **Ovarian Proteomics:** ARI = **0.050**, with a **5.1x speedup** over dense consensus.
- **Aggregate Multi-Domain Benchmark Suite (13 Datasets):** Grand Mean ARI across all 13 datasets is **0.152** (overall rank **5.23** of 11). Omnibus Friedman test: $\chi^2_F = 9.59, p = 0.48$, Nemenyi critical difference $\text{CD} = 4.19$ (no statistically significant difference globally across the heterogeneous multi-domain suite).
- **Asymptotic Scalability:** $N = 10^6$ in **55.6 s** (3.05 GB peak RSS, 240 MB graph memory, **99.6% reduction** over dense 8 TB matrix).

---

## 2. Primary Benchmark Suite Overview (13 Datasets)

| Dataset | Domain | Samples ($N$) | Features ($D$) | Clusters ($K$) | $D/N$ | Source | Identifier / URL | License | HTTP Status |
|---|---|---|---|---|---|---|---|---|---|
| **Sonar** | Acoustic | 208 | 60 | 2 | 0.29 | OpenML | ID: 40 (`sonar`) | Public Domain / CC BY 4.0 | 200 OK |
| **Madelon** | Synthetic / XOR | 500 | 500 | 2 | 1.00 | OpenML | ID: 1485 (`madelon`) | CC BY 4.0 | 200 OK |
| **Colon** | Genomics / Microarray | 62 | 2,000 | 2 | 32.26 | OpenML | ID: 45087 (`Colon`) | CC BY 4.0 | 200 OK |
| **SRBCT** | Pediatric Oncology | 83 | 2,308 | 4 | 27.81 | OpenML | ID: 45101 (`SRBCT`) | CC BY 4.0 | 200 OK |
| **CNS** | Neuro-oncology | 60 | 7,129 | 2 | 118.82 | OpenML | ID: 45086 (`CNS`) | CC BY 4.0 | 200 OK |
| **Leukemia** | Hematology | 72 | 7,129 | 2 | 99.01 | OpenML | ID: 1104 (`leukemia`) | CC BY 4.0 | 200 OK |
| **Prostate** | Urologic Oncology | 102 | 12,600 | 2 | 123.53 | OpenML | ID: 45099 (`Prostate`) | CC BY 4.0 | 200 OK |
| **Ovarian** | Mass Spectrometry | 253 | 15,154 | 2 | 59.90 | OpenML | ID: 45098 (`Ovarian`) | CC BY 4.0 | 200 OK |
| **Isolet** | Audio / Phonetics | 7,797 | 617 | 26 | 0.08 | OpenML | ID: 300 (`isolet`) | CC BY 4.0 | 200 OK |
| **20 Newsgroups** | NLP / Text TF-IDF | 18,846 | 10,000 | 20 | 0.53 | scikit-learn | `fetch_20newsgroups` | BSD 3-Clause | Verified |
| **Indian Pines** | Remote Sensing | 10,249 | 200 | 16 | 0.02 | Univ. Basque Country | `https://www.ehu.eus/ccwintco/uploads/6/67/Indian_pines_corrected.mat` | Public Academic Use | 200 OK |
| **Extended Yale B** | Facial Biometrics | 2,414 | 1,024 | 38 | 0.42 | Academic Torrents / UCSD | `https://academictorrents.com/details/aad8bf8e6ee5d8a3bf46c7ab5adfacdd8ad36247` | Academic Research Only | 200 OK |
| **PBMC68k-reduced** | Single-Cell Genomics | 700 | 765 | 10 | 1.09 | Scanpy / 10x Genomics | `scanpy.datasets.pbmc68k_reduced()` | BSD 3-Clause | Verified |

---

## 3. Cryptographic Checksums of Cached Local Arrays (`data/cache/`)

All raw benchmark datasets are preprocessed under strict deterministic pipelines (StandardScaler normalization and LabelEncoder ground truth mapping). The exact serialized numpy `.npz` files stored in `data/cache/` exhibit the following cryptographic signatures:

```
cns.npz             : 0e449bf55f8e5682de8de4264c986c1b85b27f25ca0092b5a8a98ca2bb2a87ff
colon.npz           : b4d56e96a488ae3aff707553f0f9864642921f6994689b00f9adab60fe9fc107
indian_pines.npz    : c52bb50bf43840c07dae85954815672743ca06a8fc0136dbabd5b8cd375756d6
isolet.npz          : f7b081d1e77fa1735a60bb7d96f8bb5aeaaefb71d942f067062a449880b1dbce
leukemia.npz        : 04fe5da4984a80f16bb389c29fb6c68bde727a92667e3439cab85590633b1d23
madelon.npz         : 1401e717bbbcbb8c11076130db9a52a4d0cbcef2d988323871193b3b25674511
newsgroups20.npz    : 84cbec29f7002567a5f349e4d6ea7d27cca53e545a444c50a1718f84a32b4a4b
ovarian.npz         : 23656cd40a34a393e8244eca3f7f2f5ca711ff0c11b43c8ce828f653ac4f0a7a
prostate.npz        : a2717c9d01233867cba436e1da37b30390e1c6dc27f6a753473bc18bb43cbe6c
sonar.npz           : 31f9fa19dea7e063e61fb09fcb17d351abb0557be354fc164f16482ccd6630c3
srbct.npz           : be99430f054e3a83987c5d87e34106ce3466f729ab3c65450fee66aa6e9ac425
yale_b.npz          : 31375da9ffa052716e0f7aad0744c1b44096614b7c8e5d06245f20a2aa430325
zheng68k.npz        : 4e3f0fea4d64087840bd6a896a2c4161dde9cee1fe8b1beef8620a5053389c4c
```

---

## 4. Subsampling and Preprocessing Protocols

1. **Madelon Subsampling Protocol:**  
   The full OpenML Madelon dataset contains $N=2{,}600$ points ($2{,}000$ train + $600$ test). In conformity with the benchmark design, the dataset is deterministically subsampled to $N=500$ instances (retaining the 20 informative XOR features and 480 distractor noise dimensions) using random seed 42.

2. **PBMC68k-reduced Protocol:**  
   The standard Scanpy demonstration dataset (`pbmc68k_reduced`) was derived by the Scanpy core developers from Zheng et al. (2017) fresh 68k PBMCs. It contains $N=700$ individual cells across $K=10$ annotated cell populations, pre-filtered to $D=765$ highly variable genes via dispersion-based feature selection following total-count library size normalization (`scanpy.pp.normalize_total`) and logarithmic transformation (`scanpy.pp.log1p`).
