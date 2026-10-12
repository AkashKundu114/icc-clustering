import glob, os, warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore")
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score as ari
from src.icc.consensus_v2 import InvariantCoreConsensusV2 as ICC
rows=[]
for name in ['leukemia','srbct','colon','cns']:
    d=np.load(f'experiments/exp3_real_world_benchmarks/data/cache/{name}.npz'); X,y=d['X'].astype(float),d['y']; k=len(np.unique(y))
    for s in range(10):
        r={'data':name,'seed':s,'KM_all':ari(y,KMeans(k,n_init=10,random_state=s).fit_predict(X))}
        for mode in ['legacy','random']:
            r[f'ICC_{mode}']=ari(y,ICC(n_clusters=k,n_base_models=25,n_anchors=30,random_state=s,pool_mode=mode).fit_predict(X))
        rows.append(r)
os.makedirs('experiments/audit_controls/data', exist_ok=True)
df=pd.DataFrame(rows); df.to_csv('experiments/audit_controls/data/a2_random_control.csv',index=False)
g=df.groupby('data')[['KM_all','ICC_legacy','ICC_random']].agg(['mean','std']).round(3); print(g.to_string())
