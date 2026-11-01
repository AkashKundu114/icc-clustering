# Autonomous Research Audit: Initial Repository & Hardware Inspection

**Document Reference:** `research_audit/overnight/INITIAL_AUDIT.md`  
**Execution Branch:** `research/overnight-experiments`  
**Timestamp:** 2026-11-01T00:33:00+05:30  
**Audit Lead:** Lead Experiment Orchestration & Scientific Verification Agent  

---

## 1. Hardware, System & Runtime Environment Verification

A comprehensive hardware and runtime verification was executed:

| Resource / Parameter | Specification / Measured State | Verification Status |
| :--- | :--- | :---: |
| **Host Operating System** | Windows 11 Enterprise (Build 10.0.26300) | Verified |
| **Processor (CPU)** | AMD Ryzen 9 8940HX (16 Cores, 32 Threads) | Verified |
| **Graphics Processing Unit** | NVIDIA GeForce RTX 5060 Laptop GPU (8 GB VRAM, Compute 12.0) | Verified |
| **CUDA Driver & PyTorch** | PyTorch `2.16.0.dev20261017+cu134`, CUDA Available = `True` | Verified |
| **GPU Memory Allocation** | 0.0 MB Allocated / 0.0 MB Reserved (Clean State) | Verified |
| **System Memory (RAM)** | Total: 15.21 GB, Available: 3.85 GB (74.7% in use) | **Constrained** |
| **Non-Volatile Storage (SSD)** | Drive D: Total 300.00 GB, Free 79.45 GB | Verified |
| **Active Python Environment** | Python 3.14.6 (64-bit AMD64) | Verified |

### Safety Constraints Enacted:
Because available RAM is measured at **3.85 GB**, aggressive multiprocessing or multi-threaded matrix operations will trigger Windows paging file thrashing or Out-of-Memory (OOM) fatal crashes. Therefore:
1. **Strict Sequential Single-Worker Execution:** Worker concurrency is capped at `n_jobs = 1` for all dataset loading and clustering loops.
2. **Immediate Checkpoint Flushing:** Every completed seed and model configuration is persisted to disk immediately before moving to the next.
3. **Explicit Garbage Collection:** `gc.collect()` and `torch.cuda.empty_cache()` are enforced between experimental runs.

---

## 2. Repository Structure & Existing Experiment Inventory

The repository is structured into two core package namespaces and a modular experiment suite:

```
icc-clustering/
├── src/
│   ├── icc/                  # Core Invariant Core Consensus library
│   │   ├── core.py           # Base consensus and core selection
│   │   ├── consensus_v2.py   # InvariantCoreConsensusV2 (BGSS + GAC)
│   │   ├── autok.py          # ICC-AutoK model order selection
│   │   ├── aspp.py           # Adaptive Subspace Perturbation Projection
│   │   ├── metrics.py        # Clustering metrics (ARI, NMI, AMI, Silhouette, DB, CH)
│   │   ├── datasets/         # Ingestion modules for genomics, scRNA, audio, image, text
│   │   └── baselines/        # Classical, consensus, deep, anchor, density, sparse baselines
│   └── cicc/                 # Conformal Invariant Core Clustering extensions
├── configs/
│   ├── datasets.yaml         # Dataset registry and normalization profiles
│   └── baselines.yaml        # Baseline algorithm configurations and execution paths
├── data/
│   └── registry.yaml         # Cryptographic dataset manifest with SHA-256 checksums
├── experiments/
│   ├── exp0_falsification/   # Null-hypothesis and permutation falsification
│   ├── exp1_generalization/  # Cross-domain multi-dataset generalization
│   ├── exp2_ablation/        # Component ablation (anchors, core, gating)
│   ├── exp3_real_world/      # Benchmark matrix vs classical baselines
│   ├── exp6_cohort_expansion/# 6 Expanded oncology cohorts (DLBCL, Breast, Su, Novartis, GCM, Endometrium)
│   ├── exp7_modern_baselines/# Modern baselines (Sparse K-Means, HDBSCAN, Leiden, GMM-BIC)
│   └── exp8_unknown_k/       # Unsupervised model order selection (ICC-AutoK vs baselines)
├── results/
│   ├── passF/                # Frozen historical 30-seed benchmark results
│   ├── cohort_independence/  # Prior forensic cohort independence audit outputs
│   └── overnight/            # TARGET DIRECTORY FOR ALL NEW OVERNIGHT EXPERIMENTS
└── research_audit/
    ├── cohort_independence/  # Prior cohort independence audit documentation
    └── overnight/            # TARGET DIRECTORY FOR OVERNIGHT RESEARCH AUDITS
```

---

## 3. Dataset Audit & Candidate Inventory

The repository references up to 29 dataset representations. However, our prior forensic audit established:
1. **The "21-Dataset Benchmark" Claim is 52.4% Non-Biological:** 11 of the 21 datasets in `e1_extended_benchmarks.csv` were non-genomic controls (acoustic sonar, spoken audio, handwritten digits, text, inertial sensors, etc.).
2. **OpenML Cache Mislabels:** `MagicTelescope` (astrophysics gamma-ray shower simulation) was mislabeled as `breast_cancer_genomic`; `Jungle Chess` endgame was mislabeled as `gisette`.
3. **Bit-for-Bit Duplicate:** `glioma` in e1 is a 100% duplicate copy of Pomeroy `cns` (`0e449bf...`).
4. **Composite Overlap:** Ramaswamy Global Cancer Map (`gcm`, cached as `lung_cancer`) ingested 61 of 72 Golub Leukemia patients and 8 Pomeroy CNS patients.
5. **Eligible Confirmed Independent Biological Cohorts:** Exactly **10 confirmed Category A bulk oncology cohorts** (`colon`, `srbct`, `cns`, `leukemia`, `prostate`, `ovarian`, `dlbcl`, `breast`, `su2001`, `endometrium`), plus `gli` (Nutt 2003) and `zheng68k` (10x PBMC single-cell).

---

## 4. Identified Gaps in Scientific Evidence

Prior to this overnight run, four critical scientific gaps remained unaddressed:
- **Gap 1: Limited Cohort Coverage:** Benchmark claims were based heavily on 6 early microarrays from 1999–2002.
- **Gap 2: The Two-Cohort Effect:** Performance improvements in GAC/BGSS were heavily concentrated in Leukemia ($\Delta\text{ARI} = +0.6428$) and SRBCT ($\Delta\text{ARI} = +0.5240$), attenuating to $+0.0339$ ($p=0.3680$) when both were excluded.
- **Gap 3: Missing Contemporary Baselines:** Comparisons lacked Sparse K-Means (Witten & Tibshirani), HDBSCAN* (Campello et al.), Leiden SNN (Traag et al.), and GMM with BIC/ICL.
- **Gap 4: Absence of Unknown-K Evaluation:** ICC had never been rigorously benchmarked in an unsupervised regime where true $K$ is hidden.

---

## 5. Execution Plan & Overnight Resource Allocation

The overnight execution window is budgeted across 6 sequential milestones:

```
+---------------------------------------------------------------------------------------+
|                              OVERNIGHT EXECUTION TIMELINE                             |
+---------------------------------------------------------------------------------------+
| 00:00 - 00:30 : Milestone 1 - Subagent Audits, Manifest & Execution Infrastructure    |
| 00:30 - 03:00 : Milestone 2 - Primary ICC Benchmark across Independent Cohorts (P0)   |
| 03:00 - 05:00 : Milestone 3 - BGSS Robustness, Matched Random Gating & Ablations (P1) |
| 05:00 - 07:00 : Milestone 4 - Modern Classical & Statistical Baselines (P1)           |
| 07:00 - 08:45 : Milestone 5 - Unknown-K Evaluation (Synthetic Grid + Real Biological) |
| 08:45 - 09:30 : Milestone 6 - Synthetic Falsification & Non-Convex Stress Tests (P2) |
| 09:30 - 10:00 : Milestone 7 - Result Validation, Meta-Analysis & Final Report (P0)    |
+---------------------------------------------------------------------------------------+
```

---

## 6. Execution Manifest & Output Targets

All outputs are strictly isolated into:
- Results: `results/overnight/`
  - `EXECUTION_MANIFEST.csv`
  - `dataset_manifest.csv`
  - `primary_icc/primary_icc_results.csv`
  - `bgss/bgss_ablation_results.csv`
  - `baselines/modern_baselines_results.csv`
  - `unknown_k/unknown_k_synthetic_results.csv` & `unknown_k_real_results.csv`
  - `synthetic/synthetic_stress_results.csv`
- Documentation: `research_audit/overnight/`
  - `INITIAL_AUDIT.md` (This document)
  - `DATASET_AUDIT.md` & `DATASET_MANIFEST.md`
  - `BGSS_AUDIT.md` & `BGSS_RESULTS.md`
  - `BASELINE_AUDIT.md` & `BASELINE_RESULTS.md`
  - `UNKNOWN_K_DESIGN.md` & `UNKNOWN_K_RESULTS.md`
  - `EXECUTION_PLAN.md`
  - `FINAL_REPORT.md`
