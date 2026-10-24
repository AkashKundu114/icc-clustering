# Cover Letter Draft

**Target Journal:** *Data Mining and Knowledge Discovery* (DAMI, Springer Nature)  
**Article Type:** Original Research Article  
**Canonical Title:** "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Authors:** Akash Kundu (Corresponding Author), Trinankur Guha, Rupankar Ghatak, Anubhab Naskar, Kalyan Kumar Das  
**Affiliation:** Department of Computer Science and Engineering, Techno India University, Kolkata, West Bengal, India  
**Active Release Version:** `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*

---

Dear Editor-in-Chief and Editorial Board,

We submit our original research manuscript titled **"When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"** for consideration as a regular research article in *Data Mining and Knowledge Discovery* (DAMI).

### Context & Contribution
Consensus clustering synthesizes diverse base clusterings into a unified, initialization-resilient data partition. However, standard formulations face two fundamental bottlenecks:
1. **The Transductive Bottleneck:** Operating on an $N \times N$ dense co-association matrix requires $O(N^2)$ storage and forbids inductive assignment to unseen out-of-sample queries without re-solving the global consensus graph from scratch.
2. **High-Dimensional Distractor Noise:** In small-sample, high-dimensional regimes ($D \gg N$), distance concentration degrades Euclidean metrics, trapping standard ensemble consensus in arbitrary noise boundaries.

To resolve these challenges without incurring quadratic computational overhead, we introduce **Inductive Consensus Clustering (ICC-v2)** and its conformal extension (**CICC**). Our framework couples:
- A linear $O(N \cdot D)$ marginal feature screening filter based on Sarle's Bimodality Coefficient with finite-sample null calibration (Bimodality-Gated Subspace Selection, BGSS) that isolates multimodal candidate dimensions from unimodal distractor noise;
- A rectangular bipartite anchor consensus mechanism that reduces auxiliary storage from $O(N^2)$ to $O(N \cdot L)$ ($L \ll N$) with Transfer-Cut degree and eigenvalue normalization;
- A stability-weighted centroid assignment for $O(K \cdot |\mathcal{F}_{\text{active}}|)$ instant inductive out-of-sample projection; and
- Finite-sample distribution-free $(1 - \alpha)$ conformal prediction set guarantees with target-decoy False Discovery Rate (FDR) feature screening for safe clinical point-of-care triage.

### Empirical Rigor & Single Source of Truth (`paper/numbers.tex`)
Across an extensive benchmark of 13 multi-domain datasets spanning 11 candidate algorithms (2,750 total model fits across 30 seeds on 6 high-D datasets and 10 seeds on 7 general datasets), we provide a strictly calibrated, preregistered evaluation:
- Omnibus Friedman testing confirms absence of global dominance across heterogeneous benchmark domains ($\chi_F^2 = 9.59, p = 0.48$, Nemenyi Critical Difference $CD = 4.19$).
- On the target high-dimensional biomedical subgroup ($D/N > 20$), ICC-v2 commands **Rank #1** with Mean ARI = **0.217** (substantially exceeding Standard Consensus 0.037, DEC 0.045, and K-Means 0.056).
- Across the complete collection, ICC-v2 achieves Grand Mean ARI = 0.152 (Rank 5.23), demonstrating marked gains on clinical cancer microarrays including Golub Leukemia (ARI = 0.600) and Khan SRBCT (ARI = 0.546).
- Asymptotic computational complexity scales smoothly to $N = 10^6$ instances in 55.6 seconds (3.05 GB peak RSS, 240 MB graph memory, achieving a 99.6% reduction over the dense 8 TB co-association matrix).

### Editorial & Reproducibility Declarations
- **Originality:** This work has not been published previously and is not under consideration elsewhere.
- **Reproducibility:** All datasets, experiment runners, pre-registration specifications, and the full Python codebase are completely open-source and hosted in our public GitHub repository (`https://github.com/AkashKundu114/icc-clustering`) under the MIT License (Active Release: `v2.1.0`, Historical baseline: `v2.0.0`). Every empirical value in the manuscript is dynamically generated through automated, single-source LaTeX macro bindings (`paper/numbers.tex`).
- **AI Use Disclosure:** Formatted strictly in compliance with Springer Nature author policies; generative AI tools were employed solely for code optimization, static typing, and automated syntax/grammar verification, with zero role in scientific ideation, derivations, or experimental design.

Thank you for your time and consideration of our manuscript.

Sincerely,  
**Akash Kundu** (Corresponding Author)  
Department of Computer Science and Engineering, Techno India University  
Email: `akashkundu1152@gmail.com`  

On behalf of co-authors:  
Trinankur Guha, Rupankar Ghatak, Anubhab Naskar, and Kalyan Kumar Das
