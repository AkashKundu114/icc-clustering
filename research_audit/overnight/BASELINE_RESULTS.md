# Overnight Research Audit: Modern & Classical Baseline Comparison Results

**Document Reference:** `research_audit/overnight/BASELINE_RESULTS.md`  
**Related Results:** `results/overnight/baselines/modern_baselines_results.csv`  
**Audit Date:** 2026-11-01  
**Auditor:** Agent C — Modern Baseline Auditor  

---

## 1. Executive Summary & Benchmark Rankings

We benchmarked 8 representative algorithms across the confirmed independent biological cohorts under identical known-$K$ protocols:

| Rank | Model | Algorithmic Category | Macro-Average ARI | Mean Rank (1-8) |
| :---: | :--- | :--- | :---: | :---: |
| 1 | **Ward** | Specialized / Probabilistic | **0.1586** | **4.14** |
| 2 | **Standard_Consensus** | Ensemble Consensus | **0.1507** | **4.00** |
| 3 | **Sparse_KMeans** | Classical Partitional | **0.1464** | **4.09** |
| 4 | **GMM_BIC** | Specialized / Probabilistic | **0.1369** | **4.68** |
| 5 | **HDBSCAN*** | Specialized / Probabilistic | **0.1297** | **5.64** |
| 6 | **K-Means** | Classical Partitional | **0.1137** | **4.64** |
| 7 | **FCM** | Specialized / Probabilistic | **0.1043** | **4.18** |
| 8 | **Spectral** | Specialized / Probabilistic | **0.0865** | **4.64** |

---

## 2. Per-Cohort Breakdown of Macro-Average ARI

| cohort      |        FCM |     GMM_BIC |   HDBSCAN* |     K-Means |   Sparse_KMeans |    Spectral |   Standard_Consensus |        Ward |
|:------------|-----------:|------------:|-----------:|------------:|----------------:|------------:|---------------------:|------------:|
| breast      | 0.0409069  |  0.00224186 |  0         |  0.00806868 |      0.00224186 |  0.00620148 |           0.00224186 |  0.00224186 |
| cns         | 0.00163472 | -0.0109347  |  0         | -0.0328746  |     -0.0194832  | -0.00401411 |          -0.0196819  | -0.0223732  |
| colon       | 0.0313834  | -0.0185838  |  0         |  0.0399951  |      0.0147181  | -0.0232453  |          -0.0154496  | -0.0157725  |
| dlbcl       | 0.0491169  |  0.073221   |  0         |  0.0154469  |      0.0370599  |  0.0604578  |           0.0215598  |  0.052423   |
| endometrium | 0.344191   |  0.468061   | -0.0494247 |  0.207016   |      0.429825   | -0.0626681  |           0.514816   |  0.645932   |
| leukemia    | 0.107307   |  0.0788099  |  0         |  0.0970781  |      0.182914   |  0.1389     |           0.127896   |  0.0816371  |
| ovarian     | 0.00102304 |  0.00757202 | -0.0389736 |  0.00693178 |      0.00626158 |  0.0185834  |           0.00925534 |  0.0109551  |
| prostate    | 0.0482971  |  0.0302678  |  0         |  0.0456075  |      0.049082   | -0.0034125  |           0.049082   |  0.0263806  |
| srbct       | 0.102796   |  0.065243   |  0.305481  |  0.124018   |      0.041343   |  0.0801656  |           0.0364933  |  0.109055   |
| su2001      | 0.0565059  |  0.349307   |  0.977035  |  0.274865   |      0.284258   |  0.327754   |           0.384175   |  0.359165   |
| zheng68k    | 0.364616   |  0.460338   |  0.232174  |  0.464101   |      0.582662   |  0.413073   |           0.547277   |  0.495316   |
