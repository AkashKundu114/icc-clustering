# Inductive Consensus Clustering (ICC-v2): Empirical Suite & Traceability Matrix

This document provides the definitive experimental catalog, baseline specifications, evaluation metrics, and end-to-end traceability matrix linking manuscript claims, figures, and tables to executable code and raw artifacts.

---

## 1. Experimental Suite Architecture

The empirical evaluation of ICC-v2 spans six primary investigation protocols and six statistical audit controls:

| Experiment | Title / Objective | Key Research Question | Evaluated Scale |
| :--- | :--- | :--- | :--- |
| **Exp 0** | **Consensus Stability Falsification** | Does isotropic distractor noise induce universal failure across clustering objectives? | $N=500, D \in [2, 2000], K=3$ |
| **Exp 1** | **Inductive Generalization** | Do core pseudo-labels improve downstream classifier accuracy under noise? | $N=300, D \in [2, 5000], K=3$ |
| **Exp 2** | **Architectural Ablations & VSSG** | How do determinacy cores, VSSG gating, and pool size affect cluster recovery? | Microarrays & synthetic cohorts |
| **Exp 3** | **Multi-Domain Benchmarking** | How does ICC-v2 perform against 10 baselines across 13 diverse domain datasets? | 13 datasets, 1,430 model executions |
| **Exp 4** | **Scalability & Anchor Fidelity** | What is the empirical scaling of bipartite anchor consensus vs. dense consensus? | $N \in [500, 32{,}000], D=200$ |
| **Exp 5** | **Extreme Asymptotic Scaling** | What are the limits of the scalable path under extreme dimension and sample size? | $N \le 1{,}000{,}000, D \le 100{,}000$ |
| **Audit A2** | **Subspace Pool Controls** | Does VSSG feature ranking outperform random selection and single-pass filters? | Colon, SRBCT, Leukemia |
| **Audit A3** | **Transfer-Cut Eigenspace Equivalence** | Does the $L \times L$ anchor eigensystem match the dense $N \times N$ bipartite eigensystem? | Synthetic & real graphs |
| **Audit E1** | **Extended 21-Dataset Benchmark** | How robust is ICC-v2 across an expanded suite with pre-registered held-out protocols? | 21 multi-domain datasets |
| **Audit E3** | **Pool-Size Sensitivity Curves** | What is the empirical behavior across the full candidate pool fraction range? | $D_{\text{pool}} \in [1\%, 100\%]$ |
| **Audit E5** | **Independent Re-Runs** | Do independent multi-seed runs reproduce Exp 1 and missing-data benchmarks? | 10 independent trials |
| **Audit E6** | **Per-Process Scaling Sweeps** | What is the exact RSS memory growth and runtime scaling per isolated process? | $N \in [500, 32{,}000]$ |

---

## 2. Benchmark Datasets (13 Multi-Domain Datasets)

All datasets are configured declaratively in [`configs/datasets.yaml`](../configs/datasets.yaml) and loaded via `src.icc.datasets.load_dataset`:

| Dataset | Domain | Samples ($N$) | Features ($D$) | Clusters ($K$) | Ratio ($D/N$) | Characteristics / Preprocessing |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Sonar** | Acoustic Sensors | $208$ | $60$ | $2$ | $0.29$ | Continuous sonar returns; z-score standardized |
| **Madelon** | Synthetic Distractor | $500$ | $500$ | $2$ | $1.00$ | 20 informative features + 480 distractor noise features |
| **Colon** | Cancer Genomics | $62$ | $2,000$ | $2$ | $32.26$ | Tumor vs. normal colon biopsies; log2 transformed |
| **SRBCT** | Cancer Genomics | $83$ | $2,308$ | $4$ | $27.81$ | Small Round Blue Cell Tumors (4 diagnostic subtypes) |
| **CNS** | Cancer Genomics | $60$ | $7,129$ | $2$ | $118.82$ | Embryonal central nervous system tumors |
| **Leukemia** | Cancer Genomics | $72$ | $7,129$ | $2$ | $99.01$ | Acute lymphoblastic vs. acute myeloid leukemia (ALL/AML) |
| **Prostate** | Cancer Genomics | $102$ | $12,600$ | $2$ | $123.53$ | Prostate adenocarcinoma biopsies |
| **Ovarian** | Mass Spectrometry | $253$ | $15,154$ | $2$ | $59.90$ | SELDI-TOF proteomic mass spectra; baseline corrected |
| **20 Newsgroups** | Text Classification | $18,846$ | $10,000$ | $20$ | $0.53$ | TF-IDF sparse document vectors |
| **Isolet** | Speech Recognition | $7,797$ | $617$ | $26$ | $0.08$ | Continuous spoken alphabet phoneme spectral features |
| **Indian Pines** | Hyperspectral Imaging | $10,249$ | $200$ | $16$ | $0.02$ | AVIRIS sensor continuous spectral reflectance |
| **Yale B** | Facial Biometrics | $2,414$ | $1,024$ | $38$ | $0.42$ | Cropped facial reflectance across extreme lighting |
| **Zheng68k** | scRNA-seq Genomics | $68,579$ | $2,000$ | $11$ | $0.03$ | Ultra-sparse single-cell PBMC transcriptomics |

---

## 3. Baseline Clustering Algorithms (11 Methods)

Configured declaratively in [`configs/baselines.yaml`](../configs/baselines.yaml) and implemented under `src.icc.baselines`:

1. **K-Means (Lloyd 1982):** Classical centroid-based distance minimization.
2. **Ward Linkage (Ward 1963):** Hierarchical agglomerative clustering minimizing within-cluster variance.
3. **Spectral Clustering (Von Luxburg 2007):** Graph Laplacian eigen-decomposition on dense RBF affinities.
4. **Fuzzy C-Means (FCM; Bezdek 1981):** Soft membership minimization under fuzzifier $m=2.0$.
5. **Standard Consensus (Fred & Jain 2005):** Full $N \times N$ dense co-association matrix with average-linkage consensus.
6. **Core-Halo Consensus (Li et al. 2019):** Determinacy-thresholded core extraction with dense consensus fusion.
7. **DEC (Xie et al. 2016):** Deep Embedded Clustering via autoencoder latent space Student-$t$ distribution minimization.
8. **FCAG (Nie et al. TPAMI 2024):** Fast and robust anchor-guided bipartite graph spectral clustering.
9. **FastMVC (Huang et al. TKDE 2023):** Efficient bipartite anchor graph consensus across multi-view ensembles.
10. **ICC-v1 (Ablation; Kundu 2026):** Bipartite core anchor consensus without VSSG feature gating.
11. **ICC-v2 (Proposed; Kundu 2026):** Full VSSG subspace gating + bipartite anchor consensus + ASPP profiling.

---

## 4. Evaluation Metrics

Evaluated via `src.icc.evaluation.evaluate_all`:

- **Adjusted Rand Index (ARI):**
  $$\text{ARI} = \frac{\sum_{ij} \binom{n_{ij}}{2} - [\sum_i \binom{a_i}{2} \sum_j \binom{b_j}{2}] / \binom{N}{2}}{\frac{1}{2} [\sum_i \binom{a_i}{2} + \sum_j \binom{b_j}{2}] - [\sum_i \binom{a_i}{2} \sum_j \binom{b_j}{2}] / \binom{N}{2}}$$
- **Normalized Mutual Information (NMI):**
  $$\text{NMI}(U, V) = \frac{2 \cdot I(U; V)}{H(U) + H(V)}$$
- **Adjusted Mutual Information (AMI):** Adjusted for chance expected mutual information under the hypergeometric model.
- **V-Measure Score:** Harmonic mean of homogeneity and completeness with weighting $\beta=1.0$.
- **Fowlkes-Mallows Index (FM):** Geometric mean of precision and recall over pairwise clustered instances.
- **Perturbation Sensitivity Index (PSI):** Cluster-level stability score under ASPP multi-family perturbations:
  $$\text{PSI}_k = 1.0 - \frac{1}{|\mathcal{M}|} \sum_{m \in \mathcal{M}} \text{Retention}_k(m)$$

---

## 5. End-to-End Manuscript Traceability Matrix

This table maps every major empirical figure, table, and finding in the manuscript directly to the code, raw artifacts, and random seeds:

| Manuscript Item | Topic / Focus | Generating Script | Raw Output / Artifact | Random Seeds | Key Verified Metric |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Fig. 1–8** | Exp 0: Consensus stability falsification | `experiments/exp0_falsification/run_all.py` | `results/exp0_falsification/exp0_falsification_results.csv` | `42` | Ward/Spectral report false stability under noise; K-Means collapses |
| **Fig. 9–10** | Exp 1: Inductive generalization & sample efficiency | `experiments/exp1_generalization/run_exp1.py` | `results/exp1_generalization/exp1_generalization_results.csv` | `42, 100..109` | Parity at $D_{\text{noise}} \le 50$; degrades toward chance ($\approx 33\%$) at $D=1000$ |
| **Fig. 10b–c** | Multi-classifier generalization sweep | `experiments/exp1_generalization/run_exp1.py --run-multiclassifier` | `results/exp1_generalization/exp1_multiclassifier_results.csv` | `42` | RF, SVM, MLP show identical ambient noise vulnerability |
| **Fig. 11–13** | Exp 2: Core determinacy & VSSG ablation | `experiments/exp2_ablation/run_exp2.py` | `results/exp2_ablation/exp2_1_bimodality_scores.csv` | `42` | Precision@50 $\ge 0.94$; $+34\%$ ARI boost from core determinacy |
| **Fig. 14–17** | Exp 3: 13-Dataset benchmark comparisons | `experiments/exp3_real_world_benchmarks/run_exp3.py` | `results/exp3_real_world_benchmarks/exp3_1_benchmark_matrix_v2.csv` | `42..51` (10 seeds) | Grand Mean ARI = **0.1599**, Rank 5.46/11; Rank #1 on cancer genomics |
| **Fig. 18–21** | Exp 4: Scalability & Anchor Fidelity | `experiments/exp4_scalability_and_sensitivity/run_exp4.py` | `results/exp4_scalability_and_sensitivity/exp4_1_scalability_results.csv` | `42` | Dense path $\mathcal{O}(N^2)$ memory; scalable path $\mathcal{O}(N)$ runtime |
| **Fig. 22a–c** | Audit A2: Feature screening controls | `experiments/audit_controls/src/a2_controls.py` | `experiments/audit_controls/data/a2_real.csv` | `42` | Wide ensemble pool outperforms single-pass filters by $+4,376\%$ |
| **Fig. 23–24** | Audit A3: Transfer-Cut embedding audit | `experiments/audit_controls/src/a3_embedding.py` | `experiments/audit_controls/data/a3_embedding.csv` | `42` | Eigenspace distance $< 10^{-12}$ between anchor and sample representations |
| **Fig. 25a–b** | Missing-data sensitivity audit | `experiments/exp3_real_world_benchmarks/run_exp3.py` | `results/exp3_real_world_benchmarks/exp3_5_missing_data_results.csv` | `42` | Retains $\approx 80\%$ at 20% MCAR; collapses by 30% MCAR |
| **Fig. 26** | Exp 5: Extreme Asymptotic Scaling | `experiments/exp5_extreme_scale/run_exp5.py` | `results/exp5_extreme_scale/exp5_extreme_scale_results.csv` | `42` | Linear scaling demonstrated up to $N = 1,000,000, D = 100,000$ |
| **Table 1** | Primary Benchmark ARI Matrix | `scripts/generate_supp_tables.py` | `paper/gen/table_benchmark_ari.tex` | 10 seeds | Leukemia ARI = 0.680, SRBCT = 0.538, Grand Mean = 0.1599 |
| **Table 2** | NMI Benchmark Matrix | `scripts/generate_supp_tables.py` | `paper/gen/table_benchmark_nmi.tex` | 10 seeds | Full cross-metric NMI comparisons |
| **Table 3** | Statistical Significance Tests | `tools/check_consistency.py` | `results/exp3_real_world_benchmarks/friedman_wilcoxon_tests.json` | 10 seeds | Friedman omnibus $\chi^2 = 11.38, p = 0.3341$ |
| **Table 4** | Resource Telemetry Comparison | `tools/profile_resources.py` | `results/resource_benchmarks.json` | `42` | Peak RAM cut by $74.2\%$, Throughput $+20\%$, $2.15\times$ speedup |
| **Table 5** | ASPP Fingerprints across Domains | `demo.py` | `results/aspp_stability_fingerprints.csv` | `42` | Multi-family stability calibration |

---

## 6. Execution Commands

### Fast Verification & Smoke Tests
```bash
# Interactive quickstart demo (runs in ~5s)
python demo.py

# Automated test suite (114 tests)
python -m pytest tests/ -v

# Consistency and macro traceability audit
python tools/check_consistency.py
```

### Full Experiment Re-Executions
```bash
# Exp 0: Falsification Suite
python experiments/exp0_falsification/run_all.py --reproduce-plots

# Exp 1: Inductive Generalization
python experiments/exp1_generalization/run_exp1.py --run-full

# Exp 2: Architectural Ablations
python experiments/exp2_ablation/run_exp2.py --reproduce-plots

# Exp 3: Real-World 13-Dataset Benchmarks
python experiments/exp3_real_world_benchmarks/run_exp3.py --reproduce-plots

# Exp 4: Scalability & Sensitivity
python experiments/exp4_scalability_and_sensitivity/run_exp4.py --reproduce-plots

# Exp 5: Extreme Asymptotic Scaling
python experiments/exp5_extreme_scale/run_exp5.py --reproduce-plots
```
