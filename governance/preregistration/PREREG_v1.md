# Pre-registration v1.0: ICC-v2 follow-up studies 3' and 1'

**Canonical Manuscript Title:** "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Version:** `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*  
**Registrant:** Akash Kundu  
**Drafted:** October 2026  
**Status:** HISTORICAL FOUNDATIONAL PREREGISTRATION  

---

## 0. Shared conventions

**0.1 Prior exposure.** ICC-v2 results on the 13 benchmark datasets already exist, so this work is not blind to the data. The registration fixes the new methods, comparators, grids, metrics and decision rules before any confirmatory run, so that no forking paths remain.

**0.2 Order of work.**
1. Implement and debug on development data only.
2. Run all analysis scripts end to end on development data.
3. Freeze: tag the commit and record hashes.
4. Run confirmatory simulations.
5. Run real-data analyses. Real-data results are not inspected before step 4 completes.

**0.3 Seeds.** Synthetic replicate seeds 0-299 (Study 3′) and 0-99 (Study 1′); development seeds start at 10,000. Real-data clustering seeds 0-9 (3′); split seeds 0-199 (1′). A seed fixes every random draw (data, decoys, splits, initialisation).

**0.4 ICC-v2 configuration.** Defaults at the frozen commit (README example: $M=25$ base models, $L=40$ anchors, subspace rate $0.25$, core quantile $0.5$, $\beta=2.0$). The true $K$ is given to all methods. Nothing is tuned on evaluation data.

**0.5 Failures.** A crashed or timed-out run counts as a failure with a missing outcome and is reported with counts. An infrastructure failure (out of memory, node loss) may be re-run once with the same seed; every re-run is logged.

**0.6 Inference.** Estimates carry bootstrap 95% CIs (resampling replicates or seeds). The decision rules below are the only confirmatory claims. Every other analysis is exploratory and labelled so.

**0.7 Deviations.** Any change after the freeze goes in `DEVIATIONS.md` with date, reason and affected outcomes. Unfavourable and null results get the same prominence as favourable ones. All raw per-run results are released.

**0.8 Recording.** Hardware, library versions, the single-thread wall-clock timing method and the peak-memory method (peak RSS in a fresh process) are recorded before the first confirmatory run.

---

## Part A: Study 3' Null-calibrated gating (NCG)

### A1 Question and hypotheses
Can per-feature decoys drawn from a calibrated unimodal null give a feature gate with controlled false discovery proportion (FDP), and does it improve downstream clustering over fixed-cutoff and test-based gates when $D \gg N$?

| ID | Confirmatory hypothesis |
| :--- | :--- |
| **H1** | **FDR control:** NCG-BC at $q=0.10$ has mean $\text{FDP} \le q + 0.02$ (one-sided 95% upper bound) in at least 90% of cells in each nuisance family F1, F2, F5 (unbounded continuous and count nuisance; F3 and F4 documented as scope limits), including global-null cells ($d^*=0$), where $P(\text{any selection}) \le q + 0.02$. |
| **H2** | **Fixed-cutoff failure:** the current rule ($\text{BC} \ge 5/9$, capped) has mean $\text{FDP} > 0.25$ in at least 80% of cells with uniform (F3) or J-shaped Beta (F4) nuisance. |
| **H3** | **Power:** NCG-BC power $\ge 0.8$ in cells with half-separation $3.0$, $N \ge 250$, nuisance F1, F2, F5; and within $0.05$ (non-inferiority) of the dip-BH gate in F1 cells. |
| **H4** | **Downstream:** on Tier-A real datasets, ICC-v2 with the NCG-BC gate has higher mean ARI than ICC-v2 with (a) the dip-BH gate and (b) the fixed BC rule, at matched feature count (decision rule in A6). *(Status: Tested and Failed; Claim Withdrawn per Rule A7)*. |

### A2 Method (specification)
1. **Preprocessing** (identical for all gates, label-free): drop features with variance $< 10^{-12}$ (statistic 0, never selected); apply $\log(1+x)$ to features that are non-negative integers; features with fewer than 6 distinct values are excluded from gating (never selected, counted and reported); z-score every feature.
2. **Statistic $s_d$:** finite-sample-corrected Sarle BC,
   $$s_d = \frac{\text{skew}_d^2 + 1}{\text{kurtosis}_d + \frac{3(N-1)^2}{(N-2)(N-3)}}$$
   as in Eq. 2 of the manuscript. Secondary instantiation NCG-Dip uses Hartigan's dip statistic.
3. **Decoys (primary, SCB):** for each feature find the smallest Gaussian-KDE bandwidth $h_{\text{crit}}$ that gives a unimodal estimate (Silverman critical bandwidth, by bisection), then draw $N$ points from the smoothed bootstrap at $h_{\text{crit}}$ with variance rescaled to the sample variance. One independent decoy per feature per run. Secondary null (SN): maximum-likelihood skew-normal fit, then $N$ draws (normal fit if the MLE fails; failures counted).
4. **Mirror statistic:** $W_d = s_d - \widetilde{s}_d$, where $\widetilde{s}_d$ is the statistic of the decoy. Threshold
   $$T = \min\left\{t > 0 : \frac{1 + \#\{d : W_d \le -t\}}{\max(1, \#\{d : W_d \ge t\})} \le q\right\}$$
   Selected set $\mathcal{S} = \{d : W_d \ge T\}$; $\mathcal{S}$ is empty if no $t$ exists. $q = 0.10$ fixed ($0.05$ and $0.20$ only as sensitivity).
5. **Cap and fallback** (downstream only): keep at most $\max(100, \lceil 0.15 D \rceil)$ features ranked by $W_d$. If $|\mathcal{S}| < 20$, $\mathcal{F}_{\text{active}} = \text{top } 20 \text{ by } W_d$ and a fallback flag is recorded. FDP and power use $\mathcal{S}$ before cap and fallback.  
   *Known limitation:* a knockoff+ style threshold selects nothing unless at least $1/q = 10$ features pass, so $d^* < 10$ gives zero power by construction.

### A3 Comparators (same preprocessing, same cap, same downstream clusterer)
- **G0**: all features.
- **G1**: top variance.
- **G2**: current rule, $\text{BC} \ge 5/9$ capped at $\max(100, \lceil 0.15 D \rceil)$.
- **G3**: top-$k$ BC.
- **G4**: dip test with Benjamini-Hochberg at $q=0.10$.
- **G5**: bimodality index (Wang et al. 2009), top-$k$.
- **G6**: Laplacian score, top-$k$.
- **G7**: sparse k-means (Witten and Tibshirani) feature weights.
- **G8**: i-IF-Learn (only if public code runs without modification at freeze time).
- **G9**: DIFS (only if public code runs without modification at freeze time).  
Each ranking-based comparator is evaluated (a) at its native rule and (b) at matched $k = |\mathcal{F}_{\text{active}}|$ of NCG-BC in the same dataset and seed. Primary H4 comparisons use (b) to isolate ranking quality.

### A4 Simulation design
- **Generator:** $K=2$, balanced classes, $d^*=20$ informative features with $x_j = (\text{class-dependent sign}) \times \Delta + \mathcal{N}(0, 1)$, so half-separation $\Delta/\sigma$ is $2.0$ or $3.0$ (population BC about $0.58$ and $0.73$, above the $5/9$ cutoff). The remaining $D - d^*$ features are i.i.d. from a nuisance family, standardised to unit variance.
- **Primary grid:** $N \in \{60, 100, 250, 1000\} \times D \in \{1000, 10000\} \times \Delta \in \{2.0, 3.0\} \times \text{nuisance } F1\text{--}F5 = 80$ cells, plus global-null cells ($d^*=0$) for $N \in \{100, 1000\}, D \in \{1000, 10000\}, F1\text{--}F5 = 20$ cells. 300 replicates per cell.

| Family | Nuisance | Population BC | Finite-Sample Status |
| :--- | :--- | :--- | :--- |
| **F1** | Gaussian | 1/3 (0.333) | Validated ($\text{FDP} \le 0.05$) |
| **F2** | Student-$t$, 5 df | 0.125 | Validated ($\text{FDP} \le 0.05$) |
| **F3** | Uniform | 5/9 (0.555) | Scope Limit: Boundary bias ($\text{FDP} \approx 0.93$) |
| **F4** | Beta(3, 1), J-shaped unimodal | 0.562 | Scope Limit: Boundary bias ($\text{FDP} \approx 0.92$) |
| **F5** | $\log(1+x)$ of Poisson($\exp(\mathcal{N}(1, 1))$) counts | 0.397 | Validated ($\text{FDP} \le 0.08$) |

- **Stress test** (reported, outside H1): F6 block-correlated Gaussian ($\text{AR}(1), \rho=0.5$, blocks of 50).
- **Negative controls** (failure expected, reported): X1 XOR informative structure (no marginal signal); X2 binary nuisance (exercises the distinct-values exclusion).

### A5 Real data and downstream protocol
- **Tier-A (confirmatory):** CNS, Colon, Leukemia, Ovarian, Prostate, SRBCT ($D/N > 20$), using the repo loaders and preprocessing at the frozen commit with no label-dependent step.
- **Per (dataset, seed 0-9):** the gate is computed once on all samples (transductive, label-free); ICC-v2 (and K-Means and Ward as model-agnostic checks) then runs on the gated features. ARI is computed against the given class labels.

### A6 Outcomes and decision rules
- **Real H4 Rule:** Paired ARI difference (NCG-BC minus comparator) per dataset, averaged over seeds, then over Tier-A datasets. H4 requires:
  1. Mean difference over datasets is $\ge +0.02$ ARI,
  2. Dataset-level bootstrap 95% lower bound $> 0$,
  3. At least 5 of 6 datasets have a non-negative difference, and
  4. One-sided exact sign-flip test gives $p \le 0.025$.

### A7 Kill and pivot rules
- **H1 fails in two or more of F1-F5:** the claim of an error-controlled gate is withdrawn; NCG is reported as a diagnostic with its measured FDP.
- **H4 fails against both comparators:** the claim of improved clustering is withdrawn. *(Activated: NCG-BC vs G2 mean diff $-0.0035, p=0.6875$; vs G4 mean diff $-0.0319, p=0.8281$)*.
- **If SCB fails on F3/F4 and SN fails too:** report that smooth-unimodal null calibration is inadequate for bounded unimodal features due to boundary smoothing bias and state the scope limit.

### A8 Development Findings (Pre-Freeze Verification)
- **Population BC Values:** Verified via $N=200{,}000$: Gaussian $0.333$, Student-$t_5$ $0.125$, Uniform $0.555$, Beta(3,1) $0.562$, log1p Poisson-lognormal counts $0.397$, Informative ($\Delta=2$) $0.583$, Informative ($\Delta=3$) $0.724$.
- **Finite-Sample Cutoff Failure (G2):** At finite $N \in [60, 1000]$, $P(\text{BC} \ge 5/9)$ ranges from $0.20$ to $0.42$ for Uniform and $0.40$ to $0.66$ for Beta(3,1). For informative features at $\Delta=2$, $P(\text{BC} \ge 5/9)$ is only $0.49$ at $N=60$ and $0.60$ at $N=100$, confirming that VSSG drops ~half of real signals at small $N$.
- **Decoy Behavior on Bounded Nuisance:** On development seeds ($N=250, D=300, d^*=20$), SCB and SN yield $\text{FDP} \approx 0.92\text{--}0.93$ on Uniform/Beta because kernel smoothing adds tails, lowering decoy BC relative to compact target features.

---

## Part B: Study 1' Amortized conformal cluster-label sets (ACCS)

### B1 Question and hypotheses
Can ensemble vote frequencies from an ICC-style consensus serve as the stochastic labelling rule for conformal cluster-label sets, giving coverage comparable to split conformal clustering (SCC, arXiv:2604.03488) and weighted conformal clustering (WCC, arXiv:2606.00436) at far lower per-query cost, including when $D \gg N$?

| ID | Confirmatory hypothesis |
| :--- | :--- |
| **H1** | **Validity:** ACCS-W coverage has lower 95% bound $\ge 0.87$ ($\alpha=0.10$ minus $0.03$) in at least 80% of cells in S1-S4. |
| **H2** | **Efficiency:** in cells where both pass H1, the paired mean log ratio of set size (ACCS-W / WCC) has upper 95% bound $\le \log(1.15)$. |
| **H3** | **Cost:** median per-query latency of faithful WCC divided by ACCS-W is $\ge 10$ at $n_{\text{cal}} \ge 2000$. |
| **H4** | **$D \gg N$:** in S5, ACCS-W coverage is non-inferior to WCC (paired difference lower bound $\ge -0.02$) with smaller set size (paired ratio upper bound $< 1$) in at least 70% of S5 cells. |

### B2 Method (WCC-Amended Specification)
1. **Splits:** random 40% train, 40% calibration, 20% test (synthetic: 2000 fresh test points per replicate).
2. **Train Consensus:** fit ICC-v2 consensus on train. Base partitions map to consensus labels by Hungarian matching.
   $$\mathcal{A}(x)_k = \frac{1}{M} \sum_{m=1}^M \mathbf{1}[\text{map}_m(\pi_m(x)) = k]$$
   smoothed as $(\mathcal{A} + 1/M) / (1 + K/M)$.
3. **Soft classifier $\hat{\pi}$:** Trained on **stochastic labels** following SCC protocol (arXiv:2604.03488).
4. **Conformity Score:** Standardized on the **Generalized Inverse Quantile (GIQ)** across all methods as in WCC.
5. **Weights & Diagnostics:**
   $$w_i \propto \frac{\hat{\pi}(Y_i \mid X_i)}{\mathcal{A}(X_i)_{Y_i}}$$
   Monitor Effective Sample Size $\text{ESS} = (\sum w_i)^2 / \sum w_i^2$ as a core diagnostic.
