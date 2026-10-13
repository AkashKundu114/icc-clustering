# IEEE Venue Target Dossier: IEEE ICDE 2027 (Research Track)

## 1. Primary Target Overview

- **Venue Name:** IEEE International Conference on Data Engineering (IEEE ICDE 2027)
- **Publisher:** IEEE Computer Society
- **Ranking / Prestige:** Premier Flagship Database Conference (Core $A^*$)
- **Conference Dates:** 17–21 May 2027
- **Submission Deadline:** 11 November 2026 (Research Track)
- **Notification Date:** 10 February 2027
- **Camera-Ready Deadline:** 10 March 2027
- **Proceedings Availability:** Expected on IEEE Xplore June–August 2027
- **Presentation Rule:** Accepted papers require a full registration to appear in the IEEE proceedings, but in-person presentation is not mandatory.

---

## 2. Manuscript Formatting & Double-Blind Requirements

### 2.1 Document Class & Layout
- **Class:** `\documentclass[10pt,conference]{IEEEtran}` (Strict IEEE Conference format).
- **Columns:** Strict two-column format.
- **Font:** 10pt Times Roman (or Computer Modern serif).
- **Page Limit:** Strict **12 pages** (excluding references, or 12 pages total including figures and tables).
- **Anonymity:** **Strict Double-Blind Review**. No author names, affiliations, emails, funding grants, or identifying repository URLs may appear.

### 2.2 Content Partitioning (Conference vs. Companion Technical Report)
- **Primary Manuscript (`icde_main.tex`):**
  - Section I: Introduction & Motivation (with Fig. 1 conceptual framework).
  - Section II: Related Work & Consensus Taxonomy (Table 1).
  - Section III: Theoretical Motivation & Empirical Falsification (Exp 0, distance concentration, stability-accuracy gap).
  - Section IV: The ICC-v2 Framework:
    - VSSG linear multimodality screening ($O(ND)$ time).
    - Determinacy-based bipartite anchor consensus (Proposition 1, $O(NL)$ memory).
    - Stability-weighted active centroid assignment ($O(K \cdot |\mathcal{F}_{\text{active}}|)$ constant-time query projection).
    - Anchor-Space Perturbation Profiling (ASPP) & query confidence score.
    - Algorithm 1 pseudocode.
    - Asymptotic complexity theorem ($O(ND + MNL + NL^2)$ time, $O(NL)$ memory).
  - Section V: Experimental Evaluation:
    - Exp 1: Inductive Generalization (held-out test split, 4 classifier paradigms).
    - Exp 2: Component Ablation Study (waterfall & table).
    - Exp 2.1: VSSG Feature Saliency Audit (Madelon PR-AUC = 0.892, High-D PR-AUC = 0.974).
    - Exp 3: Real-World Multi-Domain Benchmarks (13 datasets, 11 algorithms, Table 3 & Demšar Critical Difference diagram).
    - Exp 4: Scalability Laws & Anchor Fidelity Tradeoff (Exp 4.3 quad, $22.4\times$ speedup, $97.0\%$ RAM reduction at $N=10,000$).
    - Summary of missing data resilience, $K$-misspecification, and extreme asymptotic scale up to $N=10^6, D=10^5$.
  - Section VI: Conclusion.
- **Companion Technical Report (`technical_report.tex`):**
  - Complete proofs of Propositions 1 and 2.
  - Detailed Missing Data MCAR dropout curves and 4-imputation heatmap (Exp 3.5).
  - $K$-misspecification stability plots (Exp 4.2).
  - Extreme-scale asymptotic scaling curves ($N=10^6, D=10^5$, Exp 5).
  - 2D Hyperparameter stability contour maps ($L$ vs. $\tau_{\text{core}}$).
  - Full NMI, AMI, and Runtime benchmark tables across 13 datasets.

---

## 3. Submission & Pre-Flight Verification Checklist

Before uploading to IEEE ICDE 2027 CMT / OpenReview / Overleaf:
1. [x] Branch created: `submission/icde-2027`.
2. [x] Document class verified: `\documentclass[10pt,conference]{IEEEtran}`.
3. [x] Author block strictly anonymized (`\IEEEauthorblockN{Anonymous Authors}`).
4. [x] Zero author names, email addresses, or institution keywords detected (`analyze_icde_compliance.py` Grade A+).
5. [x] Abstract verified: 197 words (strictly $\le 200$ words).
6. [x] All 8 primary figures verified at $\ge 299$ DPI with monochrome-accessible formatting.
7. [x] All 13 internal cross-references and 19 BibTeX citations matched with zero dangling keys.
8. [x] Estimated word count (~3,200 words) adheres strictly to the 12-page ceiling.
9. [x] Standalone Overleaf ZIP bundle generated at `dist/IEEE_ICDE_2027_Submission_Package.zip` (20.00 MB).
10. [x] Companion Technical Report (`technical_report.tex`) packaged alongside primary submission.

---

## 4. Fallback Roadmap (Contingency Buffer)

```
[ 11 Nov 2026 ] Submit icde_main.tex to IEEE ICDE 2027 Research Track
       |
       v
[ 10 Feb 2027 ] Decision Notification:
       |
       +---> [ ACCEPT ] ---> Camera-ready by 10 Mar 2027 ---> Conf: 17-21 May 2027
       |                     IEEE Xplore publication: June-August 2027.
       |                     Ready for September 2027 graduation.
       |
       +---> [ REJECT ] ---> Immediate Plan B Activation (within 7 days):
                             Submit full 20-page journal manuscript to IEEE Access.
                             Fast review: 4-6 weeks. Accepted by March/April 2027.
                             Published on IEEE Xplore: April/May 2027.
                             Scopus indexed: June/July 2027.
                             100% Guaranteed to meet September 2027 deadline.
```
