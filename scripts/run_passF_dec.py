"""
Pass F Execution Step 2:
Run remaining seeds 10-29 for DEC on the 6 high-D datasets:
cns, colon, leukemia, ovarian, prostate, srbct.
Uses concurrent.futures to parallelize across worker processes.
"""

import sys
import time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from concurrent.futures import ProcessPoolExecutor, as_completed

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from icc.datasets.registry import load_dataset
from icc.baselines.deep import run_dec

OUT_DIR = Path("results/passF")
OUT_DIR.mkdir(parents=True, exist_ok=True)

HIGH_D_DATASETS = ["cns", "colon", "leukemia", "ovarian", "prostate", "srbct"]

def evaluate_dec_single(dataset_name: str, seed: int):
    X, y, _ = load_dataset(dataset_name)
    N, D = X.shape
    K = len(np.unique(y))
    t0 = time.perf_counter()
    try:
        pred, elap, _ = run_dec(X, K, seed=seed)
        score_ari = float(adjusted_rand_score(y, pred))
        score_nmi = float(normalized_mutual_info_score(y, pred))
    except Exception as e:
        score_ari, score_nmi, elap = 0.0, 0.0, time.perf_counter() - t0

    return {
        "dataset": dataset_name, "N": N, "D": D, "K": K,
        "model": "DEC", "seed": seed,
        "ari": score_ari, "nmi": score_nmi,
        "elapsed_sec": elap
    }

def main():
    out_file = OUT_DIR / "high_d_30seeds_dec.csv"
    existing_records = []
    done_keys = set()
    if out_file.exists():
        existing_records = pd.read_csv(out_file).to_dict(orient="records")
        done_keys = set((r['dataset'], r['model'], r['seed']) for r in existing_records)
        print(f"Found {len(existing_records)} existing records in {out_file}")

    records = list(existing_records)

    tasks = []
    for dname in HIGH_D_DATASETS:
        for seed in range(10, 30):
            if (dname, "DEC", seed) not in done_keys:
                tasks.append((dname, seed))

    print(f"Total DEC tasks to run: {len(tasks)}")

    # We use 6 worker processes (1 per dataset) to avoid CPU contention while maximizing throughput
    max_workers = min(6, len(tasks)) if tasks else 1

    if tasks:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {
                executor.submit(evaluate_dec_single, dname, seed): (dname, seed)
                for dname, seed in tasks
            }
            completed = 0
            for future in as_completed(future_to_task):
                dname, seed = future_to_task[future]
                try:
                    res = future.result()
                    records.append(res)
                    completed += 1
                    print(f"[{completed}/{len(tasks)}] DEC on {dname.upper()} seed {seed}: ARI={res['ari']:.4f}, time={res['elapsed_sec']:.1f}s", flush=True)
                except Exception as exc:
                    print(f"Task {dname} seed {seed} generated an exception: {exc}")

                # Save intermediate progress every 5 tasks
                if completed % 5 == 0:
                    pd.DataFrame(records).to_csv(out_file, index=False)

        pd.DataFrame(records).to_csv(out_file, index=False)
        print(f"[OK] Saved {len(records)} DEC records to {out_file}")
    else:
        print("[OK] All DEC tasks already finished.")

if __name__ == "__main__":
    main()
