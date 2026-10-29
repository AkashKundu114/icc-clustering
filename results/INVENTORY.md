# Empirical Results and Configuration Inventory

This inventory documents all raw per-seed result files, evaluation configurations, seeds, and hyperparameters used across all tables and analyses in the manuscript.

---

## 1. Inventory by Table and Experiment

| Table / Analysis | Raw Result File(s) | Seeds | $M$ | $L$ | $\alpha$ | $\tau_{\text{core}}$ | Datasets / Configurations | Total Model Fits |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Table 3: Held-Out Inductive Generalization** | `results/passF/inductive_paired_splits.csv`<br>`results/passE/inductive_agreement.json`<br>`results/passF/inductive_bootstrap_stats.json` | 10 splits (0--9) | 25 | 40 | 0.15 | 0.50 | 6 datasets: CNS, Colon, Leukemia, Ovarian, SRBCT, Isolet (80% train / 20% test) | $6 \times 5 \times 10 = 300$ evaluations |
| **Table 4: Computational Scalability vs. $N$** | `experiments/exp4_scalability_and_sensitivity/data/exp4_sample_scaling_summary.csv`<br>`.../exp4_sample_scaling_results.csv` | 5 seeds per $N$ | 20 | 40 | -- | -- | Synthetic Gaussians: $N \in \{500, 1000, 2000, 5000, 8000, 10000\}$, $D=500, K=3$ | $6 \times 4 \times 5 = 120$ runs |
| **Table 5: Extreme Scalability to $10^6$ Samples** | `results/passE/exp5_controlled_scaling.csv`<br>`results/passE/exp5_scaling_stats.json` | **3 seeds (0--2)** | 20 (Def), 10 (Ext) | 60 | -- | -- | Synthetic Gaussians: $N \in \{10^4, 10^5, 10^6\}$, $D=100, K=5$ | $3 \times 2 \times 3 = 18$ runs |
| **Table 7: Omnibus Benchmark Evaluation (11 Methods)** | `results/passF/benchmark_matrix_passF.csv`<br>`results/passF/benchmark_matrix_summary_passF.csv`<br>`results/passF/friedman_nemenyi_passF.json` | 30 seeds (High-$D$)<br>10 seeds (Others) | 25 | 40 | 0.15 | 0.50 | 13 datasets: 6 High-$D$ ($D/N > 20$) with 30 seeds; 7 remaining cohorts with 10 seeds | $6 \times 11 \times 30 + 7 \times 11 \times 10 = 1980 + 770 = 2750$ fits |
| **Table 8: Matched-Budget Feature Selection Baselines** | `results/passF/fair_baselines_30seeds_passF.csv`<br>`results/passF/fair_baselines_summary_passF.json` | 30 seeds (0--29) | 25 | 40 | 0.15 | 0.50 | 6 High-$D$ cohorts ($D/N > 20$), 9 models (KM/StdCons under matched budget $\lfloor 0.15 D \rfloor$) | $6 \times 9 \times 30 = 1620$ fits |
| **Table 10: Vargha-Delaney $A_{12}$ Effect Sizes** | `results/passF/vargha_delaney_a12_passF.csv` | 30 seeds (0--29) | 25 | 40 | 0.15 | 0.50 | 6 High-$D$ cohorts, ICC-v2 vs. 10 baseline models | Computed from Pass F per-seed data |
| **Table 11: Per-Seed Stability & Normality** | `results/passF/shapiro_wilk_cv_passF.csv` | 30 seeds (0--29) | 25 | 40 | 0.15 | 0.50 | 6 High-$D$ cohorts, ICC-v2 distribution properties (Shapiro-Wilk $W$, $p$, CV, fraction $> 0.50$) | Computed from Pass F per-seed data |
| **Table 13: Architectural Component Ablation (V0--V5)** | `results/passF/ablation_30seeds_passF.csv`<br>`results/passF/ablation_stats_passF.json` | 30 seeds (0--29) | 25 | 40 | 0.15 | 0.50 | 6 High-$D$ cohorts, 7 ablation variants (Ambient KM, Ambient StdCons, BGSS KM, BGSS StdCons, Ambient Anchor, BGSS Random Anchors, Full ICC-v2) | $6 \times 7 \times 30 = 1260$ runs |
| **Table 14: $2 \times 2$ Factorial Decomposition** | `results/passF/ablation_stats_passF.json` | 30 seeds (0--29) | 25 | 40 | 0.15 | 0.50 | Marginals and cell means for $\{ \text{Ambient}, \text{BGSS} \} \times \{ \text{Single/Dense}, \text{Anchor} \}$ | Derived from Table 13 data |
| **Table 15: Component Contributions (Paired $\Delta$)** | `results/passF/component_contributions_passF.csv` | 30 seeds (0--29) | 25 | 40 | 0.15 | 0.50 | 6 High-$D$ cohorts, paired difference relative to $V_5$ with 10,000 cluster-bootstrap iterations | Derived from Table 13 data |

---

## 2. Configuration Discrepancies and Audit Ledger (BLOCKER-CONFIG)

1. **Model Fit Count Discrepancy (Resolved):**
   - *Previous text:* Stated "across 30 independent canonical seeds (2,750 total model fits)".
   - *Mathematical check:* $13 \times 11 \times 30 = 4{,}290$, which conflicted with $2{,}750$.
   - *Actual protocol in code and raw logs:* 30 seeds on the 6 high-dimensional cohorts ($6 \times 11 \times 30 = 1{,}980$) and 10 seeds on the remaining 7 cohorts ($7 \times 11 \times 10 = 770$). $1{,}980 + 770 = 2{,}750$ fits.
   - *Resolution:* Explicitly state the two-tier seed allocation ($30$ seeds on $D/N > 20$, $10$ seeds on others) in Abstract, Section 5.2, Table 7 caption, and Fig. 6 caption.

2. **Table 5 Seed Count Discrepancy (Resolved):**
   - *Previous text:* Table 5 caption claimed "30 Seeds Per Configuration".
   - *Actual raw file:* `results/passE/exp5_controlled_scaling.csv` records exactly 3 independent seeds (`seed` $\in \{0, 1, 2\}$).
   - *Resolution:* Relabel Table 5 and associated prose as "3 independent seeds" matching the empirical record.

3. **Ensemble Size $M$ (Resolved):**
   - *Discrepancy:* Benchmark tables used $M = 25$ (`n_base_models: 25` in `configs/experiment_defaults.yaml` and `consensus_v2.py`), while synthetic scaling experiments (Table 4 and Table 5) used $M = 20$ (default) and $M = 10$ (extreme).
   - *Resolution:* Accurately document $M = 25$ as benchmark default in Section 5.2 and Table 2, and specify $M = 20$ / $M = 10$ in the synthetic scaling methodology (Section 6.1).

4. **Anchor Budget $L$ (Resolved):**
   - *Discrepancy:* Algorithm 1 hard-coded $40$, while text mentioned $L=40, 50, 60$. Table 5 used $L=60$.
   - *Resolution:* Algorithm 1 parameterizes $L$ explicitly (default $L=40$). Benchmark evaluation fixed $L=40$ ($L = \min(40, |\mathcal{C}_{\text{core}}|)$) a priori.

5. **Gating Fraction $\alpha$ (Resolved):**
   - *Discrepancy:* Text mentioned $\alpha = 0.50$ (giving 3,564 genes on Leukemia) vs. $\alpha = 0.15$ (giving 1,069 genes).
   - *Actual code:* All benchmark runs and `consensus_v2.py` used $\alpha = 0.15$ (`pool_frac = 0.15`), selecting $\lfloor 0.15 \times 7{,}129 \rfloor = 1{,}069$ genes on Leukemia/CNS.
   - *Resolution:* Reconcile text and Table 2 to state $\alpha = 0.15$ and $1{,}069$ genes uniformly.
