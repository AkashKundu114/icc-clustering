"""
Master CLI Runner for Experiment 1 Suite: Inductive Generalization.

Usage:
  python run_exp1.py --reproduce-plots   (re-renders fig9 and fig10 from cached data)
  python run_exp1.py --run-full          (recomputes all sweeps and updates CSVs and figures)
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

from exp1_inductive_generalization import run_generalization_experiment
from exp1_pseudolabel_generalization import run_pseudolabel_generalization
from exp1_multiclassifier_generalization import run_multiclassifier_generalization
from plot_exp1_figures import plot_exp1_figures


def main():
    parser = argparse.ArgumentParser(description="Experiment 1 Master CLI")
    parser.add_argument("--reproduce-plots", action="store_true", help="Regenerate all figures from cached CSVs")
    parser.add_argument("--run-full", action="store_true", help="Recompute all generalization sweeps and refresh figures")
    parser.add_argument("--multiclassifier-only", action="store_true", help="Run only the multi-classifier pseudo-label sweep")
    parser.add_argument("--trials", type=int, default=5, help="Number of trials per condition (default: 5)")
    args = parser.parse_args()

    if args.multiclassifier_only:
        print("\n[*] Running Multi-Classifier Pseudo-Label Generalization Test across [SVM, RF, MLP, KNN]...")
        run_pseudolabel_generalization(
            noise_dims=[0, 50, 200, 500, 1000, 3000, 5000],
            n_trials=args.trials,
        )
        print("\n[Figures] Generating Experiment 1 figures...")
        plot_exp1_figures()
        print("\nMulti-classifier sweep and figure generation complete!")
        return

    if not (args.reproduce_plots or args.run_full):
        print("No specific flag provided. Defaulting to: --reproduce-plots")
        plot_exp1_figures()
        return

    if args.run_full:
        print("=================================================================")
        print(" EXECUTING FULL EXPERIMENT 1 GENERALIZATION SUITE")
        print("=================================================================")
        print("\n[Phase 1/2] Running Ground-Truth Generalization Test...")
        run_generalization_experiment()
        print("\n[Phase 2/2] Running Multi-Classifier Pseudo-Label Generalization Test...")
        run_pseudolabel_generalization(
            noise_dims=[0, 50, 200, 500, 1000, 3000, 5000],
            n_trials=args.trials,
        )
        print("\n[Figures] Generating Experiment 1 figures...")
        plot_exp1_figures()
        print("\nExperiment 1 Suite execution complete!")
    elif args.reproduce_plots:
        plot_exp1_figures()


if __name__ == "__main__":
    main()
