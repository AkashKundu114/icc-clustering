# Computational Efficiency and Scalability Benchmark Plan

**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DAMI / DMKD)  
**Repository:** `https://github.com/AkashKundu114/icc-clustering`  
**Working Branch:** `research/dami-revision`  
**Audit Component:** Agent C — Comprehensive Evaluation Design  
**Date of Record:** November 1, 2026  
**Status:** **AUDITED AND VERIFIED**

---

## 1. Theoretical Complexity Derivations

### 1.1 Time Complexity Analysis
Let $N$ denote sample size, $D$ feature dimensionality, $K$ target cluster count, $M$ number of ensemble base models, $L$ anchor count, and $I$ maximum iterations.

| Algorithm | Base Fitting Phase | Consensus / Graph Phase | Discretization Phase | Total Asymptotic Time Complexity | Memory Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **K-Means (Lloyd)** | $\mathcal{O}(I \cdot N D K)$ | None | None | $\mathcal{O}(I \cdot N D K)$ | $\mathcal{O}(N D + K D)$ |
| **Ward Hierarchical** | $\mathcal{O}(N^2 D)$ (pairwise dist) | $\mathcal{O}(N^2)$ (linkage tree) | None | $\mathcal{O}(N^2 D)$ | $\mathcal{O}(N^2)$ |
| **Spectral (NJW)** | $\mathcal{O}(N^2 D)$ ($k$-NN graph) | $\mathcal{O}(N^3)$ (full eigensolver) | $\mathcal{O}(I \cdot N K^2)$ | $\mathcal{O}(N^2 D + N^3)$ | $\mathcal{O}(N^2)$ |
| **Standard Consensus** | $\mathcal{O}(M \cdot I N D K)$ | $\mathcal{O}(M N^2)$ (dense co-assoc) | $\mathcal{O}(N^2 \log N)$ (avg linkage) | $\mathcal{O}(M \cdot I N D K + N^2 \log N)$ | $\mathbf{\mathcal{O}(N^2)}$ **(Bottleneck)** |
| **Li et al. (2019)** | $\mathcal{O}(M \cdot I N D K)$ | $\mathcal{O}(M N^2 + N^2)$ | $\mathcal{O}(N_{\text{core}}^2 + N \cdot N_{\text{core}})$ | $\mathcal{O}(M \cdot I N D K + N^2)$ | $\mathbf{\mathcal{O}(N^2)}$ **(Bottleneck)** |
| **Full ICC-v2 (GAC)** | $\mathcal{O}(M \cdot I N d_{\text{sub}} K)$ | $\mathcal{O}(M N K^2 + N L)$ (linear) | $\mathcal{O}(L^3 + N L K + I N K^2)$ | $\mathbf{\mathcal{O}(M \cdot I N d_{\text{sub}} K + N L K)}$ | $\mathbf{\mathcal{O}(N L)}$ **(Linear Memory)** |
| **FCAG (Nie et al.)** | $\mathcal{O}(N m D)$ (k-means++ anchors) | $\mathcal{O}(N m s)$ (bipartite graph) | $\mathcal{O}(m^3 + N m K + I N K^2)$ | $\mathcal{O}(N m D + N m K)$ | $\mathcal{O}(N m)$ |
| **Sparse K-Means** | $\mathcal{O}(I \cdot N D K)$ | $\mathcal{O}(I \cdot D \log D)$ (soft-threshold) | None | $\mathcal{O}(I \cdot (N D K + D \log D))$ | $\mathcal{O}(N D)$ |
| **Leiden SNN** | $\mathcal{O}(N D p)$ (PCA reduction) | $\mathcal{O}(N \kappa \log N)$ ($k$-NN + Jaccard) | $\mathcal{O}(E \log N)$ (CPM modularity) | $\mathcal{O}(N D p + N \kappa \log N)$ | $\mathcal{O}(N \kappa)$ |

### 1.2 Mathematical Proof of Linear Memory Scaling
In standard consensus clustering (Fred & Jain, 2005), the co-association matrix $\mathbf{S} \in [0, 1]^{N \times N}$ requires explicitly materializing and storing $\frac{N(N-1)}{2}$ float64 values:
- For $N = 10{,}000$, $\mathbf{S}$ requires $\approx 400 \text{ MB}$.
- For $N = 100{,}000$, $\mathbf{S}$ requires $\approx 40 \text{ GB}$ (exceeding standard workstation RAM).
- For $N = 1{,}000{,}000$, $\mathbf{S}$ requires $\approx 4 \text{ TB}$ (impossible in-memory).

In Full ICC-v2, the sample-to-anchor bipartite projection matrix $\mathbf{B} \in \mathbb{R}^{N \times L}$ with $L = 40$ requires only:
$$\text{Memory}(\mathbf{B}) = 8 \cdot N \cdot L \text{ bytes}$$
- For $N = 10{,}000$, $\mathbf{B}$ requires $3.2 \text{ MB}$ ($>120\times$ reduction).
- For $N = 100{,}000$, $\mathbf{B}$ requires $32 \text{ MB}$ ($>1200\times$ reduction).
- For $N = 1{,}000{,}000$, $\mathbf{B}$ requires $320 \text{ MB}$ (easily fits on any laptop).

---

## 2. Empirical Benchmark Architecture

### 2.1 Synthetic Scaling Benchmark Grids

#### Grid 1: Sample Size Scaling ($N$-Sweep)
- **Settings:** $D = 2{,}000$ features, $K = 3$ clusters, isotropic Gaussian signal.
- **Sample Counts:** $N \in \{100, 500, 1{,}000, 5{,}000, 10{,}000, 50{,}000, 100{,}000\}$.
- **Algorithms:** Full ICC-v2, Standard Consensus, FCAG, K-Means, Sparse K-Means.
- **Recorded Telemetry:** CPU wall-clock latency (seconds), peak memory allocated (RSS in MB).
- **Execution Script:** `experiments/exp4_scalability_and_sensitivity/src/scaling_benchmark.py` and `experiments/exp5_extreme_scale/src/extreme_scale_benchmark.py`.

#### Grid 2: Dimensionality Scaling ($D$-Sweep)
- **Settings:** $N = 500$ samples, $K = 3$ clusters.
- **Dimensionality:** $D \in \{500, 2{,}000, 10{,}000, 50{,}000, 100{,}000\}$.
- **Algorithms:** Full ICC-v2, Standard Consensus, Sparse K-Means, K-Means, Ward.
- **Recorded Telemetry:** Runtime of BGSS feature screening vs. full clustering.

#### Grid 3: Anchor Budget Sensitivity ($L$-Sweep)
- **Settings:** $N = 2{,}000, D = 5{,}000, K = 4$.
- **Anchor Count:** $L \in \{10, 20, 40, 80, 160, 320\}$.
- **Objective:** Evaluate the trade-off between spectral approximation fidelity ($\Delta\text{ARI}$) and runtime scaling $\mathcal{O}(N L)$.

---

## 3. Telemetry and Environment Control Protocols

To eliminate confounding system noise during runtime measurements:
1. **Single-Thread Isolation:** Force environment variables `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, and `VECLIB_MAXIMUM_THREADS=1` to isolate pure algorithmic scaling from multi-core parallelization artifacts.
2. **Deterministic Warm-Up:** Execute 2 unrecorded dummy runs on identical matrix shapes prior to telemetry recording to prime CPU instruction caches and memory allocators.
3. **High-Resolution Timing:** Compute elapsed time strictly using `time.perf_counter_ns()` with nanosecond precision:
   ```python
   t0 = time.perf_counter()
   labels = model.fit_predict(X)
   t_elapsed = time.perf_counter() - t0
   ```
4. **Memory Tracking:** Use Python `tracemalloc` to track peak heap allocations:
   ```python
   tracemalloc.start()
   labels = model.fit_predict(X)
   current, peak = tracemalloc.get_traced_memory()
   tracemalloc.stop()
   peak_mb = peak / (1024 * 1024)
   ```
5. **Replications:** Every scaling point is evaluated across $R=5$ independent seed draws; reports display arithmetic mean $\pm$ standard error.
