# Experiment 6: Expanded Biological Cohort Benchmark

**Directory Reference:** `experiments/exp6_cohort_expansion/`  
**Target Venue:** *Data Mining and Knowledge Discovery* (DMKD)  
**Execution Date:** 2026-11-01  
**Status:** Completed and Audited  

---

## 1. Overview and Scientific Motivation

A primary critique of the initial manuscript (GAP-01) was the reliance on a restricted suite of six high-dimensional oncology microarray datasets (Colon, SRBCT, CNS, Leukemia, Prostate, Ovarian), with performance gains heavily concentrated in Leukemia and SRBCT.

EXP6 expands the biological evaluation to **six additional independent public oncology cohorts**:
1. **DLBCL** (Shipp et al., Nature Medicine 2002): Diffuse Large B-cell Lymphoma vs. Follicular Lymphoma ($N=77, D=5{,}469, K=2$).
2. **Breast** (van 't Veer et al., Nature 2002): Breast cancer 5-year distant metastasis prognosis ($N=97, D=24{,}481, K=2$).
3. **Su2001** (Su et al., Cancer Research 2001): 11 human primary solid tumor categories ($N=174, D=12{,}533, K=11$).
4. **Novartis** (Su et al., PNAS 2002): 9 multi-tissue carcinoma subtypes ($N=60, D=5{,}726, K=9$).
5. **GCM** (Ramaswamy et al., PNAS 2001): Global Cancer Map multi-carcinoma benchmark ($N=190, D=16{,}063, K=14$).
6. **Endometrium** (Risinger et al., Cancer Research 2003 / Armstrong et al.): Endometrial adenocarcinoma vs. renal carcinoma ($N=321, D=10{,}936, K=2$).

---

## 2. Experimental Protocol

- **Methods Benchmarked**:
  - K-Means (Lloyd / k-means++)
  - Ward Hierarchical Agglomerative Clustering
  - Normalized Spectral Clustering (Ng-Jordan-Weiss)
  - Fuzzy C-Means (FCM)
  - Standard Consensus (Dense co-association matrix)
  - GAC (Invariant Core Anchor Consensus, ICC-v2)
  - Sparse K-Means (Witten & Tibshirani, JASA 2010 $L_1$ BCSS)
- **Seeds**: 5 canonical random seeds ($s \in \{42, 43, 44, 45, 46\}$).
- **Total Model Fits**: $6 \text{ cohorts} \times 7 \text{ models} \times 5 \text{ seeds} = 210 \text{ evaluations}$.
- **Preprocessing**: Mean imputation for missing coordinates, feature-wise $Z$-score standardization, and contiguous integer label encoding.

---

## 3. Key Findings

**Table: Aggregate Performance across Expanded Cohorts (Mean ARI $\pm$ Std)**

| Cohort | $N$ | $D$ | $K^*$ | GAC (Ours) | Standard Consensus | K-Means | Ward | Spectral | Sparse K-Means | FCM |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **DLBCL** | 77 | 5,469 | 2 | **$0.147 \pm 0.08$** | $0.043 \pm 0.02$ | $0.080 \pm 0.09$ | $0.052 \pm 0.00$ | $0.061 \pm 0.00$ | $0.077 \pm 0.08$ | $0.036 \pm 0.00$ |
| **Novartis** | 60 | 5,726 | 9 | **$0.144 \pm 0.06$** | $0.072 \pm 0.03$ | $0.039 \pm 0.02$ | $0.054 \pm 0.00$ | $0.130 \pm 0.00$ | $0.023 \pm 0.01$ | $0.029 \pm 0.00$ |
| **Su2001** | 174 | 12,533 | 11 | **$0.577 \pm 0.05$** | $0.342 \pm 0.03$ | $0.303 \pm 0.03$ | $0.359 \pm 0.00$ | $0.323 \pm 0.00$ | $0.148 \pm 0.03$ | $0.057 \pm 0.01$ |
| **GCM** | 190 | 16,063 | 14 | $0.166 \pm 0.02$ | **$0.248 \pm 0.01$** | $0.182 \pm 0.01$ | $0.141 \pm 0.00$ | $0.235 \pm 0.00$ | $0.071 \pm 0.01$ | $0.126 \pm 0.00$ |
| **Breast** | 97 | 24,481 | 2 | $0.012 \pm 0.01$ | $0.005 \pm 0.00$ | $0.025 \pm 0.01$ | $0.002 \pm 0.00$ | $0.006 \pm 0.00$ | $0.002 \pm 0.00$ | **$0.043 \pm 0.00$** |
| **Endometrium** | 321 | 10,936 | 2 | $-0.008 \pm 0.00$ | **$0.688 \pm 0.00$** | $0.340 \pm 0.28$ | $0.646 \pm 0.00$ | $-0.063 \pm 0.00$ | $0.387 \pm 0.17$ | $0.337 \pm 0.00$ |
| **Mean Rank** | — | — | — | **2.67** | **3.17** | **3.50** | **4.08** | **3.83** | **5.42** | **5.33** |

### Critical Scientific Insights:
1. **Generalization Beyond Leukemia & SRBCT**:  
   GAC captures the top rank on **3 of the 6 expanded cohorts** (DLBCL, Novartis, and Su2001). In particular, on Su2001 ($N=174, D=12{,}533, K=11$), GAC delivers a massive $+0.235$ ARI lift over Standard Consensus and $+0.430$ over Sparse K-Means.
2. **Honest Failure Mode on Endometrium**:  
   On Endometrium ($N=321, K=2$), standard dense consensus and Ward clustering achieve high performance ($\text{ARI} \approx 0.65\text{--}0.69$), whereas GAC experiences assignment collapse ($-0.008$). When $N > 300$ and true $K = 2$, a default anchor budget of $L = 40$ selected solely from the stability core creates bipartite graph fragmentation across the two massive clusters. This identifies an operational parameter guideline: for large-$N$ binary cohorts, the anchor budget should be scaled with $N$ rather than fixed to a small constant.
3. **Prognostic Discordance Confirmed on Breast**:  
   On Breast ($D = 24{,}481$), all unsupervised clustering algorithms fail to reconstruct 5-year metastasis survival labels ($\text{ARI} \le 0.043$), confirming that clinical survival phenotypes in breast cancer do not reflect dominant transcriptional cluster partitions.

---

## 4. Reproducibility Files

- Execution script: `experiments/exp6_cohort_expansion/src/run_exp6.py`
- Raw per-seed outputs: `experiments/exp6_cohort_expansion/data/expanded_cohort_benchmark.csv`
- Aggregate summary table: `experiments/exp6_cohort_expansion/data/expanded_cohort_summary.csv`
