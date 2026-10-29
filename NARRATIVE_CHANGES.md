# Narrative and Methodological Changes Register (NARRATIVE_CHANGES.md)

This document records all scientific, empirical, and textual narrative revisions made to the manuscript:  
**"When Do Feature Gating and Anchor Consensus Help High-Dimensional Clustering? An Empirical and Geometric Analysis"** (ICC-v2).

---

## 1. Title De-Biasing and Harmonization (Item 6)
- **Previous Title:** *"When Does Feature Gating and Anchor Consensus Salvage High-Dimensional Clustering? An Empirical and Geometric Analysis"*
- **Revised Neutral Title:** *"When Do Feature Gating and Anchor Consensus Help High-Dimensional Clustering? An Empirical and Geometric Analysis"*
- **Rationale:** The verb "Salvage" overstates the empirical rescue capability, given that ICC-v2 does not salvage performance across non-linear parity (Madelon), sparse counts (PBMC68k), or large-$K$ datasets. "Help" accurately reflects the measured gains on continuous small-sample high-$D$ cohorts without overclaiming.
- **Affected Locations:** `paper/main.tex`, `springer_manuscript/main.tex`, `README.md`, `pyproject.toml`, `paper/README.md`, `results/PLAN.md`, `submission/COVER_LETTER.md`, `AGENTS.md`, `docs/THEORETICAL_FOUNDATIONS.md`.

---

## 2. Dual-Number Paradox Resolution & Canonical Seeds (Item 1)
- **Root Cause Identified:** Earlier drafts mixed results from two different seed sets:
  - Canonical benchmark tables: 30 seeds $\{0, \dots, 29\}$ on 6 high-$D$ cohorts $\to V_5 = 0.217$, $V_4 = 0.198$.
  - Exploratory Exp 8 drafts: 10/30 exploration seeds $\{42, \dots, 71\}$ $\to V_5 = 0.225$, $V_4 = 0.190$.
- **Action Taken:** Reran Exp 8b (anchor selection) and Exp 8c (feature gating) across all 30 canonical benchmark seeds $\{0, \dots, 29\}$ on the six high-$D$ cohorts:
  - Full ICC-v2 ($V_5$, Core Anchors): Subgroup mean **0.2168** (0.217).
  - Random Anchors ($V_4$): Subgroup mean **0.1980** (0.198).
  - Difference $V_5 - V_4 = \mathbf{+0.0188}$ (+0.019), 95% bootstrap CI $[-0.039, +0.082]$, Wilcoxon $W = 9.0, p = 0.84375$ ($n=6$, non-significant).
  - KMeans Anchors: $0.1243 \pm 0.198$; Balanced Anchors: $0.1186 \pm 0.188$.
- **Exp 8f Parameter Sensitivity Clarification:** The sensitivity grid spanning $M \in \{5, 10, 15, 25, 50\} \times L \in \{20, 40, 60, 80\}$ evaluated 10 exploration seeds $\{42, \dots, 51\}$, reaching $0.225 \pm 0.128$ at $M=25, L=40$; on the full 30 benchmark seeds, the default configuration yields the canonical 0.217. Both seed lists and contexts are now explicitly defined in the text.
- **Protocol Pre-Registration:** Defined explicit seed sets for Exp 8a through 8f in Sec 6.2.

---

## 3. BGSS Effect Decomposition & CoHiRF Contextualization (Item 2)
- **Matched Control Isolation:** Random subspace gating within ICC-v2's bipartite pipeline scores **0.1547** (0.155) on the 30 benchmark seeds.
- **True BGSS Screening Effect:**
  - BGSS ($0.217$) vs. Matched Random Gating ($0.155$): $\Delta = \mathbf{+0.0621}$ (+0.062), 95% dataset-clustered bootstrap CI $[+0.0129, +0.1419]$, Wilcoxon $W = 1.0, p = 0.0625$ ($n=6$).
- **Overall Gain Decomposition:**
  - Ambient Consensus ($0.037$) $\to$ Random-Subspace Bipartite Ensemble ($0.155$): $\mathbf{+0.118}$ (**65.6%** of total gain).
  - Random Gating ($0.155$) $\to$ BGSS Multimodality Screening ($0.217$): $\mathbf{+0.062}$ (**34.4%** of total gain).
  - Replaced $V_5 - V_3$ as the primary "BGSS effect" in Table 15 (retained $V_3$ only as a descriptive ambient row).
- **CoHiRF Claim Revision:** Deleted the assertion that "unguided random feature drawing struggles in extreme noise" (contradicted by the 0.155 result). Attributed CoHiRF's 0.017 subgroup mean to the method configuration as run (official implementation evaluated under repetitions $= 25$, subspace fraction $= 0.15$, consensus threshold $= 0.80$; Table 2), which enforces strict hierarchical consensus over unanimous components without bipartite graph spectral projection, causing cluster fragmentation under ambient noise.

---

## 4. Geometric Analysis and Distance Concentration (Item 3)
- **Sec 3 Rewritten Around Eq. (2):** Placed the distance concentration limit equations first, followed by empirical simulation results across $D_{\text{noise}} \in [0, 2000]$.
- **Minkowski Geometry Insights:** Chebyshev distance ($L_\infty$) retains an order-of-magnitude higher relative contrast ($C = 1.341 \pm 0.190$) and elevated subspace separation ($\rho_{\text{sep}} = 1.039 \pm 0.005$) at $D_{\text{noise}}=2000$ compared to Euclidean distance ($C = 0.131 \pm 0.012, \rho_{\text{sep}} = 1.002 \pm 0.000$).
- **Method Retention vs Collapse:** Spectral clustering with Chebyshev distance retains ARI $0.597 \pm 0.091$ and Cosine retains $0.308 \pm 0.072$, whereas Euclidean Spectral ($0.004 \pm 0.005$) and K-Means ($0.019 \pm 0.018$) collapse completely.
- **Connection to ICC-v2 Bound:** Connected directly to Theorem 1 anchor projection bound: BGSS feature screening bounds effective distractor dimension $D_{\text{noise}}$, preventing observable manifold collapse and preserving $\rho_{\text{sep}} \gg 1$.
- **Full Geometry Table & Citation:** Added full Table `tab:exp8d_distance` (`paper/gen/table_exp8d_distance.tex`) and cited Peng et al. (arXiv:2401.00422).

---

## 5. Large-$K$ Anchor Budget Scaling (Exp 8e) (Item 3a)
- **Refutation of Anchor Starvation:** Evaluated $L = 40$ vs $L = \max(40, 10K)$ across 4 large-$K$ benchmarks (Indian Pines, Isolet, 20 Newsgroups, Extended Yale B). Average ARI shifted marginally from $0.123$ to $0.132$ ($\Delta = +0.009$).
- **Wording Standard:** Wrote: *"refutes anchor starvation as the main cause; the multi-class coordinate-blending explanation is consistent with but not tested by these data"*.
- **Per-Dataset Table:** Embedded full Table `tab:exp8e_large_k` (`paper/gen/table_exp8e_large_k.tex`).

---

## 6. Sample Complexity Scalability & Throttling Isolation (Item 4)
- **Artifact Isolation:** The timing jump at $N=8000$ in earlier preliminary drafts was diagnosed as an artifact of host CPU throttling / swap contention on a shared testbed.
- **Dedicated Hardware Rerun:** Re-executed across $N \in \{500, 1000, 2000, 5000, 8000, 10000\}$ with 5 canonical seeds ($42, 101, 202, 303, 404$) on an isolated idle host (AMD Ryzen 9 8940HX, logged CPU freq 2401 MHz, load ~13%, RAM, swap):
  - $N=500$: $0.323 \pm 0.007\text{ s}$
  - $N=1000$: $0.420 \pm 0.010\text{ s}$
  - $N=2000$: $0.650 \pm 0.008\text{ s}$
  - $N=5000$: $1.175 \pm 0.014\text{ s}$
  - $N=8000$: $1.382 \pm 0.019\text{ s}$
  - $N=10000$: $2.302 \pm 0.497\text{ s}$ ($0.962 \pm 0.095\text{ s}$ without tracing overhead)
  - Power-law scaling exponent: $\beta = 0.618$ (vs Standard Consensus $\beta = 0.917$, steepening to $\beta > 1.5$ above 5k, reaching $4.362\text{ s}$ and $2.67\text{ GB}$ RAM).
- **Synchronized Artifacts:** Updated Table 4 (`paper/gen/table4_scaling_n.tex`), text in Sec 6.4, and re-rendered Figure 18 (Figure 4) via `plot_exp4_figures.py`.

---

## 7. Reference Vintage & Supplementary Table S1 (Item 5)
- **Verified Bibliography:** 48 total references in `refs.bib`, 100% verified via CrossRef/arXiv APIs or primary manual sources (`scripts/verify_refs.py`, exit 0).
- **Vintage Split:** 38 of 48 references (**79.2%** / ~80%) published in 2024–2026.
- **Supplementary Table S1:** Added `tab:supp_foundations` (`paper/gen/tableS1_foundational_refs.tex`) compiling the seminal foundational sources for all benchmark baselines (MacQueen 1967, Arthur & Vassilvitskii 2007, Ward 1963, Bezdek 1981, von Luxburg 2007, Breiman 2001, Bengio et al. 2013).

---

## 8. Statistical Ties, Rounding & OpenML Audits (Item 7)
- **Tie Convention:** Stated explicitly in Sec 6.3 that ties are resolved via the standard average mid-rank convention (`scipy.stats.rankdata(..., method='average')`).
- **Unrounded vs Rounded Friedman:**
  - Direct calculation on unrounded per-seed means: $\chi_F^2 = 11.56, p = 0.40$ (ICC-v2 omnibus rank 5.62).
  - Calculation on 3-decimal rounded benchmark table: $\chi_F^2 = 11.54, p = 0.40$ (ICC-v2 omnibus rank 5.58). Both confirm null retention ($p = 0.40 \gg 0.05$).
- **OpenML Metadata Verification:** Verified OpenML IDs match $N, D, K$ in Table 6: Sonar (40), Madelon (1485), Colon (45087), SRBCT (45101), CNS (45086), Leukemia (1104), Prostate (45099), Ovarian (45098), Isolet (300).
- **Reproducibility Verification:** `scripts/fetch_data.py --verify-only` verified all 13 benchmarks present and checksum-valid.
