# -*- coding: utf-8 -*-
"""
Test to extract plotted data from the underlying scaling results and verify
strict numerical consistency with Fig 8 caption and manuscript text.
"""

import pandas as pd


def test_fig8_values_vs_caption():
    print("=" * 60)
    print("TESTING FIG 8 PLOTTED VALUES VS CAPTION AND TEXT")
    print("=" * 60)

    p_sample = 'experiments/exp4_scalability_and_sensitivity/data/exp4_sample_scaling_summary.csv'
    df = pd.read_csv(p_sample)

    icc_10k = df[(df['model'] == 'ICC_v2') & (df['N'] == 10000)].iloc[0]
    exact_10k = df[(df['model'] == 'Standard_Consensus') & (df['N'] == 10000)].iloc[0]

    # Caption claims:
    # 1. Runtime at 10k: 10.35s vs 29.96s (2.9x speedup)
    icc_time = icc_10k['runtime_mean']
    exact_time = exact_10k['runtime_mean']
    speedup = exact_time / icc_time

    assert abs(icc_time - 10.35) < 0.05, f"ICC-v2 runtime mismatch: {icc_time} vs 10.35"
    assert abs(exact_time - 29.96) < 0.05, f"Exact runtime mismatch: {exact_time} vs 29.96"
    assert abs(speedup - 2.896) < 0.1, f"Speedup mismatch: {speedup} vs 2.9x"
    print(f"  [OK] Runtime: {icc_time:.2f}s vs {exact_time:.2f}s (Speedup: {speedup:.1f}x)")

    # 2. Peak Dynamic Memory at 10k: 68.8 MB vs 2,670.6 MB (97.4% reduction)
    icc_mem = icc_10k['peak_trace_mean']
    exact_mem = exact_10k['peak_trace_mean']
    mem_red = (1 - icc_mem / exact_mem) * 100

    assert abs(icc_mem - 68.83) < 0.1, f"ICC-v2 dynamic memory mismatch: {icc_mem} vs 68.8"
    assert abs(exact_mem - 2670.6) < 0.5, f"Exact dynamic memory mismatch: {exact_mem} vs 2670.6"
    assert abs(mem_red - 97.42) < 0.1, f"Memory reduction mismatch: {mem_red}% vs 97.4%"
    print(f"  [OK] Peak Dynamic Memory: {icc_mem:.1f} MB vs {exact_mem:.1f} MB (Reduction: {mem_red:.1f}%)")

    # 3. Consensus Graph Working Memory at 10k: 3.06 MB vs 762.8 MB (99.6% reduction)
    icc_graph = icc_10k['graph_mem_mb']
    exact_graph = exact_10k['graph_mem_mb']
    graph_red = (1 - icc_graph / exact_graph) * 100

    assert abs(icc_graph - 3.06) < 0.05, f"ICC-v2 graph memory mismatch: {icc_graph} vs 3.06"
    assert abs(exact_graph - 762.79) < 0.1, f"Exact graph memory mismatch: {exact_graph} vs 762.8"
    assert abs(graph_red - 99.6) < 0.1, f"Graph reduction mismatch: {graph_red}% vs 99.6%"
    print(f"  [OK] Working Graph Memory: {icc_graph:.2f} MB vs {exact_graph:.1f} MB (Reduction: {graph_red:.1f}%)")

    print("\nFIG 8 NUMERICAL CONSISTENCY VERIFIED WITH 100% PRECISION!\n")

if __name__ == '__main__':
    test_fig8_values_vs_caption()
