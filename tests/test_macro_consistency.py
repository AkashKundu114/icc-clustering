# -*- coding: utf-8 -*-
"""
Build-time test to verify macro and manuscript numerical consistency.

Verifies:
1. All macros in numbers.tex match the frozen Pass F results store.
2. main.tex text has purged all stale numbers and undefined citation markers.
3. Table 4 dataset values match results/passF/benchmark_matrix_passF.csv.
4. Table 5 dataset values match results/passF/fair_baselines_30seeds_passF.csv.
5. Fig 8 scaling curves match experiments/exp4_scalability_and_sensitivity/data/exp4_sample_scaling_summary.csv.
"""

import re
from pathlib import Path

import pandas as pd


def test_macro_and_text_consistency():
    print("=" * 60)
    print("RUNNING BUILD-TIME MACRO & TEXT CONSISTENCY TEST (PASS F)")
    print("=" * 60)

    # 1. Load numbers.tex
    num_path = Path("paper/numbers.tex")
    if not num_path.exists():
        num_path = Path("springer_manuscript/numbers.tex")
    assert num_path.exists(), f"numbers.tex not found at {num_path}"
    with open(num_path, "r", encoding="utf-8") as f:
        num_tex = f.read()

    # Extract macro definitions
    macros = dict(re.findall(r"\\newcommand\{\\([^}]+)\}\{([^}]+)\}", num_tex))

    # Verify High-D Subgroup Mean and Median match Pass F store (0.217 and 0.061)
    assert macros["FairBaselinesIccVTwoHighDMean"] == "0.217", f"Mismatch in HighDMean macro: {macros['FairBaselinesIccVTwoHighDMean']}"
    assert macros["FairBaselinesIccVTwoHighDMedian"] == "0.061", f"Mismatch in HighDMedian macro: {macros['FairBaselinesIccVTwoHighDMedian']}"
    assert macros["TableThreeFriedmanPValue"] == "0.48", f"Mismatch in Friedman p-value: {macros['TableThreeFriedmanPValue']}"
    assert macros["TrueNemenyiCD"] == "4.19", f"Mismatch in Nemenyi CD: {macros['TrueNemenyiCD']}"
    assert macros["TableThreeIccVTwoGrandMean"] == "0.152", f"Mismatch in GrandMean: {macros['TableThreeIccVTwoGrandMean']}"
    assert macros["OmnibusMedianARI"] == "0.055", f"Mismatch in OmnibusMedian: {macros['OmnibusMedianARI']}"
    assert macros["OmnibusMeanExcludingLeukemiaSrbct"] == "0.076", f"Mismatch in MeanExcl: {macros['OmnibusMeanExcludingLeukemiaSrbct']}"
    print("  [OK] Pass F macros verified: HighDMean=0.217, HighDMedian=0.061, GrandMean=0.152, OmnibusMedian=0.055, MeanExcl=0.076, CD=4.19")

    # 2. Check main.tex text for purged stale numbers (when present in local workspace)
    main_path = Path("paper/main.tex")
    if not main_path.exists():
        main_path = Path("springer_manuscript/main.tex")
    if main_path.exists():
        with open(main_path, "r", encoding="utf-8") as f:
            main_tex = f.read()

        stale_tokens = ["0.238", "22.4x", "55.6", "17.0x", "17.0\\times", "57.98", "11.34"]
        for token in stale_tokens:
            assert token not in main_tex, f"ERROR: Found stale token '{token}' in main.tex!"
            print(f"  [OK] '{token}' is completely purged from main.tex")

        # Verify no undefined citation markers
        assert "[?]" not in main_tex and "??" not in main_tex, "ERROR: Found undefined citation markers in main.tex!"
        print("  [OK] Zero [?] and ?? citation markers in main.tex")
    else:
        print(f"  [INFO] main.tex not found at {main_path} (embargoed manuscript in CI); skipping text scan.")

    # 3. Check Table 4 dataset values against results/passF/benchmark_matrix_passF.csv
    df_bm = pd.read_csv("results/passF/benchmark_matrix_passF.csv")
    high_d = ["cns", "colon", "leukemia", "ovarian", "prostate", "srbct"]
    icc_bm = df_bm[(df_bm["model"] == "ICC_v2") & (df_bm["dataset"].isin(high_d))]
    table4_means = icc_bm.groupby("dataset")["ari"].mean()
    calc_mean = float(table4_means.mean())
    calc_dataset_median = float(table4_means.median())
    calc_run_median = float(icc_bm["ari"].median())

    assert abs(calc_mean - 0.2168) < 0.005, f"Calculated mean {calc_mean} differs from 0.217"
    assert abs(calc_dataset_median - 0.0610) < 0.005, f"Calculated dataset median {calc_dataset_median} differs from 0.061"
    assert abs(calc_run_median - 0.0357) < 0.005, f"Calculated run median {calc_run_median} differs from 0.036"
    print(f"  [OK] Table 4 true High-D subgroup mean={calc_mean:.3f}, dataset median={calc_dataset_median:.3f}, run median={calc_run_median:.3f}")

    # Check 13-dataset table derivations
    all_icc = df_bm[df_bm["model"] == "ICC_v2"].groupby("dataset")["ari"].mean()
    recomputed_13_median = float(all_icc.median())
    recomputed_11_mean = float(all_icc.drop(["leukemia", "srbct"]).mean())
    assert abs(recomputed_13_median - 0.0555) < 0.005, f"13-dataset median {recomputed_13_median} differs from 0.055"
    assert abs(recomputed_11_mean - 0.0759) < 0.005, f"11-dataset mean {recomputed_11_mean} differs from 0.076"
    print(f"  [OK] Table derivations verified: 13-dataset median={recomputed_13_median:.3f}, 11-dataset mean={recomputed_11_mean:.3f}")

    # 4. Check Table 5 dataset values against results/passF/fair_baselines_30seeds_passF.csv
    df_fb = pd.read_csv("results/passF/fair_baselines_30seeds_passF.csv")
    icc_fb = df_fb[(df_fb["model"] == "ICC_v2") & (df_fb["dataset"].isin(high_d))]
    table5_means = icc_fb.groupby("dataset")["ari"].mean()
    calc_fb_mean = float(table5_means.mean())
    calc_fb_dataset_median = float(table5_means.median())
    calc_fb_run_median = float(icc_fb["ari"].median())

    assert abs(calc_fb_mean - 0.2168) < 0.005, f"Table 5 calculated mean {calc_fb_mean} differs from 0.217"
    assert abs(calc_fb_dataset_median - 0.0610) < 0.005, f"Table 5 calculated dataset median {calc_fb_dataset_median} differs from 0.061"
    assert abs(calc_fb_run_median - 0.0357) < 0.005, f"Table 5 calculated run median {calc_fb_run_median} differs from 0.036"
    print(f"  [OK] Table 5 true High-D subgroup mean={calc_fb_mean:.3f}, dataset median={calc_fb_dataset_median:.3f}, run median={calc_fb_run_median:.3f}")

    # 5. Check Fig 8 scaling data against sample scaling summary
    p_sample = "experiments/exp4_scalability_and_sensitivity/data/exp4_sample_scaling_summary.csv"
    df_sample = pd.read_csv(p_sample)
    icc_10k = df_sample[(df_sample["model"] == "ICC_v2") & (df_sample["N"] == 10000)].iloc[0]
    exact_10k = df_sample[(df_sample["model"] == "Standard_Consensus") & (df_sample["N"] == 10000)].iloc[0]

    icc_time = float(icc_10k["runtime_mean"])
    exact_time = float(exact_10k["runtime_mean"])
    speedup = exact_time / icc_time
    assert abs(icc_time - 10.35) < 0.05, f"ICC-v2 runtime mismatch: {icc_time} vs 10.35"
    assert abs(exact_time - 29.96) < 0.05, f"Exact runtime mismatch: {exact_time} vs 29.96"
    assert abs(speedup - 2.896) < 0.1, f"Speedup mismatch: {speedup} vs 2.9x"

    icc_mem = float(icc_10k["peak_trace_mean"])
    exact_mem = float(exact_10k["peak_trace_mean"])
    mem_red = (1 - icc_mem / exact_mem) * 100
    assert abs(icc_mem - 68.83) < 0.1, f"ICC-v2 dynamic memory mismatch: {icc_mem} vs 68.8"
    assert abs(exact_mem - 2670.6) < 0.5, f"Exact dynamic memory mismatch: {exact_mem} vs 2670.6"
    assert abs(mem_red - 97.42) < 0.1, f"Memory reduction mismatch: {mem_red}% vs 97.4%"

    icc_graph = float(icc_10k["graph_mem_mb"])
    exact_graph = float(exact_10k["graph_mem_mb"])
    graph_red = (1 - icc_graph / exact_graph) * 100
    assert abs(icc_graph - 3.06) < 0.05, f"ICC-v2 graph memory mismatch: {icc_graph} vs 3.06"
    assert abs(exact_graph - 762.79) < 0.1, f"Exact graph memory mismatch: {exact_graph} vs 762.8"
    assert abs(graph_red - 99.6) < 0.1, f"Graph reduction mismatch: {graph_red}% vs 99.6%"
    print(f"  [OK] Fig 8 scaling verified: time {icc_time:.2f}s vs {exact_time:.2f}s ({speedup:.1f}x), mem {icc_mem:.1f}MB vs {exact_mem:.1f}MB ({mem_red:.1f}%), graph {icc_graph:.2f}MB vs {exact_graph:.1f}MB ({graph_red:.1f}%)")

    print("\nALL BUILD-TIME CONSISTENCY CHECKS PASSED SUCCESSFULLY!\n")


if __name__ == "__main__":
    test_macro_and_text_consistency()
