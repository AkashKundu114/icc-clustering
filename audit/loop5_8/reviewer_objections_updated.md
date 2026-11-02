# Updated adversarial reviewer objections

1. **Which manuscript is under review?** The target GitHub checkout has no tracked manuscript. The accessible FYP draft is a separate repository branch and contains many later claims. Submission must freeze and identify one exact version/hash.
2. **What does stability mean here?** It is an average of 435 dependent pairwise ARIs, over overlapping partitions that reuse samples; this does not measure independent repeat outcomes. Class-stratified subsampling uses labels, and the solver seed is fixed, so the design is not label-blind and does not test initialization sensitivity.
3. **Is the bootstrap estimate coherent?** The manuscript combines a cell-weighted point with an equal-cohort bootstrap distribution. Only six cohorts are present; any cohort bootstrap is exploratory absent a defensible sampling frame.
4. **Why feature the selected nine?** The nine cells are a post-hoc selection. The “all 18” values refer to a different population from the Rule(i′) 18 cells. Selection must be transparent and supplementary.
5. **Are repeated partitions independently produced?** The artifacts are internally complete, but per-run cache hashes/protocol commit/execution logs are missing. Three exact cross-method/mode duplicates and 140 repeated-hash groups require explanation; no partition-producing script was recovered.
6. **Can readers reproduce the result?** A fresh target clone reproduces only aggregate arithmetic. It lacks the input caches, partitions, run files, raw benchmark scores and exact FYP manuscript. The DOI has no public files.
7. **Are benchmark comparisons correctly described?** Saved score rows support the count and Friedman statistic but have different seed schedules across Pass F and CoHiRF. This is a recomputation of scores, not fit-execution authentication.
8. **Are the broader claims supported?** The draft adds confirmatory, ablation, theoretical, biological, clinical, memory and runtime claims not examined by the Loop5.7/5.8 core evidence review. A prior FYP red-team report alleges baseline proxy/fidelity, leakage and cohort-overlap problems. These need item-level resolution before headline claims remain.
9. **Are data public and redistributable?** A URL to a dataset does not establish redistribution rights; no complete public package has passed acquisition-to-output testing.

**Recommendation:** Major revision / HOLD. Retain only bounded six-cohort descriptive claims and separately qualified saved-score benchmark results pending the evidence and manuscript-version blockers.
