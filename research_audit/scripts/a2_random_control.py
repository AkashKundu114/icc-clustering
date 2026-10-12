import glob, os, sys, warnings, numpy as np, pandas as pd
from pathlib import Path
warnings.filterwarnings("ignore")

root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

try:
    from sklearn.cluster import KMeans
    from sklearn.metrics import adjusted_rand_score as ari
    _ = KMeans(2, n_init=1).fit_predict(np.zeros((4, 2)))
except Exception:
    from src.icc.core import run_clusterer, adjusted_rand_score as ari
    class KMeans:
        def __init__(self, n_clusters, n_init=10, random_state=42):
            self.n_clusters = n_clusters
            self.random_state = random_state
        def fit_predict(self, X):
            return run_clusterer("kmeans", X, self.n_clusters, seed=self.random_state)
from src.icc.consensus_v2 import InvariantCoreConsensusV2 as ICC
rows=[]
for name in ['leukemia','srbct','colon','cns']:
    d=np.load(f'experiments/exp3_real_world_benchmarks/data/cache/{name}.npz'); X,y=d['X'].astype(float),d['y']; k=len(np.unique(y))
    for s in range(10):
        r={'data':name,'seed':s,'KM_all':ari(y,KMeans(k,n_init=10,random_state=s).fit_predict(X))}
        for mode in ['legacy','random']:
            r[f'ICC_{mode}']=ari(y,ICC(n_clusters=k,n_base_models=25,n_anchors=30,random_state=s,pool_mode=mode).fit_predict(X))
        rows.append(r)
df=pd.DataFrame(rows); df.to_csv('research_audit/results/a2_random_control.csv',index=False)
g=df.groupby('data')[['KM_all','ICC_legacy','ICC_random']].agg(['mean','std']).round(3); print(g.to_string())
