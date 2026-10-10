"""
Master CLI Runner for Experiment 2 Suite: Component-Wise Ablation Study.

Usage:
  python run_exp2.py --reproduce-plots   (re-renders Figures 11, 12, 13 from cached CSV)
  python run_exp2.py --run-full          (executes full ablation sweep across 10 trials)
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

src_dir = Path(__file__).resolve().parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from run_ablation_sweep import run_ablation_experiment
from plot_exp2_figures import plot_exp2_figures
from vssg_interpretability import run_all as run_vssg_interpretability
from plot_vssg_figures import generate_all_plots as plot_vssg_figures


def main():
    parser = argparse.ArgumentParser(description="Experiment 2 Master CLI: Ablation & VSSG Interpretability")
    parser.add_argument("--reproduce-plots", action="store_true", help="Regenerate all figures from cached CSVs")
    parser.add_argument("--run-full", action="store_true", help="Recompute all sweeps and refresh figures")
    parser.add_argument("--ablation-only", action="store_true", help="Run only the component ablation sweep")
    parser.add_argument("--vssg-only", action="store_true", help="Run only the VSSG interpretability audit")
    parser.add_argument("--trials", type=int, default=10, help="Number of trials per condition (default: 10)")
    args = parser.parse_args()

    if args.ablation_only:
        print("\n[*] Running Component-Wise Ablation Sweep...")
        run_ablation_experiment(n_trials=args.trials)
        plot_exp2_figures()
        return

    if args.vssg_only:
        print("\n[*] Running VSSG Interpretability Audit...")
        run_vssg_interpretability(n_trials=args.trials)
        plot_vssg_figures()
        return

    if not (args.reproduce_plots or args.run_full):
        print("Defaulting to: --reproduce-plots")
        plot_exp2_figures()
        plot_vssg_figures()
        return

    if args.run_full:
        print("=================================================================")
        print(" EXECUTING FULL EXPERIMENT 2 ABLATION & INTERPRETABILITY SUITE")
        print("=================================================================")
        print("\n[Phase 1/2] Running Component Ablation Sweep...")
        run_ablation_experiment(n_trials=args.trials)
        print("\n[Phase 2/2] Running VSSG Interpretability Audit...")
        run_vssg_interpretability(n_trials=args.trials)
        print("\n[Figures] Generating Experiment 2 publication figures...")
        plot_exp2_figures()
        plot_vssg_figures()
        print("\nExperiment 2 Suite execution complete!")
    elif args.reproduce_plots:
        plot_exp2_figures()
        plot_vssg_figures()


if __name__ == "__main__":
    main()
