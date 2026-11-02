#!/usr/bin/env python3
"""
generate_adjudication_ledgers.py
--------------------------------
Generates:
1. audit/loop5_4/icc_claim_and_novelty_adjudication.csv (Task 7)
2. audit/loop5_4/manuscript_claim_adjudication.csv (Task 8)
"""

import csv

# -------------------------------------------------------------------------
# Task 7: ICC Claims and Novelty Adjudication
# -------------------------------------------------------------------------
icc_records = [
    {
        'Component_or_Claim_ID': 'ICC-01-BIPARTITE-ANCHOR-GRAPH',
        'Component_Name': 'Bipartite Anchor Graph Consensus (BAG / GAC)',
        'Conceptual_Idea': 'Construct an N x L bipartite affinity graph between N samples and L << N representative anchors, avoiding the dense N x N co-association matrix.',
        'Current_Empirical_Evidence': 'Reduces graph storage from 762.9 MB to 3.05 MB at N=10,000, and from 19.1 GB to 15.3 MB at N=50,000 (exp6_scalability.csv). Traced RAM is 68.8 MB vs 2.61 GB.',
        'Unresolved_Mathematical_Issue': 'Theoretical spectral approximation bound ||S - B W_A^-1 B^T||_2 is sensitive to anchor distribution geometry and cluster boundary coverage.',
        'Unresolved_Empirical_Issue': 'Performance degrades when anchor budget L is smaller than effective intrinsic manifold dimension; anchor initialization requires careful k-means seeding.',
        'Appropriate_Future_Research_Question': 'Can adaptive anchor selection (e.g. leverage score sampling) provide provable spectral error guarantees under severe class imbalance?',
        'Claims_That_Should_Not_Be_Made': 'Do not claim universal equivalence to dense consensus; do not claim it solves cluster discovery in non-Euclidean manifolds.',
        'Classification': 'SUPPORTED WITH QUALIFICATION',
        'Manuscript_Action': 'RETAIN WITH QUALIFICATION. Present as an exploratory engineering architecture for scaling consensus clustering.'
    },
    {
        'Component_or_Claim_ID': 'ICC-02-BGSS-FEATURE-SCREENING',
        'Component_Name': 'Between-Group Sum of Squares (BGSS) Feature Gating',
        'Conceptual_Idea': 'Filter uninformative genes in high dimensions by ranking variance ratios across ensemble partition clusters.',
        'Current_Empirical_Evidence': 'Factorial ablation across 6 cohorts shows GAC advantage (+0.132 to +0.194) is non-significant after Holm correction (p_adj >= 0.938), driven by Leukemia and SRBCT.',
        'Unresolved_Mathematical_Issue': 'Ranking features post-clustering induces selection bias (circularity / survivorship bias); prone to reinforcing spurious cluster separations.',
        'Unresolved_Empirical_Issue': 'Fails to improve ARI on 4 out of 6 cohorts (CNS, Colon, Prostate, Ovarian); does not prevent stability-accuracy discordance.',
        'Appropriate_Future_Research_Question': 'Can out-of-fold feature screening or cross-validated stability filtering prevent circular variance inflation in high dimensions?',
        'Claims_That_Should_Not_Be_Made': 'Do not claim BGSS universally isolates true biological markers; do not claim statistically significant necessity across cohorts.',
        'Classification': 'OVERSTATED',
        'Manuscript_Action': 'MOVE TO FUTURE WORK. Reframe as an exploratory heuristic requiring independent validation against circularity bias.'
    },
    {
        'Component_or_Claim_ID': 'ICC-03-AUTOK-PAC-BOUNDS',
        'Component_Name': 'AutoK Automated Cluster Count Selection via PAC Bounds',
        'Conceptual_Idea': 'Select optimal cluster count K by minimizing a PAC-Bayesian bound on consensus stability discrepancy.',
        'Current_Empirical_Evidence': 'In 510/510 adversarial trials (100.0%), AutoK collapsed to K_min=2. In 486 trials (95.29%), all PAC bound values were identically zero (adversarial_autok_raw_results.csv).',
        'Unresolved_Mathematical_Issue': 'PAC penalty term dominates empirical stability term when sample size N is small (N < 200), driving the objective to the trivial lower boundary K_min.',
        'Unresolved_Empirical_Issue': 'Completely unusable for automated biological cluster discovery in its current formulation; acts as a constant tie-breaker.',
        'Appropriate_Future_Research_Question': 'Can finite-sample calibrated concentration bounds or empirical Bernstein bounds prevent boundary collapse for small N?',
        'Claims_That_Should_Not_Be_Made': 'MUST NOT claim AutoK provides a mathematically rigorous or reliable automated solver for K.',
        'Classification': 'MUST BE REMOVED',
        'Manuscript_Action': 'REMOVE claims of successful K determination; disclose boundary collapse in limitations and propose finite-sample redesign in future work.'
    },
    {
        'Component_or_Claim_ID': 'ICC-04-INDUCTIVE-ANCHOR-PROJECTION',
        'Component_Name': 'Inductive Out-of-Sample Cluster Assignment',
        'Conceptual_Idea': 'Assign new out-of-sample test samples to clusters by projecting onto learned anchor embedding space without re-running consensus.',
        'Current_Empirical_Evidence': '140 train/test split runs demonstrate test ARI tracks train ARI within 5-8% on stationary distributions (exp1_generalization in results.json).',
        'Unresolved_Mathematical_Issue': 'Out-of-sample projection error is uncalibrated under covariate shift or when unseen points fall outside the convex hull of anchors.',
        'Unresolved_Empirical_Issue': 'Has not been evaluated on external multi-center clinical cohorts or across batch-effect shifts.',
        'Appropriate_Future_Research_Question': 'Can conformal prediction regions provide guaranteed coverage sets for out-of-sample inductive cluster assignments?',
        'Claims_That_Should_Not_Be_Made': 'Do not claim clinical out-of-sample diagnostic utility or generalizability across independent patient cohorts.',
        'Classification': 'EXPLORATORY',
        'Manuscript_Action': 'RETAIN WITH QUALIFICATION. Frame as an exploratory capability suitable for fast streaming data, noting strong stationarity assumptions.'
    },
    {
        'Component_or_Claim_ID': 'ICC-05-DISCORDANCE-SOLUTION-CLAIM',
        'Component_Name': 'Claim of ICC Resolving Stability-Accuracy Discordance',
        'Conceptual_Idea': 'Claiming that ICC-v2 overcomes or resolves the observed stability-accuracy discordance in consensus clustering.',
        'Current_Empirical_Evidence': 'Across the 6 biomedical cohorts, ICC-v2 still exhibits a substantial mean gap (+0.300 in Table 2, stability 0.468 vs accuracy 0.168).',
        'Unresolved_Mathematical_Issue': 'High stability in consensus clustering is an intrinsic property of averaging base partitions and does not ensure reference alignment.',
        'Unresolved_Empirical_Issue': 'ICC-v2 reduces discordance only on cohorts where it achieves high accuracy; on CNS and Prostate, discordance persists.',
        'Appropriate_Future_Research_Question': 'Can external reference controls or multi-modal validation anchors bridge the gap between stability and biological ground truth?',
        'Claims_That_Should_Not_Be_Made': 'MUST NOT claim ICC solves stability-accuracy discordance. ICC is subject to the same fundamental phenomenon.',
        'Classification': 'UNSUPPORTED',
        'Manuscript_Action': 'REMOVE. Clearly articulate that ICC does not solve discordance; discordance remains an open challenge for all consensus methods.'
    },
    {
        'Component_or_Claim_ID': 'ICC-06-UNIVERSAL-BENCHMARK-SUPERIORITY',
        'Component_Name': 'Claim of Universal Benchmark Supremacy across 13 Datasets',
        'Conceptual_Idea': 'Claiming that ICC-v2 outperforms all 11 competing clustering algorithms across diverse benchmark domains.',
        'Current_Empirical_Evidence': 'Friedman test across 13 datasets on 11 methods yields chi2=11.3427, p=0.3315 (non-significant). ICC-v2 ranks 5th out of 11 (mean rank 5.462), behind DEC, Standard Consensus, K-Means, and Ward.',
        'Unresolved_Mathematical_Issue': 'No single clustering algorithm can dominate across diverse geometric geometries (Kleinberg\'s impossibility theorem for clustering).',
        'Unresolved_Empirical_Issue': 'ICC-v2 performs well on high-dimensional biomedical cohorts (mean rank 2.167), but achieves mediocre performance on low-dimensional image/text benchmarks.',
        'Appropriate_Future_Research_Question': 'What data geometric properties (e.g. D/N ratio, cluster separability) delineate the operational envelope where anchor consensus is advantageous?',
        'Claims_That_Should_Not_Be_Made': 'MUST NOT claim universal superiority or general benchmark dominance.',
        'Classification': 'OVERSTATED',
        'Manuscript_Action': 'REWRITE. Confine performance claims to high-dimensional biomedical regimes (D/N > 20) and explicitly disclose 5th-place rank on omnibus benchmarks.'
    }
]

out_icc_csv = 'audit/loop5_4/icc_claim_and_novelty_adjudication.csv'
fieldnames_icc = [
    'Component_or_Claim_ID', 'Component_Name', 'Conceptual_Idea',
    'Current_Empirical_Evidence', 'Unresolved_Mathematical_Issue',
    'Unresolved_Empirical_Issue', 'Appropriate_Future_Research_Question',
    'Claims_That_Should_Not_Be_Made', 'Classification', 'Manuscript_Action'
]

with open(out_icc_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames_icc)
    writer.writeheader()
    for r in icc_records:
        writer.writerow(r)

print(f"Successfully wrote {len(icc_records)} ICC claim records to {out_icc_csv}")

# -------------------------------------------------------------------------
# Task 8: Manuscript Claim Adjudication
# -------------------------------------------------------------------------
ms_claims = [
    {
        'Claim_ID': 'CLM-01-ABSTRACT-DISCORDANCE',
        'Manuscript_Section': 'Abstract',
        'Exact_Claim_or_Quotation': 'We show that subsample stability is frequently disconnected from reference accuracy in high-dimensional cohorts, with severe discordance observed across biomedical benchmarks.',
        'Supporting_Evidence': 'Subsample stability summary (72 cells): mean gap = +0.4643, clustered bootstrap 95% CI [+0.3643, +0.6084]. Correlation r = -0.0319.',
        'Evidence_Source': 'results/evidence_recovery/recovered/subsample_stability_summary.csv',
        'Statistical_Validity': 'HIGHLY_DEFENSIBLE',
        'Reproducibility_Status': 'REPRODUCED',
        'Generalizability': 'Observed across all 6 evaluated biomedical cancer cohorts; robust across leave-one-out analyses.',
        'Recommended_Action': 'RETAIN',
        'Suggested_Replacement_Wording': 'Retain as written. This represents the primary, rock-solid empirical contribution of the manuscript.'
    },
    {
        'Claim_ID': 'CLM-02-ABSTRACT-ICC-POSITIONING',
        'Manuscript_Section': 'Abstract',
        'Exact_Claim_or_Quotation': 'We present Innovative Consensus Clustering (ICC), a novel consensus framework that resolves stability-accuracy discordance and achieves superior performance.',
        'Supporting_Evidence': 'Friedman test across 13 benchmarks p=0.3315 (rank 5/11); ICC-v2 still exhibits a +0.300 gap on biomedical cohorts.',
        'Evidence_Source': 'results.json (exp3_1) and subsample_stability_summary.csv',
        'Statistical_Validity': 'INVALID_OVERSTATEMENT',
        'Reproducibility_Status': 'CONTRADICTED',
        'Generalizability': 'Not generalizable.',
        'Recommended_Action': 'REWRITE',
        'Suggested_Replacement_Wording': 'We introduce Innovative Consensus Clustering (ICC) as an exploratory methodological framework that pairs bipartite anchor graphs with subspace gating, offering scalable consensus while highlighting directions for future investigation.'
    },
    {
        'Claim_ID': 'CLM-03-INTRO-STABILITY-ASSUMPTION',
        'Manuscript_Section': 'Section 1 (Introduction)',
        'Exact_Claim_or_Quotation': 'Consensus clustering routinely relies on subsample stability as a surrogate for clustering validity, based on the unverified assumption that stable partitions reflect ground-truth biological clusters.',
        'Supporting_Evidence': 'Extensive literature review (Monti et al., 2003; Senbabaoglu et al., 2014) and empirical audit of 12 consensus algorithms.',
        'Evidence_Source': 'paper/sections/01_introduction.tex and references.bib',
        'Statistical_Validity': 'VALID_CONCEPTUAL_FOUNDATION',
        'Reproducibility_Status': 'VERIFIED',
        'Generalizability': 'Broadly applicable across computational biology.',
        'Recommended_Action': 'RETAIN',
        'Suggested_Replacement_Wording': 'Retain as written. Sets up the primary research question with exceptional clarity.'
    },
    {
        'Claim_ID': 'CLM-04-METHODS-AUTOK-GUARANTEES',
        'Manuscript_Section': 'Section 3.3 (AutoK Selection)',
        'Exact_Claim_or_Quotation': 'AutoK provides a PAC-Bayesian bound ensuring that the selected number of clusters K minimizes consensus risk with high probability.',
        'Supporting_Evidence': '510/510 trials in adversarial_autok_raw_results.csv collapsed to K_min=2 (95.3% zero scores).',
        'Evidence_Source': 'results/evidence_recovery/recovered/adversarial_autok_raw_results.csv',
        'Statistical_Validity': 'MATHEMATICALLY_DEFICIENT_FOR_FINITE_SAMPLES',
        'Reproducibility_Status': 'CONTRADICTED',
        'Generalizability': 'Collapses universally on small biomedical sample sizes.',
        'Recommended_Action': 'MOVE TO FUTURE WORK',
        'Suggested_Replacement_Wording': 'Disclose the boundary collapse in Section 3/Limitations: In small-sample regimes (N < 200), conservative concentration bounds dominate empirical risk, selecting K_min. Developing tight, finite-sample calibrated bounds remains an open research direction.'
    },
    {
        'Claim_ID': 'CLM-05-RESULTS-LEUKEMIA-CI',
        'Manuscript_Section': 'Section 5.1 / Table 2',
        'Exact_Claim_or_Quotation': 'Leukemia ARI 95% confidence interval is [-0.1048, 1.0397].',
        'Supporting_Evidence': 'Derived from naive Student-t distribution on 5 seeds in Loop 2 exp5 protocol; violates ARI theoretical upper bound 1.0.',
        'Evidence_Source': 'results/loop2/raw/exp5_baseline_comparison.json',
        'Statistical_Validity': 'UNSUITABLE_PARAMETRIC_MODEL',
        'Reproducibility_Status': 'CONTRADICTED',
        'Generalizability': 'Invalid statistical inference.',
        'Recommended_Action': 'REWRITE',
        'Suggested_Replacement_Wording': 'Report the 10-seed non-parametric percentile bootstrap interval [0.430, 0.859] (mean 0.680, median 0.838), qualifying that it characterizes algorithmic initialization variation on this cohort.'
    },
    {
        'Claim_ID': 'CLM-06-RESULTS-SRBCT-WILCOXON',
        'Manuscript_Section': 'Section 5.3 (Benchmark Comparisons)',
        'Exact_Claim_or_Quotation': 'GAC achieves statistically significant improvement on SRBCT with p = 0.03125.',
        'Supporting_Evidence': 'Exact Wilcoxon on 5 paired seeds yields two-sided p = 0.0625; p = 0.03125 is strictly one-sided.',
        'Evidence_Source': 'results/loop2/raw/exp5_baseline_comparison.csv',
        'Statistical_Validity': 'SELECTIVE_ONE_SIDED_REPORTING',
        'Reproducibility_Status': 'CONTRADICTED',
        'Generalizability': 'Marginally significant trend on 5 seeds; significant on 10 seeds (p=0.00195).',
        'Recommended_Action': 'REWRITE',
        'Suggested_Replacement_Wording': 'Report exact two-sided p = 0.0625 on 5 seeds (non-significant at alpha=0.05) and report two-sided p = 0.00195 on the 10 canonical seeds in exp3_1.'
    },
    {
        'Claim_ID': 'CLM-07-RESULTS-FACTORIAL-SIGNIFICANCE',
        'Manuscript_Section': 'Section 5.4 (Ablation)',
        'Exact_Claim_or_Quotation': 'Factorial ablation demonstrates statistically significant component necessity across all six biomedical cohorts.',
        'Supporting_Evidence': 'All 6 paired Wilcoxon tests yield raw p >= 0.156 and Holm-Bonferroni p_adj >= 0.938.',
        'Evidence_Source': 'results/evidence_recovery/recovered/exp2_real_high_d_factorial.csv',
        'Statistical_Validity': 'UNSUPPORTED_BY_DATA',
        'Reproducibility_Status': 'CONTRADICTED',
        'Generalizability': 'Component advantages are concentrated in Leukemia and SRBCT (+0.50 to +0.67), but negligible on other cohorts (+0.024).',
        'Recommended_Action': 'REWRITE',
        'Suggested_Replacement_Wording': 'Factorial ablation shows an observed empirical advantage for full GAC (mean ARI diff +0.132 to +0.194), though multi-comparison adjusted Wilcoxon tests fail to reach significance (p_adj >= 0.938), indicating gains are concentrated in specific multimodal cohorts.'
    },
    {
        'Claim_ID': 'CLM-08-RESULTS-OMNIBUS-SUPREMACY',
        'Manuscript_Section': 'Section 5.2 (Table 6)',
        'Exact_Claim_or_Quotation': 'GAC outperforms all 11 baseline algorithms across 13 diverse benchmarks, demonstrating state-of-the-art consensus clustering performance.',
        'Supporting_Evidence': 'Friedman omnibus test p=0.3315; GAC ranks 5th out of 11 (mean rank 5.462) across all benchmarks.',
        'Evidence_Source': 'results.json (exp3_1) and Table 6',
        'Statistical_Validity': 'OVERSTATED_AND_NON_SIGNIFICANT',
        'Reproducibility_Status': 'CONTRADICTED',
        'Generalizability': 'GAC ranks 1st only in high-dimensional biomedical cohorts (mean rank 2.167), but performs average in lower dimensions.',
        'Recommended_Action': 'REWRITE',
        'Suggested_Replacement_Wording': 'While GAC ranks 1st in the high-dimensional biomedical regime (mean rank 2.167), omnibus comparison across all 13 benchmarks shows no statistically significant divergence among algorithms (Friedman p=0.3315, GAC rank 5.462), positioning GAC as a regime-specific rather than universal architecture.'
    },
    {
        'Claim_ID': 'CLM-09-TABLE-6-FIT-COUNT',
        'Manuscript_Section': 'Table 6 Caption',
        'Exact_Claim_or_Quotation': 'Empirical Adjusted Rand Index Comparison Across All 12 Methods on 13 Benchmarks (... 3,000 Total Model Fits)',
        'Supporting_Evidence': 'results.json exp3_1 contains primary microdata for exactly 1,430 core fits (1,715 fits total). Runs for seeds 11-30 and baselines CoreHalo/CoHiRF on non-biomedical datasets are missing.',
        'Evidence_Source': 'results.json (exp3_1)',
        'Statistical_Validity': 'UNVERIFIABLE_RECORD_COUNT',
        'Reproducibility_Status': 'UNVERIFIED',
        'Generalizability': 'N/A',
        'Recommended_Action': 'REWRITE',
        'Suggested_Replacement_Wording': 'Amend Table 6 caption to cite verified primary microdata: (Mean +- SD Across Canonical Random Seeds; 1,430 Primary Verified Benchmark Fits).'
    },
    {
        'Claim_ID': 'CLM-10-SCALABILITY-HALLUCINATED-NUMBERS',
        'Manuscript_Section': 'Section 4.3 / Section 5.5',
        'Exact_Claim_or_Quotation': 'Empirical peak RSS is 142 MB at N=500 and 846 MB at N=10,000, avoiding the 800 MB - 20 GB matrix required by full consensus.',
        'Supporting_Evidence': '142 MB and 846 MB do not exist in results.json or exp6_scalability.csv. Actual traced RAM in Table 4 is 3.1 MB at N=500 and 68.8 MB at N=10,000.',
        'Evidence_Source': 'paper/tables/table04_sample_scaling.tex and results/loop2/raw/exp6_scalability.csv',
        'Statistical_Validity': 'FACTUALLY_ERRONEOUS_NUMBERS',
        'Reproducibility_Status': 'CONTRADICTED',
        'Generalizability': 'Sub-quadratic scaling is mathematically sound, but cited numbers are fictional.',
        'Recommended_Action': 'REWRITE',
        'Suggested_Replacement_Wording': 'Expunge 142 MB and 846 MB. State: Peak traced heap allocation is 3.1 MB at N=500 and 68.8 MB at N=10,000, avoiding the 762.9 MB to 19.1 GB dense co-association matrix required by standard consensus.'
    },
    {
        'Claim_ID': 'CLM-11-DISCUSSION-RESEARCH-HIERARCHY',
        'Manuscript_Section': 'Section 6 (Discussion & Limitations)',
        'Exact_Claim_or_Quotation': 'Our results confirm that ICC provides a definitive, generalizable clustering solution for clinical high-dimensional genomics.',
        'Supporting_Evidence': 'Discordance persists in consensus clustering; no external clinical cohort validation was conducted.',
        'Evidence_Source': 'subsample_stability_summary.csv',
        'Statistical_Validity': 'UNFOUNDED_CLINICAL_CLAIM',
        'Reproducibility_Status': 'UNSUPPORTED',
        'Generalizability': 'Clinical utility is unproven.',
        'Recommended_Action': 'REWRITE',
        'Suggested_Replacement_Wording': 'Align with locked research hierarchy: Our findings establish that stability cannot be treated as a surrogate for clinical clustering validity. We present ICC as an exploratory collection of methodological ideas that warrant rigorous future investigation into finite-sample calibration and external clinical validation.'
    }
]

out_ms_csv = 'audit/loop5_4/manuscript_claim_adjudication.csv'
fieldnames_ms = [
    'Claim_ID', 'Manuscript_Section', 'Exact_Claim_or_Quotation',
    'Supporting_Evidence', 'Evidence_Source', 'Statistical_Validity',
    'Reproducibility_Status', 'Generalizability', 'Recommended_Action',
    'Suggested_Replacement_Wording'
]

with open(out_ms_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames_ms)
    writer.writeheader()
    for r in ms_claims:
        writer.writerow(r)

print(f"Successfully wrote {len(ms_claims)} manuscript claim records to {out_ms_csv}")
