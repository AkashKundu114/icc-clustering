import glob, os, warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore")
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score as ari
from src.icc.consensus_v2 import InvariantCoreConsensusV2 as ICC
rows=[]
for f in sorted(glob.glob('experiments/exp3_real_world_benchmarks/data/cache/*.npz')):
    name=os.path.basename(f)[:-4]; d=np.load(f); X0,y=d['X'].astype(float),d['y']; k=len(np.unique(y))
    for rho in [0.0,0.1,0.2,0.3,0.5]:
        for s in range(5):
            rng=np.random.default_rng(1000+s); X=X0.copy(); mask=rng.random(X.shape)<rho; X[mask]=np.nan
            cm=np.nanmean(X,axis=0); cm=np.where(np.isnan(cm),0.0,cm); X=np.where(np.isnan(X),cm[None,:],X)
            rows.append(dict(data=name,rho=rho,seed=s,ICC=ari(y,ICC(n_clusters=k,n_anchors=30,random_state=s).fit_predict(X)),
                             KM=ari(y,KMeans(k,n_init=10,random_state=s).fit_predict(X))))
os.makedirs('experiments/audit_controls/data', exist_ok=True)
df=pd.DataFrame(rows); df.to_csv('experiments/audit_controls/data/e5_missing_rerun.csv',index=False)
pd.set_option('display.width',200)
inf=df[df.data.isin(['leukemia','srbct','colon'])]
print("informative 3:"); print(inf.pivot_table(index='rho',columns='data',values='ICC').round(3).to_string())
g=inf.groupby('rho')[['ICC','KM']].mean(); g['ICC_retention']=g.ICC/g.ICC.iloc[0]; print(g.round(3).to_string())
print("\nall 8 mean ARI:"); print(df.groupby('rho')[['ICC','KM']].mean().round(3).to_string())
