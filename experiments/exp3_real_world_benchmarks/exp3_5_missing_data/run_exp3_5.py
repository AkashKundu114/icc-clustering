#!/usr/bin/env python3
"""
CLI entry point for Experiment 3.5: Missing Data Robustness & Imputation Resilience Suite.

Usage:
    # Run full experiment (10 trials per condition) and generate publication figures:
    python run_exp3_5.py --run-full --trials 10

    # Quick run (e.g. 2 trials for fast smoke testing):
    python run_exp3_5.py --trials 2

    # Re-generate publication plots from existing CSV data:
    python run_exp3_5.py --reproduce-plots
"""

import argparse
import sys
import time
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from experiments.exp3_real_world_benchmarks.exp3_5_missing_data.src.missing_data_experiment import (
    run_missing_data_sweep,
)
from experiments.exp3_real_world_benchmarks.exp3_5_missing_data.src.plot_missing_data import (
    generate_all_plots,
)


def main():
    parser = argparse.ArgumentParser(description="Exp 3.5: Missing Data Robustness Suite")
    parser.add_argument("--run-full", action="store_true", help="Execute full multi-trial benchmark matrix")
    parser.add_argument("--trials", type=int, default=10, help="Number of trials per condition (default: 10)")
    parser.add_argument("--no-resume", action="store_true", help="Do not resume; overwrite from scratch")
    parser.add_argument("--reproduce-plots", action="store_true", help="Re-generate figures from existing CSV")

    args = parser.parse_args()
    t_start = time.perf_counter()

    if args.reproduce_plots:
        print("[*] Re-generating Exp 3.5 publication plots from cached CSV results...")
        generate_all_plots()
        print(f"[OK] Plots successfully created in {time.perf_counter() - t_start:.2f}s.")
    else:
        trials = args.trials if not args.run_full else max(10, args.trials)
        print(f"[*] Executing Exp 3.5 Missing Data benchmark ({trials} trials per condition)...")
        run_missing_data_sweep(n_trials=trials, resume=not args.no_resume)
        print("[*] Generating publication figures...")
        generate_all_plots()
        print(f"[OK] Exp 3.5 execution & figure generation completed in {time.perf_counter() - t_start:.2f}s.")


if __name__ == "__main__":
    main()
