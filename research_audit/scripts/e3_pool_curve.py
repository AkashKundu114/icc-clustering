import glob, os, warnings, numpy as np, pandas as pd
warnings.filterwarnings("ignore")
from sklearn.metrics import adjusted_rand_score as ari
from src.icc.consensus_v2 import InvariantCoreConsensusV2 as ICC
fr=[0.02,0.05,0.10,0.15,0.25,0.40,1.00]; rows=[]
for f in sorted(glob.glob('experiments/exp3_real_world_benchmarks/data/cache/*.npz')):
    name=os.path.basename(f)[:-4]; d=np.load(f); X,y=d['X'].astype(float),d['y']; k=len(np.unique(y))
    for fq in fr:
        for mode in ['bc_frac','random_frac']:
            if fq==1.0 and mode=='random_frac': continue
            for s in range(5):
                m=ICC(n_clusters=k,n_anchors=30,random_state=s,pool_mode=mode,pool_frac=fq)
                rows.append(dict(data=name,frac=fq,mode=mode,seed=s,ari=ari(y,m.fit_predict(X))))
df=pd.DataFrame(rows); df.to_csv('research_audit/results/e3_pool_curve.csv',index=False)
t=df.pivot_table(index=['data','mode'],columns='frac',values='ari').round(3); pd.set_option('display.width',200); print(t.to_string())
print("\nmean over datasets:"); print(df.pivot_table(index='mode',columns='frac',values='ari').round(3).to_string())
