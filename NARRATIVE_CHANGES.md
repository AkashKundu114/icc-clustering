# Narrative and Methodological Changes Register (NARRATIVE_CHANGES.md)

This document records all scientific, empirical, and textual narrative revisions made to the manuscript:  
**"Stable but Wrong: Why Consensus Clustering Can Fail in High Dimensions, and What Helps"** (GAC Pipeline).

---

## Formal Title and Terminology Modernization (Item 0)
- **Updated Formal Title:** *"Cluster Stability and Feature-Gated Bipartite Ensemble Learning for High-Dimensional Noisy Data: An Empirical Analysis"*
- **Running Head:** *Cluster Stability and Feature-Gated Bipartite Ensemble Learning*
- **Purge of Informal / Sensational Terminology:**
  - "Stable but Wrong" criterion -> "stability-accuracy discordance (SAD) criterion"
  - "stability trap" -> "stability-accuracy discordance"
  - "entrapment" / "trapped in spurious consensus" -> "convergence to partitions unrelated to the reference labels"
  - "pathology" -> "behavior"
  - Replaced dramatic adjectives ("massive" -> "large", "severe" -> "substantial", "firmly" -> "excluding zero").
  - Changed "proving that high stability does not indicate correctness" -> "indicating that high stability does not imply correctness".
- **Abstract Word Count & Scoping:** Abstract strictly calibrated to 248 words (<= 250 words) without claiming "stable clustering" as an intrinsic property of the GAC pipeline.

---

## 0. Title Alignment and Reframing: "Stable but Wrong"
- **New Title:** *"Stable but Wrong: Why Consensus Clustering Can Fail in High Dimensions, and What Helps"*
- **Short Title / Running Head:** *Why Consensus Clustering Can Fail in High Dimensions*
- **Algorithmic Relabeling:** "ICC-v2" relabeled to "GAC pipeline" (Gated Anchor Consensus pipeline) and "ICC-v1" relabeled to "ungated anchor consensus" across manuscript text, tables, and scripts; added historical notice that `icc-clustering` repository name is historical and distinct from Race & Meyer (2013).
- **Opening Focus:** Shifted the paper's opening from abstract algorithmic proposals to the empirical and theoretical *stability trap*: base clusterers and consensus methods converge with deceptively high agreement ($\text{Stab} \ge 0.50$ to $1.00$) onto arbitrary noise partitions while empirical accuracy collapses near zero ($\text{ARI} \le 0.05$).
- **Reordered Contributions:**
  1. *The Stability Trap in High Dimensions:* Empirical falsification in finite-sample simulations and real biomedical cohorts.
  2. *What Helps:* The GAC pipeline, linear-time BGSS moment gating ($O(ND)$), and bipartite anchor graph compression ($O(NL)$ auxiliary memory, 99.6% compression at $N=10^4$).
  3. *What Fails:* Boundary conditions and negative results (determinacy null result $\Delta = +0.019$, Prostate/CNS weak bimodality, Madelon XOR parity, scRNA-seq zero-inflation, and large $K$).
- **Real-Data Stability Findings:**
  - Evaluated 13 benchmark datasets across 11 models with saved per-seed partitions.
  - Documented severe stability-accuracy gaps ($\Delta = \text{Stab} - \overline{\text{ARI}}$) on high-$D$ cohorts ($D/N > 20$): Ward ($\Delta = +0.968$), Spectral ($\Delta = +0.964$), FCM ($\Delta = +0.897$), FCAG ($\Delta = +0.842$), FastMVC ($\Delta = +0.710$), Standard Consensus ($\Delta = +0.656$), Core-Halo ($\Delta = +0.612$).
  - Identified that CoHiRF's lower gap ($\Delta = +0.259$) stems from instability ($\text{Stab} = 0.279$) rather than true cluster recovery ($\overline{\text{ARI}} = 0.021$).
  - Showed that GAC achieves the lowest gap ($\Delta = +0.268$) and breaks out of the trap on Leukemia ($\text{ARI}=0.600, \text{Stab}=0.567, \Delta=-0.032$) and SRBCT ($\text{ARI}=0.546, \text{Stab}=0.541, \Delta=-0.005$), while transparently reporting that on Prostate and CNS, weak marginal bimodality limits GAC's accuracy ($\text{ARI}=0.012$ and $0.021$).
- **Related Work Additions:** Integrated Senbabaoglu et al. (2014, consensus reassessment), Race & Meyer (2013, iterative consensus), Fern & Brodley (2003, random subspaces), Lindenbaum et al. (2021, gated Laplacian), and Chen (2026, variational clustering with feature gating).

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


---

## 9. Subsample Stability & Null Control Protocol (Revision Item 1)
- **Protocol Pre-Specification:** Authored `results/PLAN_STAB.md` pre-specifying 6 cohorts ($D/N > 20$), 12 Table 7 models, 30 stratified 80% subsamples (seeds 5000–5029), independent column-permuted null control (seeds 6000–6029), and Decision Rules (i), (ii), (iii).
- **Execution:** Completed 4,320 runs in parallel with PyTorch CUDA GPU acceleration on NVIDIA RTX 5060 Laptop GPU.
- **Empirical Findings:**
  - Rule (i) ("Stable but Wrong": $\text{Stab} \ge 0.50, \text{Acc} \le 0.05$): Satisfied on $\ge 3$ cohorts by 3 methods: FCAG (Colon, CNS, Prostate), FCM (Colon, CNS, Ovarian), FastMVC (Colon, CNS, Prostate).
  - Prostate Entrapment: 10 of 12 methods satisfy Rule (i) on Prostate ($D=12{,}600$), with Ward ($\text{Stab}=0.996, \text{Acc}=0.026, \Delta=+0.970$), Spectral ($\text{Stab}=0.971, \text{Acc}=-0.002, \Delta=+0.973$), Core-Halo ($\text{Stab}=1.000, \text{Acc}=0.000, \Delta=+1.000$), GAC ($\text{Stab}=0.860, \text{Acc}=0.012, \Delta=+0.847$), while column-permuted null controls collapse to near zero ($-0.001$ to $+0.049$).
  - Rule (iii) Paper-Level Claim: Supported by the data. Paired cohort bootstrap ($B=10{,}000$) for the stability-accuracy gap firmly excludes zero ($+0.464$, 95% CI: $[+0.363, +0.607]$).
- **Narrative Updates:** Rewrote Abstract, Contributions, and Section 3.1 to strictly report subsample stability metrics and null controls.

---

## 10. Scalability & Timing Hygiene (Revision Item 2)
- **Untraced Execution Rerun:** Reran pure untraced execution time (`time.perf_counter()`) across $N \in \{500, 1000, 2000, 5000, 8000, 10000\}$ and 5 canonical seeds ($42, 101, 202, 303, 404$), measuring memory footprint separately via `tracemalloc`.
- **Table 4 / Table 6 Fix:** Fixed `\pm nan` in table generator by properly computing standard deviation across the 5 seeds ($0.736 \pm 0.089\text{ s}$ at $N=500$, $0.835 \pm 0.030\text{ s}$ at $N=10{,}000$).
- **Figure 18 Caption:** Deleted approximate $\beta \approx 1.0$ and $2.9\times$ speedup; reported fitted exponent $\beta = 0.09 \pm 0.17$ (95% CI: $[-0.03, 0.24]$) across full range ($\beta \approx 0.81$ over $N \in [500, 5000]$) and $3.80\times$ speedup at $N=10{,}000$ ($0.835\text{ s vs } 3.175\text{ s}$).
- **De-Speculation:** Removed CPU throttling speculation; replaced with "the jump at N=8,000 observed in an earlier run was not reproduced in the final runs" (5 independent reruns) with telemetry preserved in `results/timing_rerun_environment_log.json`.

---

## 11. Consistency & Attribution Hygiene (Revision Item 3)
- **Standard Deviation Consistency:** Reconciled Leukemia and SRBCT SDs in narrative text to match Table 7 per-seed SD across 30 seeds ($0.600 \pm 0.367$ and $0.546 \pm 0.102$).
- **Abstract Subgroup Comparison:** Updated Abstract to compare GAC ($0.217$) with the best baseline in the high-$D$ subgroup (FCAG, $0.065$) and ambient consensus ($0.037$).
- **CoHiRF Attribution:** Rewrote CoHiRF paragraphs to strictly attribute performance to the method configuration as run (reimplementation adhering to official specification with 25 repetitions, 0.15 subspace fraction, 0.80 unanimous threshold).
- **Section 4 Header:** Renamed to "Proposed Methodology (Gated Anchor Consensus Pipeline)".
- **Literature Descriptions:** Rewrote Senbabaoglu et al. (consensus produces apparent stability on weak/no structure) and Race & Meyer (iterative consensus extracts confident clusters and reclusters residuals) to match primary literature accurately.
- **Citation Hygiene:** Removed "cite-once" policy in `AGENTS.md` and restored standard academic citation discipline.

---

## 12. Bibliography Expansion (Revision Item 4)
- **Recent Literature Share:** Added 14 verified 2024–2026 citations to `paper/references.bib` and `springer_manuscript/references.bib`, increasing recent literature share from 75.0% (39/52) to **80.3%** (53/66).
- **Verification:** 100% verified via `scripts/verify_refs.py` (exit code 0, 58 OK, 8 MANUAL).
- **Mapping:** All 14 entries mapped in `results/refs_map.csv` and cited in the manuscript.

---

## Clean Controlled Scaling Benchmark & Exponent Recalibration (Revision Item 1)
- **Monotonicity & Hygiene:** Executed a clean, single-process, idle-workstation scalability rerun across $N \in \{500, 1000, 2000, 5000, 8000, 10000\}$ with 5 canonical seeds ($42, 101, 202, 303, 404$), fixed power plan, warm-up discards logged to `results/scaling_warmup.csv`, and pre-/post-run telemetry (CPU frequency, CPU load %, swap usage) logged to `results/scaling_env.csv`.
- **Anomalous Drop Resolution:** Completely eliminated the historical host-contention artifact (where runtime fell from 4.76 s at $N=5000$ to 0.835 s at $N=10000$ due to system CPU/swap thrashing). Runtimes are now strictly monotonic in $N$:
  - GAC: $0.836 \pm 0.096\text{ s}$ ($N=500$), $1.081 \pm 0.084\text{ s}$ ($N=1000$), $1.725 \pm 0.177\text{ s}$ ($N=2000$), $3.065 \pm 0.415\text{ s}$ ($N=5000$), $3.276 \pm 0.978\text{ s}$ ($N=8000$), $4.354 \pm 1.252\text{ s}$ ($N=10000$).
  - Dense Standard Consensus: $0.854 \pm 0.095\text{ s}$ ($N=500$), $0.999 \pm 0.198\text{ s}$ ($N=1000$), $1.627 \pm 0.245\text{ s}$ ($N=2000$), $3.477 \pm 0.405\text{ s}$ ($N=5000$), $7.019 \pm 1.115\text{ s}$ ($N=8000$), $11.046 \pm 2.055\text{ s}$ ($N=10000$).
- **Power-Law Exponent Recalibration:**
  - GAC global empirical power-law exponent: $\beta = 0.548 \pm 0.013$ ($95\%$ seed-bootstrap CI: $[0.527, 0.568]$) across full range (local exponents: $\beta_{500 \to 1000} = 0.371$, $\beta_{1000 \to 2000} = 0.674$, $\beta_{2000 \to 5000} = 0.627$, $\beta_{5000 \to 8000} = 0.142$, $\beta_{8000 \to 10000} = 1.275$).
  - Dense consensus power-law exponent: $\beta = 0.851 \pm 0.010$ ($95\%$ CI: $[0.834, 0.867]$).
- **Speedup Recalibration:**
  - GAC empirical speedup over dense consensus at $N=10000$: $2.54\times$ aggregate ($4.354\text{ s}$ vs. $11.046\text{ s}$), mean per-seed ratio $2.699 \pm 0.842\times$. Replaced previous non-credible $3.80\times$ speedup claims.
- **Table 6 Reconciled with Table 7:** Explicitly documented that Table 6 measures synthetic data with $D=200, K=3$ under pure untraced execution ($4.354\text{ s}$), whereas Table 7 Config A measures $D=100, K=5$ with inline memory tracking overhead ($5.58\text{ s}$), without attributing unmeasured causes.
- **Synchronized Artifacts:** Updated Table 6 (`paper/gen/table04_sample_scaling.tex`, `springer_manuscript/gen/table04_sample_scaling.tex`), Figure 5a/5b, `paper/main.tex`, `springer_manuscript/main.tex`, and `results/stats.json`.
