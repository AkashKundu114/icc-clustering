"""A2: pre-specified pool rules ('robust' c=3.5 MAD; 'gauss' Bonferroni a=0.05) + missing controls.
Rules fixed BEFORE running; no tuning on these results."""
import sys, glob, os, warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore")
from scipy.stats import kurtosis, skew
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score as ari
from src.icc.core import build_dataset
from src.icc.consensus_v2 import InvariantCoreConsensusV2 as ICC

def run(X,y,k,seed):
    out={}
    out['KM_all']=ari(y,KMeans(k,n_init=10,random_state=seed).fit_predict(X))
    for mode in ['legacy','robust','gauss']:
        m=ICC(n_clusters=k,n_base_models=25,n_anchors=30,random_state=seed,pool_mode=mode)
        lab=m.fit_predict(X); out[f'ICC_{mode}']=ari(y,lab); out[f'pool_{mode}']=len(m.selected_features_)
        if mode in('robust','gauss'):
            out[f'KM_pool_{mode}']=ari(y,KMeans(k,n_init=10,random_state=seed).fit_predict(X[:,m.selected_features_]))
            out[f'pred_{mode}']=ari(y,m.predict(X))
    return out
rows=[]
if sys.argv[1]=='syn':
    for kind in ["gaussian","scaled","correlated","student_t","sparse"]:
        for s in range(5):
            X,y=build_dataset(1998,kind,noise_seed=100+s,sizes=[80,80,80],k=3,signal_dim=2)
            r=run(X,y,3,s); r.update(data=kind,seed=s)
            for mode in ['robust','gauss']:
                pass
            rows.append(r)
else:
    for f in sorted(glob.glob('experiments/exp3_real_world_benchmarks/data/cache/*.npz')):
        d=np.load(f); X,y=d['X'].astype(float),d['y']; k=len(np.unique(y))
        for s in range(5):
            r=run(X,y,k,s); r.update(data=os.path.basename(f)[:-4],seed=s); rows.append(r)
df=pd.DataFrame(rows); df.to_csv(f'research_audit/results/a2_{sys.argv[1]}.csv',index=False)
pd.set_option('display.width',250)
cols=[c for c in df.columns if c not in('seed','data') and not c.startswith('pred')]
print(df.groupby('data')[cols].mean().round(3).to_string())
print("\nmean over data:\n",df[cols].mean().round(3).to_string())
