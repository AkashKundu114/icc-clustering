# ICC-v2 Remediation Master Changelog

All notable changes made during the surgical remediation across all 27 audit issues (`N1`--`N12`, `M1`--`M9`, `S1`--`S6`) are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), adhering to strict single-source data grounding, verification by execution, and git discipline.

---

## [Remediation Pipeline] - 2026-10-17

### Added
- Created `results/results.json` encapsulating all benchmark matrices, means, standard deviations, ablation metrics, anchor fidelity values, and Demšar stats.
- Automated single-source macro generator `experiments/make_paper_assets.py` exporting 27 LaTeX macros to `springer_manuscript/numbers.tex`.
- Injected `\input{numbers.tex}` into `springer_manuscript/main.tex` to eliminate drift between manuscript text and empirical data.
- Added Section 5.6 ("Reproducibility Protocols and Computational Details") specifying hardware configuration (16-core CPU, RTX 3090 GPU), data preprocessing, 10 fixed random seeds, DEC autoencoder hyperparameters, and dataset registry with open licenses (`[S6]`).
- Added feature gating control baseline comparisons (K-Means on all features, top variance, and top BC features) from `results/audit_controls/data/a2_filter_controls.csv` (`[S1]`).
- Added formal definitions for variant nomenclature: `ICC-v1`, `ICC-v2 (15%)`, and `ICC-v2 (Adaptive)` (`[S4]`).

### Changed
- **`[N1]`**: Harmonized Leukemia and SRBCT ARI across sections: primary benchmark 10-seed matrix (Leukemia $0.680 \pm 0.363$, SRBCT $0.538 \pm 0.110$) vs. ablation fixed-seed matrix (Leukemia $0.846 \pm 0.154$, SRBCT $0.681 \pm 0.037$) explicitly contextualized.
- **`[N2-N5]`**: Harmonized primary benchmark scope to 13 datasets $\times$ 11 methods (1,430 model fits); identified 21-dataset suite as extended audit control; resolved CNS vs Glioma separation; recalculated Nemenyi Critical Difference ($CD = 4.19$ for $k=11, N=13$; $CD = 6.16$ for $N=6$ subgroup); transparently reported ICC-v2 ranking 5th overall (5.46) behind DEC (4.31), StdCons (5.08), K-Means/Ward (5.31), while holding Rank #1 ($R=2.33$) on $D/N > 20$ subgroup.
- **`[N6]`**: Corrected Leukemia VSSG active candidate gene pool cap $\min(D, \max(100, \lfloor 0.15 D \rfloor)) = 1{,}069$ for $D=7{,}129$ (replacing 1,522).
- **`[N7]`**: Reconciled memory reduction regimes: exact consensus core-pruning achieves 39.1% RAM reduction at $N=8\text{k}$ (1,709.6 MB down to 1,040.5 MB); bipartite anchor approximation achieves 97.0% RAM reduction at $N=10\text{k}$ (1,529.8 MB down to 45.8 MB, 24.5x speedup).
- **`[N8]`**: Fixed "Theorem 2" $\to$ Theorem 1; deprecated unused parameter `beta` in `consensus_v2.py`; harmonized experiment numbering (Exp 3.5 $\to$ Exp 3.2).
- **`[N9]`**: Grounded Exp 1 downstream results in empirical baseline chance expectations ($33.3\%$ for $K=3$ classes); reported kNN ($+5.2\%$) and Random Forest ($+4.5\%$) accuracy advantages with confidence intervals.
- **`[N10-N12]`**: Harmonized Algorithm 1 line 179 and text anchor budget ($L=40$ default benchmark explains $<2$ anchors/class for $K \ge 20$, with adaptive $L = \max(40, 10K)$); updated Theorem 1 complexity to include determinacy contingency cost $O(M^2 N + M^2 K^2)$; replaced "constant time" with $O(K \cdot |\mathcal{F}_{\text{active}}|)$ query time; resolved figure conflicts (Fig 2b positive gap on Spectral/Ward; Madelon Recall@K peaks $\sim 0.45$; anchor fidelity numbers updated to exact values with Exact > Reduced by 0.239 at $N=5\text{k}$ and converging to $|\Delta\text{ARI}|=0.0012$ at $N=10\text{k}$).
- **`[M1-M5]`**: Aligned Sarle's Bimodality Coefficient formula with finite-sample null correction across all sections; formalized Proposition 1 separation bound ($\Delta/\sigma > 1.854$), asymmetric mixtures $w(1-w)$, and $K > 2$ spacing; resolved Transfer-Cut degree notation ($\Delta_R, \Delta_A$) to prevent clash with dimension $D$; specified eigenvectors of smallest Laplacian eigenvalues; documented determinacy anchor concentration bias on imbalanced multi-class datasets.
- **`[M6-M9]`**: Contextualized inductive centroid projection against Nyström kernel extension, $k$-NN propagation, and downstream classifiers; formally defined ASPP Retention, Coassoc, temperature $T$, and clarified heuristic nature of confidence index; explained real ablation mechanics (why V1 hurts on Leukemia due to intra-cluster dispersion on uncoordinated genes); purged cherry-picked phrase "(and up to 1.000 on representative seeds)"; verified zero label leakage; corrected distance concentration formula to dimensionless relative contrast $\frac{\mathrm{Var}}{\mathbb{E}^2} \to 0$; softened "provably" to empirical finite-sample demonstration.
- **`[S1-S6]`**: Disclosed DEC sample size failure mode on $N \le 100$; specified unsupervised parameter protocol; reported honest near-zero ARI on uninformative biological datasets (CNS, Colon, Prostate, Ovarian); calibrated missing data and K-misspecification claims.
- **`[Rule 4]`**: Stripped all inline comments from production code in `src/` across 26 files while preserving module docstrings.

### Verified
- Automated test suite `python -m pytest tests -q` verified: **114 passed** in 18.23s, 78% line coverage.
