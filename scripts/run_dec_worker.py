"""
scripts/run_dec_worker.py

Worker to run DEC on a single specified dataset for all 30 subsamples (real & null).
Skips already completed runs.
"""

import sys
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from icc.datasets.registry import load_dataset
from scripts.stability_subsample import run_single_fit

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=str, help="Dataset name, e.g. srbct, cns, leukemia, prostate, ovarian")
    args = parser.parse_args()

    d_name = args.dataset.lower()
    X, y, meta = load_dataset(d_name)
    k = meta["K"]
    print(f"[*] Starting DEC worker on {d_name.upper()} (N={len(X)}, D={X.shape[1]}, K={k})...")

    for mode in ["real", "null"]:
        for sub_id in range(30):
            rec = run_single_fit(d_name, "DEC", sub_id, mode, X, y, k)
            print(f"  [{d_name} DEC {mode} #{sub_id:02d}] {rec['status']} in {rec['runtime']:.2f}s (acc={rec['accuracy']})")

    print(f"[+] Worker finished for {d_name}!")

if __name__ == "__main__":
    main()
