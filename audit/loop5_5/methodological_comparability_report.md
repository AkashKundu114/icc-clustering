# Methodological comparability

The additional seven datasets cannot be added to the stability–accuracy estimand from available records. The stability summary contains exactly 72 rows: six biomedical datasets × twelve methods, one aggregate record per cell. It has neither repetitions nor sample-level assignments. The 13-dataset `results.json` contains 1,430 external-ARI runs (13 × 11 × 10 seeds), but it is a distinct benchmark pipeline and stores no matching stability measures.

| Design element | Six-cohort summary | 13-dataset benchmark | Audit conclusion |
|---|---|---|---|
| Repetitions | No per-repeat observations; Loop 5.4 describes 30 stratified 80% draws, but raw draws absent | 10 initialization seeds per cell | Different stochastic units |
| Methods | 12, including CoreHalo, CoHiRF, GAC, StdCons, UngatedAC | 11, including ICC_v1/v2, Standard_Consensus, Li_et_al_2019 | No complete common method identity map; GAC/ICC_v2 may be related but this is not a verified crosswalk |
| Datasets | CNS, Colon, Leukemia, Ovarian, Prostate, SRBCT | 13 named benchmark datasets | Only six overlap by name; other seven have no stability records |
| K | Registry K values; exact actual K behavior unavailable | K recorded in metric rows; method-level assignments absent | Fixed/estimated behavior not established consistently |
| Sampling/seed | Aggregate summary has no seed/draw identifiers | 10 seeds 42,101,…,909; one seed per config hash | Not pairable to stability draws |
| ARI and stability | Both columns in one summary cell | ARI only in broad benchmark | Same-cell aggregation is not proof of paired observations |
| Missing/singletons/overlap | Assignment-level handling unavailable | Assignment-level handling unavailable | Unverifiable |

No comparable paired experiment can be reconstructed without inventing pairings. The eligible expansion count is therefore **zero additional datasets; the only paired aggregate table remains 6 × 12 = 72 cells**, with repeated-observation uncertainty unavailable. The broad benchmark is reportable separately as external-ARI performance only.
