#!/usr/bin/env python3
"""
CLI entry point for Sub-Experiment 2.1: VSSG Interpretability and Feature Selection Audit.

Usage:
    # Run full experiment (10 trials per condition) and generate publication plots:
    python run_exp2_1.py --run-full --trials 10

    # Smoke test (1 trial):
    python run_exp2_1.py --trials 1

    # Re-generate publication figures from existing CSV:
    python run_exp2_1.py --reproduce-plots
"""

import argparse
import sys
import time
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from experiments.exp2_ablation.src.vssg_interpretability import run_all
from experiments.exp2_ablation.src.plot_vssg_figures import generate_all_plots


def main():
    parser = argparse.ArgumentParser(description="Exp 2.1: VSSG Feature Saliency Audit")
    parser.add_argument("--run-full", action="store_true", help="Execute full multi-trial audit")
    parser.add_argument("--trials", type=int, default=1, help="Number of trials per condition (default: 1)")
    parser.add_argument("--reproduce-plots", action="store_true", help="Re-generate figures from existing CSV")

    args = parser.parse_args()
    t_start = time.perf_counter()

    if args.reproduce_plots:
        print("[*] Re-generating Exp 2.1 publication plots from cached CSV results...")
        generate_all_plots()
        print(f"[OK] Figures generated in {time.perf_counter() - t_start:.2f}s.")
    else:
        trials = max(10, args.trials) if args.run_full else args.trials
        print(f"[*] Executing Exp 2.1 VSSG audit ({trials} trials)...")
        run_all(n_trials=trials)
        print("[*] Generating publication figures...")
        generate_all_plots()
        print(f"[OK] Exp 2.1 completed in {time.perf_counter() - t_start:.2f}s.")


if __name__ == "__main__":
    main()
