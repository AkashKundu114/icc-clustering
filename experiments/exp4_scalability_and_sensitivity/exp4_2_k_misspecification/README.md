# Sub-Experiment 4.2: $K$-Misspecification Robustness Suite

## 🔬 Executive Summary

In exploratory data analysis, single-cell transcriptomics, and real-world unsupervised clustering, the true cluster count $K_{\text{true}}$ is almost never known a priori. Practitioners must rely on heuristic cluster count selection methods (e.g., elbow method, silhouette analysis, gap statistics), which regularly misestimate the true number of underlying latent partitions. Standard clustering algorithms exhibit catastrophic vulnerability to misspecified cluster counts:
- **Over-Specification ($K_{\text{input}} > K_{\text{true}}$):** Splits genuine clusters into arbitrary, fractured micro-clusters, destroying semantic coherence.
- **Under-Specification ($K_{\text{input}} < K_{\text{true}}$):** Indiscriminately merges distinct classes, collapsing minority subpopulations.

**Sub-Experiment 4.2** evaluates whether the statistical anchor certification and variance-stabilized subspace gating in **Invariant Core Consensus (ICC-v2)** provide inductive regularization against cluster count misspecification:
- **Datasets:**
  - **Synthetic Manifold:** $N = 300, D = 200, K_{\text{true}} = 3$ (swept $K_{\text{input}} \in [2, 8]$)
  - **Sonar Acoustic:** $N = 208, D = 60, K_{\text{true}} = 2$ (swept $K_{\text{input}} \in [2, 7]$)
  - **SRBCT Cancer Microarray:** $N = 83, D = 2,308, K_{\text{true}} = 4$ (swept $K_{\text{input}} \in [2, 9]$)
- **Compared Methods (8 Models):** `K-Means`, `Ward`, `Spectral`, `FCM`, `Standard_Consensus`, `Li_et_al_2019`, `ICC_v1`, and `ICC_v2`.
- **Evaluation Scale:** 1,680 individual model fits across 10 random trials per condition. Metrics recorded include ARI, NMI, AMI, V-Measure, and FM-Index.

---

## 📂 Directory Structure

```
experiments/exp4_scalability_and_sensitivity/exp4_2_k_misspecification/
└── README.md                                  # Sub-experiment documentation & analysis
# Associated suite resources:
experiments/exp4_scalability_and_sensitivity/
├── data/
│   └── exp4_2_k_misspecification_results.csv  # 1,680-row experimental evaluation database
├── figures/
│   ├── fig23_k_misspecification_ari.png       # 3-panel ARI robustness curve across datasets
│   └── fig23_k_misspecification_nmi.png       # 3-panel NMI robustness curve across datasets
└── src/
    ├── k_misspecification_sweep.py            # Parameter sweep execution engine
    └── plot_k_misspecification.py             # Matplotlib 300 DPI publication visualizer
```

---

## 📊 Empirical Findings

### 1. Robustness Curves on High-Dimensional Cancer Array (SRBCT, $K_{\text{true}} = 4, D = 2,308$)

The table below reports the empirical mean Adjusted Rand Index (ARI) as $K_{\text{input}}$ sweeps from severe under-specification ($K=2$) to extreme over-specification ($K=9$):

| $K_{\text{input}}$ | $\Delta K$ | K-Means | Ward | Spectral | FCM | Standard Consensus | Li et al. (2019) | ICC-v1 | ICC-v2 (Ours) | Relative ICC-v2 Advantage |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **$K = 2$** | $-2$ | 0.0518 | -0.0064 | 0.1070 | 0.1037 | 0.0900 | 0.0989 | 0.0940 | **0.1845** | **$+72\%$ vs next best** |
| **$K = 3$** | $-1$ | 0.0881 | 0.0077 | 0.0506 | 0.0995 | 0.0613 | 0.1094 | 0.1191 | **0.2861** | **$+140\%$ vs next best** |
| **$K = 4$ (True)** | $0$ | 0.1002 | 0.1091 | 0.0802 | 0.1133 | 0.0414 | 0.0794 | 0.1278 | **0.5319** | **$+316\%$ vs next best** |
| **$K = 5$** | $+1$ | 0.1375 | 0.1526 | 0.0792 | 0.1052 | 0.0740 | 0.1632 | 0.1614 | **0.5172** | **$+217\%$ vs next best** |
| **$K = 6$** | $+2$ | 0.1521 | 0.1597 | 0.1470 | 0.1039 | 0.0977 | 0.1649 | 0.1592 | **0.5333** | **$+223\%$ vs next best** |
| **$K = 7$** | $+3$ | 0.1626 | 0.2037 | 0.1792 | 0.1006 | 0.1358 | 0.1883 | 0.1864 | **0.4961** | **$+144\%$ vs next best** |
| **$K = 8$** | $+4$ | 0.1789 | 0.1912 | 0.1378 | 0.1001 | 0.1570 | 0.2091 | 0.1882 | **0.4581** | **$+119\%$ vs next best** |
| **$K = 9$** | $+5$ | 0.1834 | 0.2044 | 0.1413 | 0.1177 | 0.1646 | 0.2073 | 0.1993 | **0.4054** | **$+95\%$ vs next best** |

### 2. Theoretical Analysis & Key Insights
1. **Core Anchors Insulate Against Over-Clustering:**
   - As $K_{\text{input}}$ increases up to $K=9$ (more than double the ground-truth cluster count), conventional models like K-Means and Spectral fragment natural density clusters, resulting in low recovery ($\text{ARI} < 0.21$).
   - ICC-v2 maintains $\text{ARI} > 0.40$ even at $K=9$. Because the bipartite spectral decomposition operates on statistical core anchors representing invariant cluster centroids, extraneous eigenvalues isolate peripheral halo noise into small residual clusters rather than shattering true cluster cores.
2. **Under-Specification Stability:**
   - At $K=2$ and $K=3$ on SRBCT, ICC-v2 exhibits graceful degradation ($\text{ARI} = 0.1845$ and $0.2861$), merging coherent sister classes while keeping disparate tumor subtypes segregated.

---

## 🔄 Reproduction

```powershell
# Run the complete 1,680-fit K-misspecification parameter sweep:
python experiments/exp4_scalability_and_sensitivity/run_exp4.py --k-misspec

# Direct module invocation:
python experiments/exp4_scalability_and_sensitivity/src/k_misspecification_sweep.py --trials 10

# Re-render publication figures (Figs 23a & 23b) from cached results:
python experiments/exp4_scalability_and_sensitivity/src/plot_k_misspecification.py
```
