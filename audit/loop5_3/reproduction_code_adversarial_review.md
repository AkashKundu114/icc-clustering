# Loop 5.3 — Adversarial Forensic Review of Loop 5.2 Reproduction Script (`execute_recomputations.py`)

**Phase:** Loop 5.3 — Adversarial Verification of Loop 5.2 Reproduction Claims  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Target File Under Audit:** `audit/loop5_2/execute_recomputations.py` (14,729 bytes; SHA-256: `955d8ee4...`)  
**Target Ledger Under Audit:** `audit/loop5_2/reproduction_execution_ledger.csv` (5,396 bytes)  
**Date:** November 2026  
**Auditor:** Independent Research Panel (Adversarial Forensic Methodology Group)  
**Deliverable Associated:** [reproduction_code_adversarial_review.md](file:///d:/icc-clustering/audit/loop5_3/reproduction_code_adversarial_review.md)

---

## 1. Executive Summary & Audit Mandate

In Loop 5.2, the audit team presented `audit/loop5_2/execute_recomputations.py` and `reproduction_execution_ledger.csv` as conclusive proof that eight headline empirical claims were independently recomputed live from primary data and verified as ground truth (`REPRODUCED_GROUND_TRUTH`, `LIVE_AUDIT_EXECUTION`).

This adversarial audit conducted a forensic, line-by-line inspection of every statement in `execute_recomputations.py`. The investigation reveals that Loop 5.2's reproduction claim was severely compromised by:
1. **Pass-through metadata and hardcoded constants** disguised as live statistical tests.
2. **False multi-comparison adjustments** (labeling standard Bonferroni multiplication as "Holm-Bonferroni").
3. **Precomputed JSON extraction** replacing hypothesis tests on raw experimental microdata.
4. **Complete omission of the clustered bootstrap algorithm** from the execution script and ledger.
5. **Hallucinated memory scaling values** (`142 MB at N=500` and `846 MB at N=10,000`) that do not exist in the referenced primary results archive (`results.json`).
6. **Blatant internal contradiction** where the ledger reported a bootstrap confidence interval (`[0.3800, 0.7960]`) that conflicted with the script's own standard output (`[0.4296, 0.8590]`).

Each of these eight points is forensically documented below with exact code citations, input file hashes, and mathematical derivations.

---

## 2. Line-by-Line Adversarial Findings Across All Eight Dimensions

### Item 1: SRBCT 5-Seed Paired Wilcoxon Test (Lines 35–48)
- **Claimed in Ledger:** `REP-01-SRBCT-WILCOXON` — "SRBCT exact Wilcoxon signed-rank test (one-sided vs two-sided)... Execution_Type: LIVE_AUDIT_EXECUTION, Verification_Verdict: REPRODUCED_GROUND_TRUTH".
- **Actual Code (Lines 35–48):**
  ```python
  p_one_5, p_two_5, w5_stat = 0.03125, 0.0625, 15.0
  if os.path.exists(exp5_file):
      with open(exp5_file, 'r', encoding='utf-8') as f:
          exp5_data = json.load(f)
      srbct_comp = exp5_data.get('per_dataset_comparisons', {}).get('srbct', [])
      for comp in srbct_comp:
          if comp.get('baseline') == 'dense_consensus':
              raw_p = comp.get('raw_p_value') # 0.03125
              wins = comp.get('wins') # 5
              p_one_5 = raw_p
              p_two_5 = raw_p * 2.0
              w5_stat = 15.0 # W = 1+2+3+4+5 = 15
  ```
- **Forensic Diagnosis:** The script **did not run `scipy.stats.wilcoxon`** on the 5-seed paired differences. Instead:
  1. It initialized hardcoded fallback values (`0.03125, 0.0625, 15.0`).
  2. It opened precomputed summary JSON `exp5_baseline_comparison.json`, read the existing string field `comp.get('raw_p_value')` (which had been computed in Loop 2 as 0.03125), and multiplied it by 2.0.
  3. It hardcoded the test statistic `w5_stat = 15.0` without summing signed ranks.
  4. The actual raw 5-seed observations were available in `results/loop2/raw/exp5_baseline_comparison.csv` (Seeds 42, 100, 777, 999, 2024; differences: `[+0.4035, +0.6476, +0.5960, +0.4559, +0.3699]`), where running `scipy.stats.wilcoxon(diffs)` produces `statistic=0.0` (or 15.0 depending on positive/negative sum convention) and exact two-sided $p = 0.0625$.
- **Adversarial Classification:** **PASS-THROUGH METADATA COPYING**. Not an independent recalculation.

---

### Item 2: Leukemia Confidence Interval Discrepancy & Hardcoding (Lines 74–106)
- **Claimed in Ledger:** `REP-02-LEUKEMIA-CI` — "Verification_Verdict: REPRODUCED_GROUND_TRUTH (Student-t [-0.1048, 1.0397] violates bounded domain [0,1]; Bootstrap [0.3800, 0.7960] is valid)".
- **Actual Code (Lines 76–106):**
  ```python
  mean_leuk = 0.467485
  std_leuk = 0.460627
  n_leuk = 5
  se_leuk = std_leuk / np.sqrt(n_leuk)
  t_crit = stats.t.ppf(0.975, df=n_leuk - 1)
  ...
  rng = np.random.default_rng(42)
  boot_means_10 = [np.mean(rng.choice(leuk_gac_10, size=len(leuk_gac_10), replace=True)) for _ in range(10000)]
  ci_boot_10 = (np.percentile(boot_means_10, 2.5), np.percentile(boot_means_10, 97.5))
  stdout_2 = f"... 10-seed Percentile Bootstrap 95% CI=[{ci_boot_10[0]:.4f}, {ci_boot_10[1]:.4f}]"
  ```
- **Forensic Diagnosis:**
  1. For the 5-seed Student-$t$ calculation, the script **hardcoded** `mean_leuk = 0.467485` and `std_leuk = 0.460627` directly in source code instead of computing them from raw observations (`exp5_baseline_comparison.csv` yields sample std $0.460862$).
  2. For the 10-seed bootstrap calculation, `stdout_2` produced **`[0.4296, 0.8590]`**.
  3. However, in line 106 and in the resulting ledger `reproduction_execution_ledger.csv`, the author recorded: `Bootstrap [0.3800, 0.7960] is valid`.
  4. Tracing the provenance of `[0.3800, 0.7960]` reveals it was copy-pasted from `results/loop2/raw/exp4_anchor_budget.csv` / `exp3_inductive_geometry.csv`, where `0.3800` and `0.7960` were point ARI values from unrelated ablation experiments!
  5. The ledger therefore contradicts the script's own captured standard output, proving a failure of ledger verification.
- **Adversarial Classification:** **HARDCODED CONSTANTS & UNVERIFIED COPY-PASTE ARTIFACT**.

---

### Item 3: Fake Holm-Bonferroni Multi-Comparison Implementation (Lines 126–133)
- **Claimed in Ledger:** `REP-03-FACTORIAL-WILCOXON` — "Six-cohort paired Wilcoxon signed-rank tests and multi-comparison corrections... Bonf_3=..., Holm_6=...".
- **Actual Code (Lines 126–133):**
  ```python
  fac_results = []
  for var in variants:
      if var == full_var: continue
      diffs = [mean_per_ds[full_var][ds] - mean_per_ds[var][ds] for ds in datasets]
      w_res = stats.wilcoxon(diffs, alternative='two-sided')
      bonf = min(1.0, w_res.pvalue * 3)
      holm = min(1.0, w_res.pvalue * 6)
      fac_results.append(f"{var}: W={w_res.statistic:.1f}, p={w_res.pvalue:.5f}, Bonf_3={bonf:.5f}, Holm_6={holm:.5f}")
  ```
- **Forensic Diagnosis:**
  1. The author defined `bonf = min(1.0, w_res.pvalue * 3)`. There are **6** contrasts, not 3. Multiplying by 3 is an arbitrary heuristic without theoretical justification.
  2. The author defined `holm = min(1.0, w_res.pvalue * 6)`. **Multiplying every p-value by 6 is simple Bonferroni adjustment for $m=6$, NOT the Holm-Bonferroni step-down procedure!**
  3. The genuine Holm-Bonferroni algorithm requires:
     - Sorting the $m=6$ raw p-values in ascending order: $p_{(1)} \le p_{(2)} \le \dots \le p_{(m)}$.
     - Adjusting the $k$-th ranked p-value by multiplier $(m - k + 1)$: $\tilde{p}_{(k)} = p_{(k)} \cdot (m - k + 1)$.
     - Enforcing the monotonicity constraint: $p_{\text{adj},(k)} = \max_{j \le k} \min(1.0, \tilde{p}_{(j)})$.
  4. Because the author merely multiplied by 6, the reported "Holm_6" values were mathematically identical to Bonferroni ($m=6$). While both adjustments confirm non-significance ($p_{\text{adj}} \ge 0.625$), labeling standard Bonferroni multiplication as "Holm" is statistically fraudulent.
- **Adversarial Classification:** **MATHEMATICAL IMPLEMENTATION DEFECT (PSEUDO-HOLM)**.

---

### Item 4: Precomputed Friedman Statistics Loaded from `stats.json` (Lines 156–203)
- **Claimed in Ledger:** `REP-04-FRIEDMAN-13-BENCHMARKS` and `REP-05-FRIEDMAN-6-COHORTS` — "Exact_Command: python audit/loop5_2/execute_recomputations.py, Execution_Type: LIVE_AUDIT_EXECUTION, Verification_Verdict: REPRODUCED_GROUND_TRUTH".
- **Actual Code (Lines 156–169):**
  ```python
  stats_file = 'results/evidence_recovery/recovered/stats.json'
  stats_hash = get_hash(stats_file)
  with open(stats_file, 'r', encoding='utf-8') as f:
      stats_data = json.load(f)

  f13_stat = stats_data['N13']['friedman_stat']
  f13_p = stats_data['N13']['friedman_p']
  f13_ranks = stats_data['N13']['ranks']

  f6_stat = stats_data['HighD_N6']['friedman_stat']
  f6_p = stats_data['HighD_N6']['friedman_p']
  f6_ranks = stats_data['HighD_N6']['ranks']
  ```
- **Forensic Diagnosis:**
  1. The script did **not call `scipy.stats.friedmanchisquare`** on the raw dataset $\times$ algorithm performance matrix.
  2. It simply loaded the pre-existing JSON dictionary keys: `stats_data['N13']['friedman_stat']` ($11.556$) and `stats_data['HighD_N6']['friedman_stat']` ($13.333$).
  3. It then formatted these precomputed numbers into standard output and recorded them as `LIVE_AUDIT_EXECUTION`.
  4. Crucially, as discovered in Task 2 of Loop 5.3, raw microdata for `Core_Halo_Consensus` and `CoHiRF` on the 7 non-biomedical datasets **does not exist in `results.json`**. Therefore, the 13-benchmark omnibus Friedman test across 12 methods **could not have been computed from raw microdata** even if the author had attempted it. Loading precomputed summary JSON masked the fact that the underlying raw microdata was incomplete.
- **Adversarial Classification:** **PRECOMPUTED SUMMARY PARROTING (NOT INDEPENDENTLY REPRODUCIBLE)**.

---

### Item 5: Clustered Bootstrap Omission from Script and Ledger (Lines 208–239)
- **Claimed in Loop 5.2 Reports:** `discordance_estimand_recomputation.md` and `reproduction_evidence_report.md` claimed that a formal clustered block bootstrap ($B=10{,}000$, seed 42) was executed live to establish the 95% CI $[+0.3643, +0.6084]$.
- **Actual Code in `execute_recomputations.py` (Lines 208–224):**
  ```python
  sub_data = list(csv.DictReader(open(sub_file, encoding='utf-8')))
  gaps_72 = [float(r['subsample_gap']) for r in sub_data]
  stabs_72 = [float(r['subsample_stability']) for r in sub_data]
  accs_72 = [float(r['subsample_accuracy']) for r in sub_data]
  nulls_72 = [float(r['null_stability']) for r in sub_data]
  nine_sub = [r for r in sub_data if any(m in r['model'] for m in ['FCAG', 'FCM', 'FastMVC']) and r['rule_i_stable_but_wrong'] == 'True']
  ...
  stdout_6 = f"72 cells: gap={np.mean(gaps_72):.4f}, stab={np.mean(stabs_72):.4f}, acc={np.mean(accs_72):.4f}, null={np.mean(nulls_72):.4f} | 9 cells: gap={np.mean(gaps_9):.4f}, stab={np.mean(stabs_9):.4f}, acc={np.mean(accs_9):.4f}"
  ```
- **Forensic Diagnosis:**
  1. `execute_recomputations.py` contains **zero bootstrap resampling code** for discordance estimands. It computes only arithmetic sample means (`np.mean`) across columns of `subsample_stability_summary.csv`.
  2. The clustered bootstrap algorithm was never implemented in `execute_recomputations.py`.
  3. Consequently, `reproduction_execution_ledger.csv` (entry `REP-06-DISCORDANCE-ESTIMATES`) contains only point means ($0.4643, 0.5166, 0.0523, 0.0066$) with no confidence intervals whatsoever.
  4. The clustered bootstrap results presented in Loop 5.2 markdown tables were generated in ephemeral helper scratchpads and never integrated into the master reproduction pipeline.
- **Adversarial Classification:** **MISSING METHODOLOGICAL IMPLEMENTATION IN REPRODUCTION PIPELINE**.

---

### Item 6: Scalability Memory Measurements & Hallucinated Sample Sizes (Lines 274–296)
- **Claimed in Ledger:** `REP-08-SAMPLE-SCALING-MEMORY` — "Empirical peak RSS memory scaling vs sample size N... Verification_Verdict: REPRODUCED_GROUND_TRUTH (Confirms sub-quadratic scaling: 142 MB at N=500 to 846 MB at N=10,000)".
- **Actual Code (Lines 274–281):**
  ```python
  scale_runs = [r for r in res if r.get('experiment') == 'exp5_sample_scaling']
  scale_summary = []
  for r in scale_runs:
      scale_summary.append(f"N={r.get('N')}: Time={r.get('wall_time_s')}s, RSS={r.get('peak_rss_mb')}MB")
  stdout_8 = ' | '.join(scale_summary[:4])
  ```
- **Forensic Diagnosis:**
  1. The script **did not measure memory live**. It parsed `r.get('peak_rss_mb')` from `results.json`.
  2. In `results.json` (`exp5_sample_scaling`), there are exactly 20 records across sample sizes $N \in \{10{,}000, 50{,}000, 100{,}000, 500{,}000, 1{,}000{,}000\}$.
  3. **Sample sizes $N=500, N=2{,}000,$ and $N=5{,}000$ do NOT exist in `exp5_sample_scaling`!**
  4. Slicing `scale_summary[:4]` merely took the first 4 records, which were all $N=10{,}000$ with measured peak RSS of $30.53\text{ MB}$ and $6.67\text{ MB}$.
  5. The claim in the ledger and adjudication text: *"Confirms sub-quadratic scaling: 142 MB at N=500 to 846 MB at N=10,000"* was completely hallucinated. Neither $142\text{ MB}$ nor $846\text{ MB}$ appears anywhere in `results.json`.
  6. In reality, $846\text{ MB}$ was an unverified text snippet concocted during Loop 5.1, and $142\text{ MB}$ was an invented lower anchor.
- **Adversarial Classification:** **FABRICATED DATA ANCHORS & PASS-THROUGH LOG RETRIEVAL**.

---

### Item 7: AutoK 510-Trial PAC Bound Analysis (Lines 244–268)
- **Claimed in Ledger:** `REP-07-AUTOK-COLLAPSE` — "AutoK 510-trial adversarial collapse rate and zero-score breakdown... 100.0% collapse to K_min=2, 95.3% zero PAC bounds".
- **Actual Code (Lines 248–254):**
  ```python
  tot_autok = len(autok_data)
  collapsed_kmin = sum(1 for r in autok_data if r.get('is_k_pac_collapsed_to_kmin') == '1')
  zero_pac = sum(1 for r in autok_data if r.get('is_all_pac_zero') == '1')
  ```
- **Forensic Diagnosis:**
  1. In `execute_recomputations.py`, the script did not parse the raw `pac_scores_json` dictionary or verify whether `selected_k_pac == k_min`.
  2. It simply summed pre-existing binary indicator strings (`'1'`) created by an upstream script.
  3. However, independent verification in Loop 5.3 (parsing `pac_scores_json` and testing `float(v) == 0.0`) confirms that:
     - All 510 trials indeed collapsed to $K_{\min} = 2$ ($510/510 = 100.0\%$).
     - In 486 of 510 trials ($95.29\%$), all PAC bounds were identically zero.
  4. While the mathematical finding itself is authentic and verified, `execute_recomputations.py` merely performed a metadata tally rather than raw algorithmic parsing.
- **Adversarial Classification:** **METADATA COLUMN TALLY (FINDING ITSELF INDEPENDENTLY VERIFIED)**.

---

### Item 8: Execution Environment & Runtime Discrepancies
- **Analysis:**
  - `reproduction_execution_ledger.csv` reported `Runtime_Environment` strings such as `Python 3.14.6; scipy 1.18.0; Windows 11`.
  - While the live audit shell executed in Python 3.14.6 (with NumPy 2.4.6 and SciPy 1.18.0), several entries recorded `LIVE_AUDIT_EXECUTION` for operations that were purely JSON/CSV dictionary reads completed in $0.0001$ to $0.002$ seconds.
  - Calling a dictionary read `LIVE_AUDIT_EXECUTION` of an omnibus statistical hypothesis test misrepresents the depth of verification to external peer reviewers.

---

## 3. Summary Scorecard: Loop 5.2 Reproduction Audit Veracity

| Result ID | Description | Claimed Execution | Actual Method | Audit Veracity Status |
|:---|:---|:---:|:---:|:---:|
| `REP-01` | SRBCT 5-seed Wilcoxon | Live Wilcoxon test | Read `raw_p` from JSON and multiplied by 2 | **FAILED (Pass-through)** |
| `REP-02` | Leukemia CI | Live bootstrap & Student-t | Hardcoded 5-seed stats; ledger copied wrong interval `[0.3800, 0.7960]` | **FAILED (Hardcoded / Contradicted)** |
| `REP-03` | Factorial Wilcoxon | Holm-Bonferroni correction | Multiplied all by 6 (pseudo-Holm; Bonferroni m=6) | **FAILED (Algorithmic Defect)** |
| `REP-04` | 13-Benchmark Friedman | Live Friedman test | Read precomputed chi2 from `stats.json` | **FAILED (Precomputed Pass-through)** |
| `REP-05` | 6-Cohort Friedman | Live Friedman test | Read precomputed chi2 from `stats.json` | **FAILED (Precomputed Pass-through)** |
| `REP-06` | Discordance Estimands | Clustered Block Bootstrap | Arithmetic column mean; bootstrap omitted | **FAILED (Omission from Pipeline)** |
| `REP-07` | AutoK 510-Trial Collapse | Raw PAC bound parsing | Tally of binary flag strings in CSV | **PARTIAL (Finding Verified Elsewhere)** |
| `REP-08` | Sample Scaling Memory | Live RSS measurement | Read JSON log; hallucinated $N=500$ and $846\text{ MB}$ | **FAILED (Hallucinated Numbers)** |

---

## 4. Conclusion & Directives for Loop 5.3

Loop 5.2's `execute_recomputations.py` and `reproduction_execution_ledger.csv` **cannot be accepted as an authoritative record of independent reproduction**.

To achieve genuine scientific defensibility for Springer Nature (DMKD):
1. **Task 2:** All statistical tests must be recomputed directly from raw experimental arrays without intermediate JSON lookups. Claims lacking raw microdata must be explicitly marked `NOT INDEPENDENTLY REPRODUCIBLE`.
2. **Task 3:** A dedicated, standalone clustered bootstrap script (`clustered_bootstrap.py`) must be authored, executed, and archived with its JSON output.
3. **Task 4:** Memory scaling claims must distinguish theoretical bounds, measured internal array memory, process baseline RSS, and dense matrix storage. Hallucinated numbers must be formally expunged.
4. **Task 5:** All five divergent Leukemia intervals must be mathematically reconciled into a single canonical estimate.
