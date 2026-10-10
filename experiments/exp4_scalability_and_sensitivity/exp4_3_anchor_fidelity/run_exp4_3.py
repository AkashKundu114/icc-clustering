#!/usr/bin/env python3
"""
CLI entry point for Sub-Experiment 4.3: Anchor Approximation Fidelity Suite.

Usage:
    # Run full experiment (5 trials per condition) and generate publication plots:
    python run_exp4_3.py --run-full --trials 5

    # Smoke test (1 trial):
    python run_exp4_3.py --trials 1

    # Re-generate publication figures from existing CSV:
    python run_exp4_3.py --reproduce-plots
"""

import argparse
import sys
import time
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from experiments.exp4_scalability_and_sensitivity.src.anchor_fidelity_benchmark import run_fidelity_experiment
from experiments.exp4_scalability_and_sensitivity.src.plot_anchor_fidelity import generate_all_plots


def main():
    parser = argparse.ArgumentParser(description="Exp 4.3: Anchor Approximation Fidelity Suite")
    parser.add_argument("--run-full", action="store_true", help="Execute full multi-trial audit")
    parser.add_argument("--trials", type=int, default=1, help="Number of trials per condition (default: 1)")
    parser.add_argument("--reproduce-plots", action="store_true", help="Re-generate figures from existing CSV")

    args = parser.parse_args()
    t_start = time.perf_counter()

    if args.reproduce_plots:
        print("[*] Re-generating Exp 4.3 publication plots from cached CSV results...")
        generate_all_plots()
        print(f"[OK] Figures generated in {time.perf_counter() - t_start:.2f}s.")
    else:
        trials = max(5, args.trials) if args.run_full else args.trials
        print(f"[*] Executing Exp 4.3 anchor fidelity benchmark ({trials} trials)...")
        run_fidelity_experiment(trials_per_n=trials)
        print("[*] Generating publication figures...")
        generate_all_plots()
        print(f"[OK] Exp 4.3 completed in {time.perf_counter() - t_start:.2f}s.")


if __name__ == "__main__":
    main()
