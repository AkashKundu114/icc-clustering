# Inductive Consensus Clustering (`icc`): Research Documentation

**Canonical Manuscript Title:** Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes  
**Target Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI), document class `sn-jnl.cls` (`sn-mathphys-num.bst`)  
**Canonical Release Version:** v2.2.0  
**Repository Packages:** `icc` (v2.2.0) and `cicc` (Conformal Inductive Consensus Clustering)  

This directory serves as the centralized research documentation portal for **Feature-Gated Bipartite Graph Ensembles (ICC-v2)**, an audited, mathematically certified consensus clustering framework designed for noisy, high-dimensional manifolds ($D \gg N$).

---

## 1. Documentation Roadmap

The documentation is organized into focused, self-contained reference modules:

- [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md): **Master Reproduction Guide.** Detailed mapping of all 21 manuscript tables and 10 figures to their source datasets, empirical registries, and generating commands. Includes the unified `python scripts/reproduce.py` CLI instructions.
- [`THEORETICAL_FOUNDATIONS.md`](THEORETICAL_FOUNDATIONS.md): **Mathematical Foundations & Proofs.** Complete mathematical proofs for Proposition 1 (Sarle Bimodality null bound $BC \le 5/9$), Proposition 2 (Linear Contingency Determinacy Identity in $\mathcal{O}(M^2 N + M^2 K^2)$), Theorem 1 (Inductive Assignment Convergence), and Theorem 2 (Linear Time Transfer-Cut $\mathcal{O}(N L^2 + L^3)$).
- [`DATA.md`](DATA.md): **Benchmark Dataset Specifications.** Comprehensive metadata, sample sizes ($N$), feature counts ($D$), cluster counts ($K$), cryptographic SHA-256 hashes, and download sources for all 13 benchmark datasets.
- [`api.md`](api.md): **Python API Reference.** Complete API documentation for the core solvers (`ICC`, `ICCv2`, `GAC`), baseline algorithms, dataset loaders, diagnostics, and conformal projection utilities.
- [`ENV.md`](ENV.md): **Environment & Dependency Specifications.** Step-by-step instructions for setting up the Python environment, managing optional dependencies (`deep`, `bio`), and ensuring BLAS determinism.
- [`literature/papers.md`](literature/papers.md): **Literature & Comparative Baselines.** 20-paper annotated research matrix and detailed mathematical review of 11 comparative baseline solvers.

---

## 2. Algorithmic Architecture & Traceability

All theoretical formulations map directly to production modules in [`src/icc/`](../src/icc/) and [`src/cicc/`](../src/cicc/):

| Documentation Section | Mathematical Formulation | Source Code Implementation | Test Suite Module |
| :--- | :--- | :--- | :--- |
| **Feature Gating (BGSS)** | Proposition 1, Sarle $BC$ | [`src/icc/consensus_v2.py`](../src/icc/consensus_v2.py) | [`tests/test_consensus_v2.py`](../tests/test_consensus_v2.py) |
| **Contingency Determinacy** | Proposition 2, Identity | [`src/icc/consensus_v2.py`](../src/icc/consensus_v2.py) | [`tests/test_consensus_v2.py`](../tests/test_consensus_v2.py) |
| **Bipartite Transfer-Cut** | Section 4, Theorem 2 | [`src/icc/consensus_v2.py`](../src/icc/consensus_v2.py) | [`tests/test_consensus_v2.py`](../tests/test_consensus_v2.py) |
| **Stability Profiling (ASPP)** | Definition 3, Perturbations | [`src/icc/aspp.py`](../src/icc/aspp.py) | [`tests/test_aspp.py`](../tests/test_aspp.py) |
| **Inductive Projection** | Theorem 1, $\mathcal{O}(L)$ Query | [`src/icc/consensus_v2.py`](../src/icc/consensus_v2.py) | [`tests/test_inductive_projection.py`](../tests/test_inductive_projection.py) |
| **Conformal Calibration** | Finite-Sample $(1 - \alpha)$ Sets | [`src/cicc/conformal.py`](../src/cicc/conformal.py) | [`tests/test_cicc.py`](../tests/test_cicc.py) |
| **Target-Decoy FDR Screening** | Mirror Statistics $W_d$ | [`src/cicc/decoy.py`](../src/cicc/decoy.py) | [`tests/test_cicc.py`](../tests/test_cicc.py) |
| **Incremental Memory Routing** | Novelty Triage | [`src/cicc/memory.py`](../src/cicc/memory.py) | [`tests/test_cicc.py`](../tests/test_cicc.py) |
| **11 Baseline Algorithms** | Baseline Matrix | [`src/icc/baselines/`](../src/icc/baselines/) | [`tests/test_baselines.py`](../tests/test_baselines.py) |
| **Benchmark Datasets** | 13 Benchmark Cohorts | [`src/icc/datasets/`](../src/icc/datasets/) | [`tests/test_datasets.py`](../tests/test_datasets.py) |

---

## 3. Empirical Findings (Single Source of Truth)

All numerical statements are derived programmatically from `results/stats.json` and compiled into `paper/numbers.tex`:

1. **High-Dimensional Biological Regimes ($D/N > 20$, 6 Genomics Cohorts):**  
   ICC-v2 achieves **Rank #1 performance** with an average rank of **2.17** and Mean ARI = **0.217**, significantly outperforming standard dense consensus (ARI = 0.037), DEC (ARI = 0.045), and unguided K-Means (ARI = 0.056).
   - **Golub Leukemia ($N=72, D=7{,}129, K=2$):** Active features gated down to 1,069 informative dimensions; ARI = **0.600 $\pm$ 0.367**, capturing 54.0% of verified oncogenic markers label-free.
   - **Khan SRBCT ($N=83, D=2{,}308, K=4$):** ARI = **0.546 $\pm$ 0.102**, accurately separating four pediatric malignancies.
   - **Memory Scaling:** 99.6% reduction in co-association matrix memory footprint and 97.4% reduction in peak RAM usage over standard quadratic consensus.

2. **Omnibus Multi-Domain Benchmark Suite (13 Datasets, 11 Solvers, 3,000 Model Fits):**  
   Across all 13 heterogeneous benchmark datasets, ICC-v2 achieves a Grand Mean ARI of **0.152** (Grand Median ARI of **0.055**, overall average rank of **5.62** of 11). An omnibus Friedman rank sum test yields $p = 0.40$ with a Nemenyi critical difference $\text{CD} = 4.62$, establishing that no single algorithm unconditionally dominates across heterogeneous non-high-dimensional domains.
