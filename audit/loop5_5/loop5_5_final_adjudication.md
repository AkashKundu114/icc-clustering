# Loop 5.5 final adjudication

## Direct answers

1. **Are all 13 datasets correctly identified? — CONDITIONALLY VERIFIED.** Keys/names and declared dimensions are inventoried, but exact source arrays, labels and identifiers are absent. Metadata conflicts remain.
2. **Is PBMC68k the same dataset as Zheng68K? — CONTRADICTED as an unqualified claim.** The code aliases a 700-cell reduced Scanpy dataset and also provides a distinct full 68k variant; full mode has constant labels. Current benchmark records identify the reduced 700×765 version.
3. **Which have verified reference labels? — CONDITIONALLY VERIFIED:** the six biomedical cohorts have external ARI summary values; 11-method 13-dataset benchmark records have ARI values for all 13, but no label vectors are present. Zheng label provenance is specifically conflicted. Exact labels are not independently verified for any dataset from raw files.
4. **Which have valid paired stability and external ARI? — Six datasets × 12 methods as aggregate paired columns only (72 cells).** Genuine repetition-level pairing is UNVERIFIED. No additional dataset has paired stability/ARI.
5. **Can the original analysis be expanded? — NO on present evidence.**
6. **How many datasets/methods qualify for expansion? — Zero new datasets.** Existing descriptive summary is six datasets and 12 methods; broad benchmark has 13 datasets and 11 methods for ARI only.
7. **Expanded cell count? — No defensible expanded paired cell count.** Available paired aggregate count remains 72. Broad ARI benchmark is 143 cells and 1,430 seed observations.
8. **Does the central result change? — Materially unchanged in direction and mean gap** on recomputation (0.464274); median differs from prior claimed 0.4700 to 0.448407. Status DESCRIPTIVE ONLY.
9. **Robust to individual datasets/methods? — Descriptive leave-one-out values are saved.** No independent sample-level inference; the nine-cell analysis is unreconciled and not confirmation.
10. **Is 13-dataset Friedman independently reproducible? — CONDITIONALLY VERIFIED** for the 11-method raw ARI matrix: 1430 rows, statistic 11.342657, p=.331452, ICC_v2 rank 5/11. 12-method result UNVERIFIED.
11. **Which results exploratory/descriptive?** Stability gap, all leave-one-out checks, and Friedman cross-domain ranks. No confirmatory inference from these artifacts.
12. **Legally redistributable? — UNVERIFIED.** Yale B redistribution especially unsupported; no blanket CC license can be applied based on repository text.
13. **Fresh clone/archive reproduction? — NO.** Required inputs are ignored/untracked; no verified release archive.
14. **Claims to narrow/remove:** remove 13-dataset expansion of stability–accuracy claim; qualify all 72-cell statistics as aggregate descriptions; correct median; clarify six dataset scope and lack of raw repetitions; reconcile nine-cell selection; qualify Friedman as separate exploratory benchmark; remove unqualified PBMC/Zheng equivalence and license assurances.
15. **Exact next action:** recover and legally clear versioned feature matrices, labels and sample IDs for all candidates; then run one predeclared matched resampling protocol across eligible datasets/methods and archive per-repeat assignments/configs. Do not submit until manuscript claims and public reproducibility are repaired.

## Gate decisions

| Area | Status |
|---|---|
| Dataset inventory | CONDITIONAL GO |
| 13-dataset expansion | HOLD |
| Six-cohort analysis | CONDITIONAL GO |
| Statistical validity | CONDITIONAL GO |
| Public reproducibility | HOLD |
| Manuscript revision | GO |
| DMKD submission readiness | HOLD |

The original six-cohort empirical question remains the appropriate primary focus. Current evidence does not warrant converting the broader 13-dataset benchmark into paired stability–accuracy evidence. ICC remains exploratory; no superiority claim follows from this audit.
