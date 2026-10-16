# Comprehensive Remediation & Venue Assessment Report

**Target Venue:** *Data Mining and Knowledge Discovery* (DAMI), Springer Nature  
**Submission Instructions Checked:** October 13, 2026 (Live Guidelines: `https://link.springer.com/journal/10618/submission-guidelines`)  
**Target Publication Objective:** Online publication by September 2027  
**Lead & Corresponding Author:** Akash Kundu (`akash231001001449@technoindiaeducation.com`, ORCID: `0009-0003-8246-7316`)  
**Co-Authors:** Trinankur Guha, Rupankar Ghatak, Anubhab Naskar  
**Mentor & Faculty Supervisor:** Kalyan Kumar Das  
**Institution:** Department of Computer Science and Engineering, Techno India University, Kolkata, West Bengal, India  

---

## 1. Final Scientific Contribution Supported by Corrected Evidence

Following rigorous audit remediation, the scientific contribution of ICC-v2 has been honestly and reproducibly repositioned away from universal omnibus dominance to its genuine mathematical and empirical strengths:

1. **Finite-Sample Consensus Breakdown Characterization (Exp 0):**
   Demonstrates that multi-clusterer averaging alone cannot rescue pairwise distances under finite-sample isotropic distractor noise ($D \gg N$). Due to distance concentration, random noise fluctuations create a deceptive "stability trap" where consensus stability remains $>0.8$ while true cluster recovery collapses ($\text{ARI} \to 0$).

2. **Bimodality-Gated Subspace Selection (BGSS / VSSG, Stage 1):**
   A strictly $O(N \cdot D)$ linear feature screening filter utilizing Sarle's Bimodality Coefficient with finite-sample null correction. We derived and verified the exact analytic bimodal separation threshold:
   $$\frac{\Delta}{\sigma} > \sqrt{\frac{3+\sqrt{15}}{2}} \approx 1.854$$
   (correcting the previously erroneous $\sqrt{2} \approx 1.414$). On the non-linear Madelon benchmark ($D=500, D_{\text{signal}}=20$), BGSS attains $\text{PR-AUC} = 0.892$ and $\text{Recall@50} = 0.95$.

3. **Determinacy-Based Bipartite Anchor Consensus (Stage 2 & 3):**
   Eliminates the dense $O(N^2)$ co-association matrix bottleneck by evaluating exact sample determinacy $\sigma_i = \frac{1}{N-1}\sum_{j \neq i} S_{ij}^2$ via the Proposition 2 contingency identity in $O(M^2 N + M^2 K^2)$ time and $O(N + K^2)$ memory. Core anchor selection ($L = \max(40, 10K)$) with bipartite Transfer-Cut achieves an asymptotic $O(N)$ auxiliary memory complexity ($O(NL + L^2)$), slashing auxiliary memory by $97.0\%$ ($45.8\text{ MB}$ vs $1,529.8\text{ MB}$) at $N=10,000$ and executing on $N=1,000,000$ in $55.6\text{s}$.

4. **Geometry-Calibrated Inductive Out-of-Sample Extension (Stage 4):**
   Enables instant, closed-form out-of-sample cluster assignment in $O(K \cdot |\mathcal{F}_{\text{active}}|)$ time via stability-weighted active centroids without re-solving the consensus graph.

5. **Empirical Operating Regime Boundary:**
   On high-dimensional biomedical regimes ($D/N > 20$, e.g., Leukemia, SRBCT, Ovarian), ICC-v2 achieves top performance ($R=1.50$, Grand Mean ARI $= 0.1599$, $+300\%$ to $+1,250\%$ ARI gains over classical consensus). In abundant-sample, large-class regimes ($K \ge 20$, e.g., 20 Newsgroups, Isolet), classical hierarchical methods and deep clustering maintain superiority because a bounded anchor budget under-samples fine-grained minority subtypes.

---

## 2. Venue Fit: *Data Mining and Knowledge Discovery* (DAMI)

### Scope Alignment
*Data Mining and Knowledge Discovery* publishes foundational algorithms, theoretical analyses, scalability studies, and empirical evaluations across high-dimensional and complex data mining regimes.
- **Core Problem:** Scalability and noise fragility of unsupervised consensus clustering in modern high-dimensional, small-sample data mining scenarios.
- **Technical Novelty:** Combining linear-time moment-based multimodality gating with bipartite Transfer-Cut spectral consensus and inductive out-of-sample mapping.
- **Honest Empirical Positioning:** The paper presents an empirically validated regime map rather than making unsubstantiated claims of universal superiority, aligning with DAMI's high standards of scientific rigor.

**Recommendation:** Continued targeting of *Data Mining and Knowledge Discovery* is well-justified.

---

## 3. Remaining Scientific & Empirical Tasks Prior to Submission

| Item | Action Required | Evidence Needed to Close | Target Date |
|---|---|---|---|
| **Multi-Seed Variance Bands in Main Table** | Current Table 3 reports point ARI estimates across 1,430 fits. | Include mean $\pm$ std across $\ge 10$ independent random seeds in Table 3 for all 13 benchmarks. | November 2026 |
| **Statistical Test Harmonization** | Supplementary table reports Wilcoxon signed-rank tests; main text features Friedman test ($p=0.33$) and Demšar CD diagram. | Ensure consistent reporting of omnibus vs post-hoc tests across text and supplementary materials. | November 2026 |
| **Mentor Review & Sign-Off** | Share Overleaf project with Prof. Kalyan Kumar Das. | Formal feedback and approval from faculty supervisor. | December 2026 |

---

## 4. Springer-Specific Compliance Checklist

*Checked against live DAMI guidelines on October 13, 2026:*

- [x] **Template & Document Class:** Official Springer Nature template (`sn-jnl.cls`, Dec 2024 v3.1) configured with author-year style: `\documentclass[pdflatex,sn-mathphys-ay]{sn-jnl}`.
- [x] **Citation & Bibliography Format:** Natbib author-year in-text citations (`sn-mathphys-ay.bst`), alphabetized reference list, and full DOI URLs on cited entries.
- [x] **Abstract Length:** 154 words (strictly within DAMI's 150–250-word mandate).
- [x] **Keywords:** 7 precise, domain-appropriate keywords provided.
- [x] **Section Numbering:** Standard decimal numbering, limited to three levels.
- [x] **Author & Institutional Metadata:** Complete author list with corresponding author details, institutional address (Techno India University, Kolkata), and ORCID identifiers.
- [x] **Declarations Section:**
  - Funding: *"The authors did not receive support from any organization for the submitted work."*
  - Competing Interests: *"The authors have no competing interests, financial or non-financial, to declare."*
  - Ethics Approval & Consent: Marked *"Not applicable"* (unsupervised benchmark study).
  - Data and Code Availability: Open repository link provided (`https://github.com/AkashKundu114/icc-clustering`).
  - Author Contributions: Formal CRediT breakdown across all five authors.
  - Acknowledgments: Dedicated faculty acknowledgment for Prof. Kalyan Kumar Das.
- [x] **No Residual Venue Language:** Complete removal of IEEE TKDE formatting tags and numbered IEEE reference schemes.
- [x] **Reproducibility & Traceability:** Zero fabricated numbers; all macro values trace to canonical `results/` logs via `make_paper_assets.py` and pass `check_consistency.py`.

---

## 5. Realistic Publication Schedule (Target: Online by September 2027)

To achieve online publication by **September 2027**, the following timeline accounts for realistic review, revision, and production cycles:

```
October 2026:      Audit remediation complete; author-year Springer package compiled.
November 2026:     Multi-seed variance runs finalized; mentor technical review.
December 2026:     Final mentor sign-off and preprint posting (arXiv).
January 15, 2027:  Formal initial submission to Data Mining and Knowledge Discovery (DAMI).
Feb – April 2027:  First-round peer review (typical cycle: 2.5–3.5 months).
May 1, 2027:       Decision received (Major/Minor Revision).
May 1 – 31, 2027:  Experimental revisions and detailed point-by-point rebuttal prepared.
June 15, 2027:     Revised manuscript submitted.
July 15, 2027:     Second-round review & formal Acceptance.
August 2027:       Author proofing, DOI assignment, and online first publication.
September 2027:    Online publication achieved.
```

---

## 6. Contingency Backup Venue Analysis

If editorial screening or early review at DAMI indicates a mismatch in scope or theoretical vs empirical balance:

1. **Backup Venue 1: *Machine Learning* (Springer Nature)**
   - *Scope:* High algorithmic and theoretical rigor; strong interest in unsupervised learning, ensembles, and inductive out-of-sample extensions.
   - *Template:* Uses the exact same Springer Nature `sn-jnl` author-year template (`sn-mathphys-ay`), requiring zero reformatting.
2. **Backup Venue 2: *Pattern Recognition* (Elsevier)**
   - *Scope:* Strong emphasis on clustering algorithms, spectral graph partitioning, and high-dimensional noise robustness.
   - *Transition Cost:* Moderate (Elsevier `elsarticle` template reformatting required).
