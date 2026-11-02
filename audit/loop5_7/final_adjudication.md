# Loop 5.7 final adjudication

## Direct answers

1. **Are 4,320 partitions and 4,320 fit records authentic and internally consistent?** Internally consistent in the recovered local tree: all present, statuses success, 30 distinct splits/cohort, metadata and paired splits pass. Their historical authenticity/execution time is **CONDITIONAL**; records do not bind to input hash or source commit. Duplicate-content flags require explanation.
2. **Are 72 metrics independently reconstructed correctly?** Yes from stored assignments and caches. All 72 match; max errors: stability 1.11e-16, external ARI 9.71e-17, null 9.92e-17. This is reconstructed metrics, not fit reruns.
3. **Is mean gap .464274 and median .448407 defensible?** Yes as descriptive statistics: mean of 72 within-cell `mean(435 intersection ARIs) − mean(30 label ARIs)` gaps; median across 72 gaps. Not independent-observation inference or universal excess-validity scale.
4. **Is the nine-cell result defensible?** Numeric and membership are reproduced. Rule(i)=20, Rule(i′)=18 across all methods, recurrence condition selects nine cells for FCAG/FCM/FastMVC. It remains post-hoc and conditional; decision: **retain as exploratory supplementary analysis**, not headline or confirmation. It is stable only across the tested 2/5/10% and 25/27/29/30 grid.
5. **Are stability and ARI genuinely paired?** They use the same 30 partitions/split schedule within each cohort-method. This is configuration-level pairing, not one-to-one repeat pairing: one stability summary derives from 435 dependent pairs while ARI averages 30 draws.
6. **Is the original experiment reproducible from recovered evidence?** Metric reconstruction from local saved partitions, fit rows and matching cache version is reproducible. Fresh original model fitting is not performed and exact fit-to-cache link is unverified.
7. **Publicly reproducible?** No. Clean main clone reproduces only aggregate CSV arithmetic. It lacks partitions, fits, caches and 13-dataset raw score CSVs; DOI has restricted access/zero files.
8. **Are 13-dataset claims verified?** Count and p=.40 reproduce from 3,000 raw score rows: 2,750 Pass F + 250 CoHiRF, 13 datasets, 12 methods, 156 complete cells, χ²=11.556213, df=11, p=.397908, ICC-v2 rank 4/12. No duplicate keys. These score files are tracked in local FYP history but not target public main; seed schedule inconsistencies remain.
9. **What is wrong with current CI?** The 60 nondegenerate cell-weighted point mean is .485376. Fresh 10,000-resample CI [.378581,.661716] uses equal-weight resampled cohort means centered at .499925; checked historical sequential-RNG path gives [.381104,.653002]. Both are positive, but neither licenses confirmatory generalization and the manuscript point/CI estimator pairing is inconsistent.
10. **Claims to remove/qualify?** Qualify nine as exploratory; clarify different 18-cell populations and gap definition; fix bootstrap estimand; correct benchmark seed schedules; remove full public-archive claim; narrow high-dimensional causal, Prostate mechanism, clinical and ICC superiority claims unless separately verified. GAC ablation results are outside this Loop.
11. **What blocks DMKD submission?** Unified committed audit workflow, authentic run-to-input/protocol lineage, public reproduction artifact, bootstrap reanalysis/estimand correction, benchmark seed/config reconciliation, duplicate partition explanation, exact committed manuscript and rights/attribution review.

## Claim confidence

| Claim | Status | Confidence | Evidence class |
|---|---|---:|---|
| 72-cell mean/median gap | VERIFIED as descriptive on recovered files | High numerical / conditional provenance | Local partition-level reconstruction |
| 4,320×2 grid completeness and pairing | CONDITIONALLY VERIFIED | High internal consistency / moderate authenticity | Local files, no per-run input digest |
| Rule(i), Rule(i′), nine membership and means | VERIFIED computationally; DESCRIPTIVE ONLY inferentially | High arithmetic / low confirmatory | Direct labels+partitions; post-hoc rule |
| Nondegenerate .485 point estimate | VERIFIED descriptively | High numeric | 60-cell filtered cell mean |
| Manuscript CI +.379,.662 for .485 point | CONTRADICTED as same-estimand interval | High | Bootstrap code and independent resampling |
| 13×12×3000 raw score count | VERIFIED in local FYP artifacts | High count / conditional execution provenance | Tracked CSV rows |
| Friedman p=.40, 12 methods | VERIFIED from saved score means | High recalculation / conditional fit provenance | 3,000 raw ARI records |
| Full public reproduction | CONTRADICTED | High | Clean clone + Zenodo/release checks |
| ICC universal superiority/clinical mechanism | UNSUPPORTED by this audit | High | No relevant controlled evidence in recovered artifacts |

## Final gate

**HOLD.** The central descriptive stability–accuracy result survives numerical reconstruction, and the separate broader benchmark's 3,000-row statistic is now independently reproduced. Submission remains blocked by provenance/public reproducibility, stale contradictory Loop 5.6 artifacts, seed/config inconsistencies, and the bootstrap estimand mismatch.
