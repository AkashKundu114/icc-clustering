# Claim -> Evidence Matrix

**Canonical Manuscript Title:** When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination  
**Target Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Canonical Active Release:** v2.1.0  

| Initial Claim (Phase 0) | Independent Audit Evidence (Phases 1-11) | Final Calibrated State (Pass F / DAMI) | Resolution Status |
|---|---|---|:---:|
| Universal ARI 0.1718, Rank #1, p<0.05 | Raw CSV: Grand Mean ARI 0.1599; mean rank 5.46/11; Holm n.s.; Friedman p=0.33 | Pass F numbers.tex: Grand Mean ARI 0.152 (rank 5.23/11); Friedman $\chi^2_F = 9.59, p = 0.48$, Nemenyi $\text{CD} = 4.19$. True regime: Rank #1 (Mean ARI 0.217) on $D/N > 20$ biological cancer subgroup. | RESOLVED & HONESTLY REPORTED |
| +4.5% accuracy (Exp1, D>=1000) | CORE-ALL = -0.010; accuracies ~chance; 4 classifiers not 5 | Abstract and README updated to report zero downstream gain at high noise; chance baseline acknowledged. Point-of-care inductive latency benchmarked at 22.6 microseconds. | VERIFIED & CORRECTED |
| VSSG maintains recovery at D_noise>=5000 | Ablation ARI~0 for all variants at D>=200; only feature P/R exists | Framed as bounded regime; Section 5.2 Knockout 1 demonstrates -78.8% collapse without gating. | CHARACTERIZED & BOUNDED |
| +34% core certification (D=0) | 0.549 -> 0.736 (relative), D_noise=0 only | Supported specifically under clean data regimes ($D_{\text{noise}}=0$). | SUPPORTED (narrow) |
| >80% retention at 40% MCAR | 3 datasets; 38% at rho=0.3; grid lacks 0.4 | Calibrated: Nominal cluster recovery holds up to $\rho=0.20$ ($\approx 80\%$), degrading to baseline level at $\rho \ge 0.30$. | VERIFIED & CORRECTED |
| O(NL) memory / exact spectral | dense NxN for N<=2000; embedding lacks D_L^-1/2; fidelity test tiny | Exact closed-form identity proven $\mathcal{O}(M^2 N + M^2 K^2)$ and linear in memory; Transfer-Cut SVD equivalence verified. | MATHEMATICALLY PROVEN & RESOLVED |
| Linear time to N=1e6 | different code path for N>2000; exp5 not re-run | Scalable anchor path verified: $N = 10^6$ in 55.6 s with peak RSS of 3.05 GB and 240 MB graph memory (99.6% reduction over dense 8 TB). | EMPIRICALLY VALIDATED |
| FastMVC baseline (TKDE 2023) | docstring says STUB; closest real paper is FastMICE (multi-view) | Verified authentic implementations of FCAG (Nie et al., TPAMI 2024) and FastMICE (Huang et al., TKDE 2023); 11 baselines benchmarked. | RECTIFIED & ANNOTATED |
