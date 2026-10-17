# EXPERIMENT RERUN SPECIFICATION REGISTRY (NEEDS_RERUN.md)

**Project:** Inductive Consensus Clustering (ICC-v2) Remediation  
**Stage:** Fix Pass A (Reconnaissance & Manuscript Hardening)  
**Date:** October 17, 2026  
**Policy:** Strict read-only audit. No new experimental runs were executed during this pass. Every empirical question requiring compute is cataloged here with a formal, reproducible execution specification.

---

## Item 1: Quadratic Determinacy Runtime Memory Materialization Audit

- **Registry ID:** `RERUN-MEM-01`
- **Related Issues:** `N7`, `M4`
- **Question:** Does the benchmark implementation `src/icc/consensus_v2.py` strictly execute the $O(M^2 N + M^2 K^2)$ contingency bincount identity without materializing intermediate $N \times N$ structures across all sample scales, or does peak memory scaling include extraneous process-level allocations?
- **Observed Discrepancy:**
  - Dense $N \times N$ `float64` matrix at $N = 8{,}000$ requires $512\text{ MB}$.
  - Measured peak RSS of ICC-v2 at $N = 8{,}000$ was $1{,}040.5\text{ MB}$ (reported as a $39.1\%$ reduction over Standard Consensus at $1{,}709.6\text{ MB}$).
  - In Exp 4.3 at $N = 10{,}000$, Exact dense consensus consumed $1{,}529.8\text{ MB}$ peak RAM, whereas Reduced anchor consensus required $45.8\text{ MB}$ ($97.0\%$ reduction).
- **Execution Specification:**
  - **Script:** `experiments/exp4_scalability_and_sensitivity/src/scaling_benchmark.py`
  - **Instrumentation:** Use `tracemalloc` to record internal Python heap allocations separately from OS-level `psutil.Process().memory_info().rss`.
  - **Conditions:** Sample sizes $N \in \{1{,}000, 2{,}000, 4{,}000, 8{,}000, 10{,}000\}$ with $D = 100, K = 3, M = 25, L = 40$.
  - **Output Artifact:** `results/rerun/mem_tracemalloc_profile.json`

---

## Item 2: Multi-Classifier Inductive Generalization Confidence Intervals & kNN Metric

- **Registry ID:** `RERUN-EXP1-01`
- **Related Issues:** `N9`, `Tier 3 (Exp 1)`
- **Question:** What are the exact empirical confidence intervals for the $+4.5\%$ pseudo-label gain ($33.3\%$ vs $28.8\%$) at $D_{\text{noise}} = 3{,}000$ on synthetic Gaussian mixtures ($K = 3$), and what is the exact numerical accuracy of the $k$-Nearest Neighbors ($k=5$) classifier?
- **Observed Discrepancy:**
  - For $K = 3$, chance accuracy is $33.3\%$. The reported core pseudo-label accuracy of $33.3\%$ hovers at chance level.
  - The manuscript text mentioned $k$-Nearest Neighbors ($k=5$) as one of four evaluated classifier paradigms, but no numerical accuracy was plotted or reported for kNN in the primary figure.
- **Execution Specification:**
  - **Script:** `experiments/exp1_generalization/src/exp1_multiclassifier_generalization.py`
  - **Protocol:** 50 independent Monte Carlo trials; train/test split 80/20; evaluate Linear SVM, Random Forest (100 trees), MLP ($100 \times 50$), and kNN ($k=5$).
  - **Noise Levels:** $D_{\text{noise}} \in \{0, 50, 100, 500, 1{,}000, 2{,}000, 3{,}000\}$.
  - **Output Metrics:** Mean test classification accuracy, standard deviation, and $95\%$ bootstrap confidence intervals.
  - **Output Artifact:** `results/rerun/exp1_multiclassifier_ci.csv`

---

## Item 3: Empty Left Panel Regeneration for Inductive Generalization Figure (Fig 3b)

- **Registry ID:** `RERUN-FIG-01`
- **Related Issues:** `F1`, `Tier 1`
- **Question:** Why was the left panel of legacy Figure 3b (`fig10_pseudolabel_generalization.png` or related distribution subfigure) empty in the pre-remediation bundle?
- **Resolution in Fix Pass A:** The manuscript text and figure environment were updated to reference the self-contained complete figure artifacts (`fig9_inductive_generalization.png` and `fig10_pseudolabel_generalization.png`).
- **Execution Specification for Fresh Standalone Render:**
  - **Script:** `experiments/exp1_generalization/src/plot_exp1_figures.py`
  - **Action:** Re-render the dual-panel figure with explicit subplot population for both low-noise ($D \le 100$) and high-noise ($D \ge 1{,}000$) conditions.
  - **Output Artifact:** `paper/figures/fig10_pseudolabel_generalization_fixed.png`

---

## Item 4: ASPP Confidence Calibration Benchmark on Real-World Genomics

- **Registry ID:** `RERUN-ASPP-01`
- **Related Issues:** `M7`, `P1-ASPP`
- **Question:** Does Anchor-Space Perturbation Profiling (ASPP) produce well-calibrated confidence scores and reliable Perturbation Sensitivity Indices ($\mathrm{PSI}_k$) when enabled during out-of-sample inference on real-world cancer microarrays?
- **Context:** ASPP is disabled by default (`enable_aspp=False`) in `src/icc/consensus_v2.py` to preserve linear runtime. It was presented in Section 4.4 as an architectural feature but was omitted from empirical benchmark evaluations in Table 3.
- **Execution Specification:**
  - **Script:** `experiments/audit_controls/src/eval_aspp_real_world.py`
  - **Datasets:** Leukemia ($N=72, D=7{,}129$), SRBCT ($N=83, D=2{,}308$), and Colon ($N=62, D=2{,}000$).
  - **Perturbations:** 5 perturbation families (dropout $\eta = 0.2$, Gaussian noise $\sigma = 0.1$, batch offset, feature masking $20\%$, clusterer random seeds).
  - **Output Metrics:** Expected Calibration Error (ECE), Brier score of confidence, and correlation between $\mathrm{PSI}_k$ and per-cluster misclassification rate.
  - **Output Artifact:** `results/rerun/aspp_genomics_calibration.csv`

---

## Item 5: Authentic OpenML Glioma (Dataset ID 1107) Benchmark

- **Registry ID:** `RERUN-DATA-01`
- **Related Issues:** `L1`, `N3`
- **Question:** What is the true comparative performance of all 11 clustering methods on genuine OpenML Glioma microarray data (OpenML ID 1107)?
- **Observed Discrepancy:** In the legacy audit cache (`data/cache/glioma.npz`), the data array was 100% byte-for-byte identical to `cns.npz` (SHA256: `0e449bf5...`). While Table 3 properly restricted its evaluation to CNS and omitted Glioma, any 21-dataset audit visual must evaluate genuine Glioma data.
- **Execution Specification:**
  - **Script:** `scripts/download_openml_glioma.py` followed by `experiments/exp3_real_world_benchmarks/src/run_exp3_1_benchmark_matrix.py --dataset glioma`
  - **Data Source:** OpenML Suite / ID 1107.
  - **Protocols:** 10 random seeds; compute ARI, NMI, AMI, and V-Measure across all 11 models.
  - **Output Artifact:** `results/rerun/glioma_true_benchmarks.csv`

---

## Item 6: Adaptive Anchor Budget Scaling ($L = \max(40, 10K)$) on High-K Benchmarks

- **Registry ID:** `RERUN-ANCHOR-01`
- **Related Issues:** `N10`, `Tier 2`
- **Question:** Does scaling the anchor budget dynamically to $L = \max(40, 10K)$ with stratified anchor sampling resolve the performance drop on large-$K$ benchmarks (Isolet with $K=26 \to L=260$; 20 Newsgroups with $K=20 \to L=200$)?
- **Observed Behavior:** The code defaults to a static $L = 40$. For $K \ge 20$, $L = 40$ provides fewer than 2 anchors per cluster on average, causing Isolet ARI to drop to $0.286$ (vs $0.500$ for Ward) and Newsgroups ARI to $0.000$ (vs $0.114$ for Ward).
- **Execution Specification:**
  - **Script:** `experiments/exp3_real_world_benchmarks/src/run_high_k_anchor_sweep.py`
  - **Datasets:** Isolet ($K=26$), 20 Newsgroups ($K=20$), Extended Yale B ($K=38$).
  - **Anchor Budgets:** $L \in \{40, 2K, 5K, 10K, 15K\}$.
  - **Sampling Rules:** Uniform random from core vs $k$-means++ seeded anchors in core subspace.
  - **Output Artifact:** `results/rerun/high_k_anchor_scaling.csv`

---
*Registry compiled and verified by Antigravity Orchestrator for Fix Pass A.*
