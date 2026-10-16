"""PRE-SPECIFIED (fixed before running): grid F={.02,.05,.10,.15,.25,.40}; BC-ranked pool ('bc_frac');
criteria computed WITHOUT labels: C_sil = silhouette(labels_, U_emb_), C_stab = mean(stability_).
Selected fraction = argmax criterion per (dataset, seed). Outcome = ARI vs labels (evaluation only).
Compared with: fixed 15% (default), grid-mean, oracle-best (label-peeking UPPER BOUND, not a method)."""
import glob, os, warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore")
from sklearn.metrics import adjusted_rand_score as ari, silhouette_score
from icc.consensus_v2 import InvariantCoreConsensusV2 as ICC
F=[0.02,0.05,0.10,0.15,0.25,0.40]; rows=[]
for f in sorted(glob.glob('experiments/exp3_real_world_benchmarks/data/cache/*.npz')):
    name=os.path.basename(f)[:-4]; d=np.load(f); X,y=d['X'].astype(float),d['y']; k=len(np.unique(y))
    for s in range(5):
        res=[]
        for fq in F:
            m=ICC(n_clusters=k,n_anchors=30,random_state=s,pool_mode='bc_frac',pool_frac=fq); lab=m.fit_predict(X)
            sil=silhouette_score(m.U_emb_,lab) if len(np.unique(lab))>1 else -1.0
            res.append((fq,ari(y,lab),sil,float(np.mean(m.stability_))))
        r=np.array(res)
        rows.append(dict(data=name,seed=s,fixed15=r[3,1],grid_mean=r[:,1].mean(),sel_sil=r[np.argmax(r[:,2]),1],sel_stab=r[np.argmax(r[:,3]),1],oracle=r[:,1].max(),
                         frac_sil=r[np.argmax(r[:,2]),0],frac_stab=r[np.argmax(r[:,3]),0]))
os.makedirs('experiments/audit_controls/data', exist_ok=True)
df=pd.DataFrame(rows); df.to_csv('experiments/audit_controls/data/e3b_selector.csv',index=False)
pd.set_option('display.width',200)
print(df.groupby('data')[['fixed15','grid_mean','sel_sil','sel_stab','oracle']].mean().round(3).to_string())
print("\nmean:",df[['fixed15','grid_mean','sel_sil','sel_stab','oracle']].mean().round(3).to_dict())
print("median chosen fraction  sil:",df.frac_sil.median()," stab:",df.frac_stab.median())
