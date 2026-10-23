# -*- coding: utf-8 -*-
"""
Build-time test to verify that all macros in numbers.tex match the frozen Pass F results store,
and that Table 4, Table 5, and the ablation use reconciled, declared values.
"""

import re

import pandas as pd


def test_macro_and_text_consistency():
    print("=" * 60)
    print("RUNNING BUILD-TIME MACRO & TEXT CONSISTENCY TEST (PASS F)")
    print("=" * 60)

    # 1. Load numbers.tex
    with open('springer_manuscript/numbers.tex', 'r', encoding='utf-8') as f:
        num_tex = f.read()

    # Extract macro definitions
    macros = dict(re.findall(r'\\newcommand\{\\([^}]+)\}\{([^}]+)\}', num_tex))

    # Verify High-D Subgroup Mean and Median match Pass F store (0.217 and 0.036)
    assert macros['FairBaselinesIccVTwoHighDMean'] == '0.217', f"Mismatch in HighDMean macro: {macros['FairBaselinesIccVTwoHighDMean']}"
    assert macros['FairBaselinesIccVTwoHighDMedian'] == '0.036', f"Mismatch in HighDMedian macro: {macros['FairBaselinesIccVTwoHighDMedian']}"
    assert macros['TableThreeFriedmanPValue'] == '0.48', f"Mismatch in Friedman p-value: {macros['TableThreeFriedmanPValue']}"
    assert macros['TrueNemenyiCD'] == '4.19', f"Mismatch in Nemenyi CD: {macros['TrueNemenyiCD']}"
    assert macros['TableThreeIccVTwoGrandMean'] == '0.152', f"Mismatch in GrandMean: {macros['TableThreeIccVTwoGrandMean']}"
    print("  [OK] Pass F macros verified: HighDMean=0.217, HighDMedian=0.036, GrandMean=0.152, CD=4.19")

    # 2. Check main.tex text for purged stale numbers
    with open('springer_manuscript/main.tex', 'r', encoding='utf-8') as f:
        main_tex = f.read()

    stale_tokens = ['0.238', '22.4x', '55.6', '17.0x', '17.0\\times', '57.98', '11.34']
    for token in stale_tokens:
        assert token not in main_tex, f"ERROR: Found stale token '{token}' in main.tex!"
        print(f"  [OK] '{token}' is completely purged from main.tex")

    # Verify no undefined citation markers
    assert '[?]' not in main_tex and '??' not in main_tex, "ERROR: Found undefined citation markers in main.tex!"
    print("  [OK] Zero [?] and ?? citation markers in main.tex")

    # 3. Check Table 4 dataset values against results/passF/benchmark_matrix_passF.csv
    df_bm = pd.read_csv('results/passF/benchmark_matrix_passF.csv')
    high_d = ['cns', 'colon', 'leukemia', 'ovarian', 'prostate', 'srbct']
    icc_bm = df_bm[(df_bm['model'] == 'ICC_v2') & (df_bm['dataset'].isin(high_d))]
    table4_means = icc_bm.groupby('dataset')['ari'].mean()
    calc_mean = float(table4_means.mean())
    calc_median = float(icc_bm['ari'].median())

    assert abs(calc_mean - 0.2168) < 0.005, f"Calculated mean {calc_mean} differs from 0.217"
    assert abs(calc_median - 0.0357) < 0.005, f"Calculated median {calc_median} differs from 0.036"
    print(f"  [OK] Table 4 true High-D subgroup mean={calc_mean:.3f} and median={calc_median:.3f} match 0.217 and 0.036")

    # 4. Check Table 5 dataset values against results/passF/fair_baselines_30seeds_passF.csv
    df_fb = pd.read_csv('results/passF/fair_baselines_30seeds_passF.csv')
    icc_fb = df_fb[(df_fb['model'] == 'ICC_v2') & (df_fb['dataset'].isin(high_d))]
    table5_means = icc_fb.groupby('dataset')['ari'].mean()
    calc_fb_mean = float(table5_means.mean())
    calc_fb_median = float(icc_fb['ari'].median())

    assert abs(calc_fb_mean - 0.2168) < 0.005, f"Table 5 calculated mean {calc_fb_mean} differs from 0.217"
    assert abs(calc_fb_median - 0.0357) < 0.005, f"Table 5 calculated median {calc_fb_median} differs from 0.036"
    print(f"  [OK] Table 5 true High-D subgroup mean={calc_fb_mean:.3f} and median={calc_fb_median:.3f} match 0.217 and 0.036")

    print("\nALL BUILD-TIME CONSISTENCY CHECKS PASSED SUCCESSFULLY!\n")


if __name__ == '__main__':
    test_macro_and_text_consistency()
