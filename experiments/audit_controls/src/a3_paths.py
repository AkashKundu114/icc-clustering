import warnings, numpy as np, pandas as pd, glob, os
warnings.filterwarnings("ignore")
from sklearn.metrics import adjusted_rand_score as ari
from icc.core import build_dataset
from icc.consensus_v2 import InvariantCoreConsensusV2 as ICC
print("== path equivalence: dense vs scalable branch (N=900, D=500, 4 seeds) ==")
rows=[]
for kind in ["gaussian","student_t"]:
    for s in range(4):
        X,y=build_dataset(498,kind,noise_seed=s,sizes=[300,300,300],k=3,signal_dim=2)
        a=ICC(n_clusters=3,n_anchors=30,random_state=s,pool_mode='robust'); la=a.fit_predict(X)
        b=ICC(n_clusters=3,n_anchors=30,random_state=s,pool_mode='robust',dense_threshold=0); lb=b.fit_predict(X)
        rows.append(dict(noise=kind,seed=s,ARI_dense=ari(y,la),ARI_scalable=ari(y,lb),agree=ari(la,lb)))
print(pd.DataFrame(rows).groupby('noise').mean(numeric_only=True).round(3).to_string())
print("\n== embedding legacy vs transfer_cut: real cached (5 seeds, legacy pool) ==")
R=[]
for f in sorted(glob.glob('experiments/exp3_real_world_benchmarks/data/cache/*.npz')):
    d=np.load(f); X,y=d['X'].astype(float),d['y']; k=len(np.unique(y))
    for s in range(5):
        r=dict(data=os.path.basename(f)[:-4])
        for emb in ['legacy','transfer_cut']:
            r[emb]=ari(y,ICC(n_clusters=k,n_anchors=30,random_state=s,embedding=emb).fit_predict(X))
        R.append(r)
g=pd.DataFrame(R).groupby('data').mean().round(3); print(g.to_string()); print(g.mean().round(3).to_dict())
