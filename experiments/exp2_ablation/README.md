# Experiment 2: Architectural Component Ablation Suite

## Executive Summary

Experiment 2 evaluates the individual and synergistic contributions of the core components proposed in **Invariant Core Consensus (ICC-v1 and ICC-v2)**:
1. **Feature Subspacing ($\mathcal{F}$)**: Projecting base clusterers into random feature subspaces.
2. **Anchor Consensus ($\mathcal{A}$)**: Identifying high-stability "core anchors" ($\text{Stability}(i) \ge \tau_{\text{core}}$) and performing bipartite anchor-graph consensus rather than all-pairs co-association.
3. **Dispersion Calibration ($\mathcal{C}$)**: Feature-level variance scaling and SNR noise-gating prior to consensus projection.
4. **Variance-Stabilized Subspace Gating (VSSG)**: Non-parametric bimodality and dispersion screening (evaluated in depth in [Sub-Experiment 2.1: VSSG Feature Discovery Audit](exp2_1_vssg_interpretability/README.md)).

We rigorously compare 6 architectural variants across varying noise dimensionalities $D_{\text{noise}} \in \{0, 50, 200, 1000, 3000, 5000\}$:
- **V0 (Baseline)**: Standard Ensemble Consensus (full feature space, all-pairs co-association, average linkage).
- **V1 (Subspaces Only)**: Subspace sampling ($25\%$ feature rate), all-pairs co-association, no core anchoring.
- **V2 (Anchors Only)**: Full feature space, anchor-based bipartite consensus ($\tau_{\text{core}} = 0.85$, $K$-means anchor seeds).
- **V3 (Subspaces + Anchors)**: Subspace sampling + anchor-based bipartite consensus.
- **V4 (Subspaces + Calibration)**: Subspace sampling + dispersion noise calibration, all-pairs co-association.
- **V5 (Full ICC-v1)**: Subspaces + Anchors + Dispersion Calibration.

---

## Directory Structure

```
experiments/exp2_ablation/
├── README.md                                  # Architectural ablation suite documentation
├── run_exp2.py                                # Master CLI runner
├── exp2_1_vssg_interpretability/              # Dedicated Sub-Experiment 2.1 suite
│   └── README.md                              # VSSG interpretability documentation & PR curves
├── data/
│   ├── exp2_ablation_results.csv              # Empirical sweep across 6 variants and 6 noise levels (10 trials each)
│   ├── exp2_1_madelon_pr.csv                  # VSSG Precision/Recall on Madelon benchmark
│   ├── exp2_1_synthetic_10kd_pr.csv           # VSSG Precision/Recall on D=10,000 synthetic benchmark
│   └── exp2_1_noise_sweep_pr.csv              # VSSG Recall@50 noise degradation sweep
├── figures/
│   ├── fig11_ablation_curves.png              # Recovery (ARI) vs noise dimension across all 6 variants
│   ├── fig12_ablation_waterfall.png           # Component contribution waterfall chart at D_noise = 0
│   ├── fig13_nmi_ablation.png                 # Normalized Mutual Information (NMI) vs noise dimension
│   ├── fig22a_vssg_madelon_pr.png             # Precision-Recall curve on Madelon
│   ├── fig22b_vssg_synthetic_pr.png           # Precision-Recall curve on Synthetic D=10,000
│   ├── fig22c_vssg_noise_degradation.png      # Recall@50 vs noise degradation curve
│   └── fig22_vssg_interpretability_trinity.png # 3-panel consolidated publication figure
└── src/
    ├── ablation_engine.py                     # Implementation of all 6 architectural variants
    ├── run_ablation_sweep.py                  # Multi-trial parameter sweep harness
    ├── plot_exp2_figures.py                   # Ablation figure generator (Figs 11, 12, 13)
    ├── vssg_interpretability.py               # VSSG feature scoring and PR benchmark engine
    └── plot_vssg_figures.py                   # VSSG interpretability publication plotter
```

---

## Empirical Findings

### Architectural Component Recovery Across Noise Regimes (Mean ARI, 10 Trials)

| Noise Dimension ($D_{\text{noise}}$) | V0 (Standard) | V1 (Subspaces) | V2 (Anchors Only) | V3 (Sub + Anchors) | V4 (Sub + Calib) | V5 (Full ICC-v1) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **$D=0$ (Clean)** | $0.549$ | $0.549$ | **$0.736$** (+34%) | **$0.736$** | $0.549$ | **$0.736$** |
| **$D=50$** | **$0.376$** | $0.277$ | $0.323$ | $0.165$ | $0.292$ | $0.197$ |
| **$D=200$** | **$0.041$** | $0.016$ | $0.025$ | $0.016$ | $0.014$ | $0.008$ |
| **$D=1,000$** | $0.003$ | $0.003$ | $0.002$ | $0.000$ | **$0.004$** | $-0.001$ |
| **$D=3,000$** | $0.003$ | $-0.001$ | $0.002$ | $-0.001$ | $-0.002$ | $0.001$ |
| **$D=5,000$** | $0.003$ | $0.000$ | $-0.001$ | $0.000$ | $0.000$ | $0.001$ |

### Key Scientific Insights
1. **The Manifold Advantage of Anchor Consensus ($D=0$):**
   On clean data ($D_{\text{noise}}=0$), statistical anchor certification delivers an immediate **$+0.187$ jump in ARI (from $0.549$ to $0.736$)** and an NMI jump from $0.680$ to $0.786$.
2. **The "Curse of Blind Subspacing" in High Dimensions ($D \ge 50$):**
   Unguided uniform random feature drawing dilutes consensus partitions because $>55\%$ of sub-models train purely on noise dimensions.
3. **Motivation for VSSG (Sub-Experiment 2.1):**
   To resolve this bottleneck, ICC-v2 replaces blind drawing with **Variance-Stabilized Subspace Gating (VSSG)**, which screens informative features using non-parametric bimodality scoring. See the full audit in [Exp 2.1 VSSG Interpretability](exp2_1_vssg_interpretability/README.md).

---

## Reproduction Commands

```bash
# 1. Regenerate all publication figures (Figs 11, 12, 13, 22):
python experiments/exp2_ablation/run_exp2.py --reproduce-plots

# 2. Re-run only the VSSG interpretability sweep:
python experiments/exp2_ablation/run_exp2.py --vssg-only --trials 10

# 3. Re-run only the component ablation sweep:
python experiments/exp2_ablation/run_exp2.py --ablation-only --trials 10

# 4. Recompute the full suite from scratch:
python experiments/exp2_ablation/run_exp2.py --run-full --trials 10
```
