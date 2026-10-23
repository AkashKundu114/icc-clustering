# Scope Options for Manuscript Repositioning (Human Gate 2)

**Date:** 2026-10-21  
**Status:** DRAFTED FOR HUMAN AUTHOR DECISION (GATE 2)  
**Context:** Based on empirical audits in Fix Pass C (Tasks C1–C6), several initial hypotheses and claims have been clarified or bounded. This document outlines surviving claims, empirical limitations, and strategic venue/scope options for author selection.

---

## 1. Inventory of Surviving Empirical Facts

1. **Omnibus Benchmark Matrix (13 Datasets, 11 Methods, 1,430 Fits):**
   - Deep Embedded Clustering (DEC) achieves the lowest omnibus mean rank ($R=4.31$), followed by Standard Consensus ($R=5.08$), K-Means ($R=5.31$), Ward ($R=5.31$), and ICC-v2 ($R=5.46$).
   - The Friedman test yields $\chi_F^2 = 11.34, p = 0.33$, and the Nemenyi critical difference is $CD = 4.19$ ($k=11, N=13, \alpha=0.05$). There is no statistically significant separation among the top methods across the omnibus collection.
   - ICC-v2 achieves a Grand Mean ARI of $0.160$ vs. $0.131$ for DEC and $0.127$ for Standard Consensus.
   - **Crucial Caveat:** ICC-v2's Grand Mean ($0.160$) is heavily driven by two cancer microarray datasets: Leukemia ($\text{ARI} = 0.680$) and SRBCT ($\text{ARI} = 0.538$). Across the remaining 11 benchmarks, ICC-v2 averages only $\text{ARI} = 0.078$, and its omnibus median ARI is $0.045$.
2. **Exploratory High-Dimensional Subgroup ($D/N > 20$):**
   - Across the 6 biomedical datasets (CNS, Colon, Leukemia, Ovarian, Prostate, SRBCT), ICC-v2 achieves Mean Rank \#1 ($R=2.33$) with a subgroup mean ARI of $0.217$ (Table 4) to $0.226$ (Table 2).
   - Absolute gain over strongest baseline on SRBCT: $+0.388$ over FastMVC ($0.150 \pm 0.060$).
   - **Limitation:** On Prostate ($D=12{,}600, N=102$), ICC-v2 underperforms baselines ($0.013$ vs. $0.048$ for Ambient K-Means and $0.049$ for Standard Consensus).
3. **Anchor Certification / Ablation Result:**
   - Full ICC-v2 with certified determinacy anchors (V5) achieves a subgroup mean ARI of $0.226$ vs. $0.216$ for uniform random anchors (V4).
   - Paired mean difference: $\Delta = +0.010$, with a **bootstrap 95% CI of $[-0.028, +0.054]$**.
   - Because the 95% CI encompasses zero, determinacy anchor certification provides **no statistically significant accuracy improvement** over uniform random anchor selection.
   - The primary driver of performance is bipartite anchor ensembling under BGSS feature selection (V5 vs. V2: $\Delta = +0.145$, 95% CI: $[+0.070, +0.226]$).
4. **Computational Efficiency:**
   - At $N=10{,}000$ ($D=200$), ICC-v2 executes in $10.35 \pm 0.78\text{ s}$ vs. $29.96 \pm 1.93\text{ s}$ for Standard Consensus ($2.9\times$ speedup).
   - Peak dynamic memory is reduced from $2{,}670.6\text{ MB}$ to $68.8\text{ MB}$ ($97.4\%$ reduction). Working consensus graph memory is reduced from $762.8\text{ MB}$ to $3.06\text{ MB}$ ($99.6\%$ reduction).
   - On synthetic benchmarks with $D=100, K=5$, ICC-v2 scales linearly to $N=1{,}000{,}000$ in $55.6\text{ s}$ ($3.05\text{ GB}$ peak RAM).
5. **Inductive Out-of-Sample Extension:**
   - Stability-weighted centroid projection (Eq. 7) assigns query points in closed-form $O(K \cdot |\mathcal{F}_{\text{active}}|)$ time, achieving $\text{ARI} = 0.339$ on Leukemia and $0.392$ on SRBCT (vs. $0.172$ and $0.083$ for ambient K-Means).
   - Spectral Nyström extension achieves higher fidelity ($0.714$ on Leukemia and $0.455$ on SRBCT), demonstrating an explicit tradeoff between $O(K \cdot |\mathcal{F}_{\text{active}}|)$ centroid latency and $O(L \cdot |\mathcal{F}_{\text{active}}| + L K)$ spectral projection accuracy.

---

## 2. Positioning Options for Author Selection

### Option A: Narrowed Method Paper (Targeted High-D Regime)
- **Title Focus:** *"Geometry-Calibrated Consensus Clustering for High-Dimensional Noise Regimes"*
- **Core Narrative:** Position ICC-v2 not as an omnibus replacement for deep clustering or classical linkage, but as a specialized, linear-time architecture tailored for small-sample, high-dimensional regimes ($D/N > 20$) subject to isotropic distractor noise.
- **Framing:**
  - Honestly report fifth-place omnibus rank ($R=5.46, p=0.33$) and state that deep clustering (DEC) is superior on general multi-class benchmarks.
  - Highlight Rank \#1 on the high-D biomedical subgroup ($R=2.33$), with explicit disclosure of the two-dataset driver caveat (Leukemia/SRBCT) and Prostate failure.
  - Characterize determinacy certification as a stability and filtering heuristic rather than a source of statistical dominance over random anchors.
- **Likely Reviewer Objections:**
  - *Reviewer 1:* "Why does the method fail on Prostate, and why is the omnibus rank only fifth?" $\to$ Addressed by upfront scoping to $D/N > 20$ cancer microarray settings with distinct biological bimodality.
  - *Reviewer 2:* "Gain over random anchors is not significant ($\Delta=0.010$)." $\to$ Addressed by presenting anchor graph reduction as the primary architectural benefit.
- **Venue Tier:** Springer Nature *Pattern Analysis and Applications* (PAAP, Q2, IF 3.9) — **High Probability of Acceptance**.

### Option B: Empirical Falsification & Critical Study
- **Title Focus:** *"When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"*
- **Core Narrative:** Reposition as a rigorous empirical and methodological evaluation of consensus clustering assumptions in high-dimensional noise regimes.
- **Framing:**
  - Falsify the assumption that consensus averaging alone protects against distance concentration.
  - Disclose the null result of anchor certification ($\Delta = 0.010$, CI $[-0.028, 0.054]$) as an empirical finding: random anchors are surprisingly competitive with certified anchors.
  - Thoroughly document failure modes: platykurtic distributions in small cohorts, non-linear parity structures (Madelon), and high class counts ($K \ge 20$).
- **Likely Reviewer Objections:**
  - *Reviewer 1:* "Is this a new algorithm or an experimental benchmark paper?" $\to$ Requires clear structural framing under empirical software/data mining tracks.
- **Venue Tier:** *Data Mining and Knowledge Discovery* (DAMI, Q1) or *ACM Transactions on Knowledge Discovery from Data* (TKDD) — **Medium Probability; Higher Methodological Scrutiny**.

### Option C: Author Choice / Hybrid
- The author may provide specific modifications or alternate framing combinations.

---

## 3. Recommendation

We recommend **Option A** targeted at **Springer Nature PAAP**:
- Preserves the algorithmic contribution and software implementation of ICC-v2.
- Preempts reviewer hostility by openly disclosing empirical limitations (omnibus rank 5, two-dataset driver, Prostate failure, certification null CI).
- Aligns with the manuscript's current structure, figures, and Springer Nature template (`sn-jnl.cls`).
