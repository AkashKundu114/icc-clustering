# Simulated Hostile Peer Review Report: Iteration 01
**Date:** 2026-10-17  
**Manuscript:** Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes (`springer_manuscript/main.tex`, `main.pdf`)  
**Target Venue:** Pattern Analysis and Applications (Springer Nature `sn-jnl` template)  
**Roles:** R8 Independent Triad (Clustering Methodologist, Statistician/Reproducibility Reviewer, Associate Editor) + R9 Integrity Auditor.

---

## Reviewer 1: Clustering Methodologist
**Rating:** Minor Revision  
**Recommendation:** Accept with Minor Revisions on Baseline Scoping and Bimodality Limitations

### Strengths:
1. **Computational Architecture:** The combination of exact quadratic determinacy ($O(M^2 N + M^2 K^2)$ without computing the $N \times N$ matrix) and bipartite anchor graph spectral projection ($O(N L)$ auxiliary memory) is technically sound and solves a legitimate scalability bottleneck of classical consensus clustering.
2. **Extreme Scalability:** Real-world benchmark scaling up to $N = 1{,}000{,}000$ points and $D = 100{,}000$ dimensions in under a minute with $3.05\text{ GB}$ peak memory is impressive and reproducible.
3. **Out-of-sample Generalization:** Formulating closed-form centroid projection in the certified active subspace avoids the quadratic re-clustering penalty for new queries.

### Critiques & Blocking Inquiries:
1. **Marginal Feature Screening Failure Modes:**
   - The authors rely heavily on Sarle's Bimodality Coefficient ($BC \ge 5/9$). While Proposition 1 correctly establishes the threshold $\Delta/\sigma > \sqrt{(3+\sqrt{15})/2} \approx 1.854$ for symmetric Gaussian mixtures, marginal 1D screening fundamentally fails under non-linear feature interactions (such as the XOR structure on Madelon). The authors acknowledge this on Madelon, but must emphasize that VSSG is strictly a marginal filter, not a universal manifold discovery tool.
2. **Baseline Parity:**
   - In Table 3 (benchmark comparison across 13 datasets), competing algorithms (K-Means, DEC, Ward, Spectral) were run on the raw ambient feature space without upstream feature selection. The paper should reiterate clearly that when fair feature selection (variance filtering or sparse clustering) is applied, the gap narrows on certain domains, though ICC-v2 retains an advantage on cancer microarrays.
3. **Cluster Count Parameterization:**
   - The paper notes that $L=40$ causes under-sampling when $K \ge 20$ (e.g., 20 Newsgroups, Isolet). The recommendation $L = \max(40, 10K)$ should be formalized as a core parameter guideline.

---

## Reviewer 2: Statistician and Reproducibility Reviewer
**Rating:** Minor Revision  
**Recommendation:** Transparent Statistical Scoping and Honest Rank Reporting

### Strengths:
1. **Macro-Driven Traceability:** All empirical metrics, table entries, and rankings are dynamically bound to `numbers.tex`, guaranteeing zero fabricated or adrift numbers.
2. **Rigorous Significance Testing:** The manuscript avoids inflated claims of "decisive superiority". The Friedman omnibus test ($\chi_F^2 = 11.34, p = 0.33$) and true Nemenyi critical difference ($CD = 4.21$ for $k=11, N=13$) are stated accurately, acknowledging that omnibus separation is not statistically significant.
3. **Transparent Overall Ranking:** The abstract and experimental section honestly report that Deep Embedded Clustering (DEC) achieves the lowest mean rank ($R = 4.31$), with ICC-v2 ranking fifth overall ($R = 5.46$).

### Critiques & Blocking Inquiries:
1. **Subgroup Ranking Qualification:**
   - The manuscript highlights that ICC-v2 achieves Rank #1 ($R = 2.33$) on the $D/N > 20$ subgroup (6 datasets). However, as the authors note, post-hoc Holm adjustment across 10 baselines yields $p_{\text{adj}} \ge 0.3125$. The authors must maintain their explicit caveat that this subgroup ranking is exploratory and post-hoc.
2. **Proposition 1 Mathematical Precision:**
   - The derivation of $\Delta/\sigma > \sqrt{(3+\sqrt{15})/2} \approx 1.854$ is verified and correct (replacing the previous erroneous $1.87$ or $\sqrt{3.55}$). Ensure the proof in the appendix preserves all finite-sample degrees of freedom corrections.
3. **Reproducibility Repository:**
   - Release tag `v2.0.0` is referenced. All raw JSON benchmark outputs and scripts must be tracked in `results/`.

---

## Reviewer 3: Associate Editor (Scope, Novelty & Venue Alignment)
**Rating:** Favorable for Regular Research Article  
**Recommendation:** Align with Pattern Analysis and Applications (PAAP) or DAMI Guidelines

### Assessment:
1. **Venue Compatibility:**
   - The manuscript fits the scope of *Pattern Analysis and Applications* (PAAP) and *Data Mining and Knowledge Discovery* (DAMI). It delivers a substantive analysis of distance concentration failure modes and provides an efficient bipartite anchor ensemble architecture.
2. **Compliance & Declarations:**
   - Fully conforms to Springer Nature submission requirements:
     - Formatted in `sn-jnl.cls` (`[pdflatex,sn-mathphys-num]`).
     - Contains complete mandatory declarations: Funding, Conflict of Interest, Ethics Approval, Consent, Data & Code Availability, Author Contributions, and an AI Use Disclosure documenting use solely for code optimization and grammar/syntax checking without research/LaTeX claims.
     - Unstructured abstract (199 words) adheres to the $\le 250$-word limit.
     - PDF compiles cleanly via Tectonic/XeTeX with zero undefined citations or broken labels.

---

## Integrity Auditor (R9) Sign-Off:
- **Audit Verdict:** PASS.
- **Findings:**
  - No inflated claims: The manuscript explicitly documents 5th place omnibus ranking, lack of omnibus statistical significance ($p = 0.33$), and failure modes of marginal screening.
  - No data fabrication: All values in Table 1, Table 2, Table 3, and text body are generated from frozen artifacts in `results/` and defined in `numbers.tex`.
  - Independent scope maintained: Study 1' (conformal label sets) is cleanly quarantined and not merged into this submission.
