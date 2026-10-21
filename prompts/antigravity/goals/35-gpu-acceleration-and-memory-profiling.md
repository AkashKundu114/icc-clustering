# Goal: GPU Acceleration, Memory Profiling & High-D Scaling

Deploy this goal to profile runtime bottlenecks, eliminate memory leaks, optimize PyTorch/CUDA utilization, and ensure linear scalability in high-dimensional or large-sample regimes.

---

## Assigned Subagent Personas
1. **Performance Profiler (`roo_debugger`)**: Instruments memory tracking (`tracemalloc`, PyTorch CUDA memory snapshots) and runtime cProfile.
2. **GPU Optimization Engineer (`roo_coder`)**: Implements vectorized tensor operations, mixed precision, and out-of-core batching.
3. **Scaling Analyst (`roo_ask`)**: Measures empirical time complexity $\mathcal{O}(N^\alpha D^\beta)$ against theoretical bounds.

---

## Profiling Protocol

### 1. Memory Footprint & Peak RAM/VRAM Audit
- Profile peak host memory consumption across sample sizes $N \in [10^3, 10^5]$:
  ```python
  import tracemalloc
  tracemalloc.start()
  # Execute solver / pipeline
  peak_gb = tracemalloc.get_traced_memory()[1] / 1e9
  ```
- If GPU is utilized:
  ```python
  import torch
  torch.cuda.reset_peak_memory_stats()
  # Execute tensor ops
  peak_vram_gb = torch.cuda.max_memory_allocated() / 1e9
  ```
- Verify that intermediate co-association matrices or spectral graphs do not cause out-of-memory (OOM) crashes.

### 2. Algorithmic Vectorization
- Replace native Python loops over $N$ or $D$ with batched NumPy/PyTorch broadcast operations or Numba `@njit(parallel=True)` kernels.
- Ensure sparse matrix operations (`scipy.sparse.csr_matrix`) are used when adjacency or co-association matrices have high sparsity ($> 90\%$).

### 3. Empirical Scaling Benchmark
- Run extreme-scale benchmarking scripts (e.g. `python -m experiments.exp5_extreme_scale.run`).
- Verify that scaling behavior matches asymptotic targets:
  - ASPP projection runtime scales at $\mathcal{O}(N \cdot m)$ with $m \ll N$ anchors rather than $\mathcal{O}(N^3)$.
  - Peak memory remains bounded under configured hardware limits (e.g. $\le 16$ GB RAM).
