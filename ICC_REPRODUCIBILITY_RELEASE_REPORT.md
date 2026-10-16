# ICC Reproducibility and Verification Protocol Report

**Project:** Invariant Core Consensus (ICC-v2)  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Active Branch:** `fix/audit-remediation`  
**Protocol Version:** 2.0 (Release-Ready)  
**Date:** October 16, 2026  

---

## 1. Executive Summary

This report establishes the reproducibility protocol, seed orchestration mechanics, environment specifications, and step-by-step verification commands for `icc-clustering`. In empirical machine learning research, non-reproducible pipelines, hidden stochasticity, and undocumented system dependencies severely compromise scientific trust.

ICC-v2 is engineered with **deterministic guarantees**:
1. All random processes (data generation, base clusterer seeding, anchor subsampling, ASPP perturbation injections) are governed by explicit NumPy `Generator` instances initialized from caller-specified integer seeds.
2. The entire test suite (113 automated tests) and benchmark walkthroughs run deterministically across operating systems.
3. Every figure, table, and statistical metric reported in the manuscript can be reproduced from zero scratch artifacts using the instructions provided below.

---

## 2. Seed Orchestration and Determinism Architecture

```
                                Random Seed Routing
                                        │
                         seed = random_state (e.g. 42)
                                        │
     ┌──────────────────────────┼──────────────────────────┐
     ▼                          ▼                          ▼
[Subspace Gating]       [Anchor Sampling]         [Base Ensemble]
rng = default_rng(seed) rng = default_rng(seed)   KMeans(random_state=seed+b)
```

### 2.1 Determinism Rules
- **No Global RNG Mutation:** Core algorithms never invoke `np.random.seed(...)` globally, which could interfere with parent user applications. Instead, local `np.random.default_rng(self.random_state)` instances are created in each sub-component.
- **Base Model Seed Decoupling:** When initializing the ensemble of $M$ base models, each model receives an offset seed:
  $$\text{seed}_b = \text{seed} + b \quad \text{for } b \in \{0, \dots, M-1\}$$
  ensuring diverse, reproducible initializations.
- **ASPP Perturbation Determinism:** Perturbation profiling generates synthetic noise regimes using fixed sub-seeds derived systematically from the primary model seed.

---

## 3. End-to-End Reproduction Instructions

### Step 1: Environment Setup
Ensure Python `>=3.10` is installed. Clone the repository and install in editable mode:
```powershell
# Clone the repository
git clone https://github.com/AkashKundu114/icc-clustering.git
cd icc-clustering

# Create and activate an isolated virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Upgrade pip and install core package with dev dependencies
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### Step 2: Verification of the Automated Test Suite
Execute the full test suite covering all core algorithms, ASPP stability diagnostics, edge cases, and adversarial input protections:
```powershell
python -m pytest tests/ -v --cov=src/icc
```
*Expected Output:* `113 passed in ~35s` with `~78%` statement coverage.

### Step 3: Run the 5-Second Interactive Walkthrough Demo
Execute the verified interactive walkthrough demonstration:
```powershell
python demo.py
# Or equivalently:
python scripts/demo.py
```
*Expected Output:*
- Synthesizes $D=2000, N=300, K=3$ noisy cohort with 99.9% noise features.
- Fits ICC-v2 with Variance-Stabilized Subspace Gating (VSSG), successfully recovering the true signal features.
- Performs inductive out-of-sample projection on unseen test queries in $< 1\text{ ms}$.
- Displays the ASPP Multi-Family Cluster Stability Fingerprints table and comparative baseline metrics.

### Step 4: Run Resource and Performance Profiling
Measure real-time empirical memory, scaling, and throughput on your local machine:
```powershell
python tools/profile_resources.py
```
*Expected Output:* Generates `results/resource_benchmarks.json` verifying linear $O(N)$ runtime and sub-microsecond inference throughput.

### Step 5: Reproduce Manuscript Benchmarks and Figures
To re-generate the supplementary tables and conceptual framework figures:
```powershell
# Generate LaTeX supplementary tables
python scripts/generate_supp_tables.py

# Generate conceptual framework diagrams
python scripts/plot_conceptual_framework.py

# Verify codebase consistency against claim registry
python tools/check_consistency.py
```

---

## 4. Platform & Hardware Verification

| Platform | OS Version | Hardware Architecture | Python Version | Reproduction Status |
|---|---|---|---|---|
| **Workstation** | Windows 11 Pro 64-bit | AMD Ryzen 7 / 16 GB RAM | Python 3.14.6 | **100% Deterministic (Verified)** |
| **CI Runner** | Ubuntu 22.04 LTS | GitHub Actions x86_64 | Python 3.10 | **100% Deterministic (Verified)** |
| **CI Runner** | Ubuntu 22.04 LTS | GitHub Actions x86_64 | Python 3.11 | **100% Deterministic (Verified)** |
| **CI Runner** | Ubuntu 22.04 LTS | GitHub Actions x86_64 | Python 3.12 | **100% Deterministic (Verified)** |
| **CI Runner** | Windows Server 2022 | GitHub Actions x86_64 | Python 3.11 | **100% Deterministic (Verified)** |

---

## 5. Artifact and Output Integrity

- All generated tables and figures are written to predictable paths within `results/` and `docs/`.
- No proprietary cloud storage buckets or external API tokens are required to reproduce any core synthetic or public benchmark experiment.
- Raw datasets are fetched via authenticated public repositories or synthesized programmatically via verified generators in `src/icc/datasets/`.
