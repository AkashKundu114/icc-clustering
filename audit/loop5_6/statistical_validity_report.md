# Statistical validity

The 72-cell grid is balanced, so equal cell, dataset-first, and method-first averaging of gap coincide numerically. This does not make 72 cells independent. Cells share cohort data, method implementations and a common split schedule. Within each cell, 30 ARIs share a dataset and the 435 pairwise stability values reuse 30 partitions. Recovered summary provides valid descriptive cell estimates; it does not provide an independent 435- or 72-observation inferential sample.

All six leave-one-cohort-out means remain positive (range 0.3983–0.4973); all 12 leave-one-method-out means remain positive (0.4406–0.4822). This establishes descriptive direction robustness within this fixed grid, not population generalization. Largest cohort influence is Prostate (omission raises? observed leave-out mean falls to 0.3983); no cohort removal reverses the sign. Largest method influence is FCM (leave-out mean 0.4406), still positive. Details in CSV.

There are only six selected biomedical cohorts. No exchangeable-cohort bootstrap or cell-level significance test is justified. No confirmatory p-value, stability-predictive-utility null, or universal inference is supported. Correlations at dataset or method level are exploratory and have very small unit counts; the current audit does not elevate them to confirmatory evidence. The gap is a descriptive subtraction on [0,1]-scale stability and ARI (ARI may be negative), not a calibrated universal “excess reproducibility over validity” scale.

Evidence class: reconstructed descriptive evidence; exploratory sensitivity; no confirmatory inferential evidence.
