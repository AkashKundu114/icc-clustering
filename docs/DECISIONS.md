# Architecture and Scientific Decision Records (ADR)

**Project:** Inductive Consensus Clustering (ICC-v2)  
**Repository:** `AkashKundu114/icc-clustering`  
**Target Manuscript:** *When Does Feature Gating and Anchor Consensus Salvage High-Dimensional Clustering? An Empirical and Geometric Analysis*  
**Target Venue:** Springer Nature *Data Mining and Knowledge Discovery* (DAMI)  
**Lead Author / Maintainer:** Akash Kundu  

---

## Index of Decision Records

- **ADR-001:** Manuscript Title and Scientific Scope Definition
- **ADR-002:** Authorship and Attribution Separation (Repo vs Manuscript)
- **ADR-003:** Benchmark Matrix Harmonization and 3,000 Fit Arithmetic
- **ADR-004:** Retirement of "Certified Core" in Favor of "High-Determinacy Core"
- **ADR-005:** BGSS Candidate Pool Gating: Minimum Diversity Floor vs Strict Analytical Cutoff
- **ADR-006:** Inclusion of 12th Baseline (CoHiRF) in the Primary Benchmark Matrix
- **ADR-007:** Decoupling of Track B into Independent Repository (`nullconsensus`)
- **ADR-008:** Target Publication Venue Strategy and Fallback Hierarchy

---

### ADR-001: Manuscript Title and Scientific Scope Definition
- **Status:** ACCEPTED
- **Context:** The working draft title varied across early iterations (e.g., *"When Does Bimodality-Gated Feature Selection Help Consensus Clustering?"*, *"Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data"*).
- **Decision:** Formalized the unified canonical title:  
  **"When Does Feature Gating and Anchor Consensus Salvage High-Dimensional Clustering? An Empirical and Geometric Analysis"**
- **Rationale:** This title precisely captures the dual core mechanisms evaluated (bimodality gating and bipartite anchor consensus), emphasizes the critical empirical findings regarding failure boundaries, and aligns with the editorial scope of Springer Nature's *Data Mining and Knowledge Discovery* (DAMI).
- **Consequences:** All files, documentation (`README.md`, `CITATION.cff`, `AGENTS.md`), and submission bundles were systematically updated to this exact canonical title.

---

### ADR-002: Authorship and Attribution Separation (Repo vs Manuscript)
- **Status:** ACCEPTED
- **Context:** User directive specified that code development, testing, infrastructure, and repository management are solely executed by Akash Kundu, while institutional university guidelines require co-authors (teammates and faculty mentor) to be listed on the formal academic paper.
- **Decision:** Strict division of attribution:
  1. **Repository and Code Artifacts:** Exclusively attributed to Akash Kundu (`pyproject.toml`, `LICENSE`, `CITATION.cff`, `README.md`, git commit history, GitHub metadata).
  2. **Academic Manuscript Source:** Preserves the 4 institutional co-authors (Trinankur Guha, Rupankar Ghatak, Anubhab Naskar, and Prof. Kalyan Kumar Das) in `paper/main.tex` and `submission/arxiv_source/main.tex`.
- **Rationale:** Accurately reflects individual code contribution while satisfying academic project requirements without violating publication ethics.

---

### ADR-003: Benchmark Matrix Harmonization and 3,000 Fit Arithmetic
- **Status:** ACCEPTED
- **Context:** An earlier version evaluated 11 clustering pipelines across $(6 \times 11 \times 30) + (7 \times 11 \times 10) = 2{,}750$ fits. When CoHiRF was introduced as a 12th baseline, the total number of fits increased to $(6 \times 12 \times 30) + (7 \times 12 \times 10) = 3{,}000$, but line 303 in `paper/main.tex` retained the legacy `2,750` text.
- **Decision:** Corrected the text to explicitly state 3,000 fits across 12 pipelines: $(6 \times 12 \times 30) + (7 \times 12 \times 10) = 2{,}160 + 840 = 3{,}000$ model fits.
- **Rationale:** Ensures complete internal consistency between paper text, empirical tables, and frozen CSV data artifacts.

---

### ADR-004: Retirement of "Certified Core" in Favor of "High-Determinacy Core"
- **Status:** ACCEPTED
- **Context:** Initial drafts described samples with high quadratic determinacy ($\sigma_i \ge \tau_{\text{core}}$) as the "certified core" and anchor selection from this set as "anchor certification". In machine learning theory, "certification" implies formal guarantees of true class correctness.
- **Decision:** Retired "certified core" across all manuscript files and documentation. Adopted "high-determinacy core" ($\mathcal{C}_{\text{core}}$) and "determinacy-based anchor selection".
- **Rationale:** Prevents overclaiming and technical inaccuracy. Sample determinacy measures ensemble consensus stability across base partitions, not ground-truth classification accuracy.

---

### ADR-005: BGSS Candidate Pool Gating: Minimum Diversity Floor vs Strict Analytical Cutoff
- **Status:** ACCEPTED
- **Context:** Proposition 1 proves that continuous unimodal noise has population Sarle coefficient $BC \le 5/9$. However, applying a hard analytical cutoff $\hat{b}_d \ge 5/9$ on finite-sample datasets (such as parity datasets or small cohorts) can select zero features or discard informative features due to sample variance.
- **Decision:** Implement BGSS as a ranked candidate pool selection:
  $$\text{pool\_size} = \min(D, \max(K, \max(100, \lfloor \alpha \cdot D \rfloor)))$$
  with $\alpha = 0.15$. Setting a minimum floor of $\min(100, D)$ features ensures adequate subspace diversity across base clusterers in high dimensions while retaining top bimodal signals.
- **Rationale:** Balances the theoretical rejection of unimodal noise with empirical stability across heterogeneous dataset dimensionalities.

---

### ADR-006: Inclusion of 12th Baseline (CoHiRF) in the Primary Benchmark Matrix
- **Status:** ACCEPTED
- **Context:** High-dimensional clustering literature frequently benchmarks against consensus methods with random projections or random forests. CoHiRF (Consensus of Hierarchical Random Forests) represents a competitive recent baseline.
- **Decision:** Included CoHiRF as the 12th pipeline across all 13 benchmark datasets and 30/10 seeds, bringing the total benchmark model fits to 3,000.
- **Rationale:** Strengthens empirical rigor and benchmarking fairness against state-of-the-art consensus clustering algorithms.

---

### ADR-007: Decoupling of Track B into Independent Repository (`nullconsensus`)
- **Status:** ACCEPTED
- **Context:** Track B explores a new clustering method (Candidate 12: NullGate non-parametric permutation-null gating, and Candidate 2: HurdleGate count-aware hurdle module) under a strict pre-registration protocol.
- **Decision:** Established an entirely isolated repository at `d:\nullconsensus`, decoupled from Track A (`d:\Final Year Project`). Tagged the initial frozen architecture as `prereg-v1` at commit `78c0808`.
- **Rationale:** Eliminates data leakage, prevents cross-contamination of code and experimental setups, and guarantees compliance with pre-registration integrity rules.

---

### ADR-008: Publication Venue Strategy and Fallback Hierarchy
- **Status:** ACCEPTED
- **Context:** Determining the optimal academic venue for Track A.
- **Decision:**
  1. **Primary Target:** Springer Nature *Data Mining and Knowledge Discovery* (DAMI). The manuscript matches DAMI's emphasis on comprehensive empirical validation, scalability, negative results, and rigorous algorithm analysis.
  2. **Methodological Fallback:** *Journal of Classification* (Springer Nature / Classification Society). Ideal if reviewers recommend emphasizing foundational geometric properties and clustering metric behavior.
  3. **High-Impact Stretch:** IEEE *Transactions on Knowledge and Data Engineering* (TKDE), only if additional algorithmic extensions and theoretical bounds are requested.
- **Rationale:** Maximizes submission readiness and aligns with Springer Nature `sn-jnl.cls` template structure.
