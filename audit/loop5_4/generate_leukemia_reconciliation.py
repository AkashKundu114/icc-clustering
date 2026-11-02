#!/usr/bin/env python3
"""
generate_leukemia_reconciliation.py
-----------------------------------
Generates audit/loop5_4/leukemia_ci_final_reconciliation.csv
Reconciles all conflicting Leukemia estimates across audit iterations and manuscript tables.
"""

import csv

records = [
    {
        'Interval_or_Estimate_ID': 'LEUK-01-PERCENTILE-BOOTSTRAP-10SEEDS',
        'Reported_String': '[0.4296, 0.8590]',
        'Original_Source_File': 'results/evidence_recovery/recovered/results.json (exp3_1)',
        'Underlying_Observation_Vector': '[-0.029015, 0.837557, 0.944156, 0.837557, 0.837557, 0.837557, 0.019232, 0.837557, 0.890017, 0.786751]',
        'Sample_Size_N': '10',
        'Seed_Identities_or_Draws': 'Seeds 42, 101, 202, 303, 404, 505, 606, 707, 808, 909',
        'Sampling_Type': 'Algorithmic random initialization seeds on fixed cohort (N=72, D=7129)',
        'Estimator_Formula_or_Procedure': 'Non-parametric percentile bootstrap (B=10,000, seed=42); quantiles [0.025, 0.975]',
        'Recomputed_Point_Estimate': 'Mean = 0.6799, Median = 0.8376',
        'Recomputed_Interval': '[0.4291, 0.8594]',
        'Exact_Estimand_Represented': 'Mean algorithmic initialization performance of GAC on this specific Leukemia sample',
        'Validity_Adjudication': 'STATISTICALLY_DEFENSIBLE_ALGORITHMIC_INTERVAL',
        'Scientific_Recommendation': 'Report in manuscript with explicit qualification that it reflects algorithmic stochasticity over random seeds, NOT population-level biological uncertainty.'
    },
    {
        'Interval_or_Estimate_ID': 'LEUK-02-BCA-BOOTSTRAP-10SEEDS',
        'Reported_String': '[0.4086, 0.8535]',
        'Original_Source_File': 'audit/loop5_3/check_task1.py (computed via scipy.stats.bootstrap)',
        'Underlying_Observation_Vector': '[-0.029015, 0.837557, 0.944156, 0.837557, 0.837557, 0.837557, 0.019232, 0.837557, 0.890017, 0.786751]',
        'Sample_Size_N': '10',
        'Seed_Identities_or_Draws': 'Seeds 42, 101, 202, 303, 404, 505, 606, 707, 808, 909',
        'Sampling_Type': 'Algorithmic random initialization seeds on fixed cohort (N=72, D=7129)',
        'Estimator_Formula_or_Procedure': 'Bias-Corrected and Accelerated (BCa) bootstrap (B=10,000, seed=42)',
        'Recomputed_Point_Estimate': 'Mean = 0.6799, Median = 0.8376',
        'Recomputed_Interval': '[0.4086, 0.8535]',
        'Exact_Estimand_Represented': 'Mean algorithmic initialization performance adjusted for skewness and acceleration',
        'Validity_Adjudication': 'STATISTICALLY_DEFENSIBLE_ALGORITHMIC_INTERVAL',
        'Scientific_Recommendation': 'Valid alternative to percentile bootstrap; accurately adjusts for negative skewness caused by 20% initialization failure rate.'
    },
    {
        'Interval_or_Estimate_ID': 'LEUK-03-SPURIOUS-LEDGER-ENTRY',
        'Reported_String': '[0.3800, 0.7960]',
        'Original_Source_File': 'audit/loop5_2/reproduction_execution_ledger.csv (line 3, REP-02)',
        'Underlying_Observation_Vector': 'Single run ARI values in exp4_anchor_budget.csv / exp3_inductive_geometry.csv',
        'Sample_Size_N': 'N/A (Two isolated point evaluations)',
        'Seed_Identities_or_Draws': 'Unrelated anchor budget parameter combinations',
        'Sampling_Type': 'Erroneous transcription / copy-paste accident',
        'Estimator_Formula_or_Procedure': 'None (Not a confidence interval)',
        'Recomputed_Point_Estimate': 'N/A',
        'Recomputed_Interval': 'N/A',
        'Exact_Estimand_Represented': 'None (Spurious audit artifact)',
        'Validity_Adjudication': 'DISPROVEN_SPURIOUS_COPY_PASTE',
        'Scientific_Recommendation': 'Permanently expunge from all audit tables and manuscripts.'
    },
    {
        'Interval_or_Estimate_ID': 'LEUK-04-UNVERIFIABLE-LOOP51-INTERVAL',
        'Reported_String': '[0.0076, 0.8879]',
        'Original_Source_File': 'audit/loop5_1/independent_reproduction_report.md (lines 37, 242)',
        'Underlying_Observation_Vector': 'Untraceable (Generated without script or seed preservation in Loop 5.1)',
        'Sample_Size_N': 'Unknown (presumed 5 or 10)',
        'Seed_Identities_or_Draws': 'Undocumented',
        'Sampling_Type': 'Undocumented bootstrap resample',
        'Estimator_Formula_or_Procedure': 'Undocumented percentile bootstrap',
        'Recomputed_Point_Estimate': 'Unknown',
        'Recomputed_Interval': 'Cannot be reproduced',
        'Exact_Estimand_Represented': 'Unverifiable residual calculation',
        'Validity_Adjudication': 'UNVERIFIABLE_RESIDUAL_ARTIFACT',
        'Scientific_Recommendation': 'Expunge from all records; replace with canonical 10-seed verified bootstrap.'
    },
    {
        'Interval_or_Estimate_ID': 'LEUK-05-INVALID-STUDENT-T-INTERVAL',
        'Reported_String': '[-0.1048, 1.0397]',
        'Original_Source_File': 'results/loop2/raw/exp5_baseline_comparison.json & .csv',
        'Underlying_Observation_Vector': '[0.837557, 0.786751, 0.786751, -0.029015, -0.044618]',
        'Sample_Size_N': '5',
        'Seed_Identities_or_Draws': 'Seeds 42, 100, 2024, 777, 999',
        'Sampling_Type': '5 algorithmic seeds in Loop 2 exp5 protocol',
        'Estimator_Formula_or_Procedure': 'Parametric Student-t: mean +- t(0.975, df=4) * (std / sqrt(5))',
        'Recomputed_Point_Estimate': 'Mean = 0.4675, Std = 0.4609, SE = 0.2061',
        'Recomputed_Interval': '[-0.1048, 1.0397]',
        'Exact_Estimand_Represented': 'Parametric normal mean under assumed Gaussianity across 5 seeds',
        'Validity_Adjudication': 'UNSUITABLE_PARAMETRIC_MODEL',
        'Scientific_Recommendation': 'Do not use. While negative ARI is mathematically possible, upper limit > 1.0 is impossible for ARI. Moreover, Gaussian assumption fails catastrophically on bimodal 5-seed data.'
    },
    {
        'Interval_or_Estimate_ID': 'LEUK-06-TABLE-2-SUBSAMPLE-ACCURACY',
        'Reported_String': '0.412',
        'Original_Source_File': 'paper/tables/table02_real_data_stability.tex (line 22)',
        'Underlying_Observation_Vector': '30 stratified 80% subsample ARI values against reference pathology labels',
        'Sample_Size_N': '30',
        'Seed_Identities_or_Draws': '30 stratified 80% random patient subsamples (N_sub approx 58)',
        'Sampling_Type': 'Perturbation subsampling (data-level perturbation)',
        'Estimator_Formula_or_Procedure': 'Sample mean ARI across 30 subsampled evaluation folds',
        'Recomputed_Point_Estimate': 'Mean = 0.412',
        'Recomputed_Interval': 'N/A (Point mean)',
        'Exact_Estimand_Represented': 'Expected clustering accuracy under 20% patient subsample dropout',
        'Validity_Adjudication': 'VALID_SUBSAMPLING_ACCURACY_ESTIMAND',
        'Scientific_Recommendation': 'Retain in Table 2 as empirical subsample accuracy. Explicitly distinguish from full-cohort clustering performance.'
    },
    {
        'Interval_or_Estimate_ID': 'LEUK-07-TABLE-6-FULL-COHORT-ARI',
        'Reported_String': '+0.600 +- 0.367',
        'Original_Source_File': 'paper/tables/table06_omnibus_benchmark_ari.tex (line 13)',
        'Underlying_Observation_Vector': '30 canonical full-dataset random seed runs',
        'Sample_Size_N': '30',
        'Seed_Identities_or_Draws': 'Seeds 1 to 30 on full Leukemia cohort (N=72)',
        'Sampling_Type': 'Full-cohort algorithmic randomization across 30 seeds',
        'Estimator_Formula_or_Procedure': 'Sample mean +- sample standard deviation across 30 seeds',
        'Recomputed_Point_Estimate': 'Mean = 0.600, Std = 0.367',
        'Recomputed_Interval': '[0.4687, 0.7313] (approx 95% CI via normal approximation)',
        'Exact_Estimand_Represented': 'Sample mean and sample variance across 30 initializations on full cohort',
        'Validity_Adjudication': 'DESCRIPTIVE_SAMPLE_MOMENTS',
        'Scientific_Recommendation': 'Retain as descriptive sample mean +- SD. Clarify that large SD (0.367) reflects bimodal initialization sensitivity.'
    }
]

out_file = 'audit/loop5_4/leukemia_ci_final_reconciliation.csv'
fieldnames = [
    'Interval_or_Estimate_ID', 'Reported_String', 'Original_Source_File',
    'Underlying_Observation_Vector', 'Sample_Size_N', 'Seed_Identities_or_Draws',
    'Sampling_Type', 'Estimator_Formula_or_Procedure', 'Recomputed_Point_Estimate',
    'Recomputed_Interval', 'Exact_Estimand_Represented', 'Validity_Adjudication',
    'Scientific_Recommendation'
]

with open(out_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in records:
        writer.writerow(r)

print(f"Successfully wrote {len(records)} reconciliation records to {out_file}")
