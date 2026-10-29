"""
scripts/finish_dec_runs.py

Completes all remaining DEC subsample runs using PyTorch GPU acceleration.
Skips any run already saved in results/stability/runs.
"""

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from icc.datasets.registry import load_dataset
from scripts.stability_subsample import run_single_fit

DATASETS = ["srbct", "cns", "leukemia", "prostate", "ovarian"]

def main():
    print("=" * 60, flush=True)
    print("FINISHING REMAINING DEC RUNS ON GPU", flush=True)
    print("=" * 60, flush=True)

    total_done = 0
    t0_all = time.time()

    for d_name in DATASETS:
        X, y, meta = load_dataset(d_name)
        k = meta["K"]
        print(f"\n[*] Dataset: {d_name.upper()} (N={len(X)}, D={X.shape[1]}, K={k})", flush=True)

        for mode in ["real", "null"]:
            for sub_id in range(30):
                p_run = Path(f"results/stability/runs/{d_name}_DEC_{mode}_{sub_id}.parquet")
                if p_run.exists():
                    continue
                t0 = time.time()
                rec = run_single_fit(d_name, "DEC", sub_id, mode, X, y, k)
                dt = time.time() - t0
                total_done += 1
                print(f"  [{d_name} DEC {mode} #{sub_id:02d}] {rec['status']} in {dt:.2f}s (acc={rec['accuracy']})", flush=True)

    print(f"\n[+] All DEC runs completed! Total newly processed: {total_done} in {time.time()-t0_all:.1f}s", flush=True)

if __name__ == "__main__":
    main()
