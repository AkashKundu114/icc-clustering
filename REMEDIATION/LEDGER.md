# ICC-v2 Remediation Master Ledger

This ledger tracks the end-to-end surgical remediation of all registered issues across Numerical Consistency (`N1`--`N12`), Methodology & Theory (`M1`--`M9`), and Experimental Design & Statistics (`S1`--`S6`) as mandated by the Project Global Rules.

**Global Rules Enforced:**
1. Integrity First: Every single number in the manuscript is generated from `results/results.json` into `paper/gen/numbers.tex` (and `springer_manuscript/numbers.tex`). No manual number edits.
2. Verified by Execution: Every claim is verified by running pytest, lint, typecheck, or experiment scripts. Command outputs are pasted into this ledger.
3. Git Discipline: One commit per issue ID on branch `fix/full-remediation-pipeline`.
4. Final Code Cleanliness: Production repo code contains no comments; manuscript and README retain full prose.
5. Defensible Science: If empirical evidence contradicts an overclaim, the claim is softened or rewritten honestly.
6. Rigorous Statistics: 10 seeds minimum, mean ± std reported everywhere, Wilcoxon-Holm testing with correct CD values.

---

## Issue Status Ledger

| Issue ID | Domain | Short Description | Status | Files Touched | Verification Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **N1** | Numerical | Leukemia ARI (0.846 vs 0.680 vs 0.708) & SRBCT (0.681 vs 0.538 vs 0.574/0.607) | open | `experiments/make_paper_assets.py`, `springer_manuscript/main.tex` | Pending single-source generation |
| **N2** | Numerical | Fig 6/7 (21 datasets x 9 methods) vs text/Table 3 (13 x 11, 1430 fits) | open | `springer_manuscript/main.tex`, `experiments/exp3_real_world_benchmarks/src/plot_exp3_figures.py` | Pending alignment |
| **N3** | Numerical | Fig 6 CNS/Glioma row duplication & Table 3 mismatch | open | `springer_manuscript/main.tex`, `results/exp3_real_world_benchmarks/data/exp3_1_ari_table_v2.csv` | Pending macro harmonization |
| **N4** | Numerical | Nemenyi CD=2.62 (k=9, N=21) vs (k=11, N=13 CD~4.2) & subgroup CD~6 | open | `springer_manuscript/main.tex`, `experiments/exp3_real_world_benchmarks/src/run_exp3_4_statistical_significance.py` | Pending Demšar recomputation |
| **N5** | Numerical | Mean rank 5.46 is 5th overall (behind DEC 4.31, StdCons 5.08) vs "top tier" claim | open | `springer_manuscript/main.tex` | Pending honest ranking rewrite |
| **N6** | Numerical | Leukemia VSSG keeps 1,522 genes vs cap max(100, 0.15D) ~ 1,069 | open | `src/icc/consensus_v2.py`, `springer_manuscript/main.tex` | Pending cap enforcement / doc fix |
| **N7** | Numerical | Memory: Exact at N=10k (1529.8MB) < StdCons at 8k (1709.6MB); 39.1% vs 97%; Fig 9a runtime curves | open | `springer_manuscript/main.tex`, `results/exp4_scalability_and_sensitivity/data/` | Pending text/macro alignment |
| **N8** | Numerical | "Theorem 2" vs Theorem 3 exists; Fig 2b rho_sep; beta undefined in Fig 9d; Exp numbering mismatch | open | `springer_manuscript/main.tex` | Pending numbering & symbol audit |
| **N9** | Numerical | Exp1: kNN missing; pseudo-label gain 33.3% vs 28.8% at K=3 chance; core-only worse than full; Fig 3b empty | open | `springer_manuscript/main.tex`, `results/exp1_generalization/` | Pending empirical reconciliation |
| **N10** | Numerical | L parameter: Alg 1 L=max(40,10K) vs "default 40" vs "<2 anchors per class for K>=20" | open | `src/icc/consensus_v2.py`, `springer_manuscript/main.tex` | Pending formulation sync |
| **N11** | Numerical | Complexity claims: O(LD) vs O(K\|F_active\|); Eq 4 omits O(M^2 N + M^2 K^2); "constant time" overclaim | open | `springer_manuscript/main.tex` | Pending rigorous complexity sync |
| **N12** | Numerical | Fig conflicts: Fig 2b positive gap; Fig 5a Recall@K peak ~0.45; Fig 8a/b gaps; Fig 11a erratic vs claimed fidelity | open | `springer_manuscript/main.tex`, `experiments/make_paper_assets.py` | Pending figure caption/text audit |
| **M1** | Method/Theory | BC definitions inconsistent (Eq 2, Eq 9, Alg 1 line 3); selection rule inconsistent | open | `src/icc/consensus_v2.py`, `springer_manuscript/main.tex` | Pending definition alignment |
| **M2** | Method/Theory | Assumption 1 fails for skewed unimodal; XOR structure (Madelon); 0.892 PR-AUC; false-positive at small N | open | `springer_manuscript/main.tex`, `docs/THEORETICAL_FOUNDATIONS.md` | Pending boundary & scope discussion |
| **M3** | Method/Theory | Prop 1: Delta/sigma threshold must be sqrt((3+sqrt15)/2) ~ 1.854; discuss imbalanced mixtures | open | `springer_manuscript/main.tex` | Pending proof verification |
| **M4** | Method/Theory | Embedding U: D_W vs D_A; "top K eigenvectors of Laplacian" (smallest); symbol D clash; Transfer-Cut norm | open | `src/icc/consensus_v2.py`, `springer_manuscript/main.tex` | Pending Laplacian symbol normalization |
| **M5** | Method/Theory | Anchors chosen by top determinacy without per-cluster stratification (dense cluster bias) | open | `src/icc/consensus_v2.py`, `springer_manuscript/main.tex` | Pending documentation of limitation |
| **M6** | Method/Theory | Inductive step (Eq 6) evaluated vs Nystrom, kNN propagation, classifier on consensus labels | open | `springer_manuscript/main.tex`, `experiments/audit_controls/src/` | Pending held-out empirical framing |
| **M7** | Method/Theory | ASPP: missing experiments, undefined Retention/Coassoc/T, uncalibrated confidence | open | `springer_manuscript/main.tex`, `src/icc/aspp.py` | Pending calibration & formula definitions |
| **M8** | Method/Theory | Ablation logic: VSSG+KMeans hurts (0.019 vs 0.101); cherry-picking "up to 1.000"; audit label leakage | open | `springer_manuscript/main.tex` | Pending honest ablation rewrite |
| **M9** | Method/Theory | "provably" vs empirical; Var/E->0 should be relative contrast / CV; Definition 1 behavior | open | `springer_manuscript/main.tex` | Pending math claim softening |
| **S1** | Statistics | Baselines run on full D vs ICC-v2 on gated features; add variance/PCA/Laplacian/sparse k-means | open | `springer_manuscript/main.tex`, `results/audit_controls/` | Pending baseline fairness disclosure |
| **S2** | Statistics | No tuning protocol for L, tau_core, alpha, M, T; define unsupervised tuning protocol | open | `springer_manuscript/main.tex` | Pending protocol specification |
| **S3** | Statistics | Table 3 missing std; Wilcoxon-Holm; a priori D/N>20 subgroup with CD; honest ARI near zero | open | `springer_manuscript/main.tex`, `results/exp3_real_world_benchmarks/` | Pending std & subgroup reporting |
| **S4** | Statistics | DEC on N<=100 is weak baseline; undefined variants in figures ("15%", "Adaptive", "ICC-v1") | open | `springer_manuscript/main.tex` | Pending baseline discussion & variant definitions |
| **S5** | Statistics | K-misspecification & missing data claims ("all baselines <0.10") overclaimed | open | `springer_manuscript/main.tex` | Pending claim softening & calibration |
| **S6** | Statistics | Hardware, dataset preprocessing, seeds, DEC hyperparams, licenses, registry details | open | `springer_manuscript/main.tex`, `docs/REPRODUCIBILITY.md` | Pending comprehensive metadata addition |
