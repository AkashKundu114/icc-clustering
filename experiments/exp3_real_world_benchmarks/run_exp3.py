"""
Master CLI Entrypoint for Experiment 3: Real-World High-Dimensional Benchmarks.
Runs all 4 modular sub-experiments:
- Exp 3.1: 8-Dataset Multi-Domain Benchmark Matrix (Sonar to Ovarian D=15,154)
- Exp 3.2: Noise Corruption Stress-Test (0% to 200% injected noise)
- Exp 3.3: Downstream Inductive Generalization on Real Held-Out Test Splits
- Exp 3.4: Rigorous Statistical Significance Testing (Friedman & Wilcoxon Signed-Rank Tests)

Usage:
    python run_exp3.py [--all] [--sub 1|2|3|4] [--reproduce-plots]
"""

import sys
import argparse
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root_dir))

import os
import pandas as pd
from experiments.exp3_real_world_benchmarks.src.run_exp3_1_benchmark_matrix import (
    run_sub_exp3_1,
    plot_fig14_13datasets,
    OUTPUT_CSV_V2,
    ORIGINAL_CSV,
    FIG14_PATH_13DS,
    FIG14B_PATH_13DS_NMI,
)
from experiments.exp3_real_world_benchmarks.src.run_exp3_2_noise_stress_test import run_sub_exp3_2
from experiments.exp3_real_world_benchmarks.src.run_exp3_3_inductive_real_world import run_sub_exp3_3
from experiments.exp3_real_world_benchmarks.src.run_exp3_4_statistical_significance import run_sub_exp3_4
from experiments.exp3_real_world_benchmarks.src.missing_data_experiment import run_missing_data_sweep as run_missing_data_experiment
from experiments.exp3_real_world_benchmarks.src.plot_exp3_figures import generate_all_figures as generate_all_publication_plots
from experiments.exp3_real_world_benchmarks.src.plot_missing_data import generate_all_plots as plot_missing_data_plots


def main():
    parser = argparse.ArgumentParser(description="Experiment 3 Runner: Real-World Benchmarks Suite")
    parser.add_argument("--all", action="store_true", help="Run all sub-experiments (3.1 to 3.5)")
    parser.add_argument("--sub", type=int, choices=[1, 2, 3, 4, 5], help="Run a specific sub-experiment (1, 2, 3, 4, or 5)")
    parser.add_argument("--missing-data", action="store_true", help="Run only Sub-Experiment 3.5 (Missing Data Robustness)")
    parser.add_argument("--reproduce-plots", action="store_true", help="Regenerate all publication plots from cached CSVs")
    parser.add_argument("--trials", type=int, default=10, help="Number of Monte Carlo trials")
    args = parser.parse_args()

    if args.reproduce_plots:
        print("\n[*] Re-generating all Experiment 3 publication figures...")
        generate_all_publication_plots()
        plot_missing_data_plots()

        csv_to_use = OUTPUT_CSV_V2 if os.path.exists(OUTPUT_CSV_V2) else ORIGINAL_CSV
        if os.path.exists(csv_to_use):
            print(f"[*] Re-generating 13-dataset figures from: {csv_to_use}")
            df = pd.read_csv(csv_to_use)
            plot_fig14_13datasets(df, metric="ari", save_path=FIG14_PATH_13DS)
            plot_fig14_13datasets(df, metric="nmi", save_path=FIG14B_PATH_13DS_NMI)

        print("[+] All figures re-generated successfully!")
        return

    if args.missing_data or args.sub == 5:
        print("\n>>> Executing Sub-Experiment 3.5: Missing Data Robustness & Imputation Resilience...")
        run_missing_data_experiment(n_trials=min(5, args.trials))
        plot_missing_data_plots()
        return

    print("\n" + "=" * 80)
    print("EXPERIMENT 3: REAL-WORLD HIGH-DIMENSIONAL BENCHMARK SUITE (EXP 3.1 - 3.5)")
    print("=" * 80)

    if args.sub == 1 or args.all or (args.sub is None and not args.missing_data):
        print("\n>>> [1/5] Executing Sub-Experiment 3.1: 8-Dataset Benchmark Matrix...")
        run_sub_exp3_1(n_trials=args.trials)

    if args.sub == 2 or args.all or (args.sub is None and not args.missing_data):
        print("\n>>> [2/5] Executing Sub-Experiment 3.2: Noise Corruption Stress-Test...")
        run_sub_exp3_2(n_trials=min(5, args.trials))

    if args.sub == 3 or args.all or (args.sub is None and not args.missing_data):
        print("\n>>> [3/5] Executing Sub-Experiment 3.3: Downstream Inductive Generalization...")
        run_sub_exp3_3(n_trials=args.trials)

    if args.sub == 4 or args.all or (args.sub is None and not args.missing_data):
        print("\n>>> [4/5] Executing Sub-Experiment 3.4: Statistical Significance Audit...")
        run_sub_exp3_4()

    if args.sub == 5 or args.all:
        print("\n>>> [5/5] Executing Sub-Experiment 3.5: Missing Data Robustness...")
        run_missing_data_experiment(n_trials=min(5, args.trials))
        plot_missing_data_plots()

    print("\n" + "=" * 80)
    print("[+] Experiment 3 Suite Completed Successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()
