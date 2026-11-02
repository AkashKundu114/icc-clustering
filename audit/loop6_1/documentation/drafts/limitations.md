# Limitations

- **Small cohort set:** the stability analysis covers six biomedical cohorts. The cohorts are not a probability sample; broad biomedical population inference is not supported.
- **Sampling is not initialization robustness:** the recorded model seed is fixed. The stability calculation reflects variation under saved sample subsets at one initialization setting.
- **Reference labels inform design:** the reference labels were used for class-stratified sampling and to set requested K. The evaluation is not fully label-blind. ARI quantifies agreement with these operational reference categories, not clinical validity or a complete biological truth.
- **Dependent observations:** 435 pairwise ARIs reuse partitions and observations. Seventy-two method-by-cohort cells share six cohorts, method labels, and sampling design. They are not independent cohort replications.
- **Historical provenance:** the original partition-writing producer and contemporaneous execution trace were not recovered. Recomputed metrics establish consistency of locally saved arrays with summaries, not authenticated historical model execution.
- **Duplicate outputs:** 140 repeated partition-hash groups were identified. Their cause remains unresolved; no benign or erroneous explanation is asserted.
- **Benchmark fairness:** the 13-dataset benchmark has copied/imported saved scores, differing seed schedules, method budgets and implementations, and ambiguous failure status for some zeros. Its Friedman calculation is descriptive/exploratory.
- **Access and redistribution:** most data and derived artifact rights remain unresolved. Yale B imagery may not be redistributed absent permission.
- **Public reproducibility:** only aggregate arithmetic was tested in a clean public clone. Partition-level reproduction is unavailable, and full experimental reproduction was not run.
- **Software claims:** the code repository contains many methods and utilities, but audited performance evidence does not establish universal superiority, clinical usefulness, causal mechanisms, or universal scaling guarantees for ICC/ICC-v2.
