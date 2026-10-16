# Benchmark Datasets Inventory and Licensing (Phase B)

This document provides provenance, download endpoints, citations, and redistribution policies for all 13 benchmark datasets evaluated in Inductive Consensus Clustering (ICC-v2).

All datasets can be downloaded on demand using `python scripts/fetch_data.py`.

---

## 1. Dataset Provenance Matrix

| Dataset | Domain | Samples ($N$) | Features ($D$) | Clusters ($K$) | Source / Endpoint | Upstream Licence | Redistribution Status | Citation |
| :--- | :--- | :---: | :---: | :---: | :--- | :--- | :--- | :--- |
| **Sonar** | Acoustic Sensors | $208$ | $60$ | $2$ | OpenML ID 40 (UCI) | CC-BY-4.0 / Public Domain | Permitted | Gorman & Sejnowski (1988) |
| **Madelon** | Synthetic Distractor | $500$ | $500$ | $2$ | OpenML ID 1485 (NIPS 2003) | Public Domain | Permitted | Guyon et al. (2004) |
| **Colon** | Cancer Genomics | $62$ | $2{,}000$ | $2$ | OpenML / Princeton Data | Academic Open Access | Permitted | Alon et al. (1999) |
| **SRBCT** | Cancer Genomics | $83$ | $2{,}308$ | $4$ | OpenML / NHGRI | Academic Open Access | Permitted | Khan et al. (2001) |
| **CNS** | Cancer Genomics | $60$ | $7{,}129$ | $2$ | OpenML / Whitehead Inst. | Academic Open Access | Permitted | Pomeroy et al. (2002) |
| **Leukemia** | Cancer Genomics | $72$ | $7{,}129$ | $2$ | OpenML / Broad Institute | Academic Open Access | Permitted | Golub et al. (1999) |
| **Prostate** | Cancer Genomics | $102$ | $12{,}600$ | $2$ | OpenML / Harvard Data | Academic Open Access | Permitted | Singh et al. (2002) |
| **Ovarian** | Mass Spectrometry | $253$ | $15{,}154$ | $2$ | OpenML / NCI-FDA | Public Domain (US Gov) | Permitted | Petricoin et al. (2002) |
| **20 Newsgroups** | Sparse Text | $18{,}846$ | $10{,}000$ | $20$ | `sklearn.datasets` | Open Research Data | Download Script Only | Lang (1995) |
| **Isolet** | Speech Recognition | $7{,}797$ | $617$ | $26$ | OpenML ID 300 (UCI) | CC-BY-4.0 / Public Domain | Permitted | Fanty & Cole (1991) |
| **Indian Pines** | Hyperspectral | $10{,}249$ | $200$ | $16$ | Purdue University AVIRIS | NASA / Academic Public | Permitted | Baumgardner et al. (2015) |
| **Yale B** | Facial Biometrics | $2{,}414$ | $1{,}024$ | $38$ | Zhejiang University CAD | Academic Research Use | Download Script Only | Georghiades et al. (2001) |
| **Zheng68k** | scRNA-seq | $68{,}579$ | $2{,}000$ | $11$ | 10x Genomics Cloud | Open Access Single Cell | Download Script Only | Zheng et al. (2017) |

---

## 2. Redistribution Policy

1. **No Raw Data in Git:** Raw multi-megabyte archives (`.mat`, `.tar.gz`, `.h5ad`) are excluded via `.gitignore`.
2. **Automated Verification:** `scripts/fetch_data.py` performs download and SHA256 checksum verification before preprocessing into `data/cache/`.
3. **Attribution:** Any research utilizing these benchmark subsets must cite both the original data creators listed above and the ICC-v2 methodology.
