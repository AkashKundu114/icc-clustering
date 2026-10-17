# Pre-registration v1.0: ICC-v2 follow-up studies 3' and 1'

**Registrant:** Akash Kundu.  
**Drafted:** 2026-10-17.  
**Status:** BINDING / FROZEN.  
**Frozen commit:** `0f1f12370a6541b843588c597e2812800e768b0e`  
**File SHA-256:** `bf81bf96c68aca1fbb914b24ab04951e5048c8e6c877baa3ac80cb752cd71a07` (recorded at freeze)  
**Freeze date:** 2026-10-17  

---

## 0. Shared conventions

**0.1 Prior exposure.** ICC-v2 results on the 13 benchmark datasets already exist, so this work is not blind to the data. The registration fixes the new methods, comparators, grids, metrics and decision rules before any confirmatory run, so that no forking paths remain.

**0.2 Order of work.**
1. Implement and debug on development data only.
2. Run all analysis scripts end to end on development data.
3. Freeze: tag the commit and record hashes.
4. Run confirmatory simulations.
5. Run real-data analyses. Real-data results are not inspected before step 4 completes.

**0.3 Seeds.** Synthetic replicate seeds 0–299 (Study 3′) and 0–99 (Study 1′); development seeds start at 10,000. Real-data clustering seeds 0–9 (3′); split seeds 0–199 (1′). A seed fixes every random draw (data, decoys, splits, initialisation).

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
| **H1** | **FDR control:** NCG-BC at $q=0.10$ has mean $\text{FDP} \le q + 0.02$ (one-sided 95% upper bound) in at least 90% of cells in each nuisance family F1–F5, including global-null cells ($d^*=0$), where $P(\text{any selection}) \le q + 0.02$. |
| **H2** | **Fixed-cutoff failure:** the current rule ($\text{BC} \ge 5/9$, capped) has mean $\text{FDP} > 0.25$ in at least 80% of cells with uniform (F3) or J-shaped Beta (F4) nuisance. |
| **H3** | **Power:** NCG-BC power $\ge 0.8$ in cells with half-separation $3.0$, $N \ge 250$, nuisance F1, F2, F5; and within $0.05$ (non-inferiority) of the dip-BH gate in F1 cells. |
| **H4** | **Downstream:** on Tier-A real datasets, ICC-v2 with the NCG-BC gate has higher mean ARI than ICC-v2 with (a) the dip-BH gate and (b) the fixed BC rule, at matched feature count (decision rule in A6). |

### A2 Method (frozen specification)
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

| Family | Nuisance | Population BC |
| :--- | :--- | :--- |
| **F1** | Gaussian | 1/3 |
| **F2** | Student-$t$, 5 df | about 0.11 |
| **F3** | Uniform | 5/9 (exactly the cutoff) |
| **F4** | Beta(3, 1), J-shaped unimodal | about 0.563 |
| **F5** | $\log(1+x)$ of Poisson($\exp(\mathcal{N}(1, 1))$) counts | $0.394$ (verified by simulation) |

- **Stress test** (reported, outside H1): F6 block-correlated Gaussian ($\text{AR}(1), \rho=0.5$, blocks of 50).
- **Negative controls** (failure expected, reported): X1 XOR informative structure (no marginal signal); X2 binary nuisance (exercises the distinct-values exclusion).
- **Secondary grid** (exploratory): $d^* \in \{5, 50\}$, 0.8/0.2 imbalance, $K=4$, half-separation $1.5$ and $2.5$.

### A5 Real data and downstream protocol
- **Tier-A (confirmatory):** CNS, Colon, Leukemia, Ovarian, Prostate, SRBCT ($D/N > 20$), using the repo loaders and preprocessing at the frozen commit with no label-dependent step.
- **Tier-B (secondary):** Sonar, Madelon, Indian Pines, Isolet, 20 Newsgroups, Yale B, Zheng68k.
- **Development datasets (debugging only):** Lymphoma, Lung cancer, Gisette, HAR, USPS, Waveform where loaders exist.
- **Per (dataset, seed 0–9):** the gate is computed once on all samples (transductive, label-free); ICC-v2 (and K-Means and Ward as model-agnostic checks) then runs on the gated features. ARI is computed against the given class labels.
- **Exploratory E2:** marker-gene recovery on Zheng68k against a published marker list recorded in the appendix before the first run.

### A6 Outcomes and decision rules
- **Synthetic:** $\text{FDP} = |\mathcal{S} \cap \text{nuisance}| / \max(1, |\mathcal{S}|)$; $\text{power} = |\mathcal{S} \cap \text{informative}| / d^*$; per-cell means with Monte Carlo SE. H1 uses the one-sided upper 95% bound of mean FDP (and of $P(\text{any selection})$ in global-null cells) and is supported for NCG-BC if at least 90% of cells in every family F1–F5 pass. H2 uses the same estimates for G2 (FDP of its own selected set after cap). H3 uses paired replicate differences for non-inferiority.
- **Real:** the primary outcome is the paired ARI difference (NCG-BC minus comparator) per dataset, averaged over seeds, then over Tier-A datasets. H4 is supported against a comparator if:
  1. the mean difference over datasets is $\ge +0.02$ ARI,
  2. the dataset-level bootstrap 95% lower bound is $> 0$,
  3. at least 5 of 6 datasets have a non-negative difference, and
  4. the one-sided exact sign-flip test over the 6 datasets gives $p \le 0.025$ (Holm over the two comparators; the smallest attainable $p$ with 6 datasets is $0.0156$).
- **Secondary:** $|\mathcal{S}|$ distribution and fallback rate; split-half Jaccard of $\mathcal{S}$; runtime (single thread, median of 3); sensitivity to $q$; SCB versus SN null; NCG-Dip versus dip-BH; all Tier-B results.

### A7 Kill and pivot rules
- H1 fails in two or more of F1–F5: the claim of an error-controlled gate is withdrawn; NCG is reported as a diagnostic with its measured FDP.
- H4 fails against both comparators: the claim of improved clustering is withdrawn.
- If SCB fails on F3/F4 and SN fails too, report that unimodal-null calibration is inadequate for bounded unimodal features and state the scope limit.
- XOR and binary negative controls are reported; their failure is expected and is not grounds for exclusion.

---

## Part B: Study 1' Amortized conformal cluster-label sets (ACCS)

### B1 Question and hypotheses
Can ensemble vote frequencies from an ICC-style consensus serve as the stochastic labelling rule for conformal cluster-label sets, giving coverage comparable to split conformal clustering (SCC, Hur-Nath-Allen) and weighted conformal clustering (WCC, Nath-Hur-Allen) at far lower per-query cost, including when $D \gg N$? The coverage target is the latent cluster label (alignment in B5). ACCS validity is not covered by a theorem; the approximation gap relative to augmented calibration is what is tested.

| ID | Confirmatory hypothesis |
| :--- | :--- |
| **H1** | **Validity:** ACCS-W coverage has lower 95% bound $\ge 0.87$ ($\alpha=0.10$ minus $0.03$) in at least 80% of cells in S1–S4. |
| **H2** | **Efficiency:** in cells where both pass H1, the paired mean log ratio of set size (ACCS-W / WCC) has upper 95% bound $\le \log(1.15)$. |
| **H3** | **Cost:** median per-query latency of faithful WCC divided by ACCS-W is $\ge 10$ at $n_{\text{cal}} \ge 2000$. |
| **H4** | **$D \gg N$:** in S5, ACCS-W coverage is non-inferior to WCC (paired difference lower bound $\ge -0.02$) with smaller set size (paired ratio upper bound $< 1$) in at least 70% of S5 cells, with the same gate for all methods. |

### B2 Method (frozen)
1. **Splits:** random 40% train, 40% calibration, 20% test (synthetic: 2000 fresh test points per replicate).
2. **Train:** fit the ICC-v2 consensus on train (frozen configuration). Base partitions are K-Means on random subspaces, so each assigns any new $x$ by nearest centroid; each base partition is mapped to consensus labels by Hungarian matching on train. The stochastic rule is:
   $$\mathcal{A}(x)_k = \frac{1}{M} \sum_{m=1}^M \mathbf{1}[\text{map}_m(\pi_m(x)) = k]$$
   smoothed as $(\mathcal{A} + 1/M) / (1 + K/M)$. Per-query cost $O(M K |\mathcal{F}_{\text{sub}}|)$.
3. **Soft classifier $\hat{\pi}$:** $k\text{-NN}$ with $k = \lceil \sqrt{n_{\text{train}}} \rceil$ fitted on train consensus labels, Laplace-smoothed. Conformity score $1 - \hat{\pi}_y(x)$ (LAC); APS secondary.
4. **Calibration labels:** $Y_i \sim \text{Categorical}(\mathcal{A}(X_i))$, one draw per calibration point (secondary: argmax).
5. **ACCS-W (primary):** weights as in WCC Eq. 5 with the fixed rule $\mathcal{A}$ replacing the augmented clustering:
   $$w_i \propto \frac{\hat{\pi}(Y_i \mid X_i)}{\mathcal{A}(X_i)_{Y_i}}$$
   For a test point $x$ and candidate $y$, the test weight is proportional to $\hat{\pi}(y \mid x) / \mathcal{A}(x)_y$; weights are normalised per candidate;
   $$C(x) = \{y : s(x, y) \le \text{weighted } (1-\alpha)\text{-quantile with test point mass at }\infty\}$$
   No alignment step is needed because $\mathcal{A}$ and $\hat{\pi}$ share the consensus label space. ACCS-U (secondary): unweighted split conformal with the same stochastic labels.
6. **Alpha:** $0.10$ primary; $0.05$ and $0.20$ secondary. For $D \gg N$ runs the gate is the current ICC-v2 rule (G2), fitted on train only and applied to calibration and test (primary, independent of Study 3′); the NCG-BC gate (if 3′ H1 is supported) and no gate are secondary.

### B3 Baselines
- **B0**: naive cutoff on $\hat{\pi}$ (smallest set with probability mass $\ge 1 - \alpha$).
- **B1**: SCC, implemented from the authors' description (arXiv:2604.03488).
- **B2**: WCC Algorithm 1 (arXiv:2606.00436) with per-test-point augmented clustering.
- **B3**: WCC-batched (cluster once on calibration plus the whole test batch).
- **B4**: split conformal on consensus labels (coverage with respect to consensus labels only; sanity check, not comparable).  
*B1–B3 use the base clusterers of their papers (stochastic GMM in low dimension, spectral plus GMM in high dimension). Exploratory: B2 with ICC refit per test point for $N \le 600$.*

**Reproduction gate (before any comparison):** our B2 on the published settings (2-D GMM, $K=5, n=1200, \sigma^2=2.6$; 50-D GMM, $n=3000, \sigma^2=2.3$; moons $n=600, \sigma^2=1.8$; circles $n=400, \sigma^2=1.05$; $\alpha=0.1$) must reach average coverage $\ge 0.87$ over 50 replicates with mean set size $< 2.0$. Debugging uses development seeds only. If the gate fails, comparative claims are suspended and the authors contacted.

### B4 Data
- **Synthetic (100 replicates per cell, 2000 fresh test points):** S1–S4 replicate the published settings above. S5 ($D \gg N$): $K=3$ GMM, $d^*=10$ informative dimensions (half-separation $3.0$), noise dimensions in $\{490, 1990, 4990\}$, $N_{\text{total}} \in \{600, 1500, 3000\}$ (9 cells).
- **Real (descriptive only, 200 random splits each):** R1 text embeddings of 20 Newsgroups and R2 image embeddings; R3 MNIST reduced to 10 dimensions by PCA; R4 Isolet; R5 Tier-A microarrays as an acknowledged stress case.
- **Development data:** synthetic seeds $\ge 10{,}000$; Madelon and Sonar.

### B5 Outcomes and decision rules
- Coverage of the latent label on test points, averaged over replicates (bootstrap CI over replicates); mean set size; singleton and empty-set fractions; worst-cluster coverage and coverage by margin decile; per-query latency (single thread, median of 3) and memory.
- **Alignment:** primary is Hungarian matching between consensus labels and true labels on the train split (fixed before test evaluation, deployable); secondary is oracle alignment (the permutation maximising test coverage, as in the published definition).
- Faithful WCC is evaluated on a common random subset of 200 test points per replicate, and all methods are compared on that subset; other results use all 2000 points.
- **Exploratory E3:** for $N \le 600$, the total-variation distance between the augmented-fit rule and the fixed rule on test points, to measure the amortization gap.

### B6 Kill and pivot rules
- H1 fails in S1–S4: ACCS-W is not validity-preserving; report the measured gap and pivot to a study of the amortization gap.
- H3 below $10\times$: drop the efficiency claim.
- The B2 reproduction gate fails: stop comparative claims.
- Real-data and small-$N$ results never support confirmatory statements.

---

## Pre-freeze checklist

- [x] 1. Audit the ICC-v2 code against the BC formula, selection rule, default parameters and base-clusterer out-of-sample assignment; record the commit hash.
- [x] 2. Verify the population BC values in the A4 table by simulation.
- [x] 3. Read arXiv:2604.03488 and confirm the SCC description; confirm whether code for SCC, WCC, i-IF-Learn and DIFS is public.
- [x] 4. Fix the embedding models and revisions (R1, R2) and the marker list (E2).
- [x] 5. Run every analysis script end to end on development data; record hardware and library versions.
- [x] 6. Write the file SHA-256, the commit hash and the freeze date at the top; tag; register on OSF.
