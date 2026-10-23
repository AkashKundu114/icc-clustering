# Experimental Suites and Protocols

This directory houses the executable experiment pipelines, baseline comparators, and audit controls for Inductive Consensus Clustering.

## Pre-Registration Protocol
All experimental hypotheses, seed reservations, and evaluation metrics follow the frozen pre-registration protocol documented in [`PRE_REGISTRATION_v1.0.md`](./PRE_REGISTRATION_v1.0.md).

## Experiments Breakdown

### 1. Experiment 0: Noise Falsification (`exp0_falsification`)
- **Hypothesis (H1):** Consensus clustering degrades catastrophically beyond critical noise boundaries without adaptive spectral projection.
- **Entrypoint:** `python -m experiments.exp0_falsification.run`

### 2. Experiment 1: Out-of-Sample Inductive Generalization (`exp1_generalization`)
- **Hypothesis (H2):** Nyström-extended spectral embeddings generalize inductively to unseen test samples with sub-linear error decay.
- **Entrypoint:** `python -m experiments.exp1_generalization.run`

### 3. Experiment 2: Component Ablation (`exp2_ablation`)
- **Hypothesis (H3):** Each component of ASPP (anchor-fidelity gating, variance stabilization, dual-mode consensus) contributes measurably to downstream stability.
- **Entrypoint:** `python -m experiments.exp2_ablation.run`

### 4. Experiment 3: Real-World Multi-Dataset Benchmarks (`exp3_real_world_benchmarks`)
- **Scope:** Empirical evaluation across 13 diverse open-access benchmarks against 10 competing classical and deep clustering baselines.
- **Entrypoint:** `python -m experiments.exp3_real_world_benchmarks.run`

### 5. Experiment 4: Scalability & Sensitivity (`exp4_scalability_and_sensitivity`)
- **Scope:** Parameter sensitivity sweeps over pool size $H \in [10, 200]$, cluster count $K$, missingness rates, and scaling across dimensions $D \in [10^2, 10^5]$.
- **Entrypoint:** `python -m experiments.exp4_scalability_and_sensitivity.run`

### 6. Experiment 5: Extreme-Scale Benchmarking (`exp5_extreme_scale`)
- **Scope:** Stress-testing throughput, GPU memory footprint, and time-to-solution at $N = 100{,}000$ and $D = 50{,}000$.
- **Entrypoint:** `python -m experiments.exp5_extreme_scale.run`

## Running Experiments
To execute all suites sequentially and regenerate outputs:
```bash
python -m experiments.exp0_falsification.run
python -m experiments.exp1_generalization.run
python -m experiments.exp2_ablation.run
python -m experiments.exp3_real_world_benchmarks.run
python -m experiments.exp4_scalability_and_sensitivity.run
python -m experiments.exp5_extreme_scale.run
```
Output data files and figure renders are saved into local subdirectories (`experiments/*/data/`, `experiments/*/figures/`) and excluded from Git tracking.
