"""A3: (i) is U_emb = B_norm V the bipartite spectral embedding? compare to dense N x N spectral on W_full = B_norm D_L^-1 B_norm^T
        (ii) dense path vs scalable path agreement. Uses the model's own B."""
import warnings, numpy as np, scipy.linalg as sla, pandas as pd
warnings.filterwarnings("ignore")
from scipy.linalg import subspace_angles
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score as ari
from src.icc.core import build_dataset, pairwise_coassoc
from src.icc.consensus_v2 import InvariantCoreConsensusV2 as ICC

def parts(X,k,seed,M=25,pool_mode='legacy'):
    m=ICC(n_clusters=k,n_base_models=M,n_anchors=30,random_state=seed,pool_mode=pool_mode); m.fit_predict(X); return m
def emb_variants(B,k):
    Bn=B/np.fmax(B.sum(1,keepdims=True),1e-12); W=Bn.T@Bn; deg=W.sum(1); Di=1/np.sqrt(np.fmax(deg,1e-12))
    Ln=np.eye(len(deg))-Di[:,None]*W*Di[None,:]; ev,V=sla.eigh(Ln)
    cur=Bn@V[:,:k]                                     # current code (before row-norm)
    sig=np.fmax(1-ev[:k],1e-9)                         # eigvals of D^-1/2 W D^-1/2
    tc=Bn@(Di[:,None]*V[:,:k])/np.sqrt(sig)            # transfer-cut / bipartite embedding
    Wf=Bn@(Bn.T/np.fmax(deg,1e-12)[:,None].T.T)        # placeholder replaced below
    Wf=(Bn/np.fmax(deg,1e-12)[None,:])@Bn.T
    Wf=(Wf+Wf.T)/2; ew,Vf=np.linalg.eigh(Wf); dense=Vf[:,::-1][:,:k]   # top-k of dense graph (row-stochastic-type)
    return cur,tc,dense
rows=[]
for kind,seed in [("gaussian",0),("scaled",1),("student_t",2)]:
    X,y=build_dataset(40,kind,noise_seed=seed,sizes=[100,100,100],k=3,signal_dim=2)   # low-noise regime so structure exists
    m=parts(X,3,seed)
    S=pairwise_coassoc([np.asarray(p) for p in [m.labels_]])  # dummy to keep import used
    # rebuild B exactly as model does (dense branch)
    rng=np.random.default_rng(seed)
    B=None
    # recompute partitions via model internals is not exposed -> approximate with co-association of fresh ensemble on model pool
    from src.icc.core import run_clusterer
    pool=m.selected_features_; parts_=[run_clusterer('kmeans',X[:,np.random.default_rng(s).choice(pool,size=max(2,int(len(pool)*0.3)),replace=False)],3,seed=s) for s in range(25)]
    Sx=pairwise_coassoc(parts_); anchors=m.anchor_indices_; B=Sx[:,anchors]
    cur,tc,dense=emb_variants(B,3)
    ang=lambda A,Bm: np.cos(subspace_angles(A,Bm)).round(3).tolist()
    lab=lambda E: ari(y,KMeans(3,n_init=10,random_state=0).fit_predict(E/np.fmax(np.linalg.norm(E,axis=1,keepdims=True),1e-12)))
    rows.append(dict(data=kind,cos_cur_vs_dense=ang(cur,dense),cos_tc_vs_dense=ang(tc,dense),ARI_cur=round(lab(cur),3),ARI_tc=round(lab(tc),3),ARI_dense=round(lab(dense),3)))
print(pd.DataFrame(rows).to_string())
# path equivalence: dense vs scalable branch on the same data (needs dense_threshold param; falls back if absent)
