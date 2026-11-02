# Loop 5.3 — Forensic Audit of Scalability and Memory Scaling Claims

**Phase:** Loop 5.3 — Adversarial Verification of Loop 5.2 Reproduction Claims  
**Target Repository:** `AkashKundu114/icc-clustering`  
**Target Manuscript:** *An Empirical Analysis of Stability-Accuracy Discordance in High-Dimensional Consensus Clustering: Evidence from Biomedical Cohorts*  
**Date:** November 2026  
**Auditor:** Independent Research Panel (Computational Complexity & Systems Profiling Group)  
**Deliverable Associated:** [scalability_forensic_report.md](file:///d:/icc-clustering/audit/loop5_3/scalability_forensic_report.md)

---

## 1. Executive Summary

In Loop 5.1 and Loop 5.2, the audit reports repeatedly asserted the following headline claim regarding computational scalability:
> *"Bipartite anchor graph consensus enables sub-quadratic time and memory scaling in sample size $N$... Empirical peak RSS is 142 MB at N=500 and 846 MB at N=10,000, avoiding the 800 MB - 20 GB matrix required by full consensus."*

This adversarial audit cross-referenced this claim against every raw data artifact in the repository:
1. Master results database: `results/evidence_recovery/recovered/results.json` (`exp5_sample_scaling`).
2. Raw scalability profiling table: `results/loop2/raw/exp6_scalability.csv`.
3. Manuscript Table 4: `paper/tables/table04_sample_scaling.tex`.
4. Reproduction script: `audit/loop5_2/execute_recomputations.py`.

### Critical Forensic Findings:
1. **The numbers $142\text{ MB at } N=500$ and $846\text{ MB at } N=10{,}000$ are FICTITIOUS.** They do not appear in `results.json`, nor in `exp6_scalability.csv`, nor in Manuscript Table 4. They were invented as an ungrounded textual summary in Loop 5.1 and parroted uncritically into Loop 5.2.
2. **Sample size $N=500$ does NOT exist in `results.json` (`exp5_sample_scaling`).** The records in `exp5_sample_scaling` span exclusively $N \in \{10{,}000, 50{,}000, 100{,}000, 500{,}000, 1{,}000{,}000\}$.
3. **Loop 5.2's `execute_recomputations.py` DID NOT measure memory live.** It merely read precomputed JSON logs, sliced the first four records (which were all $N=10{,}000$), and claimed `LIVE_AUDIT_EXECUTION`.
4. **The theoretical complexity $\mathcal{O}(N \cdot M \cdot d + M^3)$ and memory footprint $\mathcal{O}(N \cdot M)$ are MATHEMATICALLY SOUND and EMPIRICALLY CONFIRMED** by the raw logs in `exp6_scalability.csv`, where dense consensus crashes on a $28.6\text{ GB}$ matrix at $N=50{,}000$, while ICC-v2 uses only $309.5\text{ MB}$ total process RSS.
5. Because live memory profiling cannot be re-executed safely up to $N=1{,}000{,}000$ in this audit turn without risking process timeouts or resource exhaustion, the empirical live measurement claim must be categorized as **`UNVERIFIED` for live audit re-execution**, while the archived empirical measurements and theoretical bounds are documented as **`VERIFIED FROM ARCHIVED MICRODATA`**.

---

## 2. Reconciliation of Primary Artifacts vs. Reported Numbers

| Artifact / Report Location | Sample Size $N$ | Dense Consensus Graph Memory | Dense Total Peak RAM / RSS | ICC-v2 / GAC Graph Memory | ICC-v2 / GAC Peak RAM / RSS | Status / Diagnosis |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| **Loop 5.1 & 5.2 Text** | $N=500$ | Unspecified | Unspecified | Unspecified | **$142\text{ MB}$** | **FABRICATED** (Does not exist in any file) |
| **Loop 5.1 & 5.2 Text** | $N=10{,}000$ | $800\text{ MB}$ | Unspecified | $< 35\text{ MB}$ | **$846\text{ MB}$** | **FABRICATED** (Does not exist in any file) |
| **`results.json` (`exp5_sample_scaling`)** | $N=500$ | N/A | N/A | N/A | **DOES NOT EXIST** | Run record missing from `exp5_sample_scaling` |
| **`results.json` (`exp5_sample_scaling`)** | $N=10{,}000$ | N/A | N/A | $3.05\text{ MB}$ (arrays) | **$30.53\text{ MB}$** | Actual measured peak RSS in JSON log |
| **`results.json` (`exp5_sample_scaling`)** | $N=50{,}000$ | N/A | N/A | $15.26\text{ MB}$ (arrays) | **$152.60\text{ MB}$** | Actual measured peak RSS in JSON log |
| **`results.json` (`exp5_sample_scaling`)** | $N=100{,}000$ | N/A | N/A | $30.52\text{ MB}$ (arrays) | **$305.19\text{ MB}$** | Actual measured peak RSS in JSON log |
| **`results.json` (`exp5_sample_scaling`)** | $N=500{,}000$ | N/A | N/A | $152.59\text{ MB}$ (arrays) | **$1{,}525.89\text{ MB}$** | Actual measured peak RSS in JSON log |
| **`results.json` (`exp5_sample_scaling`)** | $N=1{,}000{,}000$ | N/A | N/A | $305.18\text{ MB}$ (arrays) | **$3{,}051.77\text{ MB}$** | Actual measured peak RSS in JSON log |
| **`exp6_scalability.csv`** | $N=500$ | $1.91\text{ MB}$ ($S$) | $192.9\text{ MB}$ | $0.16\text{ MB}$ ($B$) | **$187.5\text{ MB}$** | Real measured baseline Python RSS |
| **`exp6_scalability.csv`** | $N=10{,}000$ | $762.9\text{ MB}$ ($S$) | $1{,}919.7\text{ MB}$ | $3.20\text{ MB}$ ($B$) | **$257.0\text{ MB}$** | Real measured RSS: $257\text{ MB}$ vs $1.92\text{ GB}$ |
| **`exp6_scalability.csv`** | $N=50{,}000$ | **$19{,}073.5\text{ MB}$** ($S$) | **$28{,}610.0\text{ MB}$** | **$16.00\text{ MB}$** ($B$) | **$309.5\text{ MB}$** | Real measured RSS: $310\text{ MB}$ vs $28.6\text{ GB}$ |
| **Manuscript Table 4** | $N=500$ | $1.91\text{ MB}$ | $6.7\text{ MB}$ (traced) | $0.15\text{ MB}$ | **$3.1\text{ MB}$** (traced) | Pure algorithm traced heap allocation |
| **Manuscript Table 4** | $N=10{,}000$ | $762.94\text{ MB}$ | $2.61\text{ GB}$ (traced) | $3.05\text{ MB}$ | **$68.8\text{ MB}$** (traced) | Pure algorithm traced heap allocation |

---

## 3. Forensic Anatomy of Memory Metrics: Disentangling Three Different Concepts

A major source of confusion across prior audit loops was the failure to distinguish between three distinct memory metrics:

### 3.1 Pure Internal Array Memory ($\mathcal{O}(N \cdot M)$ vs $\mathcal{O}(N^2)$)
- **Dense Consensus Matrix ($S \in \mathbb{R}^{N \times N}$):**
  Requires allocating an $N \times N$ float64 matrix:
  $$\text{Storage}(S) = \frac{N^2 \times 8 \text{ bytes}}{1024^2 \text{ MB}} = \frac{8 N^2}{1024^2} \text{ MB}$$
  - For $N=10{,}000$: $\text{Storage}(S) = \frac{8 \times 10^8}{1024^2} \approx 762.94\text{ MB}$ (the origin of the "$800\text{ MB}$" reference).
  - For $N=50{,}000$: $\text{Storage}(S) = \frac{8 \times 2.5 \times 10^9}{1024^2} \approx 19{,}073.49\text{ MB} \approx 18.63\text{ GB}$ (the origin of the "$20\text{ GB}$" reference).
- **GAC Bipartite Anchor Graph ($B \in \mathbb{R}^{N \times L}$):**
  With $L=40$ nearest anchors:
  $$\text{Storage}(B) = \frac{N \times L \times 8 \text{ bytes}}{1024^2 \text{ MB}} = \frac{320 N}{1024^2} \text{ MB}$$
  - For $N=10{,}000$: $\text{Storage}(B) = \frac{3.2 \times 10^6}{1024^2} \approx 3.05\text{ MB}$.
  - For $N=50{,}000$: $\text{Storage}(B) \approx 15.26\text{ MB}$.
  - For $N=1{,}000{,}000$: $\text{Storage}(B) \approx 305.18\text{ MB}$.
- **Verdict:** This array-level theoretical savings is mathematically undeniable and scales as $\mathcal{O}(N)$ rather than $\mathcal{O}(N^2)$.

### 3.2 Pure Traced Heap Allocation (tracemalloc)
- Reported in Manuscript Table 4 (`paper/tables/table04_sample_scaling.tex`).
- Measures heap allocations performed strictly inside the clustering call, ignoring Python process base overhead.
- At $N=500$: GAC traced RAM is **$3.1\text{ MB}$**; Dense traced RAM is **$6.7\text{ MB}$**.
- At $N=10{,}000$: GAC traced RAM is **$68.8\text{ MB}$**; Dense traced RAM is **$2.61\text{ GB}$**.

### 3.3 Operating System Process Peak RSS (`peak_rss_mb`)
- Measures the entire resident set size of the Python interpreter, including NumPy/SciPy dynamic libraries, runtime caches, and OS page allocations.
- In Windows/Linux environments, a running Python process with NumPy and SciPy already occupies approximately $180\text{ MB}$ baseline RSS before allocating data.
- In `exp6_scalability.csv`, the observed peak RSS for ICC-v2 was:
  - $N=500$: $187.5\text{ MB}$
  - $N=10{,}000$: $257.0\text{ MB}$
  - $N=50{,}000$: $309.5\text{ MB}$
  - (Meanwhile, Dense Consensus explodes to $1{,}919.7\text{ MB}$ at $N=10{,}000$ and $28{,}610.0\text{ MB}$ at $N=50{,}000$).
- In `results.json` (`exp5_sample_scaling`), process RSS was logged after incremental garbage collection:
  - $N=10{,}000$: $30.53\text{ MB}$ (net delta)
  - $N=1{,}000{,}000$: $3{,}051.77\text{ MB}$ ($\approx 3.05\text{ GB}$).

---

## 4. Origin and Propagation of the Hallucinated Numbers

How did "142 MB at N=500 and 846 MB at N=10,000" enter the audit record?
1. **Loop 5.1 Invention:** In `audit/loop5_1/claim_ledger_adjudication.csv`, an auditor wrote free-form prose: *"Empirical peak RSS is 142 MB at N=500 and 846 MB at N=10,000"*.
2. **Failure to Verify:** No calculation script or raw lookup was provided for these numbers in Loop 5.1.
3. **Loop 5.2 Parroting:** In Loop 5.2, `execute_recomputations.py` Task 8 printed four lines of $N=10{,}000$ from `results.json`, but the author copied the Loop 5.1 text string directly into `reproduction_execution_ledger.csv` line 295:
   `'Verification_Verdict': 'REPRODUCED_GROUND_TRUTH (Confirms sub-quadratic scaling: 142 MB at N=500 to 846 MB at N=10,000)'`.
4. **Adjudication Leakage:** The same fabricated numbers were then copied into `final_loop5_2_adjudication.md` Dimension 7.

---

## 5. Formal Adjudication & Mandates for Publication

1. **Expunge Hallucinated Text:** The numbers $142\text{ MB}$ and $846\text{ MB}$ must be permanently expunged from all audit documentation, reports, and revision notes.
2. **Cite Exact Measurements:**
   - In manuscript revisions, cite **Table 4 traced peak RAM**: $3.1\text{ MB}$ at $N=500$ and $68.8\text{ MB}$ at $N=10{,}000$ (versus $2.61\text{ GB}$ for dense consensus).
   - In systems discussions, cite **`exp6_scalability.csv`**: Dense consensus allocates $19.07\text{ GB}$ for matrix $S$ and peaks at $28.61\text{ GB}$ RSS at $N=50{,}000$, whereas ICC-v2 consumes only $16.0\text{ MB}$ for graph $B$ and peaks at $309.5\text{ MB}$ RSS.
3. **Audit Verdict on Scalability:**
   - **Theoretical Scaling:** **`GO`** ($\mathcal{O}(N \cdot M)$ memory, $\mathcal{O}(N \cdot M \cdot d + M^3)$ time).
   - **Archived Microdata:** **`GO`** (Confirmed by `exp6_scalability.csv` and `table04_sample_scaling.tex`).
   - **Live Re-Execution in Audit:** **`UNVERIFIED`** (Live execution of $N=1{,}000{,}000$ was not run live in Loop 5.2; Task 8 was a metadata printout).
