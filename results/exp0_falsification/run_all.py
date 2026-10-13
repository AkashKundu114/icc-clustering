"""
Master pipeline execution script for Experiment 0.
Runs the entire experiment suite or regenerates figures from pre-computed data.

Usage:
  python run_all.py --reproduce-plots   (re-renders all 8 figures from cached data)
  python run_all.py --run-fast          (runs quick validation sweeps: ~2 minutes)
  python run_all.py --run-full          (recomputes all sweeps and saves fresh CSVs + figures)
"""

import argparse
import sys
from pathlib import Path

# Add src to python path
src_dir = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(src_dir))

from plot_all_figures import generate_all_figures
from exp0_run import run_baseline_sweep
from exp0_noisetypes import run_noisetypes_experiment
from exp0_scaled_run import run_scaled_sweep
from exp0_finegrid import run_finegrid_sweep


def main():
    parser = argparse.ArgumentParser(description="Experiment 0 Master Execution Pipeline")
    parser.add_argument("--reproduce-plots", action="store_true", help="Regenerate all figures from cached CSVs")
    parser.add_argument("--run-fast", action="store_true", help="Run fast verification sweeps")
    parser.add_argument("--run-full", action="store_true", help="Recompute all sweeps and update CSVs and figures")
    args = parser.parse_args()

    if not (args.reproduce_plots or args.run_fast or args.run_full):
        # Default behavior: generate plots and verify
        print("No specific flag provided. Defaulting to: --reproduce-plots")
        generate_all_figures()
        return

    if args.run_full:
        print("=================================================================")
        print(" EXECUTING FULL EXPERIMENT 0 PIPELINE")
        print("=================================================================")
        print("\n[Phase 1/4] Running Baseline Noise Sweep (N=300, K=3)...")
        run_baseline_sweep()
        print("\n[Phase 2/4] Running 5-Noise-Regime Robustness Sweep...")
        run_noisetypes_experiment()
        print("\n[Phase 3/4] Running Genomics-Scale Imbalanced Sweep (ALLAML scale)...")
        run_scaled_sweep()
        print("\n[Phase 4/4] Running Fine-Grid FCM Phase Transition Sweep...")
        run_finegrid_sweep()
        print("\n[Figures] Generating all 8 publication figures...")
        generate_all_figures()
        print("\nFull pipeline execution complete!")

    elif args.reproduce_plots:
        generate_all_figures()


if __name__ == "__main__":
    main()
