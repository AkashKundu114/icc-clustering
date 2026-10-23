# Loop: Performance Profiling, Vectorization & Scaling Loop

Use this loop to isolate runtime and memory bottlenecks, optimize computational hotspots, and verify empirical scaling behavior without sacrificing mathematical accuracy.

---

## Operating Budget & Setup
- **Maximum Iterations:** 4 iterations per run.
- **Assigned Subagent Personas:**
  - `Profiler (roo_debugger)`: Runs runtime benchmarks, line-profiler, and memory tracking.
  - `Optimization Engineer (roo_coder)`: Applies vectorization, caching, Numba JIT, or sparse algebra.
  - `Numerical Equivalence Auditor (roo_reviewer)`: Verifies that optimizations produce bitwise or $\epsilon$-identical mathematical outputs.

---

## Iteration Protocol

### 1. Bottleneck Profiling
- Profile the target module under realistic dimension/sample sizes:
  ```python
  import cProfile, pstats
  profiler = cProfile.Profile()
  profiler.runcall(target_function, *args)
  stats = pstats.Stats(profiler).sort_stats('cumtime')
  stats.print_stats(15)
  ```
- Identify the single function consuming the highest cumulative runtime or host memory.

### 2. Surgical Optimization
Apply standard high-performance scientific Python patterns:
- **Loop Elimination:** Replace nested Python loops with NumPy vectorization or PyTorch tensor broadcasting.
- **Just-In-Time Compilation:** Annotate pure numerical kernels with `@numba.njit(parallel=True, fastmath=True)`.
- **Memory Allocation Reduction:** Use in-place operations (`out=` parameters) to prevent allocating large temporary matrices.
- **Sparse Representations:** Transition large similarity or co-association matrices to `scipy.sparse.csr_matrix` when sparsity $> 85\%$.

### 3. Numerical Equivalence Verification
- Run strict assertion checks comparing output before and after optimization:
  ```python
  assert np.allclose(output_optimized, output_baseline, rtol=1e-5, atol=1e-7)
  ```
- **Fail condition:** Any discrepancy beyond floating-point precision ($> 1e-5$) causes immediate rejection of the optimization.

### 4. Benchmark Speedup Measurement
- Measure speedup factor ($S = T_{\text{baseline}} / T_{\text{optimized}}$) and peak RAM reduction.
- Verify that unit and integration tests (`pytest tests/`) continue to pass 100%.

### 5. Record & Diff Audit
Log the profiling traces, speedup multipliers, and diff in `prompts/antigravity/logs/`.
