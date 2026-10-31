import pandas as pd
import numpy as np

for f in ['experiments/exp3_real_world_benchmarks/data/exp3_1_benchmark_matrix_v2.csv', 'experiments/exp3_real_world_benchmarks/data/exp3_1_benchmark_matrix.csv', 'results/passF/benchmark_matrix_passF.csv']:
    df = pd.read_csv(f)
    print(f"\n--- File: {f} ---")
    print("Models:", df['model'].unique())
    print("Datasets count:", df['dataset'].nunique())
    # Mean ARI Pivot Table (Datasets x Models)
    pivot = df.groupby(["dataset", "model"])["ari"].mean().unstack()
    # Rank descending (highest ARI = rank 1)
    ranks = pivot.rank(axis=1, ascending=False, method="average")
    mean_ranks = ranks.mean().sort_values()
    print("Mean ranks:")
    for m, r in mean_ranks.items():
        print(f"  {m:25s}: {r:.2f}")
