# Experiment plan (priority order)
E1 more datasets x strong FS baselines (variance, Laplacian score, sparse k-means, Wasserman screen) with BC-pool ICC; dataset-level Friedman/Nemenyi.
E2 noise-model sweep (gauss, t, sparse, correlated, non-marginal signal) x pool rule; report pool precision/recall.
E3 pool-size sensitivity curve (5%-50%) on Leukemia/SRBCT/Colon/CNS with random-pool control.
E4 anchor vs dense spectral equivalence on N<=2000 (ARI/embedding distance).
E5 rerun Exp1 and missing-data on 13 datasets with fixed protocol.
E6 scalability re-run with measured memory per component.
Command pattern: PYTHONPATH=. python research_audit/scripts/<script>.py
