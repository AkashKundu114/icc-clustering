import sys, time, warnings, pathlib, numpy as np
warnings.filterwarnings("ignore")
REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
try:
    import resource
    def get_rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
except ImportError:
    import psutil
    def get_rss(): return psutil.Process().memory_info().rss / 1024 / 1024

from src.icc.core import build_dataset
from src.icc.consensus_v2 import InvariantCoreConsensusV2 as ICC
N=int(sys.argv[1]); D=int(sys.argv[2]); sz=[N//3,N//3,N-2*(N//3)]
X,y=build_dataset(D-2,"gaussian",noise_seed=0,sizes=sz,k=3,signal_dim=2)
base=get_rss()
t=time.perf_counter(); m=ICC(n_clusters=3,n_anchors=30,random_state=0,pool_mode='robust'); m.fit_predict(X); t=time.perf_counter()-t
peak=get_rss()
print(f"{N},{D},{t:.2f},{base:.0f},{peak:.0f}")
