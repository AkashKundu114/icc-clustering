# Reproduction tier status

Tested using a fresh shallow clone of the fetched public target at exact commit `d0c4665af327ec284d931c94f9658309ec13763c`, not the ignored local `paper/`, `results/`, or `data/` trees.

| Tier | Status | What is established |
|---|---|---|
| Tier 1 — aggregate verification | **PASS** | Tracked aggregate-only script recalculates 72 summary rows, 6 datasets × 12 methods and mean stability / external ARI / mean gap / median gap. It reads stored aggregate summaries, not raw runs. |
| Tier 2 — partition-level verification | **FAIL in clean clone; locally available evidence is separate** | Clone lacks the 4,320 NPY partitions, 4,320 Parquet records and six caches. No claim that public users can reconstruct pairwise stability or per-repeat ARI. |
| Tier 3 — full experimental reproduction | **NOT RUN** | Original producer/configuration/execution chain is not authenticated; raw inputs and exact runtime environment are not in clone. No fresh clustering fits were executed. |

This is not a certification or badge. Tier 1 arithmetic must not be described as full reproducibility. The aggregate verification script writes one untracked `recomputed.json` into the temporary clone; its generation is recorded as test output, not treated as a clean unchanged working tree after execution.
