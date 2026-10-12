# Verification log
Clone: git clone --depth 50 (c38a4c9). Branch audit/remediation-a1-a2 (commit 45e157b). Commands: demo.py; pytest tests -o addopts="" (58 pass/6 skip/5 net-fail); scripts a2_controls.py {syn,real}, a2_random_control.py, a2_filter_controls.py. Pandas recomputation of exp3/exp1/missing-data/exp2 tables. Web searches: U-SENC, BC feature selection, FCAG/FastMICE. NOT done: ASPP audit, exp0/exp4/exp5 reruns, exp3 rerun, manuscript review, TKDE policy check, 5 download datasets.
Artifacts: experiments/audit_controls/data/*.csv, experiments/audit_controls/src/*.py, docs/audit_reports/*.md. Original files unmodified except on branch: README.md, demo.py, src/icc/consensus_v2.py (pool_mode opt-in, default 'legacy' preserves behaviour).

## A3/A4 additions
Scripts a3_embedding.py, a3_paths.py. tests/test_audit_a3.py (new, 4+ cases). Regression subset (test_audit_a3, consensus_v2, inductive_projection, aspp, edge_cases): 28 passed, 4 skipped. Exp3 stats recomputed excluding FastMVC from the committed CSV.

## E3 additions
consensus_v2.py: opt-in pool_mode 'bc_frac'/'random_frac' + pool_frac (default 0.15; default behaviour unchanged). Script e3_pool_curve.py; 8 datasets x 7 sizes x 2 modes x 5 seeds (flat results in experiments/audit_controls/data/e3_pool_curve.csv).

## E3b additions
Script e3b_label_free_selector.py (no src changes). 8 datasets x 5 seeds x 6 pool sizes. Flat results in experiments/audit_controls/data/e3b_selector.csv.

## E5 additions
e5_exp1_rerun.py (4 noise dims x 10 trials x 4 classifiers = 320 evaluations), e5_missing_rerun.py (8 datasets x 5 rho x 5 seeds). Restored tracked exp1_pseudolabel_results.csv after runner overwrote it.
