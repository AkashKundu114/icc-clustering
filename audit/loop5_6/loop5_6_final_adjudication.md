# Loop 5.6 final adjudication

1. Original inputs: six local preprocessed X/y caches recovered, not source raw matrices or IDs. **CONDITIONALLY VERIFIED.**
2. Resampling partitions: all six cohorts ×12 methods ×30 real/null partitions recovered. **VERIFIED locally.**
3. Per-repeat stability/ARI records: 4,320 fit rows and 62,640 pairwise calculations reconstructed. **VERIFIED locally.**
4. Stability metric: reconstructed from partitions and script; specific to stratified subsampling and intersection ARI. **CONDITIONALLY VERIFIED.**
5. Pairing: same cohort/method/repeat samples underlie stability and external ARI; methods share split schedules. **VERIFIED locally.**
6. Aggregate results: independently recomputed from run-level outputs, max errors ~1e-16. **VERIFIED numerically, conditional provenance.**
7. Mean gap 0.464274: confirmed as equal-weight mean of 72 cell gaps. **VERIFIED DESCRIPTIVELY.**
8. Median gap 0.448407: confirmed median of those 72 cell gaps. **VERIFIED DESCRIPTIVELY.**
9. Nine-cell rule: recovered as posthoc degeneracy screen plus method recurrence. **CONDITIONALLY VERIFIED.**
10. Boolean 20: implements Rule(i) stability≥.50 and ARI≤.05; later degeneracy screen leaves 18, recurrence criterion selects nine. **VERIFIED.**
11. Nine-cell result: retain only qualified as posthoc conditional description, not independent confirmation.
12. Inference: six selected cohorts, dependent cells/repeats; descriptive and exploratory only, no confirmatory generalization.
13. 13-dataset benchmark remains separate external-ARI benchmark. **VERIFIED scope distinction.**
14. 3,000-fit and 12-method claims remain unverified; previous evidence supports 1,430 11-method benchmark records, not the manuscript claim.
15. Clean reproduction: only aggregate arithmetic package reproduced; full experiment cannot be reproduced from fresh clone. **CONDITIONALLY VERIFIED / full package HOLD.**
16. Dataset legal redistribution: unresolved; no blanket authorization established. **UNVERIFIED.**
17. Narrow/remove: nine-cell confirmatory language, universal/general claims, public reproduction assertion, unverified fit/method counts, causal/clinical language, ICC superiority.
18. Needed: public run/partition archive or deterministic reproduction; raw source/version and stable IDs; input hashes attached to runs; preprocessing lineage; rights clearance; resolve benchmark fit/method counts; clean rerun.

## Decisions

| Area | Decision |
|---|---|
| Experimental evidence recovery | CONDITIONAL GO |
| Stability implementation validity | CONDITIONAL GO |
| Aggregate numerical reconstruction | GO (local evidence; provenance conditional) |
| Nine-cell subset | QUALIFY |
| Statistical validity | CONDITIONAL GO (descriptive scope) |
| Public reproducibility | HOLD |
| Manuscript revision | GO |
| DMKD submission | HOLD |
