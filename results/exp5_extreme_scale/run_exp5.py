#!/usr/bin/env python3
"""
CLI runner for Experiment 5: Extreme Asymptotic Scaling Stress Suite.

Usage:
    python run_exp5.py --run-full --trials 3
    python run_exp5.py --reproduce-plots
    python run_exp5.py
"""

import argparse
import sys
import time
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from experiments.exp5_extreme_scale.src.extreme_scale_benchmark import run_all
from experiments.exp5_extreme_scale.src.plot_exp5 import generate_all_plots


def main():
    parser = argparse.ArgumentParser(description="Exp 5: Extreme Asymptotic Scaling Suite")
    parser.add_argument("--run-full", action="store_true", help="Run full multi-trial scaling simulations")
    parser.add_argument("--trials", type=int, default=3, help="Number of trials per condition (default: 3)")
    parser.add_argument("--reproduce-plots", action="store_true", help="Re-generate figures from existing CSVs")

    args = parser.parse_args()

    t_start = time.time()
    if args.reproduce_plots:
        print("[*] Re-generating Exp 5 figures from cached CSVs...")
        generate_all_plots()
        print("[OK] Plots re-generated successfully.")
    elif args.run_full:
        print(f"[*] Starting Exp 5 full sweep ({args.trials} trials per condition)...")
        run_all(n_trials=args.trials)
        generate_all_plots()
        print(f"[OK] Finished Exp 5 full execution in {time.time() - t_start:.2f}s.")
    else:
        # Default: execute standard benchmark and generate publication plots
        print(f"[*] Running Exp 5 standard execution ({args.trials} trials)...")
        run_all(n_trials=args.trials)
        generate_all_plots()
        print(f"[OK] Exp 5 completed in {time.time() - t_start:.2f}s.")


if __name__ == "__main__":
    main()
