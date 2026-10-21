# Benchmark Datasets and Data Management

This directory manages all raw, cached, and preprocessed datasets used in Inductive Consensus Clustering (ICC / CICC).

## Repository Policy
In strict compliance with GitHub repository size guidelines and scientific open-access licensing:
- **No large binary datasets (`*.npz`, `*.mat`, `*.h5ad`, `*.tar.gz`) are committed to Git.**
- All raw datasets and caches are ignored by Git via `.gitignore`.
- Datasets are automatically downloaded, verified, and preprocessed via `scripts/fetch_data.py`.

## Directory Layout
```text
data/
├── raw/        # Original, immutable downloads from OpenML and public repositories
├── interim/    # Intermediate representations and feature-filtered arrays
├── processed/  # Canonical, standardized benchmark matrices ready for models
└── cache/      # High-speed memory-mapped and compressed tensors (.npz)
```

## Benchmark Datasets Overview
The evaluation suite benchmarks ICC across 13 diverse real-world datasets spanning cancer genomics, acoustics, biometrics, text, and speech:

| Dataset | Domain | Samples ($N$) | Features ($D$) | Clusters ($K$) | Source / Endpoint | Upstream License |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| **Sonar** | Acoustic Sensors | $208$ | $60$ | $2$ | OpenML ID 40 (UCI) | CC-BY-4.0 |
| **Madelon** | Synthetic Distractor | $500$ | $500$ | $2$ | OpenML ID 1485 (NIPS 2003) | Public Domain |
| **Colon** | Cancer Genomics | $62$ | $2{,}000$ | $2$ | OpenML / Princeton Data | Academic Open Access |
| **SRBCT** | Cancer Genomics | $83$ | $2{,}308$ | $4$ | OpenML / NHGRI | Academic Open Access |
| **CNS** | Cancer Genomics | $60$ | $7{,}129$ | $2$ | OpenML / Whitehead Inst. | Academic Open Access |
| **Leukemia** | Cancer Genomics | $72$ | $7{,}129$ | $2$ | OpenML / Broad Institute | Academic Open Access |
| **Prostate** | Cancer Genomics | $102$ | $12{,}600$ | $2$ | OpenML / Harvard Data | Academic Open Access |
| **Ovarian** | Mass Spectrometry | $253$ | $15{,}154$ | $2$ | OpenML / NCI-FDA | Public Domain |
| **20 Newsgroups** | Sparse Text | $18{,}846$ | $10{,}000$ | $20$ | `sklearn.datasets` | Open Research Data |
| **Isolet** | Speech Recognition | $7{,}797$ | $617$ | $26$ | OpenML ID 300 (UCI) | CC-BY-4.0 |
| **Indian Pines** | Hyperspectral | $10{,}249$ | $200$ | $16$ | Purdue University AVIRIS | NASA / Academic Public |
| **Yale B** | Facial Biometrics | $2{,}414$ | $1{,}024$ | $38$ | Zhejiang University CAD | Academic Research Use |
| **Zheng68k** | scRNA-seq | $68{,}579$ | $2{,}000$ | $11$ | 10x Genomics Cloud | Open Access Single Cell |

## Automated Fetching and Verification
To provision and preprocess all datasets locally:
```bash
python scripts/fetch_data.py
```
This script validates SHA-256 checksums before caching tensors into `data/cache/`.
