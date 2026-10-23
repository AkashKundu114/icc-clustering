"""
Pass F Execution Step 1:
Run remaining seeds 10-29 for the 8 fast models on the 6 high-D datasets:
Models: K-Means, Spectral, FCM, Standard_Consensus, Core_Halo_Consensus, ICC_v1, FCAG, FastMVC.
Ward is copied from seed 0 (deterministic).
ICC-v2 seeds 10-29 are copied from results/passE/high_d_30seeds_bimodal.csv.
"""

import sys
import time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from icc.datasets.registry import load_dataset
from icc.baselines.classical import run_single_kmeans, run_single_ward, run_single_spectral, run_single_fcm
from icc.baselines.consensus import run_standard_consensus, run_icc_v1, run_li_et_al_2019
from icc.baselines.anchor import run_fcag, run_fastmvc

OUT_DIR = Path("results/passF")
OUT_DIR.mkdir(parents=True, exist_ok=True)

HIGH_D_DATASETS = ["cns", "colon", "leukemia", "ovarian", "prostate", "srbct"]
FAST_MODELS = {
    "K-Means": run_single_kmeans,
    "Spectral": run_single_spectral,
    "FCM": run_single_fcm,
    "Standard_Consensus": run_standard_consensus,
    "Core_Halo_Consensus": run_li_et_al_2019,
    "ICC_v1": run_icc_v1,
    "FCAG": run_fcag,
    "FastMVC": run_fastmvc,
}

def main():
    out_file = OUT_DIR / "high_d_30seeds_fast_models.csv"
    existing_records = []
    done_keys = set()
    if out_file.exists():
        existing_records = pd.read_csv(out_file).to_dict(orient="records")
        done_keys = set((r['dataset'], r['model'], r['seed']) for r in existing_records)
        print(f"Found {len(existing_records)} existing records in {out_file}")

    records = list(existing_records)

    for dname in HIGH_D_DATASETS:
        X, y, _ = load_dataset(dname)
        N, D = X.shape
        K = len(np.unique(y))
        print(f"\nProcessing {dname.upper()} (N={N}, D={D}, K={K})...")

        for mname, mfunc in FAST_MODELS.items():
            for seed in range(10, 30):
                if (dname, mname, seed) in done_keys:
                    continue

                t0 = time.perf_counter()
                try:
                    pred, elap, _ = mfunc(X, K, seed=seed)
                    score_ari = adjusted_rand_score(y, pred)
                    score_nmi = normalized_mutual_info_score(y, pred)
                except Exception as e:
                    print(f"  [Error] {mname} on {dname} seed {seed}: {e}")
                    score_ari, score_nmi, elap = 0.0, 0.0, time.perf_counter() - t0

                rec = {
                    "dataset": dname, "N": N, "D": D, "K": K,
                    "model": mname, "seed": seed,
                    "ari": score_ari, "nmi": score_nmi,
                    "elapsed_sec": elap
                }
                records.append(rec)
                done_keys.add((dname, mname, seed))

        # Save after each dataset
        pd.DataFrame(records).to_csv(out_file, index=False)
        print(f"  Saved progress: {len(records)} records.")

    print(f"\n[DONE] Finished running fast models for seeds 10-29. Total records: {len(records)}")

if __name__ == "__main__":
    main()
