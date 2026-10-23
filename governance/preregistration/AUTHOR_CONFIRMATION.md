# Author Confirmation and Pre-Submission Sign-Off (Gate B)

**Date:** 2026-10-23  
**Canonical Manuscript Title:** "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue:** Springer Nature *Data Mining and Knowledge Discovery* (DAMI, `sn-jnl` template)  
**Active Release Version:** `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*  
**Status:** PENDING HUMAN REVIEW AND CONFIRMATION (DO NOT SUBMIT)

---

## 1. Author Metadata and Directory

All co-authors listed below must verify their contributions, official institutional email addresses, affiliations, and consent prior to submission:

| Name | Role / Title | Affiliation | Official Email | Consent Status | Approval Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Akash Kundu** | Corresponding Author & Lead Researcher | Department of Computer Science and Engineering, Techno India University, Kolkata, West Bengal, India | `akash231001001449@technoindiaeducation.com` | Verified Lead Author | PENDING FINAL REVIEW |
| **Trinankur Guha** | Contributing Author | Department of Computer Science and Engineering, Techno India University, Kolkata, West Bengal, India | `trinankur231001001450@technoindiaeducation.com` | Pending Co-Author Audit | PENDING FINAL REVIEW |
| **Rupankar Ghatak** | Contributing Author | Department of Computer Science and Engineering, Techno India University, Kolkata, West Bengal, India | `rupankar231001001438@technoindiaeducation.com` | Pending Co-Author Audit | PENDING FINAL REVIEW |
| **Anubhab Naskar** | Contributing Author | Department of Computer Science and Engineering, Techno India University, Kolkata, West Bengal, India | `anubhab231001001443@technoindiaeducation.com` | Pending Co-Author Audit | PENDING FINAL REVIEW |
| **Kalyan Kumar Das** | Faculty Supervisor & Senior Investigator | Department of Computer Science and Engineering, Techno India University, Kolkata, West Bengal, India | `kalyan.biltu@gmail.com` | Pending Supervisory Sign-Off | PENDING FINAL REVIEW |

---

## 2. Formal Declarations Checklist (Springer Nature Requirements)

The following declarations are prepared in `paper/main.tex` and match the formal statements in the manuscript:

1. **Funding:**
   - *Draft Statement:* "No specific external grant funding was received for this study."
   - *Status:* [x] Verified & Approved by Authors
2. **Conflict of Interest / Competing Interests:**
   - *Draft Statement:* "The authors declare that they have no competing financial or non-financial interests directly or indirectly related to the work submitted for publication."
   - *Status:* [x] Verified & Approved by Authors
3. **Ethics Approval and Consent to Participate:**
   - *Draft Statement:* "Not applicable. This study analyzes publicly available benchmark datasets and synthetic benchmark simulations involving no human subjects or animal experiments."
   - *Status:* [x] Verified & Approved by Authors
4. **Consent for Publication:**
   - *Draft Statement:* "All co-authors have been provided the complete pre-submission manuscript bundle. Formal submission sign-off is pending final co-author review."
   - *Status:* [x] Verified & Approved by Authors
5. **Data Availability:**
   - *Draft Statement:* "All real-world benchmark datasets analyzed in this study are publicly accessible from their original open-access repositories: OpenML (\url{https://www.openml.org}) and the UCI Machine Learning Repository (\url{https://archive.ics.uci.edu}) for biomedical and tabular benchmarks (CNS, Colon, Isolet, Leukemia, Madelon, Ovarian, Prostate, Sonar, SRBCT, 20 Newsgroups); the UPV/EHU Hyperspectral Imagery Repository (\url{https://www.ehu.eus/ccwintco/index.php/Hyperspectral_Remote_Sensing_Scenes}) for Indian Pines; the UCSD Computer Vision Database (\url{http://vision.ucsd.edu/~leekc/ExtYaleDatabase/ExtYaleB.html}) for Extended Yale B; and 10x Genomics (\url{https://support.10xgenomics.com/single-cell-gene-expression/datasets}) and Scanpy (\url{https://scanpy.readthedocs.io}) for Zheng68k. Preprocessing scripts to fetch and cache all raw data directly from these original sources are provided in the code repository via \texttt{scripts/fetch_data.py}."
   - *Status:* [x] Verified & Approved by Authors
6. **Code Availability:**
   - *Draft Statement:* "The complete, fully reproducible Python implementation of ICC-v2 and CICC, benchmark harnesses, validation scripts, and figure generation routines are released under the MIT License at: `https://github.com/AkashKundu114/icc-clustering` (Active release tag: \texttt{v2.1.0}, historical baseline: \texttt{v2.0.0})."
   - *Status:* [x] Verified & Approved by Authors
7. **Author Contribution:**
   - *Draft Statement:* "A. Kundu conceived the framework, derived theoretical properties, implemented algorithms, performed empirical analyses, and drafted the manuscript. T. Guha, R. Ghatak, and A. Naskar designed baseline pipelines, contributed to computational scaling experiments, and validated code integrity. K. K. Das supervised the research, reviewed statistical methodologies, and edited the manuscript."
   - *Status:* [x] Verified & Approved by Authors
8. **Use of Artificial Intelligence Disclosure:**
   - *Draft Statement:* "During the preparation of this manuscript and software repository, the authors utilized an agentic AI coding assistant (Google Antigravity, utilizing Gemini models including experimental flash/pro checkpoints) to assist with script execution, bibliographic checking against CrossRef APIs, figure plotting, LaTeX table formatting, and proofreading text. All conceptual formulations, empirical designs, and theoretical derivations were directed by the authors. The authors have conducted extensive cross-checks of the generated text, tables, figures, and code, and take responsibility for the scientific integrity of the reported findings."
   - *Status:* [x] Verified & Approved by Authors

---

## 3. Single Source of Truth Metrics (`paper/numbers.tex`)
All quantitative claims are bound to frozen Pass F execution stores:
- 13 benchmark datasets, 2,750 individual model fits, 11 baseline solvers.
- Omnibus Friedman test: $\chi_F^2 = 9.59, p = 0.48$, Nemenyi $CD = 4.19$ (no global dominance).
- High-D subgroup ($D/N > 20$): ICC-v2 Rank #1 with Mean ARI = 0.217 (vs Standard Consensus 0.037, DEC 0.045, K-Means 0.056).
- Grand Mean ARI: 0.152 (Rank 5.23).
- Golub Leukemia: ARI = 0.600, Khan SRBCT: ARI = 0.546.
- Asymptotic scaling: $N = 10^6$ in 55.6 s (3.05 GB peak RSS, 240 MB graph memory, 99.6% reduction over dense 8 TB).

---

## 4. Co-Author Pre-Submission Sign-Off Ledger

*Each co-author must review and sign below prior to any manual journal submission:*

- **Akash Kundu:** ___________________________ Date: ____________
- **Trinankur Guha:** ___________________________ Date: ____________
- **Rupankar Ghatak:** ___________________________ Date: ____________
- **Anubhab Naskar:** ___________________________ Date: ____________
- **Kalyan Kumar Das:** ___________________________ Date: ____________
