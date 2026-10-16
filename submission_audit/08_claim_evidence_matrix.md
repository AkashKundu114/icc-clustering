# 08 — Claim-to-Evidence Traceability Matrix

**Auditor:** Scientific Coordinator  
**Date:** October 13, 2026  
**Status:** FULLY RECONCILED  

---

## 1. Traceability Mapping

| Claim ID | Paper Claim | Section | Canonical Raw Source | Visual / Tabular Asset | Audit Verdict |
|---|---|---|---|---|---|
| **CLM-01** | Isotropic distractor noise causes deceptive consensus stability trap (>0.8 stability, ARI $\to 0$). | Sec 3 (Falsification) | `results/exp0_falsification/data/exp0_agg.csv` | Fig 1, Fig 2 | **SUPPORTED** |
| **CLM-02** | Prop 2 contingency identity computes exact determinacy in linear memory without $N \times N$ matrix. | Sec 4.2 | Analytic proof (`docs/THEORETICAL_FOUNDATIONS.md`) | Prop 2, Alg 1 | **SUPPORTED** |
| **CLM-03** | Sarle's BC isolates non-linear XOR features on Madelon with PR-AUC = 0.892 and Recall@50 = 0.95. | Sec 5.3 (Exp 2.1) | `results/exp2_ablation/data/exp2_1_madelon_pr.csv` | Fig 22a | **SUPPORTED** |
| **CLM-04** | Core training matches full 100% training under low-to-moderate noise ($D_{\text{noise}} \le 50$). | Sec 5.1 (Exp 1) | `results/exp1_generalization/data/exp1_generalization_results.csv` | Fig 3a | **SUPPORTED** |
| **CLM-05** | Core pseudo-labels provide accuracy advantage over full pseudo-labels at high noise ($D \ge 1,000$). | Sec 5.1 (Exp 1) | `results/audit_controls/data/e5_exp1_pseudolabel_rerun.csv` | Fig 3b | **WEAKENED / SOFTENED** (Gain shrinks to ~0.4% at chance baseline). |
| **CLM-06** | Subspace ensembling and anchor graph prevent cluster collapse observed in single-model VSSG+KMeans. | Sec 5.2 (Exp 2) | `results/exp2_ablation/data/exp2_ablation_results.csv` | Table 2, Fig 4 | **SUPPORTED** |
| **CLM-07** | ICC-v2 commands Rank #1 ($R=1.50$) across high-dimensional biomedical datasets ($D/N > 20$). | Sec 5.4 (Exp 3) | `results/exp3_real_world_benchmarks/data/exp3_1_ari_table_v2.tex` | Table 3, Fig 17 | **SUPPORTED** |
| **CLM-08** | Reduced anchor graph slashes RAM by 97.0% and yields $22.4\times$ speedup at $N=10,000$ with $|\Delta \text{ARI}| \le 0.05$. | Sec 5.5 (Exp 4.3) | `results/exp4_scalability_and_sensitivity/data/exp4_3_anchor_fidelity_results.csv` | Fig 24 | **SUPPORTED** |
| **CLM-09** | Linear scalability up to $N=1,000,000$ instances in 55.6 seconds with 3.05 GB peak RAM. | Sec 5.6 (Exp 5) | `results/exp5_extreme_scale/data/exp5_sample_scaling_results.csv` | Fig 26 | **SUPPORTED** |
| **CLM-10** | Universal superiority across all 13 multi-domain benchmark collections. | Abstract / Intro | `results/exp3_real_world_benchmarks/data/exp3_4_statistical_significance_v2.csv` | Table 3, Fig 17 | **DISPROVEN / REMOVED** (Friedman $p=0.33$; properly framed as regime-specific). |
