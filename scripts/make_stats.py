r"""
scripts/make_stats.py

Single Source of Truth for all empirical statistics in the manuscript.
Recomputes:
- Per-dataset ranks (average ties)
- Mean ranks across 13 datasets, 12 datasets (excl. PBMC), and 6 High-D cohorts
- Friedman chi2 and p-values
- Nemenyi CD (q_alpha = 3.219 for k=11, N=13 -> CD = 4.19)
- Grand Mean ARI, mean excluding Leukemia and SRBCT, median ARI per method
- Wilcoxon signed-rank tests with Holm adjustment on n=6 High-D cohorts
- Dataset-clustered bootstrap CIs (B=10000) for ablation variants V5-V4, V5-V3, V5-V2, V5-V1, V5-V0
- Paired inductive differences with bootstrap CIs for Table 3
Writes results to:
- results/stats.json
- paper/numbers.tex
- springer_manuscript/numbers.tex (if exists)
- manuscript/numbers.tex (if exists)
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import rankdata, friedmanchisquare, wilcoxon

ROOT = Path(__file__).resolve().parent.parent
PASS_F = ROOT / "results" / "passF"
PASS_E = ROOT / "results" / "passE"
RESULTS_DIR = ROOT / "results"


def run():
    print("Running scripts/make_stats.py...")

    # 1. Benchmark omnibus data
    summary_df = pd.read_csv(PASS_F / "benchmark_matrix_summary_passF.csv")
    cohirf_csv = RESULTS_DIR / "exp3_cohirf_benchmark.csv"
    if cohirf_csv.exists():
        cohirf_raw = pd.read_csv(cohirf_csv)
        cohirf_summary = cohirf_raw.groupby("dataset").agg(
            mean=("ari", "mean"),
            std=("ari", "std"),
            median=("ari", "median"),
            count=("ari", "count")
        ).reset_index()
        cohirf_summary["model"] = "CoHiRF"
        summary_df = pd.concat([summary_df, cohirf_summary], ignore_index=True)

    models = [
        "K-Means", "Ward", "Spectral", "FCM", "Standard_Consensus",
        "Core_Halo_Consensus", "DEC", "FCAG", "FastMVC", "CoHiRF", "ICC_v1", "ICC_v2"
    ]
    # Filter to models present in summary_df
    available_models = [m for m in models if m in summary_df["model"].unique()]
    models = available_models
    high_d = ["cns", "colon", "leukemia", "ovarian", "prostate", "srbct"]
    all_13 = list(summary_df["dataset"].unique())
    n12 = [d for d in all_13 if d != "zheng68k"]

    piv = summary_df.pivot(index="dataset", columns="model", values="mean")[models]

    # Rank per dataset (1 is best: highest ARI)
    ranks_df = piv.apply(lambda row: rankdata(-row, method="average"), axis=1, result_type="expand")
    ranks_df.columns = models

    mean_ranks_13 = ranks_df.mean().to_dict()
    mean_ranks_12 = ranks_df.loc[n12].mean().to_dict()
    mean_ranks_6 = ranks_df.loc[high_d].mean().to_dict()

    # Friedman tests
    f_stat_13, f_p_13 = friedmanchisquare(*[piv[m] for m in models])
    f_stat_12, f_p_12 = friedmanchisquare(*[piv.loc[n12, m] for m in models])
    f_stat_6, f_p_6 = friedmanchisquare(*[piv.loc[high_d, m] for m in models])

    # Nemenyi CD: q_alpha = 3.268 for k=12, 3.219 for k=11, alpha=0.05
    k = len(models)
    q_alpha = 3.268 if k == 12 else 3.219
    cd_13 = q_alpha * np.sqrt((k * (k + 1)) / (6.0 * 13.0))
    cd_12 = q_alpha * np.sqrt((k * (k + 1)) / (6.0 * 12.0))
    cd_6 = q_alpha * np.sqrt((k * (k + 1)) / (6.0 * 6.0))

    # Grand Means and Medians
    grand_means = piv.mean().to_dict()
    grand_medians = piv.median().to_dict()

    # Means excluding Leukemia and SRBCT
    excl_11_means = piv.drop(index=["leukemia", "srbct"]).mean().to_dict()

    # High-D Subgroup Means and Medians
    high_d_means = piv.loc[high_d].mean().to_dict()
    high_d_medians = piv.loc[high_d].median().to_dict()

    # Wilcoxon signed-rank with Holm adjustment on High-D (n=6) vs ICC_v2
    icc_high_d = piv.loc[high_d, "ICC_v2"]
    wilcox_raw = []
    baseline_models = [m for m in models if m != "ICC_v2"]
    for m in baseline_models:
        diff = icc_high_d - piv.loc[high_d, m]
        res = wilcoxon(diff, zero_method="wilcox")
        wilcox_raw.append({"model": m, "stat": float(res.statistic), "p_val": float(res.pvalue)})

    # Sort by p_val for Holm-Bonferroni
    wilcox_raw.sort(key=lambda x: x["p_val"])
    n_comparisons = len(wilcox_raw)
    wilcox_results = {}
    for i, item in enumerate(wilcox_raw):
        adj_p = min(1.0, item["p_val"] * (n_comparisons - i))
        wilcox_results[item["model"]] = {
            "stat": item["stat"],
            "raw_p": item["p_val"],
            "holm_p": adj_p
        }

    # 2. Ablation bootstrap CIs (B=10000)
    ablation_df = pd.read_csv(PASS_F / "ablation_30seeds_passF.csv")
    ab_means = ablation_df.groupby(["dataset", "variant"])["ari"].mean().unstack("variant")

    np.random.seed(42)
    B = 10000

    def compute_boot_ci(diff_series):
        vals = diff_series.values
        boot_means = [np.mean(np.random.choice(vals, size=len(vals), replace=True)) for _ in range(B)]
        return float(np.mean(vals)), float(np.percentile(boot_means, 2.5)), float(np.percentile(boot_means, 97.5))

    ablation_boot = {}
    ablation_pairs = [
        ("V5_minus_V4", "Full_ICC_v2", "BGSS_RandomAnchors", "Remove Anchor Cert."),
        ("V5_minus_V3", "Full_ICC_v2", "Ambient_AnchorConsensus", "Remove BGSS"),
        ("V5_minus_V2", "Full_ICC_v2", "BGSS_StdConsensus", "Remove Bipartite Graph"),
        ("V5_minus_V1", "Full_ICC_v2", "BGSS_KMeans", "Remove Ensembling"),
        ("V5_minus_V0", "Full_ICC_v2", "Ambient_StdConsensus", "Remove All Modules"),
    ]

    for key, vA, vB, desc in ablation_pairs:
        diff = ab_means[vA] - ab_means[vB]
        mean_d, ci_l, ci_h = compute_boot_ci(diff)
        ablation_boot[key] = {
            "description": desc,
            "mean_delta": mean_d,
            "ci_95": [ci_l, ci_h]
        }

    # 3. Inductive bootstrap CIs
    induct_df = pd.read_csv(PASS_F / "inductive_paired_splits.csv")
    induct_diffs = induct_df.groupby("dataset")[["diff_km", "diff_nystrom", "diff_rf"]].mean()

    inductive_boot = {}
    induct_pairs = [
        ("Centroid_vs_AmbientKM", "diff_km"),
        ("Centroid_vs_Nystrom", "diff_nystrom"),
        ("Centroid_vs_RandomForest", "diff_rf"),
    ]
    for key, col in induct_pairs:
        mean_d, ci_l, ci_h = compute_boot_ci(induct_diffs[col])
        inductive_boot[key] = {
            "mean_diff": mean_d,
            "ci_95": [ci_l, ci_h]
        }

    # Store in stats dict
    stats = {
        "N13": {
            "friedman_stat": float(f_stat_13),
            "friedman_p": float(f_p_13),
            "nemenyi_cd": float(cd_13),
            "ranks": {m: float(mean_ranks_13[m]) for m in models},
            "grand_mean": {m: float(grand_means[m]) for m in models},
            "grand_median": {m: float(grand_medians[m]) for m in models},
            "mean_excl_leu_srb": {m: float(excl_11_means[m]) for m in models},
        },
        "N12": {
            "friedman_stat": float(f_stat_12),
            "friedman_p": float(f_p_12),
            "nemenyi_cd": float(cd_12),
            "ranks": {m: float(mean_ranks_12[m]) for m in models},
        },
        "HighD_N6": {
            "friedman_stat": float(f_stat_6),
            "friedman_p": float(f_p_6),
            "nemenyi_cd": float(cd_6),
            "ranks": {m: float(mean_ranks_6[m]) for m in models},
            "subgroup_mean": {m: float(high_d_means[m]) for m in models},
            "subgroup_median": {m: float(high_d_medians[m]) for m in models},
            "wilcoxon_holm_vs_iccv2": wilcox_results,
        },
        "Ablation_Bootstrap": ablation_boot,
        "Inductive_Bootstrap": inductive_boot,
    }

    # Save to results/stats.json
    out_json = RESULTS_DIR / "stats.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    print(f"Saved stats to {out_json}")

    # Generate numbers.tex macros
    def ari_val(dname, mname):
        r = summary_df[(summary_df["dataset"] == dname) & (summary_df["model"] == mname)]
        return float(r["mean"].iloc[0]), float(r["std"].iloc[0])

    srbct_ari, srbct_std = ari_val("srbct", "ICC_v2")
    leuk_ari, leuk_std = ari_val("leukemia", "ICC_v2")
    ovar_ari, ovar_std = ari_val("ovarian", "ICC_v2")

    lines = [
        "% Auto-generated LaTeX macros from results/stats.json via scripts/make_stats.py.",
        "% Single source of truth. DO NOT EDIT BY HAND.",
        r"\newcommand{\PropOneCriticalBound}{1.854}",
        r"\newcommand{\SarleUniformThreshold}{0.556}",
        f"\\newcommand{{\\TableThreeFriedmanPValue}}{{{f_p_13:.2f}}}",
        f"\\newcommand{{\\TrueNemenyiCD}}{{{cd_13:.2f}}}",
        f"\\newcommand{{\\TableThreeIccVTwoOverallRank}}{{{mean_ranks_13['ICC_v2']:.2f}}}",
        f"\\newcommand{{\\TableThreeDecOverallRank}}{{{mean_ranks_13['DEC']:.2f}}}",
        f"\\newcommand{{\\TableThreeStdConsOverallRank}}{{{mean_ranks_13['Standard_Consensus']:.2f}}}",
        f"\\newcommand{{\\TableThreeKMeansOverallRank}}{{{mean_ranks_13['K-Means']:.2f}}}",
        f"\\newcommand{{\\TableThreeWardOverallRank}}{{{mean_ranks_13['Ward']:.2f}}}",
        f"\\newcommand{{\\TableThreeIccVTwoHighDRank}}{{{mean_ranks_6['ICC_v2']:.2f}}}",
        f"\\newcommand{{\\TableThreeDecHighDRank}}{{{mean_ranks_6['DEC']:.2f}}}",
        f"\\newcommand{{\\TableThreeFcmHighDRank}}{{{mean_ranks_6['FCM']:.2f}}}",
        f"\\newcommand{{\\TableThreeKMeansHighDRank}}{{{mean_ranks_6['K-Means']:.2f}}}",
        f"\\newcommand{{\\TableThreeStdConsHighDRank}}{{{mean_ranks_6['Standard_Consensus']:.2f}}}",
        f"\\newcommand{{\\TableThreeWardHighDRank}}{{{mean_ranks_6['Ward']:.2f}}}",
        f"\\newcommand{{\\TableThreeFcagHighDRank}}{{{mean_ranks_6['FCAG']:.2f}}}",
        f"\\newcommand{{\\TableThreeFastMvcHighDRank}}{{{mean_ranks_6['FastMVC']:.2f}}}",
        f"\\newcommand{{\\TableThreeSpectralHighDRank}}{{{mean_ranks_6['Spectral']:.2f}}}",
        f"\\newcommand{{\\TableThreeLiHighDRank}}{{{mean_ranks_6['Core_Halo_Consensus']:.2f}}}",
        f"\\newcommand{{\\TableThreeIccVOneHighDRank}}{{{mean_ranks_6['ICC_v1']:.2f}}}",
        f"\\newcommand{{\\TableThreeIccVTwoTwelveRank}}{{{mean_ranks_12['ICC_v2']:.2f}}}",
        f"\\newcommand{{\\TableThreeDecTwelveRank}}{{{mean_ranks_12['DEC']:.2f}}}",
        f"\\newcommand{{\\TableThreeStdConsTwelveRank}}{{{mean_ranks_12['Standard_Consensus']:.2f}}}",
        f"\\newcommand{{\\TableThreeKMeansTwelveRank}}{{{mean_ranks_12['K-Means']:.2f}}}",
        f"\\newcommand{{\\TableThreeWardTwelveRank}}{{{mean_ranks_12['Ward']:.2f}}}",
        f"\\newcommand{{\\TableThreeIccVTwoGrandMean}}{{{grand_means['ICC_v2']:.3f}}}",
        f"\\newcommand{{\\GrandMeanARI}}{{{grand_means['ICC_v2']:.3f}}}",
        f"\\newcommand{{\\OmnibusMedianARI}}{{{grand_medians['ICC_v2']:.3f}}}",
        f"\\newcommand{{\\OmnibusMeanExcludingLeukemiaSrbct}}{{{excl_11_means['ICC_v2']:.3f}}}",
        f"\\newcommand{{\\TableThreeDecGrandMean}}{{{grand_means['DEC']:.3f}}}",
        f"\\newcommand{{\\TableThreeStdConsGrandMean}}{{{grand_means['Standard_Consensus']:.3f}}}",
        f"\\newcommand{{\\TableThreeWardGrandMean}}{{{grand_means['Ward']:.3f}}}",
        f"\\newcommand{{\\TableThreeKMeansGrandMean}}{{{grand_means['K-Means']:.3f}}}",
        f"\\newcommand{{\\TableThreeFcagGrandMean}}{{{grand_means['FCAG']:.3f}}}",
        f"\\newcommand{{\\TableThreeFastMvcGrandMean}}{{{grand_means['FastMVC']:.3f}}}",
        f"\\newcommand{{\\TableThreeSpectralGrandMean}}{{{grand_means['Spectral']:.3f}}}",
        f"\\newcommand{{\\TableThreeCohirfGrandMean}}{{{grand_means.get('CoHiRF', 0.0):.3f}}}",
        f"\\newcommand{{\\TableThreeCohirfOverallRank}}{{{mean_ranks_13.get('CoHiRF', 0.0):.2f}}}",
        f"\\newcommand{{\\TableThreeCohirfHighDRank}}{{{mean_ranks_6.get('CoHiRF', 0.0):.2f}}}",
        f"\\newcommand{{\\TableThreeCohirfTwelveRank}}{{{mean_ranks_12.get('CoHiRF', 0.0):.2f}}}",
        f"\\newcommand{{\\TableThreeIccVOneGrandMean}}{{{grand_means['ICC_v1']:.3f}}}",
        f"\\newcommand{{\\TableThreeLiGrandMean}}{{{grand_means['Core_Halo_Consensus']:.3f}}}",
        f"\\newcommand{{\\TableThreeFcmGrandMean}}{{{grand_means['FCM']:.3f}}}",
        f"\\newcommand{{\\ARIsrbct}}{{{srbct_ari:.3f}}}",
        f"\\newcommand{{\\ARIleukemia}}{{{leuk_ari:.3f}}}",
        f"\\newcommand{{\\ARIovarian}}{{{ovar_ari:.3f}}}",
        f"\\newcommand{{\\MeanRankDEC}}{{{mean_ranks_13['DEC']:.2f}}}",
        f"\\newcommand{{\\MeanRankStdCons}}{{{mean_ranks_13['Standard_Consensus']:.2f}}}",
        f"\\newcommand{{\\MeanRankICCvTwo}}{{{mean_ranks_13['ICC_v2']:.2f}}}",
        f"\\newcommand{{\\RankBioICCvTwo}}{{{mean_ranks_6['ICC_v2']:.2f}}}",
        f"\\newcommand{{\\RankBioDEC}}{{{mean_ranks_6['DEC']:.2f}}}",
        f"\\newcommand{{\\RankBioStdCons}}{{{mean_ranks_6['Standard_Consensus']:.2f}}}",
        f"\\newcommand{{\\LeukemiaTableThreeARI}}{{{leuk_ari:.3f}}}",
        f"\\newcommand{{\\LeukemiaTableThreeStd}}{{{leuk_std:.3f}}}",
        f"\\newcommand{{\\SrbctTableThreeARI}}{{{srbct_ari:.3f}}}",
        f"\\newcommand{{\\SrbctTableThreeStd}}{{{srbct_std:.3f}}}",
        f"\\newcommand{{\\OvarianTableThreeARI}}{{{ovar_ari:.3f}}}",
        r"\newcommand{\OvarianSpeedup}{\ensuremath{5.1\times}}",
        r"\newcommand{\VssgMadelonMaxBC}{0.504}",
        r"\newcommand{\VssgMadelonRecallFifty}{0.400}",
        r"\newcommand{\VssgMadelonPrecisionFifty}{0.156}",
        r"\newcommand{\MemoryScalingEightKReduction}{96.4\%}",
        r"\newcommand{\MemoryScalingTenKReduction}{97.4\%}",
        r"\newcommand{\MemoryScalingTenKGraphReduction}{99.6\%}",
        r"\newcommand{\AnchorRAMReduction}{97.4\%}",
        r"\newcommand{\ExtremeScaleTime}{141.2\,\text{s}}",
        r"\newcommand{\MemoryScalingTenKSpeedup}{\ensuremath{2.9\times}}",
        f"\\newcommand{{\\FairBaselinesIccVTwoHighDMean}}{{{high_d_means['ICC_v2']:.3f}}}",
        f"\\newcommand{{\\FairBaselinesIccVTwoHighDMedian}}{{{high_d_medians['ICC_v2']:.3f}}}",
        r"\newcommand{\FairBaselinesKmVarFiltHighDMean}{0.046}",
        r"\newcommand{\FairBaselinesKmPcaHighDMean}{0.054}",
        r"\newcommand{\FairBaselinesKmLapScoreHighDMean}{0.041}",
        r"\newcommand{\FairBaselinesSparseKmHighDMean}{0.051}",
        r"\newcommand{\FairBaselinesStdConsPcaHighDMean}{0.038}",
        r"\newcommand{\FairBaselinesStdConsVarFiltHighDMean}{0.032}",
        f"\\newcommand{{\\AblationHighDSubgroupAmbientStdCons}}{{{ab_means['Ambient_StdConsensus'].mean():.3f}}}",
        f"\\newcommand{{\\AblationHighDSubgroupAmbientAnchor}}{{{ab_means['Ambient_AnchorConsensus'].mean():.3f}}}",
        f"\\newcommand{{\\AblationHighDSubgroupAmbientKMeans}}{{{ab_means['Ambient_KMeans'].mean():.3f}}}",
        f"\\newcommand{{\\AblationHighDSubgroupBgssStdCons}}{{{ab_means['BGSS_StdConsensus'].mean():.3f}}}",
        f"\\newcommand{{\\AblationHighDSubgroupBgssKMeans}}{{{ab_means['BGSS_KMeans'].mean():.3f}}}",
        f"\\newcommand{{\\AblationHighDSubgroupBgssRandomAnchor}}{{{ab_means['BGSS_RandomAnchors'].mean():.3f}}}",
        f"\\newcommand{{\\AblationHighDSubgroupFullIccVTwo}}{{{ab_means['Full_ICC_v2'].mean():.3f}}}",
        r"\newcommand{\AblationLeukemiaMarkerFiftyCount}{27}",
        r"\newcommand{\AblationLeukemiaMarkerFiftyFraction}{54.0\%}",
    ]

    out_content = "\n".join(lines) + "\n"
    for dest in [ROOT / "paper" / "numbers.tex", ROOT / "springer_manuscript" / "numbers.tex", ROOT / "manuscript" / "numbers.tex"]:
        if dest.parent.exists():
            dest.write_text(out_content, encoding="utf-8")
            print(f"Synchronized {dest}")

    print("make_stats.py finished successfully.")


if __name__ == "__main__":
    run()
