# Dataset access and third-party terms

The dataset registry lists 13 variants. Shapes below are configured registry values, not a guarantee that a fresh upstream download has been matched byte-for-byte. Rights decisions are conservative: **REDISTRIBUTION_NOT_CLEARED** means this review did not establish affirmative permission to redistribute the exact repository variant; it does not assert that use is forbidden. The MIT software license does not apply to dataset files or derivatives. Do not bundle raw data, caches, sample IDs, partitions, or derived records without rights for the exact variant.

| Dataset / registry variant | Configured N × D; K | Source and access | Associated source citation | Terms and release status |
|---|---:|---|---|---|
| CNS | 60 × 7,129; K=2 | [OpenML and Pomeroy et al. CNS cohort](https://www.openml.org/d/45086) | Pomeroy et al. Nature 2002; confirm exact citation from source record | REDISTRIBUTION_NOT_CLEARED; variant identity/attribution limitations apply. |
| Colon | 62 × 2,000; K=2 | [OpenML and Alon et al. colon cohort](https://www.openml.org/d/45087) | Alon et al. PNAS 1999; confirm exact citation from source record | REDISTRIBUTION_NOT_CLEARED; variant identity/attribution limitations apply. |
| Indian Pines | 10,249 × 200; K=16 | [EHU-hosted Indian Pines corrected scene; related Purdue PURR original AVIRIS record](https://www.ehu.eus/ccwintco/uploads/6/67/Indian_pines_corrected.mat) | EHU corrected variant; Purdue Baumgardner et al. record is a different 220-band product | REDISTRIBUTION_NOT_CLEARED; variant identity/attribution limitations apply. |
| Isolet | 7,797 × 617; K=26 | [OpenML; canonical UCI ISOLET dataset 54](https://archive.ics.uci.edu/dataset/54/isolet) | Cole & Fanty (1991); UCI DOI 10.24432/C51G69 | REDISTRIBUTION_NOT_CLEARED; the named canonical-source license does not clear this variant. |
| Leukemia | 72 × 7,129; K=2 | [OpenML; Golub et al. leukemia cohort](https://www.openml.org/d/1104) | Golub et al. Science 1999; confirm exact citation and source terms | REDISTRIBUTION_NOT_CLEARED; variant identity/attribution limitations apply. |
| Madelon | 500 × 500; K=2 | [OpenML challenge variant; UCI canonical Madelon dataset 171](https://www.openml.org/d/1485) | Guyon et al. NIPS feature selection challenge; UCI DOI 10.24432/C5602H | REDISTRIBUTION_NOT_CLEARED (variant identity unresolved); attribution limitations apply. |
| Newsgroups20 | 18,846 × 10,000; K=20 | [UCI 20 Newsgroups record / scikit-learn fetcher](https://archive.ics.uci.edu/dataset/113/twenty+newsgroups) | UCI source citation / Tom Mitchell (1997); verify filtered collection attribution | REDISTRIBUTION_NOT_CLEARED; the named canonical-source license does not clear this variant. |
| Ovarian | 253 × 15,154; K=2 | [OpenML and Petricoin et al. ovarian cohort](https://www.openml.org/d/45098) | Petricoin et al. Lancet 2002; confirm exact source citation | REDISTRIBUTION_NOT_CLEARED; variant identity/attribution limitations apply. |
| Prostate | 102 × 12,600; K=2 | [OpenML and Singh et al. prostate cohort](https://www.openml.org/d/45099) | Singh et al. Cancer Cell 2002; confirm exact source citation | REDISTRIBUTION_NOT_CLEARED; variant identity/attribution limitations apply. |
| Sonar | 208 × 60; K=2 | [OpenML variant; canonical UCI Sonar record](https://archive.ics.uci.edu/dataset/151/connectionist%2Bbench%2B%28sonar%2C%2Bmines%2Bvs.%2Brocks%29) | Sejnowski & Gorman (1988); UCI DOI 10.24432/C5T01Q | REDISTRIBUTION_NOT_CLEARED for the OpenML variant until identity with the CC BY 4.0 UCI record is verified. |
| SRBCT | 83 × 2,308; K=4 | [OpenML and Khan et al. SRBCT cohort](https://www.openml.org/d/45101) | Khan et al. Nature Medicine 2001; confirm exact citation | REDISTRIBUTION_NOT_CLEARED; variant identity/attribution limitations apply. |
| Yale B | 2,414 × 1,024; K=38 | [Yale University Vision Lab](https://cvc.cs.yale.edu/cvc/projects/yalefacesB/yalefacesB.html) | Cite the Yale Face Database B source paper as required by Yale | RESTRICTED; permission is required before redistribution; variant identity/attribution limitations apply. |
| Zheng68K / PBMC68k | 700 × 765; K=10 | [Scanpy example dataset derived from 10x Genomics historical PBMC 68k source](https://github.com/10XGenomics/single-cell-3prime-paper) | Zheng et al. (2017) source family; cite exact Scanpy distribution and variant | REDISTRIBUTION_NOT_CLEARED; variant identity/attribution limitations apply. |

**REDISTRIBUTION_NOT_CLEARED** means this review did not establish permission for the exact configured variant. A canonical-source license does not automatically extend to an OpenML/scikit-learn copy or subset.

## Dataset-specific cautions

- OpenML dataset metadata containing `licence=Public` is not a named standard redistribution license and is not enough to clear a local copy. For OpenML datasets, use the dataset page’s current license/citation record and confirm the exact version.
- Canonical UCI pages for ISOLET, 20 Newsgroups, Sonar, and Madelon report CC BY 4.0, but the project uses OpenML/scikit-learn variants or a selected subset. The canonical terms do not automatically establish permissions for those exact variants.
- The project registry points to the EHU corrected 200-band Indian Pines file. Purdue’s CC0 record concerns a distinct 220-band item; do not transfer its license to the EHU variant.
- Yale’s official page permits research use with acknowledgment but requires permission to include images in a publicly distributed larger database. Do not redistribute images or derived sample-level artifacts absent permission.
- The registry’s `Zheng68K` entry uses Scanpy’s `pbmc68k_reduced` example (700 samples × 765 features), not the full 68,579-cell Zheng matrix. The names refer to related source family, not identical feature matrices; exact lineage and rights remain unresolved.

For any use, acquire data from the linked official provider, follow its current terms, cite the exact source/version and underlying study, record retrieval date and local checksums, and do not share uncleared transformed or sample-level artifacts.
