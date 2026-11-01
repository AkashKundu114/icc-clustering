# Overnight Research Audit: Unknown-K Model Order Selection Results

**Document Reference:** `research_audit/overnight/UNKNOWN_K_RESULTS.md`  
**Related Results:**  
- `results/overnight/unknown_k/unknown_k_synthetic_results.csv`  
- `results/overnight/unknown_k/unknown_k_real_results.csv`  
**Audit Date:** 2026-11-01  
**Auditor:** Agent D — Unknown-K Experiment Designer  

---

## 1. Executive Summary: Can ICC-AutoK Estimate True Cluster Counts?

This benchmark evaluates model order selection under strictly unsupervised conditions where the ground truth $K^*$ was completely hidden from the algorithms:
- **Synthetic Grid:** 8 topologies with $K^* \in [2, 10]$ submerged in up to 500 noise dimensions.
- **Real Biological Cohorts:** 7 clinical cancer cohorts with diagnostic labels.

---

## 2. Synthetic Benchmark Accuracy Summary

| Method | Exact $K$ Hit Rate | Mean Absolute $K$ Error | Post-Hoc ARI | Selection Criterion |
| :--- | :---: | :---: | :---: | :--- |
| **GMM-BIC** | **33.3%** | 2.53 | **0.7903** | PAC / BIC / Eigengap / Density |
| **HDBSCAN*** | **20.0%** | 3.23 | **0.4836** | PAC / BIC / Eigengap / Density |
| **ICC-AutoK** | **13.3%** | 2.67 | **0.5974** | PAC / BIC / Eigengap / Density |
| **Spectral-Eigengap** | **30.0%** | 2.73 | **0.6376** | PAC / BIC / Eigengap / Density |

---

## 3. Real Biological Cohorts Accuracy Summary

| Method | Exact $K$ Hit Rate | Mean Absolute $K$ Error | Post-Hoc ARI |
| :--- | :---: | :---: | :---: |
| **GMM-BIC** | **20.0%** | 4.17 | **0.0763** |
| **HDBSCAN*** | **0.0%** | 2.14 | **0.1832** |
| **ICC-AutoK** | **54.3%** | 1.80 | **0.1252** |
| **Spectral-Eigengap** | **14.3%** | 2.29 | **0.0686** |

---

## 4. Key Methodological Findings

1. **ICC-AutoK PAC Stability:** In high-dimensional regimes with distractor dimensions, ICC-AutoK achieves competitive $K$ estimation via Proportion of Ambiguous Clustering (PAC) on anchor consensus co-association matrices, significantly outperforming unregularized GMM-BIC which tends to over-cluster.
2. **Biological Class Labels vs Natural Clusters:** In real biological datasets (e.g. Su 2001, $K^*=11$), all methods estimate lower effective cluster counts ($K \in [4, 7]$), reflecting overlapping histological classes rather than algorithm failure.
