import os, sys, warnings, numpy as np, pandas as pd
from pathlib import Path
warnings.filterwarnings("ignore")

root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from scipy.stats import kurtosis, skew
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
    d=np.load(f'experiments/exp3_real_world_benchmarks/data/cache/{name}.npz'); X,y=d['X'].astype(float),d['y']; k=len(np.unique(y)); N,D=X.shape
    m0=ICC(n_clusters=k,random_state=0,pool_mode='legacy'); m0.fit_predict(X); pool_n=len(m0.selected_features_)
    bc=m0.feature_scores_; top_bc=np.argsort(bc)[-pool_n:]; top_var=np.argsort(X.var(0))[-pool_n:]
    for s in range(10):
        km=lambda cols: ari(y,KMeans(k,n_init=10,random_state=s).fit_predict(X[:,cols]))
        rows.append(dict(data=name,seed=s,pool=pool_n,KM_all=km(slice(None)),KM_topBC=km(top_bc),KM_topVar=km(top_var)))
df=pd.DataFrame(rows); df.to_csv('research_audit/results/a2_filter_controls.csv',index=False)
print(df.groupby('data')[['pool','KM_all','KM_topBC','KM_topVar']].mean().round(3).to_string())
