# Inductive Consensus Clustering (ICC-v2): Documentation & Research Dossier

**Canonical Manuscript Title:** When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination  
**Target Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI), document class `sn-jnl.cls` (`sn-mathphys-num.bst`)  
**Canonical Release Version:** v2.1.0  
**Repository Package:** `icc` (v2.1.0) and `cicc` (Conformal Inductive Consensus Clustering)

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
  • Role: Initial university allotment title and problem definition.
  • Focus: Exploratory heuristics utilizing sample stability in noisy high-dimensional clustering.
  • Scope: Formulating base clustering diversity and sample-level stability weighting.

                                            │
                                            ▼ (Theoretical & Algorithmic Maturation)
                                            │

  [ 2. Early Proposal Blueprint Title (Early Capstone Proposals) ]
  • Title: "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation
            for High-Dimensional Noise Regimes"
  • Target Venue: Springer Nature (*Data Mining and Knowledge Discovery* / DAMI).
  • Focus: Transition from transductive heuristics to an inductive, geometry-calibrated framework.
  • Breakthroughs:
    1. Exact Linear-Memory Determinacy Identity via contingency tables in O(M^2 N + M^2 K^2).
    2. Finite-sample Sarle Bimodality Coefficient bound (BC <= 5/9) and zero-inflation boundary.
    3. Reduced Bipartite Spectral Transfer-Cut consensus scaling in O(N L^2 + L^3).
    4. Inductive out-of-sample projection bounds and Anchor-Space Perturbation Profiling (ASPP).

                                            │
                                            ▼ (Peer-Reviewed Empirical Falsification & Venue Unification)
                                            │

  [ 3. Canonical Journal Manuscript Title (Springer Nature DAMI Submission) ]
  • Title: "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering?
            An Empirical Examination"
  • Venue: Springer Nature Journal (Data Mining and Knowledge Discovery / DAMI)
  • Class: sn-jnl.cls with sn-mathphys-num.bst citation formatting.
  • Focus: Rigorous empirical examination answering precisely WHEN feature gating and anchor
    consensus succeed vs fail across heterogeneous data regimes, grounded in frozen experimental
    registries and verified numbers.tex macros.
```

---

## 2. Documentation Architecture & Master Directory Map

The documentation hierarchy is structured into five distinct academic and technical modules:

```
docs/
├── README.md                            # Master navigation index and documentation roadmap (this file)
├── DATA.md                              # Benchmark dataset metadata, cryptographic hashes, and cache ledger
├── THEORETICAL_FOUNDATIONS.md          # Formal mathematical definitions, propositions, proofs, and complexity
├── api.md                               # Complete Python API reference for icc and cicc packages
├── literature/                          # Research landscape, prior art taxonomies, and paper dossiers
│   ├── papers.md                        # 20-paper annotated matrix, 11 baselines comparison, BibTeX records
│   └── prep.md                          # Comprehensive research preparation dossier and mentor directive realization
├── proposal/                            # Formal research proposals and early scientific blueprints
│   ├── inductive_consensus_proposal.md  # Capstone proposal blueprint
│   └── cluster_stability_proposal.md    # Preserved alias / initial title allotment
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
│   ├── 10_final_reviewer_report.md      # Adversarial reviewer report evaluating defensibility
│   ├── 11_verification_log.md           # Hash-verified execution records of test sweeps
│   ├── 12_adversarial_rereview.md       # Phase 12 re-review and Springer Nature transition synthesis
│   └── remediation_reports/             # Author technical defense notes (01 through 12)
└── figures/                             # Conceptual schematics and high-dimensional manifold illustrations
    └── high_d_noisy_manifold_concept.jpg # Distance concentration and geometric ridge distortion
```

---

## 3. Core Research Modules & Reading Order

For reviewers, collaborators, and students navigating this repository, the recommended sequence is:

### Step 1: Scientific Lineage & Research Blueprint
* Read [`proposal/inductive_consensus_proposal.md`](./proposal/inductive_consensus_proposal.md) (or [`proposal/cluster_stability_proposal.md`](./proposal/cluster_stability_proposal.md)) to understand the initial capstone allotment, the fundamental **"Hallucinated Stability" trap**, and how ICC-v2 was formulated to fulfill Prof. Kalyan Kumar Das's research directives (Points 1, 2, and 5). Note that the unified canonical manuscript is published under Springer Nature DAMI.

### Step 2: Prior Art, Literature & Baselines
* Read [`literature/papers.md`](./literature/papers.md) for an exhaustive 20-paper annotated literature matrix, the comprehensive comparative analysis of the **11 baseline algorithms** (K-Means, Ward, Spectral, SEC, CSPA, MCLA, LWEA, LWGP, FastMICE, DEC, Li et al. Core-Halo), and the formal prior art taxonomy (Categories A through D).
* Read [`literature/prep.md`](./literature/prep.md) to trace the evolution of the research preparation, methodological decisions, and team role division.

### Step 3: Mathematical Formulation & Proofs
* Read [`THEORETICAL_FOUNDATIONS.md`](./THEORETICAL_FOUNDATIONS.md) for formal proofs of:
  - **Proposition 1:** Finite-sample Sarle Bimodality Coefficient null bound ($BC \le 5/9$) rejecting continuous unimodal distractor noise.
  - **Remark 1:** The zero-inflation boundary where point-mass sparsity mimics bimodality.
  - **Proposition 2:** Exact Linear-Memory Determinacy Identity via cross-model contingency tables in $\mathcal{O}(M^2 N + M^2 K^2)$ time and $\mathcal{O}(N + M K)$ memory.
  - **Theorems 1 & 2:** Inductive assignment convergence and strictly linear asymptotic time complexity $\mathcal{O}(N)$.
  - **ASPP Theory:** Scalable Anchor-Space Perturbation Profiling across 5 perturbation operators.

### Step 4: Adversarial Audit & Empirical Verification
* Read [`audit_reports/README.md`](./audit_reports/README.md) and [`audit_reports/12_adversarial_rereview.md`](./audit_reports/12_adversarial_rereview.md) to review the empirical findings from 2,750 benchmark executions, pool sensitivity curves (E3), label-free selector negative results (E3b), missing-data sweeps (E5), and per-process memory scaling (E6).

---

## 4. Algorithmic Architecture & Codebase Traceability

All theoretical formulations and documentation sections map directly to the production implementation in [`src/icc/`](../src/icc/) and [`src/cicc/`](../src/cicc/):

| Documentation Section | Mathematical Formulation | Source Code Implementation | Test Verification |
| :--- | :--- | :--- | :--- |
| **VSSG / BGSS Feature Gating** | Definition 1, Proposition 1 | [`src/icc/consensus_v2.py`](../src/icc/consensus_v2.py) | [`tests/test_consensus_v2.py`](../tests/test_consensus_v2.py) |
| **Exact Linear Determinacy** | Proposition 2 | [`src/icc/consensus_v2.py`](../src/icc/consensus_v2.py) | [`tests/test_consensus_v2.py`](../tests/test_consensus_v2.py) |
| **Bipartite Transfer-Cut** | Section 4, Theorem 2 | [`src/icc/consensus_v2.py`](../src/icc/consensus_v2.py) | [`tests/test_consensus_v2.py`](../tests/test_consensus_v2.py) |
| **ASPP Stability Profiling** | Definition 3 | [`src/icc/aspp.py`](../src/icc/aspp.py) | [`tests/test_aspp.py`](../tests/test_aspp.py) |
| **Inductive Prediction** | Theorem 1 | [`src/icc/consensus_v2.py`](../src/icc/consensus_v2.py) (`predict`) | [`tests/test_inductive_projection.py`](../tests/test_inductive_projection.py) |
| **Conformal Inductive Calibration** | Finite-Sample $(1 - \alpha)$ Sets | [`src/cicc/conformal.py`](../src/cicc/conformal.py) | [`tests/test_cicc.py`](../tests/test_cicc.py) |
| **Target-Decoy FDR Gating** | Mirror Statistics $W_d$ | [`src/cicc/decoy.py`](../src/cicc/decoy.py) | [`tests/test_cicc.py`](../tests/test_cicc.py) |
| **Agent Episodic Memory** | Conformal Triage / Novelty | [`src/cicc/memory.py`](../src/cicc/memory.py) | [`tests/test_cicc.py`](../tests/test_cicc.py) |
| **11 Baseline Algorithms** | Baseline Matrix | [`src/icc/baselines/`](../src/icc/baselines/) | [`tests/test_baselines.py`](../tests/test_baselines.py) |
| **Benchmark Datasets** | Benchmark Matrix | [`src/icc/datasets/`](../src/icc/datasets/) | [`tests/test_datasets.py`](../tests/test_datasets.py) |

---

## 5. Single Source of Truth Empirical Findings (from `paper/numbers.tex`)

All quantitative claims strictly trace to verified macros in [`paper/numbers.tex`](../paper/numbers.tex) generated from frozen Pass F benchmark results:

1. **Ultra-High-Dimensional Biological Cancer Subgroup ($D/N > 20$, 6 Datasets):**  
   ICC-v2 commands **Rank #1 dominance** with Mean ARI = **0.217** (median 0.036), substantially outperforming standard consensus (0.037), DEC (0.045), and K-Means (0.056).
   - **Golub Leukemia ($N=72, D=7{,}129, K=2$):** ARI = **0.600 +/- 0.367**, with **54.0%** oncogenic marker recovery (27 of top 50 known driver genes captured label-free).
   - **Khan SRBCT ($N=83, D=2{,}308, K=4$):** ARI = **0.546 +/- 0.102**, cleanly partitioning four pediatric malignancies.
   - **Ovarian Proteomics ($N=253, D=15{,}154, K=2$):** ARI = **0.050**, delivering a **5.1x speedup** over dense consensus.

2. **Omnibus Multi-Domain Benchmark Suite (13 Datasets, 2,750 Model Fits, 11 Solvers):**  
   Across all 13 heterogeneous datasets, ICC-v2 achieves a Grand Mean ARI of **0.152** (overall rank **5.23** of 11). An omnibus Friedman rank sum test yields $\chi^2_F = 9.59, p = 0.48$ with a Nemenyi critical difference $\text{CD} = 4.19$. This proves that across heterogeneous multi-domain suites, no single algorithm universally dominates, and performance differences do not reach statistical significance globally.

3. **Sparse Text and Count Manifolds (Boundary Limitation):**  
   On highly sparse text (20 Newsgroups) and single-cell dropouts (Zheng68k), Hierarchical Ward and DEC outperform ICC-v2. Point-mass zero-inflation violates the continuous unimodal distractor assumption (Remark 1), elevating marginal kurtosis and diluting unimodal bimodality screening.

4. **Missing-Data Resilience (MCAR):**  
   In multi-dataset missingness sweeps, cluster recovery retains approximately $108\%$ / $80\%$ / $33\%$ / $41\%$ of 0%-missing ARI at $10\%$ / $20\%$ / $30\%$ / $50\%$ missing data, demonstrating stability up to $20\%$ dropout before degrading to baseline levels by $30\%$.

5. **Asymptotic Scalability:**  
   The scalable anchor path ($N > 2{,}000$) breaks the $N \times N$ memory wall. At extreme scale, ICC-v2 clusters $N = 10^6$ instances in **55.6 s** with peak RSS of **3.05 GB** and auxiliary bipartite graph memory of **240 MB**, representing a **99.6% reduction** over the dense 8 TB co-association matrix.

---

## 6. Extended Knockout Ablation Study (Section 5.2)

To dissect the exact mechanism of ICC-v2, Section 5.2 evaluates a factorial component knockout across all 6 high-dimensional biological datasets ($D/N > 20$, 30 random seeds):

1. **Knockout 1: Removing Feature Gating (V5 -> V3):**  
   Disabling BGSS feature gating causes subgroup mean ARI to collapse from **0.217** to **0.046** (a **-78.8%** drop). On Leukemia, ARI falls from 0.600 to 0.155; on SRBCT, from 0.546 to 0.101. This demonstrates that bipartite anchor consensus in isolation cannot overcome isotropic distance concentration without upstream feature selection.
2. **Knockout 2: Removing Bipartite Anchor Graph (V5 -> V2):**  
   Replacing bipartite anchor consensus with full dense consensus under identical gated features causes subgroup mean ARI to drop from **0.217** to **0.077** ($\Delta = -0.139$, 95% CI: $[+0.065, +0.218]$). Dense averaging across noisy base partitions creates spurious dense edges, whereas anchor distillation concentrates consensus weights exclusively on stable manifold anchors.
3. **Knockout 3: Removing Consensus Ensembling (V5 -> V1):**  
   Replacing ensemble consensus with a single K-Means partition on the gated pool drops subgroup mean ARI to **0.070**. On Leukemia, single K-Means fails completely (mean ARI -0.017), showing that random subspace ensembling is required to sample subsets where discriminative markers co-occur.
4. **Knockout 4: Anchor Determinacy Null Result (V5 -> V4):**  
   Certified core anchors (V5, ARI 0.217) vs uniform random anchors (V4, ARI 0.198) yields $\Delta = +0.019$ (dataset-level bootstrap 95% CI: $[-0.039, +0.082]$, paired Wilcoxon $W = 9.0, p = 0.84$). Because the confidence interval encompasses zero, determinacy anchor certification provides no statistically significant accuracy lift over uniform random anchors. Thus, bipartite graph compression rather than anchor certification is the primary operational driver.

---

## 7. Practical Real-World Applications & Clinical Case Studies (Section 6)

The framework translates into four real-world deployment case studies documented in Section 6:

1. **Translational Oncology & Cancer Subtyping ([`examples/clinical_cancer_subtyping.py`](../examples/clinical_cancer_subtyping.py)):**  
   Unsupervised disease subtyping on clinical gene expression cohorts without pathology labels. Identifies ALL vs AML on Golub Leukemia (ARI = 0.600) and 4 childhood cancer categories on Khan SRBCT (ARI = 0.546), recovering 54.0% of top oncogenic driver genes.
2. **Point-of-Care Inductive Biopsy Decision Support ([`examples/realtime_patient_projection.py`](../examples/realtime_patient_projection.py)):**  
   Sub-millisecond inductive patient projection (**22.6 microseconds** latency per biopsy) coupled with split-conformal certainty quantification providing guaranteed $(1 - \alpha = 90\%)$ coverage sets. Triages incoming biopsies into high-confidence singletons, ambiguous cases prompting secondary testing, and empty-set novelty abstentions.
3. **Million-Scale Single-Cell Transcriptomics:**  
   Bypasses the 8 TB dense RAM barrier at $N = 10^6$ single cells, executing in 55.6 s with 240 MB graph memory on single-node research workstations.
4. **Conformal Inductive Consensus Clustering ([`src/cicc/`](../src/cicc/)):**  
   Integrates split-conformal prediction sets ([`src/cicc/conformal.py`](../src/cicc/conformal.py)), target-decoy / knockoff FDR feature screening with mirror statistics $W_d = |T_d| - |\tilde{T}_d|$ ([`src/cicc/decoy.py`](../src/cicc/decoy.py)), and episodic semantic agent memory ([`src/cicc/memory.py`](../src/cicc/memory.py)).

---

## 8. Academic Citation

If referencing the theoretical proofs, audit methodology, or empirical benchmarks from this documentation:

```bibtex
@article{kundu2026when,
  author    = {Akash Kundu and Trinankur Guha and Rupankar Ghatak and Anubhav Naskar},
  title     = {When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination},
  journal   = {Data Mining and Knowledge Discovery},
  publisher = {Springer Nature},
  year      = {2026},
  note      = {Canonical Release v2.1.0. Initial University Allotment: Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data (CSE\_PROJECT\_68, Dept. of CSE, Faculty Mentor: Prof. Kalyan Kumar Das). Early Proposal Blueprint: Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes. Target Venue: Springer Nature DAMI.}
}
```
