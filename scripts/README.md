# ICC Utility, Benchmarking & Verification Scripts

This directory contains standalone execution scripts, replication runners, mathematical verification suites, and performance profiling tools for the Invariant Core Consensus (ICC-v2) clustering framework.

---

## Script Catalog & Execution Guide

### 1. Dataset Management

#### [`download_data.py`](file:///D:/icc-clustering/scripts/download_data.py) *(formerly `fetch_data.py`)*
Downloads, unpacks, and validates all 13 canonical benchmark datasets across genomics, biomedical, text, audio, image, hyperspectral, and single-cell domains. Verifies sample count $N$, feature dimension $D$, cluster count $K$, and absence of NaNs.

- **Parameters:**
  - `--dataset <name>`: Download/validate a single dataset by identifier (e.g., `colon`, `leukemia`, `isolet`).
  - `--summary`: Display tabular overview of all registered datasets without loading arrays into memory.
- **Outputs:** Cached datasets in `data/` and `experiments/exp3_real_world_benchmarks/data/cache/`.
- **Usage:**
  ```powershell
  python scripts/download_data.py --summary
  python scripts/download_data.py --dataset leukemia
  ```
  *(Note: [`fetch_data.py`](file:///D:/icc-clustering/scripts/fetch_data.py) is retained as a backward-compatible wrapper).*

---

### 2. Performance & Scaling Benchmarks

#### [`benchmark_scaling.py`](file:///D:/icc-clustering/scripts/benchmark_scaling.py) *(formerly `rerun_table4_timing.py`)*
Measures empirical sample complexity scaling and peak heap memory consumption of ICC-v2 on an idle system across large sample sizes $N \in \{5000, 6000, 8000, 10000\}$ with feature dimension $D=200$ and $K=3$.

- **Algorithmic Rationale:** Validates the theoretical $O(N \cdot L)$ time and memory scaling of the anchor bipartite graph compared to the $O(N^2)$ scaling of dense co-association consensus.
- **Parameters:**
  - `--n-values`: List of sample sizes $N$ to benchmark (default: `5000 6000 8000 10000`).
  - `--seeds`: Random seeds for data generation (default: `42 101 202 303 404`).
  - `--profile-n`: Target $N$ for detailed `cProfile` function hotspot inspection (default: `8000`).
- **Outputs:**
  - `experiments/exp4_scalability_and_sensitivity/data/exp4_sample_scaling_results.csv`
  - `experiments/exp4_scalability_and_sensitivity/data/timing_rerun_environment_log.json`
  - `experiments/exp4_scalability_and_sensitivity/data/profiler_n8000.txt`
- **Usage:**
  ```powershell
  python scripts/benchmark_scaling.py
  ```
  *(Note: [`rerun_table4_timing.py`](file:///D:/icc-clustering/scripts/rerun_table4_timing.py) is retained as a backward-compatible wrapper).*

#### [`benchmark_latency.py`](file:///D:/icc-clustering/scripts/benchmark_latency.py) *(formerly `measure_query_latency.py`)*
Evaluates closed-form out-of-sample inductive query prediction latency (ms per query) across 6 real-world benchmark cohorts (CNS, Colon, Leukemia, Ovarian, SRBCT, ISOLET).

- **Algorithmic Rationale:** Demonstrates that projecting a novel sample onto geometry-calibrated anchor centroids runs in $O(K \cdot |\mathcal{S}|)$ time without retraining, achieving sub-millisecond query latency ($< 0.01$ ms/query).
- **Parameters:**
  - `--datasets`: List of cohorts to measure (default: `cns colon leukemia ovarian srbct isolet`).
  - `--repeats`: Repetition count for wall-clock averaging (default: `50`).
  - `--output-json`: Destination JSON file path (default: `results/query_latency.json`).
- **Outputs:** `results/query_latency.json`
- **Usage:**
  ```powershell
  python scripts/benchmark_latency.py --repeats 50
  ```
  *(Note: [`measure_query_latency.py`](file:///D:/icc-clustering/scripts/measure_query_latency.py) is retained as a backward-compatible wrapper).*

---

### 3. Real-World Replication & Stability Audits

#### [`reproduce_stability.py`](file:///D:/icc-clustering/scripts/reproduce_stability.py) *(formerly `run_real_data_stability.py`)*
Executes the empirical stability-accuracy analysis across 13 benchmark datasets and 12 clustering algorithms to audit the "stability-accuracy trap".

- **Mathematical Rationale:**
  - Evaluates mean ground-truth accuracy: $\text{Mean ARI} = \frac{1}{S} \sum_s \text{ARI}(y_{\text{pred}}^{(s)}, y_{\text{true}})$
  - Evaluates pairwise partition stability across seeds: $\text{Stability} = \frac{2}{S(S-1)} \sum_{i < j} \text{ARI}(y_{\text{pred}}^{(i)}, y_{\text{pred}}^{(j)})$
  - Measures the stability gap: $\Delta = \text{Stability} - \text{Accuracy}$
- **Parameters:**
  - `--skip-dec`: Skip Deep Embedded Clustering to reduce execution time.
  - `--only-dataset <name>`: Restrict audit to a single dataset (e.g., `colon`).
  - `--max-seeds <int>`: Cap seeds per dataset for fast smoke testing.
- **Outputs:**
  - `results/stability/real_data_stability_summary.csv`
  - `results/stability/labels/*.npy`
- **Usage:**
  ```powershell
  python scripts/reproduce_stability.py --skip-dec
  python scripts/reproduce_stability.py --only-dataset leukemia
  ```
  *(Note: [`run_real_data_stability.py`](file:///D:/icc-clustering/scripts/run_real_data_stability.py) is retained as a backward-compatible wrapper).*

#### [`reproduce.py`](file:///D:/icc-clustering/scripts/reproduce.py)
Master experiment orchestrator for automated end-to-end replication of manuscript findings across synthetic noise regimes and real benchmarks.

- **Usage:**
  ```powershell
  python scripts/reproduce.py --help
  ```

---

### 4. Mathematical Identity & Analytical Verifications

#### [`verify_identities.py`](file:///D:/icc-clustering/scripts/verify_identities.py) *(formerly `verify_determinacy_identity.py`)*
Independent mathematical proof and numerical verification of **Proposition 2 (Exact Sample Determinacy Identity)**.

- **Mathematical Rationale:**
  Proves that sample determinacy can be computed exactly in $O(N \cdot M^2)$ time using contingency matrices without ever instantiating the quadratic $N \times N$ dense co-association matrix $S$:
  $$\sum_{j=1}^N S_{ij}^2 = \frac{1}{M^2} \sum_{m_1=1}^M \sum_{m_2=1}^M C_{m_1, m_2}(\pi_{m_1}(i), \pi_{m_2}(i))$$
- **Verification Criteria:** Max numerical discrepancy strictly $< 10^{-12}$ across tiny, moderate, binary, high-cluster, and degenerate identical partition ensembles.
- **Usage:**
  ```powershell
  python scripts/verify_identities.py
  ```
  *(Note: [`verify_determinacy_identity.py`](file:///D:/icc-clustering/scripts/verify_determinacy_identity.py) is retained as a backward-compatible wrapper).*

#### [`verify_prop1.py`](file:///D:/icc-clustering/scripts/verify_prop1.py)
Numerical root-solving and integration verifying **Proposition 1 (Bimodality Coefficient Separation Bound)**. Proves that Sarle's Bimodality Coefficient exceeds the uniform distribution boundary ($b \ge 5/9$) when cluster separation satisfies $\Delta / \sigma_0 \ge \sqrt{(3 + \sqrt{15})/2} \approx 1.854$.

- **Usage:**
  ```powershell
  python scripts/verify_prop1.py
  ```

#### [`verify_bc.py`](file:///D:/icc-clustering/scripts/verify_bc.py)
Analytical and numerical comparison of Sarle's Bimodality Coefficient across standard distributions (Exponential, Uniform, Lognormal, Beta).

- **Usage:**
  ```powershell
  python scripts/verify_bc.py
  ```

#### [`verify_bc_simulation.py`](file:///D:/icc-clustering/scripts/verify_bc_simulation.py)
Monte Carlo finite-sample simulation of the empirical null distribution of Sarle's Bimodality Coefficient under unimodal Gaussian noise.

- **Usage:**
  ```powershell
  python scripts/verify_bc_simulation.py
  ```

---

### 5. Diagnostics & Visualizations

#### [`verify_environment.py`](file:///D:/icc-clustering/scripts/verify_environment.py)
Audits host hardware, Python environment, optional deep learning accelerators (PyTorch, TensorFlow, CUDA), and package dependencies.

- **Usage:**
  ```powershell
  python scripts/verify_environment.py
  ```

#### [`plot_conceptual_framework.py`](file:///D:/icc-clustering/scripts/plot_conceptual_framework.py)
Generates high-resolution publication diagrams depicting the ICC-v2 geometry-calibrated consensus pipeline, bipartite graph formulation, and inductive out-of-sample projection.

- **Usage:**
  ```powershell
  python scripts/plot_conceptual_framework.py
  ```

#### [`compute_inductive_bootstrap.py`](file:///D:/icc-clustering/scripts/compute_inductive_bootstrap.py)
Computes bootstrap confidence intervals for inductive projection classification accuracy and Adjusted Rand Index across repeated data splits.

- **Usage:**
  ```powershell
  python scripts/compute_inductive_bootstrap.py
  ```

#### [`compute_stats_summary.py`](file:///D:/icc-clustering/scripts/compute_stats_summary.py)
Aggregates experimental outputs from `results/` into LaTeX and CSV summary tables.

- **Usage:**
  ```powershell
  python scripts/compute_stats_summary.py
  ```
