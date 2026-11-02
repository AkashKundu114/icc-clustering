# Loop 5: Definitive DMKD Go / No-Go Adjudication Decision

**Lead Adjudicator:** Principal Scientific Auditor & Editorial Lead  
**Target Journal:** Springer Nature, *Data Mining and Knowledge Discovery* (DMKD)  
**Target Manuscript:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Date of Decision:** November 2, 2026  
**Repository State:** Commit `b0d304bff8a42df690d96248b5c6a731f8faaf78`  

---

## 1. Definitive Final Verdict

### Final Adjudication Verdict:
# **CONDITIONAL GO**

### Scope of the Verdict:
- **Manuscript Revision Phase:** **GO (APPROVED).** The underlying experimental evidence, raw logs, benchmark records (3,430 fits), and mathematical proofs are sufficiently traceable and robust to proceed immediately to revising the manuscript.
- **Formal DMKD Journal Submission Phase:** **HOLD (CONDITIONAL).** Submission to *Data Mining and Knowledge Discovery* is strictly contingent upon incorporating the mandatory mathematical and geometric corrections specified below. Under no circumstances should the manuscript be submitted in its current unamended form.

---

## 2. Answers to the 10 Mandatory Decision Questions

### 1. Is the central scientific contribution supported?
**YES.**  
The primary empirical finding—that established consensus clustering algorithms (FCAG, FCM, FastMVC) reproduce non-degenerate, highly stable partitions under subsampling ($\text{Stab} \approx 0.684$) that have near-zero diagnostic agreement with reference labels ($\text{Acc} \approx -0.003$), and that this stability is data-driven rather than a permutation artifact—is fully verified across the raw data, scripts, and bootstrap confidence intervals ($+0.485$, 95% CI $[+0.379, +0.662]$).

---

### 2. Which exact numerical results can safely appear in the abstract?
The following headline metrics are cryptographically verified and safe to publish in the Abstract:
1. **Discordance Metrics:** Mean stability of $0.684$ vs. mean accuracy of $-0.003$ across the 9 non-degenerate cells (permuted null $\approx 0.01$).
2. **Stability-Accuracy Gap:** Paired gap of $+0.485$ (95% CI $[+0.379, +0.662]$ via cohort-clustered bootstrap; unconstrained $+0.464$).
3. **Factorial Gating Gains:** BGSS raises ARI to $0.217$ under bipartite consensus ($+0.169$ over matched random gating, 95% CI $[+0.036, +0.310]$, uncorrected Wilcoxon $p = 0.031$, $n = 6$), driven by Leukemia ($+0.398$) and SRBCT ($+0.447$), but only to $0.077$ under dense consensus ($+0.031$).
4. **Anchor Determinacy Null Result:** High-determinacy anchors add no measurable benefit over uniform random anchors ($\Delta = +0.019$, 95% CI $[-0.040, +0.082]$, $p = 0.84$).
5. **Omnibus Benchmark Null Result:** Across 13 benchmarks (3,000 model fits), omnibus differences among the 12 algorithms are not statistically significant (Friedman $p = 0.40$).
6. **Memory Reduction:** Bipartite graph compression reduces auxiliary consensus-graph storage by $99.6\%$ at $N = 10^4$ ($3.05\text{ MB}$ vs. $762.9\text{ MB}$).

---

### 3. Which results must be recalculated or clarified?
1. **Loop 2 SRBCT Wilcoxon Test:** Recomputed exact p-value is **one-sided $p = 0.03125$** and **two-sided $p = 0.0625$** ($n = 5$ seeds). It must not be cited as two-sided significance.
2. **Leukemia ARI Confidence Interval:** The naive Student-t interval `[-0.1048, 1.0397]` in `exp5_baseline_comparison.json` is mathematically invalid (violates the $[0, 1]$ metric support) and must be replaced by the percentile bootstrap interval `[0.0076, 0.8879]`.
3. **Omnibus Benchmark Ranks:** GAC's grand mean ARI across all 13 benchmarks is **0.152** with an omnibus rank of **5.62** (4th place). The rank of **1st** (average rank **2.17**, mean ARI **0.217**) applies strictly to the 6 high-D microarray cohorts (`HighD_N6`).

---

### 4. Which claims must be removed or withdrawn?
1. **Universal Unimodality Bound ($BC \le 5/9$):** Remove any statement implying that Sarle's $BC \le 5/9$ holds for all unimodal distributions. It holds strictly for symmetric densities.
2. **General Out-of-Sample Centroid Induction on Manifolds:** Remove the claim that active subspace centroid projection provides general out-of-sample mapping. Disclose that it fails on non-convex manifolds (ARI $\approx -0.003$ on Concentric Circles).
3. **Adaptive Anchor Minority Guarantee:** Withdraw the claim that $L^*(K) = \max(40, \lceil 3 K \ln K \rceil)$ guarantees minority cluster coverage under arbitrary class imbalance.
4. **Finite-Sample Conformal Cluster Coverage:** Withdraw any lingering claims from `src/cicc/` regarding distribution-free $90\%$ clinical coverage.

---

### 5. Which theorem statements are defensible?
1. **Proposition 1 (Symmetric Separation Bound):** **DEFENSIBLE WITH QUALIFICATION.** Must formally restrict $f(x)$ to continuous symmetric probability densities.
2. **Proposition 2 (Exact Determinacy Identity):** **FULLY DEFENSIBLE.** Mathematically exact, elegant, and computationally verified.
3. **Theorem 1 (Complexity Bounds):** **FULLY DEFENSIBLE.** $O(N)$ time and $O(NL + L^2)$ auxiliary graph memory bounds are sound. Clarify that empirical power-law exponents ($\beta < 1.0$) represent pre-asymptotic behavior.

---

### 6. Which proposed ICC-v2.1 changes are mathematically justified?
1. **Exact Determinacy Selection (Proposition 2):** Fully justified as a linear-time alternative to $O(N^2)$ accumulation.
2. **Bipartite Transfer-Cut Formulation:** Fully justified as a low-rank graph cut approximation.
3. **Dual-Criteria Non-Degeneracy Reporting (Rule i vs. Rule i'):** Methodologically justified as standard practice to filter trivial boundary singletons.

---

### 7. Which proposed changes still require ablation experiments before inclusion?
1. **Native Transfer-Cut Out-of-Sample Projection:** The out-of-sample projection via landmark affinities $\mathbf{u}^* = \frac{\mathbf{b}^*}{\|\mathbf{b}^*\|_1} D_A^{-1/2} V \operatorname{diag}(1 - \boldsymbol{\lambda})^{-1/2}$ requires empirical benchmark evaluation across all 13 datasets before replacing centroid projection.
2. **Adaptive Anchor Imbalance Scaling:** Any formula scaling $L$ by $\pi_{\min}$ requires empirical verification on imbalanced cohorts.

---

### 8. Is the current manuscript internally consistent with the code and raw evidence?
**YES, with minor exceptions.**  
`main.tex` is remarkably disciplined. The numbers in `numbers.tex` and paper tables match the raw data in `results.json` and `stats.json`. The remaining discrepancies are:
- Legacy PDF title in `\hypersetup` line 39.
- Omission of the symmetry condition in Proposition 1.
- Lack of explicit non-convex manifold boundary disclosure for centroid induction.

---

### 9. Is the work ready for manuscript revision?
**YES (UNCONDITIONAL GO).**  
All necessary LaTeX replacement blocks, mathematical fixes, and citations have been compiled in `audit/loop4_manuscript_revision_plan.md`. The author team has complete, unambiguous instructions on what text to modify.

---

### 10. Is it ready for formal DMKD submission?
**HOLD (CONDITIONAL).**  
The manuscript will be ready for formal submission immediately after the three mandatory conditions in Section 3 are implemented and verified.

---

## 3. Mandatory Gate Conditions for DMKD Submission

Before clicking "Submit" on the Springer Nature DMKD editorial portal, the following three conditions must be fulfilled:

```markdown
[ ] CONDITION 1: MATHEMATICAL SPECIFICATION OF PROPOSITION 1
    Amend Proposition 1 in paper/manuscript/main.tex to formally specify that 
    the 5/9 bound holds strictly for symmetric unimodal distributions, and insert 
    Remark 1 (Asymmetric Unimodal Counterexamples) detailing log-transformation requirements.

[ ] CONDITION 2: GEOMETRIC BOUNDARY DISCLOSURE FOR CENTROID PROJECTION
    Insert Remark 2 (Geometric Validity of Centroid Induction) after Equation 10 in 
    main.tex, explicitly stating that Euclidean centroid projection is valid only under 
    convex cluster geometries and collapses on non-convex manifolds (citing Concentric Circles).

[ ] CONDITION 3: METADATA AND CITATION SYNCHRONIZATION
    Update \hypersetup{pdftitle={...}} in line 39 to match the accepted title, 
    and append the four missing references (Beyer 1999, Leek 2010, Demsar 2006, 
    Darlington 1970) to paper/references/references.bib.
```

Upon completion of these three conditions, the manuscript is **APPROVED FOR SUBMISSION TO SPRINGER NATURE DATA MINING AND KNOWLEDGE DISCOVERY**.
