# Inductive Consensus Clustering (ICC-v2): Documentation & Research Dossier

This directory serves as the centralized research documentation portal for **Inductive Consensus Clustering (ICC-v2)** (also designated **Invariant Core Consensus**), an audited, mathematically certified consensus clustering framework designed for noisy, ultra-high-dimensional manifolds ($D \gg N$).

---

## 1. Project Title Evolution & Academic Lineage

This research was conducted as a final-year engineering capstone project (`CSE_PROJECT_68`) at the Department of Computer Science and Engineering, under the guidance of **Prof. Kalyan Kumar Das**.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   PROJECT TITLE EVOLUTION                                        │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
  [ 1. University Course / Registered Project Title (Initial Allotment) ]
  • Title: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data"
  • Focus: Exploratory heuristics utilizing sample stability in noisy high-dimensional clustering.
  • Scope: Formulating base clustering diversity and sample-level stability weighting.

                                            │
                                            ▼ (Theoretical & Algorithmic Maturation)
                                            │

  [ 2. Evolved Scientific Manuscript Title (Target IEEE Publication) ]
  • Title: "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation
            for High-Dimensional Noise Regimes"
  • Venues: IEEE TKDE / IEEE TNNLS / IEEE TPAMI / ICDE
  • Focus: Transition from transductive heuristics to an inductive, geometry-calibrated framework.
  • Breakthroughs:
    1. Exact Linear-Memory Determinacy Identity via contingency tables in O(M^2 N + M^2 K^2).
    2. Finite-sample Sarle Bimodality Coefficient bound (BC <= 5/9) and zero-inflation boundary.
    3. Reduced Bipartite Spectral Transfer-Cut consensus scaling in O(N L^2 + L^3).
    4. Inductive out-of-sample projection bounds and Anchor-Space Perturbation Profiling (ASPP).
```

---

## 2. Documentation Architecture & Master Directory Map

The documentation hierarchy is structured into five distinct academic and technical modules:

```
docs/
├── README.md                            # Master navigation index and documentation roadmap (this file)
├── THEORETICAL_FOUNDATIONS.md          # Formal mathematical definitions, propositions, proofs, and complexity
├── literature/                          # Research landscape, prior art taxonomies, and paper dossiers
│   ├── papers.md                        # 20-paper annotated matrix, 10 baselines comparison, BibTeX records
│   ├── prep.md                          # Comprehensive research preparation dossier & mentor directive realization
│   ├── literature_review.md             # Canonical alias for papers.md
│   └── research_preparation.md          # Canonical alias for prep.md
├── proposal/                            # Formal research proposal and scientific blueprint
│   ├── IEEE_Research_Proposal_Inductive_Consensus_Clustering.md # Definitive proposal for IEEE TKDE / ICDE
│   ├── IEEE_Research_Proposal_Cluster_Stability.md             # Preserved alias / initial title markdown
│   ├── Inductive_Consensus_Clustering_IEEE_Research_Proposal.pdf # Proposal PDF under evolved title
│   └── Cluster_Stability_IEEE_Research_Proposal.pdf             # Archived initial proposal PDF
├── audit_reports/                       # 12-stage independent adversarial research audit dossier
│   ├── README.md                        # Audit index and overview of verification milestones
│   ├── 00_executive_review.md           # Executive summary and prioritized audit milestones
│   ├── 01_repository_inventory.md       # Comprehensive inventory of code, datasets, and artifacts
│   ├── 02_claim_evidence_matrix.md      # Claim-to-evidence mapping for all paper and repo assertions
│   ├── 03_mathematical_audit.md         # Proof audits (Sarle BC bound, Transfer-Cut, anchor bounds)
│   ├── 04_algorithm_code_traceability.md # LaTeX-to-NumPy code traceability audit
│   ├── 05_novelty_and_related_work.md   # Prior art taxonomy and citation corrections
│   ├── 06_experiment_audit.md           # Empirical benchmark re-computations and pool-size findings
│   ├── 07_red_flag_register.md          # Empirical anomaly tracking and verification log
│   ├── 08_experiment_plan.md            # Experimental plans for controls (A2), embedding checks (A3)
│   ├── 09_remediation_roadmap.md        # Chronological execution timeline and claim calibrations
│   ├── 10_final_reviewer_report.md      # Adversarial reviewer report evaluating TKDE defensibility
│   ├── 11_verification_log.md           # Hash-verified execution records of test sweeps
│   └── remediation_reports/             # Author technical defense notes (01 through 12)
└── figures/                             # Conceptual schematics and high-dimensional manifold illustrations
    └── high_d_noisy_manifold_concept.jpg # Distance concentration and geometric ridge distortion
```

---

## 3. Core Research Modules & Reading Order

For reviewers, collaborators, and students reading this repository, the recommended navigation path is:

### Step 1: Scientific Vision & Research Proposal
* Read [`proposal/IEEE_Research_Proposal_Inductive_Consensus_Clustering.md`](./proposal/IEEE_Research_Proposal_Inductive_Consensus_Clustering.md) (or [`proposal/IEEE_Research_Proposal_Cluster_Stability.md`](./proposal/IEEE_Research_Proposal_Cluster_Stability.md)) to understand the fundamental unsolved problem, the **"Hallucinated Stability" trap**, and how ICC-v2 was formulated to fulfill Prof. Kalyan Kumar Das's research directives (Points 1, 2, and 5).

### Step 2: Prior Art, Literature & Baselines
* Read [`literature/papers.md`](./literature/papers.md) (or [`literature/literature_review.md`](./literature/literature_review.md)) for an exhaustive 20-paper annotated literature matrix, the comprehensive comparative analysis of the **10 baseline algorithms** (K-Means, Ward, Spectral, SEC, CSPA, MCLA, LWEA, LWGP, FastMICE, DEC), and the formal prior art taxonomy (Categories A through D).
* Read [`literature/prep.md`](./literature/prep.md) (or [`literature/research_preparation.md`](./literature/research_preparation.md)) to trace the evolution of the research preparation, methodological decisions, and team role division.

### Step 3: Mathematical Formulation & Proofs
* Read [`THEORETICAL_FOUNDATIONS.md`](./THEORETICAL_FOUNDATIONS.md) for formal proofs of:
  - **Proposition 1:** Finite-sample Sarle Bimodality Coefficient null bound ($BC \le 5/9$) rejecting continuous unimodal distractor noise.
  - **Remark 1:** The zero-inflation boundary where point-mass sparsity mimics bimodality.
  - **Proposition 2:** Exact Linear-Memory Determinacy Identity via cross-model contingency tables in $\mathcal{O}(M^2 N + M^2 K^2)$ time and $\mathcal{O}(N + M K)$ memory.
  - **Theorems 1 & 2:** Inductive assignment convergence and strictly linear asymptotic time complexity $\mathcal{O}(N)$.
  - **ASPP Theory:** Scalable Anchor-Space Perturbation Profiling across 5 perturbation operators.

### Step 4: Adversarial Audit & Empirical Verification
* Read [`audit_reports/README.md`](./audit_reports/README.md) and [`audit_reports/06_experiment_audit.md`](./audit_reports/06_experiment_audit.md) to review the empirical findings from 1,430 benchmark executions, pool sensitivity curves (E3), label-free selector negative results (E3b), missing-data sweeps (E5), and per-process memory scaling (E6).

---

## 4. Algorithmic Architecture & Codebase Traceability

All theoretical formulations and documentation sections map directly to the production implementation in [`src/icc/`](../src/icc/):

| Documentation Section | Mathematical Formulation | Source Code Implementation | Test Verification |
| :--- | :--- | :--- | :--- |
| **VSSG Feature Gating** | Definition 1, Proposition 1 | [`src/icc/consensus_v2.py`](../src/icc/consensus_v2.py) | [`tests/test_consensus_v2.py`](../tests/test_consensus_v2.py) |
| **Exact Linear Determinacy** | Proposition 2 | [`src/icc/consensus_v2.py`](../src/icc/consensus_v2.py) | [`tests/test_consensus_v2.py`](../tests/test_consensus_v2.py) |
| **Bipartite Transfer-Cut** | Section 4, Theorem 2 | [`src/icc/consensus_v2.py`](../src/icc/consensus_v2.py) | [`tests/test_consensus_v2.py`](../tests/test_consensus_v2.py) |
| **ASPP Stability Profiling** | Definition 3 | [`src/icc/aspp.py`](../src/icc/aspp.py) | [`tests/test_aspp.py`](../tests/test_aspp.py) |
| **Inductive Prediction** | Theorem 1 | [`src/icc/consensus_v2.py`](../src/icc/consensus_v2.py) (`predict`) | [`tests/test_inductive_projection.py`](../tests/test_inductive_projection.py) |
| **Conformal Inductive Calibration** | Finite-Sample $(1 - \alpha)$ Sets | [`src/cicc/conformal.py`](../src/cicc/conformal.py) | [`tests/test_cicc.py`](../tests/test_cicc.py) |
| **Target-Decoy FDR Gating** | Mirror Statistics $W_d$ | [`src/cicc/decoy.py`](../src/cicc/decoy.py) | [`tests/test_cicc.py`](../tests/test_cicc.py) |
| **Agent Episodic Memory** | Conformal Triage / Novelty | [`src/cicc/memory.py`](../src/cicc/memory.py) | [`tests/test_cicc.py`](../tests/test_cicc.py) |
| **10 Baseline Algorithms** | Baseline Matrix | [`src/icc/baselines/`](../src/icc/baselines/) | [`tests/test_baselines.py`](../tests/test_baselines.py) |
| **Benchmark Datasets** | Benchmark Matrix | [`src/icc/datasets/`](../src/icc/datasets/) | [`tests/test_datasets.py`](../tests/test_datasets.py) |

---

## 5. Key Empirical Takeaways & Operating Envelope

The rigorous adversarial research audit established the following empirical truths:

1. **Continuous Ultra-High-Dimensional Cancer Assays ($D/N > 20$):**  
   ICC-v2 exhibits **Rank #1 dominance** ($R = 1.50$), achieving major lifts over deep and classical baselines (Leukemia ARI = 0.680 vs. DEC 0.148; SRBCT ARI = 0.538 vs. Std Consensus 0.040).
2. **Sparse Text & Count Manifolds (Zheng68k, 20 Newsgroups):**  
   Hierarchical Ward and DEC outperform ICC-v2. Extreme zero-inflation creates an analytical failure mode for unimodal kurtosis screening (Remark 1).
3. **General Multi-Domain Suite (13 Datasets):**  
   Grand Mean ARI is **0.1599** (mean rank 5.46 of 11). An omnibus Friedman test yields $\chi^2_F = 11.38, p = 0.33$, indicating that across heterogeneous multi-domain suites, no single method universally dominates.
4. **Missing-Data Resilience (MCAR):**  
   Cluster recovery retains approximately $108\%$ / $80\%$ / $33\%$ / $41\%$ of 0%-missing ARI at $10\%$ / $20\%$ / $30\%$ / $50\%$ missing data, holding stability up to $20\%$ dropout before degrading to baseline levels by $30\%$.
5. **Linear Scalability:**  
   The scalable anchor path ($N > 2{,}000$) exhibits linear $\mathcal{O}(N)$ scaling (time log-log slope 0.66, 6 MB to 98 MB up to $N = 32{,}000$ in $0.77\text{s}$), enabling processing at scales where dense methods trigger memory exhaustion.

---

## 6. Academic Citation

If referencing the theoretical proofs, audit methodology, or empirical benchmarks from this documentation:

```bibtex
@misc{kundu2026inductive,
  author       = {Akash Kundu and Trinankur Guha and Rupankar Ghatak and Anubhav Naskar},
  title        = {Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes},
  howpublished = {Final Year Engineering Research Project (CSE\_PROJECT\_68), Department of Computer Science and Engineering},
  year         = {2026},
  note         = {Original University Title: Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data. Faculty Mentor: Prof. Kalyan Kumar Das. Target Venues: IEEE TKDE / ICDE}
}
```
