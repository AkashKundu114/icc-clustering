# Inventory
src/icc: consensus_v2.py (ICC-v2), consensus.py (v1), core.py (generators, clusterer wrappers, co-association), aspp.py (ASPP, NOT audited), metrics.py, baselines/*, datasets/*.
experiments/exp0..exp5: runners, data CSVs, figures. 8 real datasets cached as .npz (colon, cns, leukemia, madelon, ovarian, prostate, sonar, srbct); the other 5 (20NG, Isolet, Indian Pines, Yale B, Zheng68k) require downloads (not reproducible offline).
Missing: manuscript (only docs/proposal), proofs ("Section IV" placeholder), raw data for 5 datasets.
Env: Python 3.12, sklearn 1.8.0, scipy 1.17.1, numpy 2.4.4, pandas 3.0.2. pytest: 58 passed, 6 skipped, 5 failed (network downloads). Tests rewrite tracked file experiments/exp1_generalization/data/exp1_pseudolabel_results.csv (committed 0.25/0.0 vs regenerated 1.0/1.0).
