# Roadmap
Plan A (min defensible): A1 correct claims (DONE on branch); A2 pool rule + controls (partially done: pool_mode opt-in, results in 06); A3 unify code paths + embedding proof/test + beta; A4 baselines/citations; A5 rerun Exp1/Exp3/missing-data.
Plan B: theory for conditional BC gating, noise sweeps, stronger baselines, scope narrowed to conditional-gating paper.
Plan C: speculative (learned/adaptive pool sizing; supervised-free stability bounds), validate independently.

## Progress
A1 done; A2 partial (opt-in pool rules + controls; default unchanged); A3 partial (options, tests, measurements; branches not unified); A4 partial (docs/citations/stub flag). Open: faithful FCAG/FastMICE or removal, A5 reruns, pool-size curve (E3), more datasets + FS baselines (E1).

## Progress (E3)
Pool-size curve done: effect real but window-limited and unselectable without labels today. Plan B item added: label-free pool-size selection + dataset-level test across >=20 datasets. Defensible narrowed claim candidate: "BC-ranked wide subspace pools help when informative genes are enriched in the top ~5-15% by bimodality; sensitive outside that band."

## Progress (E3b)
Label-free pool selection: two pre-specified criteria failed. Plan B now frames pool sensitivity as an explicit limitation unless a selector validated on held-out datasets is found. Plan A claim wording: results at the default 15% pool are reported with the pool-size curve alongside.

## Progress (E5)
Exp1 and missing-data claims must be rewritten to the rerun numbers (README patch not yet updated for E5 numbers beyond A1 wording). Open: A5 on 13 datasets (local), E1, E4, scalability (E6), manuscript audit.
