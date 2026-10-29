"""
scripts/run_dec_stability.py

Runs DEC across the 6 high-dimensional cohorts for 30 subsamples (real & null),
resumable, saving directly into results/stability/runs/*.parquet and partitions/*.npy.
"""

import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from icc.datasets.registry import load_dataset
from scripts.stability_subsample import HIGH_D_DATASETS, run_single_fit, evaluate_stability

def main():
    print("[*] Starting DEC Subsample Stability Runs...")
    for d_name in HIGH_D_DATASETS:
        X, y, meta = load_dataset(d_name)
        k = meta["K"]
        print(f"\n--- DEC on {d_name.upper()} (N={len(X)}, D={X.shape[1]}, K={k}) ---")
        for mode in ["real", "null"]:
            for sub_id in range(30):
                rec = run_single_fit(d_name, "DEC", sub_id, mode, X, y, k)
                print(f"  [DEC {mode} #{sub_id:02d}] {rec['status']} in {rec['runtime']:.2f}s (acc={rec['accuracy']})")

    print("\n[*] DEC complete! Re-evaluating summary...")
    import subprocess
    subprocess.run([sys.executable, "scripts/stability_subsample.py", "--compile-only"], check=True)

if __name__ == "__main__":
    main()
