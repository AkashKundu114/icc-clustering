import sys
from pathlib import Path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))
import numpy as np
from src.icc.consensus_v2 import InvariantCoreConsensusV2

data_leuk = np.load("experiments/exp3_real_world_benchmarks/data/cache/leukemia.npz")
X_leuk, y_leuk = data_leuk["X"].astype(np.float64), data_leuk["y"]
from sklearn.metrics import adjusted_rand_score as ari

print("=== SMOKE RUN BASELINE ===")
for seed in [0, 1, 2]:
    model = InvariantCoreConsensusV2(n_clusters=2, random_state=seed)
    preds = model.fit_predict(X_leuk)
    score = ari(y_leuk, preds)
    test_preds = model.predict(X_leuk[:10], subspace=True)
    print(f"Leukemia Seed {seed}: ARI = {score:.4f}, test_preds = {test_preds.tolist()}")
