# Experiment 0: Falsification & Characterization of the "Hallucinated Stability Trap"

## Executive Summary

This suite resolves the central theoretical bottleneck of the **Invariant Core Consensus (ICC)** proposal by answering the falsification question:

> **Core Research Question:** *Does high-dimensional nuisance noise ($D \gg N$) cause clustering ensembles across random seeds to converge to identical spurious partitions ($S_{ij} \to 1.0$), or does it produce conventional partition instability ($S_{ij} \approx 1/K$)?*

### Foundational Theoretical & Empirical Conclusions:
1. **The Universal Hypothesis is Refuted:**
   - Under pure isotropic white noise, distance concentration does **not** universally force all base clusterers into the same spurious minimum.
   - For **K-Means** and **Gaussian Mixture Models (GMM)**, accuracy and stability collapse together ($\text{ARI} \to 0, \text{Stability} \to 0$), exhibiting conventional instability.
2. **The "Hallucinated Stability Trap" is Formally Confirmed for Specific Objectives:**
   - **Fuzzy C-Means (FCM):** Exhibits an abrupt **first-order phase transition** between $D_{\text{noise}} = 150$ and $200$. 
     - While true accuracy plunges from $1.0 \to 0.48$, **$100\%$ of 30 independent random initializations land on the exact same wrong partition** (`dominant_share = 1.0`, `n_distinct = 1`, `stability = 1.0`) from $D_{\text{noise}} = 200$ to $D_{\text{noise}} = 800$.
     - The stability-accuracy gap reaches **$G = +0.52$**. Prior determinacy metrics (Li et al., 2019) misclassify this pure noise artifact as a "perfectly stable invariant core".
   - **Ward Linkage & Spectral Clustering:** In the genomics-scale imbalanced regime ($N=72, K=2$, mimicking ALLAML leukemia with $D/N$ up to 278), both Ward and Spectral clustering remain **$\text{Stability} = 1.0$ all the way to $D_{\text{noise}} = 20,000$** while accuracy degrades, yielding positive stability gaps up to **$G = +0.69$**.
   - **Noise-Type Susceptibility:** Under heteroscedastic ("scaled") noise where feature variances vary, Spectral and Ward show near-total hallucinated stability ($G = +0.85$ and $G = +1.00$).

---

## Directory Structure

```
experiments/exp0_falsification/
├── README.md                      # Scientific documentation & user manual
├── run_all.py                     # Master CLI runner
├── data/                          # Aggregated CSV experiment datasets
│   ├── exp0_agg.csv               # Baseline sweep across D_noise ∈ [0, 10000]
│   ├── exp0_noisetypes.csv        # 5-noise-regime robustness sweep at D_noise=1000
│   ├── exp0_scaled_agg.csv        # Genomics-scale imbalanced regime (ALLAML scale)
│   ├── exp0_finegrid.csv          # Fine-grid sweep on FCM, KMeans, GMM
│   └── exp0_fcm_full_curve.csv    # FCM phase transition curve
├── figures/                       # Publication-grade figures (300 DPI)
│   ├── fig1_ari_stability.png     # Accuracy vs Stability across algorithms
│   ├── fig2_gap.png               # Stability-Accuracy Gap (G = Stability - ARI)
│   ├── fig3_within_between.png    # Co-association margin collapse
│   ├── fig4_noisetype_heatmap.png # Noise type vs Algorithm gap heatmap
│   ├── fig5_scaled_ari_stability.png # Scaled genomics-scale regime curves
│   ├── fig6_scaled_gap.png        # Scaled stability gap
│   ├── fig7_regime_comparison.png # Balanced vs Imbalanced regime comparison
│   └── fig8_fcm_phase_transition.png # FCM phase transition & distinct partitions
└── src/                           # Cross-platform Python modules
    ├── exp0_core.py               # Core benchmark generator & dual-backend clusterers
    ├── exp0_diagnose.py           # Canonical partition mapping & entropy tools
    ├── exp0_run.py                # Baseline sweep runner
    ├── exp0_noisetypes.py         # Noise distributions runner
    ├── exp0_scaled_run.py         # Genomics-scale sweep runner
    ├── exp0_finegrid.py           # Fine-grid FCM runner
    └── plot_all_figures.py        # Master plotting engine
```

---

## Empirical Findings

### 1. Hallucinated Stability Phase Transition Breakdown
- Under low noise ($D_{\text{noise}} \le 100$), all algorithms correctly recover cluster structure with high accuracy ($\text{ARI} > 0.95$) and stability ($\text{Stability} > 0.95$).
- At $D_{\text{noise}} \in [150, 200]$, Fuzzy C-Means undergoes a sudden phase transition into a fixed attractor state where multiple random seeds converge to the identical sub-optimal partition.
- In imbalanced high-dimensional settings ($N=72, K=2, D=20,000$), agglomerative Ward and Spectral clustering partition according to peripheral noise vectors, displaying an artificial consensus that masquerades as genuine convergence.

### 2. Multi-Metric Evaluation Invariance (ARI, NMI, AMI)
To ensure that the "Hallucinated Stability Trap" is not an artifact of pairwise permutation counting in Adjusted Rand Index (ARI), the evaluation infrastructure incorporates information-theoretic metrics:
- **Normalized Mutual Information (NMI)**: Bounded in $[0, 1]$, measuring shared information between partitions independent of cluster index labeling.
- **Adjusted Mutual Information (AMI)**: Corrected for chance under the generalized hypergeometric model.
- **Empirical Confirmation**: Under high-dimensional noise ($D_{\text{noise}} \ge 200$), the stability-accuracy gap $G$ is consistently replicated under NMI and AMI. For Fuzzy C-Means (FCM), $\text{Stability}_{\text{NMI}} \to 1.0$ while ground-truth $\text{NMI} \to 0.45$, confirming that hallucinated consensus stability is an objective-driven mathematical attractor rather than an evaluation metric artifact.

### 3. Data Schema & Metric Definitions

| Column | Type | Definition |
| :--- | :--- | :--- |
| `d_noise` | int | Number of appended nuisance distractor dimensions ($D_{\text{noise}}$) |
| `clusterer` | string | Algorithm name (`kmeans`, `gmm`, `ward`, `spectral`, `fcm`, `ALL_POOLED`) |
| `scope` | string | `per_algorithm` (within-model agreement) or `pooled` (diverse ensemble) |
| `mean_ari` | float | Average clustering accuracy against ground truth |
| `stability` | float | Average pairwise ARI between independent runs across random seeds |
| `nmi` / `ami` | float | Information-theoretic accuracy and stability metrics |
| `gap` | float | Stability–Accuracy Gap: $G = \text{Stability} - \text{mean\_ari}$ |
| `mu_within` | float | Expected co-association for true same-cluster pairs: $\mathbb{E}[S_{ij} \mid y_i = y_j]$ |
| `mu_between` | float | Expected co-association for true different-cluster pairs: $\mathbb{E}[S_{ij} \mid y_i \ne y_j]$ |
| `n_distinct` | int | Number of distinct partitions discovered across all $M$ seeds |
| `dominant_share` | float | Fraction of seeds converging to the single most frequent partition |

---

## Reproduction

### 1. Regenerate All Publication Figures from Cached Data
```powershell
python experiments/exp0_falsification/run_all.py --reproduce-plots
```
Figures will be rendered at 300 DPI in `experiments/exp0_falsification/figures/`.

### 2. Execute Full Recomputations
```powershell
python experiments/exp0_falsification/run_all.py --run-full
```
Runs all sweeps across seeds, re-exports CSVs to `experiments/exp0_falsification/data/`, and regenerates all figures.
