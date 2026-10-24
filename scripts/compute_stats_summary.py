import numpy as np
import pandas as pd
from scipy import stats

df = pd.read_csv('results/passF/high_d_30seeds_all_models.csv')
icc = df[df['model'] == 'ICC_v2']

print(f"{'Dataset':10s} | {'Mean':6s} | {'Std':6s} | {'CV':6s} | {'Shapiro W':10s} | {'p-value':10s} | {'Seeds > 0.50':12s}")
print('-'*70)
for d in ['cns', 'colon', 'leukemia', 'ovarian', 'prostate', 'srbct']:
    vals = icc[icc['dataset'] == d]['ari'].values
    mean = vals.mean()
    std = vals.std(ddof=1)
    cv = std / abs(mean) if abs(mean) > 1e-6 else 0.0
    w, p = stats.shapiro(vals)
    gt_half = np.sum(vals > 0.5)
    print(f"{d:10s} | {mean:+.3f} | {std:.3f} | {cv:.2f}   | {w:.4f}     | {p:.2e}   | {gt_half}/30 ({gt_half/30*100:.1f}%)")
