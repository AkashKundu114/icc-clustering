# Human Review Verification Checklist (Pass F)

**Canonical Manuscript Title:** "When Does Feature Gating and Anchor Consensus Improve High-Dimensional Clustering? An Empirical Examination"  
*(Historical Project Allotment Titles: "Cluster Stability-Based Ensemble Learning for Noisy High-Dimensional Data", "Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes")*  
**Canonical Publication Venue:** Springer Nature Journal (*Data Mining and Knowledge Discovery* / DAMI)  
**Active Release Version:** `v2.1.0` *(with `v2.0.0` documented as prior historical release baseline)*  
**Date:** 2026-10-23  
**Target:** Independent Human Review Package for Project Supervisor and Co-Authors  
**Objective:** Provide concrete, falsifiable verification checkpoints with exact script commands and file locations. Every cell, macro, and citation can be recomputed directly from raw data stores (`results/passF/`) without trusting agent summaries.

---

## 1. Concrete Numerical Checkpoints to Recompute

Run the verification commands below and compare output directly against the manuscript (`springer_manuscript/main.tex` and compiled PDF `springer_manuscript/main.pdf`):

| # | Item / Claim in Paper | Value in Paper / Store | Direct Recomputation Command |
| :--- | :--- | :--- | :--- |
| **1** | Nemenyi Critical Difference ($N=13$) | $CD = 4.19$ | `python -c "import numpy as np; print(round(3.219 * np.sqrt(11 * 12 / (6 * 13)), 2))"` |
| **2** | Nemenyi Critical Difference ($N=12$) | $CD = 4.36$ | `python -c "import numpy as np; print(round(3.219 * np.sqrt(11 * 12 / (6 * 12)), 2))"` |
| **3** | Friedman Omnibus Test ($N=13$, 2,750 fits) | $\chi_F^2 = 9.59, p = 0.48$ | `python -c "import json; d=json.load(open('results/passF/friedman_nemenyi_passF.json')); print('chi2:', round(d['N13']['friedman']['stat'],2), 'p:', round(d['N13']['friedman']['p'],2))"` |
| **4** | Omnibus Top Mean Ranks ($N=13$) | Std Cons 4.85, KM 5.00, DEC 5.08, ICC-v2 5.23, Ward 5.31 | `python -c "import json; d=json.load(open('results/passF/friedman_nemenyi_passF.json'))['N13']['ranks']; print({k: round(d[k],2) for k in ['Standard_Consensus','K-Means','DEC','ICC_v2','Ward']})"` |
| **5** | High-D Subgroup Rank #1 (6 datasets, 30 seeds) | $R = 2.00$ | `python -c "import json; d=json.load(open('results/passF/friedman_nemenyi_passF.json')); print(d['HighD_N6']['ranks']['ICC_v2'])"` |
| **6** | 30-Seed Ablation Gain V5 - V4 | $\Delta = +0.019$ | `python -c "import json; d=json.load(open('results/passF/ablation_stats_passF.json')); print(round(d['v5_vs_v4']['mean_diff'],3))"` |
| **7** | 30-Seed Ablation 95% Bootstrap CI & Wilcoxon Test | $[-0.039, +0.082]$ ($W=9.0, p=0.84$) | `python -c "import json; d=json.load(open('results/passF/ablation_stats_passF.json')); print('CI:', [round(x,3) for x in d['v5_vs_v4']['ci_95']], 'W:', d['v5_vs_v4']['wilcoxon_w'], 'p:', round(d['v5_vs_v4']['wilcoxon_p'],2))"` |
| **8** | Fair Baselines 30-Seed ICC-v2 Subgroup Mean | $0.217 \pm 0.305$ | `python -c "import pandas as pd; df=pd.read_csv('results/passF/fair_baselines_30seeds_passF.csv'); s=df[df['model']=='ICC_v2']['ari']; print(f'{s.mean():.3f} +/- {s.std():.3f}')"` |
| **9** | Fair Baselines 30-Seed ICC-v2 Subgroup Median | $0.036$ | `python -c "import pandas as pd; df=pd.read_csv('results/passF/fair_baselines_30seeds_passF.csv'); print(round(float(df[df['model']=='ICC_v2']['ari'].median()), 3))"` |
| **10** | 30-Seed Leukemia Recovery (Mean, Med, Success) | Mean $0.600 \pm 0.367$, Med $0.787$, $73.3\% > 0.5$ | `python -c "import pandas as pd; s=pd.read_csv('results/passF/high_d_30seeds_all_models.csv').query('dataset==\"leukemia\" and model==\"ICC_v2\"')['ari']; print(f'Mean: {s.mean():.3f}, Med: {s.median():.3f}, Share>0.5: {(s>0.5).mean()*100:.1f}%')"` |
| **11** | 30-Seed SRBCT Recovery (Mean, Med, Success) | Mean $0.546 \pm 0.102$, Med $0.547$, $70.0\% > 0.5$ | `python -c "import pandas as pd; s=pd.read_csv('results/passF/high_d_30seeds_all_models.csv').query('dataset==\"srbct\" and model==\"ICC_v2\"')['ari']; print(f'Mean: {s.mean():.3f}, Med: {s.median():.3f}, Share>0.5: {(s>0.5).mean()*100:.1f}%')"` |
| **12** | Prostate Failure Mode under 30 Seeds | Ambient KM $0.049$, ICC-v2 $0.012 \pm 0.013$ | `python -c "import pandas as pd; df=pd.read_csv('results/passF/fair_baselines_30seeds_passF.csv'); km=df[(df['dataset']=='prostate') & (df['model']=='K-Means_All')]['ari'].mean(); icc=df[(df['dataset']=='prostate') & (df['model']=='ICC_v2')]['ari'].mean(); print(f'KM: {km:.3f}, ICC: {icc:.3f}')"` |
| **13** | Inductive Paired Diff: Centroid vs Ambient KM | $\Delta = +0.046$ (95% CI: $[-0.029, +0.129]$) | `python -c "import json; d=json.load(open('results/passF/inductive_bootstrap_stats.json'))['centroid_vs_ambient_km']; print('Diff:', round(d['mean_diff'],3), 'CI:', [round(x,3) for x in d['ci_95']])"` |
| **14** | Inductive Paired Diff: Centroid vs Nystrom | $\Delta = -0.023$ (95% CI: $[-0.081, +0.033]$) | `python -c "import json; d=json.load(open('results/passF/inductive_bootstrap_stats.json'))['centroid_vs_nystrom']; print('Diff:', round(d['mean_diff'],3), 'CI:', [round(x,3) for x in d['ci_95']])"` |
| **15** | Inductive Paired Diff: Centroid vs Random Forest | $\Delta = -0.006$ (95% CI: $[-0.053, +0.046]$) | `python -c "import json; d=json.load(open('results/passF/inductive_bootstrap_stats.json'))['centroid_vs_rf']; print('Diff:', round(d['mean_diff'],3), 'CI:', [round(x,3) for x in d['ci_95']])"` |
| **16** | Exp 5 Controlled Scaling: Default Exponent $\beta$ | $\beta = 0.755 \pm 0.084$ (95% CI: $[0.590, 0.921]$) | `python -c "import json; d=json.load(open('results/passE/exp5_scaling_stats.json'))['Default_Exp4']; print('Beta:', round(d['beta'],3), 'CI:', [round(x,3) for x in d['ci_95']])"` |
| **17** | Exp 5 Controlled Scaling: Reduced Exponent $\beta$ | $\beta = 0.873 \pm 0.076$ (95% CI: $[0.724, 1.023]$) | `python -c "import json; d=json.load(open('results/passE/exp5_scaling_stats.json'))['Optimized_Exp5']; print('Beta:', round(d['beta'],3), 'CI:', [round(x,3) for x in d['ci_95']])"` |
| **18** | Exp 5 Runtimes at $N=10^6$ | Default $182.6\text{ s}$ vs Reduced $141.2\text{ s}$ | `python -c "import json; d=json.load(open('results/passE/exp5_scaling_stats.json')); print('Def:', round(d['Default_Exp4']['mean_time_1M'],1), 'Opt:', round(d['Optimized_Exp5']['mean_time_1M'],1))"` |
| **19** | Scaling Peak Memory Reduction at $N=10{,}000$ | $97.4\%$ reduction ($68.8\text{ MB}$ vs $2{,}670.6\text{ MB}$) | `python -c "import pandas as pd; df=pd.read_csv('experiments/exp4_scalability_and_sensitivity/data/exp4_sample_scaling_summary.csv'); r=df[df['N']==10000]; exact=r[r['model']=='Standard_Consensus']['peak_trace_mean'].values[0]; red=r[r['model']=='ICC_v2']['peak_trace_mean'].values[0]; print(f'{100*(1-red/exact):.1f}%')"` |
| **20** | Scaling Graph Working Memory at $N=10{,}000$ | $99.6\%$ reduction ($3.06\text{ MB}$ vs $762.8\text{ MB}$) | `python -c "import pandas as pd; df=pd.read_csv('experiments/exp4_scalability_and_sensitivity/data/exp4_sample_scaling_summary.csv'); r=df[df['N']==10000]; exact=r[r['model']=='Standard_Consensus']['graph_mem_mb'].values[0]; red=r[r['model']=='ICC_v2']['graph_mem_mb'].values[0]; print(f'{100*(1-red/exact):.1f}%')"` |
| **21** | Stale Token Purge (0.704, 0.537, 55.6, 17.0x, 57.98) | 0 occurrences in main.tex and compiled PDF | `python tests/test_macro_consistency.py` |
| **22** | PDF-Level Text Extractor & Allowlist Test | 100% allowed decimals in abstract, sec 5-6, captions | `python tests/test_pdf_allowlist.py` |
| **23** | Fig. 7 Bar Chart Values vs Caption Ranks | Exact equality ($4.85, 5.00, 5.08, 5.23, 5.31$) | `python tests/test_pdf_allowlist.py` |
| **24** | All Unit & Integration Tests | 84 passed | `python -m pytest tests/` |
| **25** | Static Typing & Linting | 0 errors | `python -m ruff check src/ tests/ && python -m mypy -p icc` |

---

## 2. Automated Test Suite Commands

```powershell
# 1. Macro and text consistency
python tests/test_macro_consistency.py

# 2. PDF text extractor & allowlist test
python tests/test_pdf_allowlist.py

# 3. Full pytest suite
python -m pytest tests/

# 4. Lint and typecheck
python -m ruff check src/ tests/
python -m mypy -p icc

# 5. Compile PDF
manuscript/scripts/bin/tectonic.exe -X compile springer_manuscript/main.tex
```
