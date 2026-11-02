# Datasets and access

The code registry lists 13 datasets used by the broader external-ARI benchmark. Registry dimensions below are configured/expected metadata, not a guarantee that a fresh upstream download has been validated byte-for-byte. The stability analysis uses only the six biomedical cohorts CNS, Colon, Leukemia, Ovarian, Prostate, and SRBCT. No raw datasets, caches, partitions, or sample-level identifiers are included in this public documentation draft.

| Dataset (registry identifier) | Registry N × D; K | Source/access | Rights and release status |
|---|---:|---|---|
| CNS (`cns`) | 60 × 7,129; 2 | [OpenML 45086](https://www.openml.org/d/45086) | Dataset-specific terms and derived-cache redistribution not cleared. |
| Colon (`colon`) | 62 × 2,000; 2 | [OpenML 45087](https://www.openml.org/d/45087) | Dataset-specific terms and derived-cache redistribution not cleared. |
| Indian Pines (`indian_pines`) | 10,249 × 200; 16 | [University of the Basque Country source file](https://www.ehu.eus/ccwintco/uploads/6/67/Indian_pines_corrected.mat) | Source-specific redistribution terms not confirmed; do not bundle. |
| Isolet (`isolet`) | 7,797 × 617; 26 | [OpenML 300](https://www.openml.org/d/300) | Dataset-level terms not confirmed; obtain source attribution and terms. |
| Leukemia (`leukemia`) | 72 × 7,129; 2 | [OpenML 1104](https://www.openml.org/d/1104) | Source/accession terms and derived-data rights not cleared. |
| Madelon (`madelon`) | 500 × 500; 2 | [OpenML 1485](https://www.openml.org/d/1485) | Dataset-level license not verified for this configured subset. |
| Newsgroups20 (`newsgroups20`) | 18,846 × 10,000; 20 | [UCI record](https://archive.ics.uci.edu/dataset/113/twenty+newsgroups) / scikit-learn loader | UCI record reports CC BY 4.0, but text-derived processed data and this exact vectorization need separate review; no cache release cleared. |
| Ovarian (`ovarian`) | 253 × 15,154; 2 | [OpenML 45098](https://www.openml.org/d/45098) | Dataset-specific terms and derived-cache redistribution not cleared. |
| Prostate (`prostate`) | 102 × 12,600; 2 | [OpenML 45099](https://www.openml.org/d/45099) | Source-specific human-data/attribution review incomplete; no cache release cleared. |
| Sonar (`sonar`) | 208 × 60; 2 | [OpenML 40](https://www.openml.org/d/40) | Dataset license not confirmed in the current rights review. |
| SRBCT (`srbct`) | 83 × 2,308; 4 | [OpenML 45101](https://www.openml.org/d/45101) | Source/accession and derived-data terms not cleared. |
| Yale B (`yale_b`) | 2,414 × 1,024; 38 | [Yale Face Database B](https://cvc.cs.yale.edu/cvc/projects/yalefacesB/yalefacesB.html) | Research use with acknowledgement; redistribution of images is not permitted absent Yale permission. Do not distribute images, caches, or partitions. |
| Zheng68K (`zheng68k`) | 700 × 765; 10 | Loader uses Scanpy reduced PBMC resource; upstream [10x Genomics datasets](https://www.10xgenomics.com/datasets) | Exact variant/source identity and terms are unresolved. Do not assume `PBMC68k` means the same artifact as this reduced registry variant. |

The values above are taken from the software registry; Madelon refers to the configured 500-row experiment subset, not the complete upstream archive. The source links identify provider records but do not replace the original study citation. Dataset-specific bibliography recommendations have not been verified for every entry. The rights statuses follow the available source-specific review and are not legal advice or permission to redistribute. For every source, researchers must check current provider terms, cite the dataset record and underlying study as instructed by its provider, record release/version and retrieval date, and retain local hashes. If access is restricted, obtain access from the provider; do not place raw, transformed, or sample-level derived data in this repository.

## Preprocessing in the software

`configs/datasets.yaml` declares imputation, standardization, log transformation, and (where relevant) feature filtering. The common preprocessing helper mean-imputes missing features when enabled, optionally applies `log1p` to nonnegative inputs, standardizes columns, and encodes labels. Dataset loaders can apply domain-specific transformations before that helper. These are code-level behaviors; they do not authenticate historical experiment preprocessing.
