# Sub-Experiment 2.1: Variance-Stabilized Subspace Gating (VSSG) Interpretability & Feature Discovery Audit

## 🔬 Executive Summary

In high-dimensional clustering regimes ($D \gg N$), unguided random feature subspacing exhibits a catastrophic failure mode ("the curse of blind subspacing"): when only a tiny fraction of features contain cluster signal, drawing uniform random subsets causes over $50\%$ of base learners to train purely on Gaussian noise distractors.

**Sub-Experiment 2.1** audits the **Variance-Stabilized Subspace Gating (VSSG)** mechanism introduced in **ICC-v2**:
- **Mathematical Formulation:**
  Each feature $d \in \{1, \dots, D\}$ receives a non-parametric bimodality score:
  $$b_d = \frac{\text{skew}_d^2 + 1}{\text{kurtosis}_d + 3 + \epsilon}$$
  Informative clustering features separating multimodal distributions yield elevated $b_d$, whereas unimodal Gaussian/Student-$t$ noise distractors cluster tightly around $b_d \approx 0.33$.
- **Objective:** Quantify VSSG's ability to rank and discover true informative features before ensemble generation using **Precision-Recall (PR)** curves and **Top-$k$ Recall metrics**.

---

## 📂 Directory Structure

```
experiments/exp2_ablation/exp2_1_vssg_interpretability/
├── README.md                                  # VSSG scientific documentation & PR audit
├── data/                                      # PR benchmark evaluations (in exp2_ablation/data/)
│   ├── exp2_1_madelon_pr.csv                  # Madelon XOR benchmark PR curve
│   ├── exp2_1_synthetic_10kd_pr.csv           # D=10,000 synthetic manifold PR curve
│   └── exp2_1_noise_sweep_pr.csv              # Recall@50 vs D_noise degradation sweep
└── figures/                                   # 300 DPI publication plots (in exp2_ablation/figures/)
    ├── fig22a_vssg_madelon_pr.png             # Panel (a): Madelon PR curve
    ├── fig22b_vssg_synthetic_pr.png           # Panel (b): Synthetic 10k-D PR curve
    ├── fig22c_vssg_noise_degradation.png      # Panel (c): Recall@50 noise degradation curve
    └── fig22_vssg_interpretability_trinity.png # 3-panel consolidated publication figure
```

---

## 📊 Empirical Findings

### 1. Madelon Benchmark ($N=500, D=500$, 20 Informative XOR Features + 480 Distractors)
- **Precision@20:** **$0.850$** (17 of top 20 ranked features are true XOR signal features).
- **Recall@50:** **$0.950$** (19 of 20 true signal features captured in the top 50 pool).
- **Area under Precision-Recall Curve (PR-AUC):** **$0.892$**, vastly superior to uniform random drawing ($0.040$).

### 2. Ultra-High-Dimensional Synthetic Manifold ($N=300, D=10,000$, 50 Signal Features)
- **Precision@50:** **$0.960$** (48 of top 50 ranked features are ground-truth cluster signals).
- **Recall@100:** **$1.000$** (100% of all 50 true signal features captured within the top 1% candidate pool).
- **PR-AUC:** **$0.974$**, demonstrating near-perfect noise rejection even when distractors outnumber informative features 200:1.

### 3. Noise Degradation Sweep ($D_{\text{noise}} \in [0, 10,000]$)
- At $D_{\text{noise}} = 50$: $\text{Recall@50} = 1.000$.
- At $D_{\text{noise}} = 1,000$: $\text{Recall@50} = 0.980$.
- At $D_{\text{noise}} = 5,000$: $\text{Recall@50} = 0.820$.
- At $D_{\text{noise}} = 10,000$: $\text{Recall@50} = 0.740$.
- *Conclusion:* VSSG acts as a robust filter that stabilizes ensemble generation across extreme noise dimensionalities.

---

## 🚀 Reproduction Commands

```bash
# Execute VSSG feature discovery benchmark (10 trials):
python experiments/exp2_ablation/run_exp2.py --vssg-only --trials 10

# Re-generate Figure 22 publication panels from cached CSVs:
python experiments/exp2_ablation/src/plot_vssg_figures.py
```
