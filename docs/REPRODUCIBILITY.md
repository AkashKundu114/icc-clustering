# Inductive Consensus Clustering (ICC-v2): Reproducibility Guide

This guide provides explicit, end-to-end instructions for reproducing all results, benchmarks, and figures in the ICC-v2 paper from a clean environment.

---

## 1. Supported Environments & Hardware Requirements

| Parameter | Specification | Notes |
| :--- | :--- | :--- |
| **Python Version** | Python $\ge 3.10$ (tested on 3.10, 3.11, 3.12, 3.14) | Standard CPython distribution |
| **Operating Systems** | Windows 10/11 (64-bit), Ubuntu Linux $\ge 20.04$, macOS $\ge 12.0$ | Platform-agnostic (POSIX & Windows paths supported) |
| **Minimum Hardware** | 4-Core CPU, 8 GB RAM, 5 GB free disk space | Sufficient for all experiments except Exp 5 extreme scaling |
| **Recommended Hardware**| 8-Core CPU, 16 GB RAM, 20 GB free disk space | Enables parallel multi-seed benchmark execution |
| **Optional GPU** | NVIDIA CUDA $\ge 11.8$ (for DEC deep baseline) | Not required for core ICC-v2 algorithm or classical baselines |

---

## 2. Clean Environment Setup

### Step 1: Create an Isolated Virtual Environment
```bash
# Clone the repository
git clone https://github.com/AkashKundu114/icc-clustering.git
cd icc-clustering

# Create and activate virtual environment
python -m venv .venv

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# On Linux / macOS (bash):
source .venv/bin/activate
```

### Step 2: Install Package & Dependencies
```bash
# Upgrade build tools
pip install --upgrade pip setuptools wheel

# Option A: Core Package Only (sufficient for ICC-v2, classical & consensus baselines)
pip install -e .

# Option B: Development & Testing (adds pytest, ruff, black)
pip install -e ".[dev]"

# Option C: Full Evaluation Suite (adds deep learning and single-cell dependencies)
pip install -e ".[all]"
```

---

## 3. Fast Verification & Smoke Tests

Verify installation integrity in under 60 seconds:

```bash
# 1. Run interactive synthetic demo (~5s)
python demo.py

# 2. Run automated test suite (114 passing tests, ~42s)
python -m pytest tests/ -v

# 3. Verify statistical consistency and macro definitions
python tools/check_consistency.py
```

Expected Output:
```
============================== 114 passed in 41.49s ==============================
[*] Running ICC Consistency & Traceability Audit...
[+] Verified 22 macros against raw results. Errors: 0
[+] Pre-registered datasets in registry: 21
[+] SUCCESS: All consistency and traceability gates PASSED.
```

---

## 4. Experiment Reproduction Workflows

All experiments are structured to support both:
1. **Instant Plot Generation:** Regenerate publication-quality figures directly from committed, hash-verified CSV results in `results/`.
2. **Full Re-Execution:** Re-run models from scratch across specified random seeds.

### Experiment 0: Consensus Stability Falsification (Figures 1–8)
```bash
# Instant plot reproduction:
python experiments/exp0_falsification/run_all.py --reproduce-plots

# Full re-execution from scratch:
python experiments/exp0_falsification/run_all.py --run-full
```
- **Runtime:** Instant (~2s); Full run (~4 min).
- **Output:** Figures saved to `experiments/exp0_falsification/figures/` and metrics saved to `results/exp0_falsification/`.

### Experiment 1: Inductive Generalization (Figures 9, 10, 10b, 10c)
```bash
# Re-run full inductive generalization sweep across 10 trials:
python experiments/exp1_generalization/run_exp1.py --run-full

# Re-run multi-classifier sweep (RF, SVM, MLP):
python experiments/exp1_generalization/run_exp1.py --run-multiclassifier
```
- **Runtime:** ~6 min across 10 random seeds (`42, 100..109`).
- **Output:** `results/exp1_generalization/exp1_generalization_results.csv`.

### Experiment 2: Architectural Component Ablations (Figures 11–13, 22a–c)
```bash
# Instant plot reproduction:
python experiments/exp2_ablation/run_exp2.py --reproduce-plots

# Full re-execution:
python experiments/exp2_ablation/run_exp2.py --run-full
```
- **Runtime:** Instant (~3s); Full run (~8 min).
- **Output:** Saliency ranking CSVs and component ablation comparisons in `results/exp2_ablation/`.

### Experiment 3: Real-World 13-Dataset Benchmarks (Figures 14–17, Tables 1–3)
```bash
# Instant plot and LaTeX table generation:
python experiments/exp3_real_world_benchmarks/run_exp3.py --reproduce-plots
python scripts/generate_supp_tables.py

# Full re-run across 10 seeds (1,430 model executions):
python experiments/exp3_real_world_benchmarks/run_exp3.py --run-full --n-seeds 10
```
- **Runtime:** Instant (~5s); Full re-run (~45 min on 8-core CPU).
- **Output:** `results/exp3_real_world_benchmarks/exp3_1_benchmark_matrix_v2.csv` and LaTeX tables in `paper/gen/`.

### Experiment 4: Scalability & Anchor Fidelity (Figures 18–21, 23, 24)
```bash
python experiments/exp4_scalability_and_sensitivity/run_exp4.py --reproduce-plots
```
- **Runtime:** Instant (~3s); Full run (~12 min).
- **Output:** Scaling curves and anchor fidelity measurements in `results/exp4_scalability_and_sensitivity/`.

### Experiment 5: Extreme Asymptotic Scaling (Figure 26)
```bash
python experiments/exp5_extreme_scale/run_exp5.py --reproduce-plots
```
- **Runtime:** Instant (~2s); Full run requires 32 GB RAM for $N = 1,000,000$.

---

## 5. Security & Data Loading Protocol

To ensure reproducible security when executing third-party benchmarks:
1. **Zero Deserialization Vulnerabilities:** All `.npz` caches are loaded with `allow_pickle=False`. Untrusted pickled Python objects are strictly rejected.
2. **Deterministic Seed Routing:** Base clustering, feature subspace sampling, and anchor subsampling use explicit seed offsets:
   $$\text{Seed}_h = \text{base\_seed} + 100 \cdot h$$
3. **No Automatic Network Downloads in Production:** Pre-cached datasets in `data/cache/` are verified against SHA-256 integrity hashes.
