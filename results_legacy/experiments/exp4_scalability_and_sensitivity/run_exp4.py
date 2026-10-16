"""
Master CLI Entrypoint for Experiment 4: Scalability, Sensitivity, and Robustness Suite.

Includes:
- 4.1: Asymptotic Scaling (N in [200, 8000], D in [100, 20000]) and Hyperparameter Sensitivity Maps
- 4.2: K-Misspecification Sensitivity & Robustness (Synthetic, Sonar, SRBCT)
- 4.3: Anchor Approximation Fidelity & O(N) vs O(N^2) Complexity Tradeoff

Usage:
    python run_exp4.py --reproduce-plots
    python run_exp4.py --all
    python run_exp4.py --scaling
    python run_exp4.py --sensitivity
    python run_exp4.py --k-misspec
    python run_exp4.py --anchor-fidelity
"""

import sys
import argparse
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

from experiments.exp4_scalability_and_sensitivity.src.scaling_benchmark import (
    run_sample_scaling_experiment,
    run_dimension_scaling_experiment,
)
from experiments.exp4_scalability_and_sensitivity.src.sensitivity_sweep import run_all_sensitivity_sweeps
from experiments.exp4_scalability_and_sensitivity.src.plot_exp4_figures import generate_all_exp4_figures
from experiments.exp4_scalability_and_sensitivity.src.k_misspecification_sweep import run_k_sweep_experiment
from experiments.exp4_scalability_and_sensitivity.src.plot_k_misspecification import generate_all_plots as generate_k_misspec_plots
from experiments.exp4_scalability_and_sensitivity.src.anchor_fidelity_benchmark import run_fidelity_sweep
from experiments.exp4_scalability_and_sensitivity.src.plot_anchor_fidelity import generate_all_plots as generate_anchor_fidelity_plots


def main():
    parser = argparse.ArgumentParser(description="Experiment 4: Scalability, Sensitivity, and Anchor Fidelity")
    parser.add_argument("--scaling", action="store_true", help="Run sample & dimension scaling benchmarks")
    parser.add_argument("--sensitivity", action="store_true", help="Run hyperparameter sensitivity sweeps")
    parser.add_argument("--k-misspec", action="store_true", help="Run K-misspecification robustness sweeps")
    parser.add_argument("--anchor-fidelity", action="store_true", help="Run anchor approximation fidelity benchmarks")
    parser.add_argument("--all", action="store_true", help="Run all sweeps (scaling, sensitivity, k-misspec, anchor fidelity)")
    parser.add_argument("--reproduce-plots", action="store_true", help="Regenerate all figures from existing CSV data")
    args = parser.parse_args()

    # If no specific sweep flag is selected, check if --all or default
    if not (args.scaling or args.sensitivity or args.k_misspec or args.anchor_fidelity or args.reproduce_plots):
        args.all = True

    if not args.reproduce_plots:
        print("\n" + "=" * 80)
        print("RUNNING EXPERIMENT 4: ASYMPTOTIC SCALABILITY, SENSITIVITY & FIDELITY BENCHMARKS")
        print("=" * 80)

        if args.all or args.scaling:
            print("\n[+] Step 4.1a: Sample Complexity Scaling (N in [200, 8000])...")
            run_sample_scaling_experiment(n_values=[200, 500, 1000, 2000, 5000, 8000], fixed_dim=200, n_trials=3)

            print("\n[+] Step 4.1b: Dimension Scaling (D in [100, 20000])...")
            run_dimension_scaling_experiment(d_values=[100, 500, 2000, 5000, 10000, 20000], fixed_n=500, n_trials=3)

        if args.all or args.sensitivity:
            print("\n[+] Step 4.1c: Hyperparameter Sensitivity Sweeps...")
            run_all_sensitivity_sweeps(n_trials=5)

        if args.all or args.k_misspec:
            print("\n[+] Step 4.2: K-Misspecification Sweep...")
            run_k_sweep_experiment(n_trials=10)

        if args.all or args.anchor_fidelity:
            print("\n[+] Step 4.3: Anchor Approximation Fidelity Benchmark...")
            run_fidelity_sweep(n_samples_list=[200, 500, 1000, 2000, 5000, 10000], n_trials=5)

    print("\n" + "=" * 80)
    print("[*] Generating Publication Figures...")
    print("=" * 80)

    if args.reproduce_plots or args.all or args.scaling or args.sensitivity:
        print("\n[*] Generating Scalability & Sensitivity Figures (Figures 18-21)...")
        generate_all_exp4_figures()

    if args.reproduce_plots or args.all or args.k_misspec:
        print("\n[*] Generating K-Misspecification Figures (Figure 23 ARI & NMI)...")
        generate_k_misspec_plots()

    if args.reproduce_plots or args.all or args.anchor_fidelity:
        print("\n[*] Generating Anchor Approximation Fidelity Figures (Figure 24)...")
        generate_anchor_fidelity_plots()

    print("\n[+] Experiment 4 Completed Successfully!")


if __name__ == "__main__":
    main()
