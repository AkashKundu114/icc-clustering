"""
Updates Table 4 (Omnibus Benchmark Matrix) and numbers.tex from results/passE/benchmark_matrix_seeds0_9.csv.
Ensures zero numerical discrepancy between text, tables, and macros.
"""

from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare

CSV_PATH = Path("results/passE/benchmark_matrix_seeds0_9.csv")
MAIN_TEX = Path("springer_manuscript/main.tex")
NUMBERS_TEX = Path("springer_manuscript/numbers.tex")
PAPER_NUMBERS_TEX = Path("paper/numbers.tex")

HIGH_D_DATASETS = ["cns", "colon", "leukemia", "ovarian", "prostate", "srbct"]
DATASET_ORDER = [
    "cns", "colon", "indian_pines", "isolet", "leukemia",
    "madelon", "newsgroups20", "ovarian", "prostate", "sonar",
    "srbct", "yale_b", "zheng68k"
]

DATASET_DISPLAY = {
    "cns": r"CNS ($60, 7.1\text{k}, 2$)",
    "colon": r"Colon ($62, 2.0\text{k}, 2$)",
    "indian_pines": r"Indian Pines ($10.2\text{k}, 200, 16$)",
    "isolet": r"Isolet ($7.8\text{k}, 617, 26$)",
    "leukemia": r"Leukemia ($72, 7.1\text{k}, 2$)",
    "madelon": r"Madelon ($500, 500, 2$)",
    "newsgroups20": r"20 Newsgroups ($18.8\text{k}, 10\text{k}, 20$)",
    "ovarian": r"Ovarian ($253, 15.1\text{k}, 2$)",
    "prostate": r"Prostate ($102, 12.6\text{k}, 2$)",
    "sonar": r"Sonar ($208, 60, 2$)",
    "srbct": r"SRBCT ($83, 2.3\text{k}, 4$)",
    "yale_b": r"Yale B ($2.4\text{k}, 1.0\text{k}, 38$)",
    "zheng68k": r"PBMC68k-reduced ($700, 765, 10$)$^*$"
}

MODELS_PART1 = ["K-Means", "Ward", "Spectral", "FCM"]
MODELS_PART2 = ["Standard_Consensus", "Core_Halo_Consensus", "DEC", "FCAG"]
MODELS_PART3 = ["FastMVC", "ICC_v1", "ICC_v2"]

ALL_MODELS = MODELS_PART1 + MODELS_PART2 + MODELS_PART3


def compute_metrics(df: pd.DataFrame):
    # Group by dataset and model
    stats = df.groupby(["dataset", "model"])["ari"].agg(["mean", "std"]).reset_index()
    pivot_mean = df.groupby(["dataset", "model"])["ari"].mean().unstack()[ALL_MODELS]
    pivot_std = df.groupby(["dataset", "model"])["ari"].std().unstack()[ALL_MODELS]

    # Reindex datasets to canonical order
    pivot_mean = pivot_mean.reindex(DATASET_ORDER)
    pivot_std = pivot_std.reindex(DATASET_ORDER)

    # Ranks (1 = highest ARI)
    ranks_all = pivot_mean.rank(axis=1, ascending=False)
    mean_ranks_all = ranks_all.mean(axis=0)

    # 12 datasets (excluding PBMC)
    ranks_12 = pivot_mean.loc[[d for d in DATASET_ORDER if d != "zheng68k"]].rank(axis=1, ascending=False)
    mean_ranks_12 = ranks_12.mean(axis=0)

    # High-D subgroup (6 datasets)
    ranks_highd = pivot_mean.loc[HIGH_D_DATASETS].rank(axis=1, ascending=False)
    mean_ranks_highd = ranks_highd.mean(axis=0)

    # Grand Means
    grand_means = pivot_mean.mean(axis=0)

    # Friedman test (All 13)
    f_stat_13, f_pval_13 = friedmanchisquare(*[pivot_mean[m].values for m in ALL_MODELS])
    
    # Friedman test (12)
    f_stat_12, f_pval_12 = friedmanchisquare(*[pivot_mean.loc[[d for d in DATASET_ORDER if d != "zheng68k"]][m].values for m in ALL_MODELS])

    # Nemenyi CD: q_alpha = 3.219 for alpha=0.05, k=11
    cd_13 = 3.219 * np.sqrt((11 * 12) / (6 * 13))
    cd_12 = 3.219 * np.sqrt((11 * 12) / (6 * 12))

    return {
        "pivot_mean": pivot_mean,
        "pivot_std": pivot_std,
        "mean_ranks_all": mean_ranks_all,
        "mean_ranks_12": mean_ranks_12,
        "mean_ranks_highd": mean_ranks_highd,
        "grand_means": grand_means,
        "f_stat_13": f_stat_13,
        "f_pval_13": f_pval_13,
        "f_stat_12": f_stat_12,
        "f_pval_12": f_pval_12,
        "cd_13": cd_13,
        "cd_12": cd_12,
    }


def main():
    if not CSV_PATH.exists():
        print(f"Error: {CSV_PATH} does not exist.")
        return

    df = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df)} records from {CSV_PATH}.")
    if len(df) < 13 * 11 * 10:
        print(f"Warning: Only {len(df)} records present out of {13 * 11 * 10}. Some datasets/models still running.")
        return

    metrics = compute_metrics(df)
    p_mean = metrics["pivot_mean"]
    p_std = metrics["pivot_std"]
    mr_all = metrics["mean_ranks_all"]
    mr_12 = metrics["mean_ranks_12"]
    mr_hd = metrics["mean_ranks_highd"]
    gm = metrics["grand_means"]

    print("\n--- Summary of Computed Metrics ---")
    print(f"Friedman 13: Q={metrics['f_stat_13']:.4f}, p={metrics['f_pval_13']:.4f}, CD={metrics['cd_13']:.2f}")
    print(f"Friedman 12: Q={metrics['f_stat_12']:.4f}, p={metrics['f_pval_12']:.4f}, CD={metrics['cd_12']:.2f}")
    print("\nGrand Means:")
    for m in ALL_MODELS:
        print(f"  {m:<20}: {gm[m]:.3f} (Rank 13: {mr_all[m]:.2f}, Rank 12: {mr_12[m]:.2f}, Rank High-D: {mr_hd[m]:.2f})")

    # Format cell helper
    def fmt_cell(d, m):
        val = p_mean.loc[d, m]
        sd = p_std.loc[d, m]
        row_max = p_mean.loc[d].max()
        sign = "+" if val >= 0 else "-"
        abs_val = abs(val)
        txt = f"{sign}{abs_val:.3f} \\pm {sd:.3f}"
        if abs(val - row_max) < 1e-6:
            return f"$\\mathbf{{{txt}}}$"
        return f"${txt}$"

    # Build Table 4 LaTeX
    lines = []
    lines.append(r"\begin{table*}[!t]")
    lines.append(r"\caption{Omnibus Benchmark Matrix Across 13 Real-World Datasets and 11 Clustering Frameworks (10 Canonical Random Seeds, Mean $\pm$ Standard Deviation ARI)}")
    lines.append(r"\label{tab:benchmark_ari}")
    lines.append(r"\centering")
    lines.append(r"\tiny")
    lines.append(r"\setlength{\tabcolsep}{2.5pt}")
    lines.append("")

    # Part I
    lines.append(r"% Block 1: Classical Clustering Baselines")
    lines.append(r"\begin{tabular}{@{}lcccc@{}}")
    lines.append(r"\toprule")
    lines.append(r"\multicolumn{5}{c}{\textbf{Part I: Classical Clustering Baselines}} \\")
    lines.append(r"\midrule")
    lines.append(r"\textbf{Dataset ($N, D, K$)} & \textbf{K-Means}~\cite{macqueen1967methods,arthur2007k} & \textbf{Ward}~\cite{ward1963hierarchical} & \textbf{Spectral}~\cite{vonluxburg2007tutorial} & \textbf{FCM}~\cite{bezdek1981pattern} \\")
    lines.append(r"\midrule")
    for d in DATASET_ORDER:
        d_lbl = DATASET_DISPLAY[d]
        cells = [fmt_cell(d, m) for m in MODELS_PART1]
        lines.append(f"{d_lbl} & " + " & ".join(cells) + r" \\")
    lines.append(r"\midrule")
    lines.append(f"\\textbf{{Grand Mean ARI}} & {gm['K-Means']:.3f} & {gm['Ward']:.3f} & {gm['Spectral']:.3f} & {gm['FCM']:.3f} \\\\")
    lines.append(f"\\textbf{{Mean Rank (All 13)}} & {mr_all['K-Means']:.2f} & {mr_all['Ward']:.2f} & {mr_all['Spectral']:.2f} & {mr_all['FCM']:.2f} \\\\")
    lines.append(f"\\textbf{{Mean Rank (12, Excl. PBMC)}} & {mr_12['K-Means']:.2f} & {mr_12['Ward']:.2f} & {mr_12['Spectral']:.2f} & {mr_12['FCM']:.2f} \\\\")
    lines.append(f"\\textbf{{Mean Rank ($D/N > 20$ Subgroup)}} & {mr_hd['K-Means']:.2f} & {mr_hd['Ward']:.2f} & {mr_hd['Spectral']:.2f} & {mr_hd['FCM']:.2f} \\\\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append("")
    lines.append(r"\vspace{1.0ex}")
    lines.append("")

    # Part II
    lines.append(r"% Block 2: Consensus and Scalable Graph Baselines")
    lines.append(r"\begin{tabular}{@{}lcccc@{}}")
    lines.append(r"\toprule")
    lines.append(r"\multicolumn{5}{c}{\textbf{Part II: Consensus and Scalable Graph Baselines}} \\")
    lines.append(r"\midrule")
    lines.append(r"\textbf{Dataset ($N, D, K$)} & \textbf{Std Cons} & \textbf{Core-Halo Cons.} & \textbf{DEC} & \textbf{FCAG} \\")
    lines.append(r"\midrule")
    for d in DATASET_ORDER:
        d_lbl = DATASET_DISPLAY[d]
        cells = [fmt_cell(d, m) for m in MODELS_PART2]
        lines.append(f"{d_lbl} & " + " & ".join(cells) + r" \\")
    lines.append(r"\midrule")
    lines.append(f"\\textbf{{Grand Mean ARI}} & {gm['Standard_Consensus']:.3f} & {gm['Core_Halo_Consensus']:.3f} & {gm['DEC']:.3f} & {gm['FCAG']:.3f} \\\\")
    lines.append(f"\\textbf{{Mean Rank (All 13)}} & {mr_all['Standard_Consensus']:.2f} & {mr_all['Core_Halo_Consensus']:.2f} & {mr_all['DEC']:.2f} & {mr_all['FCAG']:.2f} \\\\")
    lines.append(f"\\textbf{{Mean Rank (12, Excl. PBMC)}} & {mr_12['Standard_Consensus']:.2f} & {mr_12['Core_Halo_Consensus']:.2f} & {mr_12['DEC']:.2f} & {mr_12['FCAG']:.2f} \\\\")
    lines.append(f"\\textbf{{Mean Rank ($D/N > 20$ Subgroup)}} & {mr_hd['Standard_Consensus']:.2f} & {mr_hd['Core_Halo_Consensus']:.2f} & {mr_hd['DEC']:.2f} & {mr_hd['FCAG']:.2f} \\\\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append("")
    lines.append(r"\vspace{1.0ex}")
    lines.append("")

    # Part III
    lines.append(r"% Block 3: Anchor Consensus and Proposed Frameworks")
    lines.append(r"\begin{tabular}{@{}lccc@{}}")
    lines.append(r"\toprule")
    lines.append(r"\multicolumn{4}{c}{\textbf{Part III: Anchor Consensus and Proposed Frameworks}} \\")
    lines.append(r"\midrule")
    lines.append(r"\textbf{Dataset ($N, D, K$)} & \textbf{FastMVC} & \textbf{ICC-v1} & \textbf{ICC-v2 (Ours)} \\")
    lines.append(r"\midrule")
    for d in DATASET_ORDER:
        d_lbl = DATASET_DISPLAY[d]
        cells = [fmt_cell(d, m) for m in MODELS_PART3]
        lines.append(f"{d_lbl} & " + " & ".join(cells) + r" \\")
    lines.append(r"\midrule")
    lines.append(f"\\textbf{{Grand Mean ARI}} & {gm['FastMVC']:.3f} & {gm['ICC_v1']:.3f} & \\textbf{{{gm['ICC_v2']:.3f}}} \\\\")
    lines.append(f"\\textbf{{Mean Rank (All 13)}} & {mr_all['FastMVC']:.2f} & {mr_all['ICC_v1']:.2f} & {mr_all['ICC_v2']:.2f} \\\\")
    lines.append(f"\\textbf{{Mean Rank (12, Excl. PBMC)}} & {mr_12['FastMVC']:.2f} & {mr_12['ICC_v1']:.2f} & {mr_12['ICC_v2']:.2f} \\\\")
    lines.append(f"\\textbf{{Mean Rank ($D/N > 20$ Subgroup)}} & {mr_hd['FastMVC']:.2f} & {mr_hd['ICC_v1']:.2f} & \\textbf{{{mr_hd['ICC_v2']:.2f}}} \\\\")
    lines.append(r"\midrule")
    lines.append(r"\multicolumn{4}{@{}l@{}}{\parbox{0.95\linewidth}{\vspace{0.4ex}\footnotesize $^*$PBMC68k-reduced is Scanpy's preprocessed demonstration subset (\texttt{pbmc68k\_reduced}, $N=700$ cells, $D=765$ highly variable genes, $K=10$ cell types) subsampled from the original $68.6\text{k}$ single-cell PBMC repository~\cite{zheng2017massively}.}} \\")
    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table*}")

    table4_tex = "\n".join(lines)

    # Now read main.tex and replace Table 4
    with open(MAIN_TEX, "r", encoding="utf-8") as f:
        main_content = f.read()

    # Find boundaries of Table 4 in main.tex using label
    lbl_pos = main_content.find(r"\label{tab:benchmark_ari}")
    if lbl_pos == -1:
        print("Could not find \\label{tab:benchmark_ari} in main.tex")
        return
    t4_start = main_content.rfind(r"\begin{table*}", 0, lbl_pos)
    if t4_start == -1:
        print("Could not find \\begin{table*} before \\label{tab:benchmark_ari}")
        return

    t4_end = main_content.find(r"\end{table*}", lbl_pos) + len(r"\end{table*}")

    updated_main = main_content[:t4_start] + table4_tex + main_content[t4_end:]
    with open(MAIN_TEX, "w", encoding="utf-8") as f:
        f.write(updated_main)
    print("Updated Table 4 in main.tex.")

    # Now update numbers.tex
    # Read existing numbers.tex
    with open(NUMBERS_TEX, "r", encoding="utf-8") as f:
        num_lines = f.readlines()

    macro_updates = {
        r"\TableThreeFriedmanPValue": f"{metrics['f_pval_13']:.2f}",
        r"\TrueNemenyiCD": f"{metrics['cd_13']:.2f}",
        r"\TableThreeIccVTwoOverallRank": f"{mr_all['ICC_v2']:.2f}",
        r"\TableThreeDecOverallRank": f"{mr_all['DEC']:.2f}",
        r"\TableThreeStdConsOverallRank": f"{mr_all['Standard_Consensus']:.2f}",
        r"\TableThreeKMeansOverallRank": f"{mr_all['K-Means']:.2f}",
        r"\TableThreeIccVTwoHighDRank": f"{mr_hd['ICC_v2']:.2f}",
        r"\TableThreeDecHighDRank": f"{mr_hd['DEC']:.2f}",
        r"\TableThreeFcmHighDRank": f"{mr_hd['FCM']:.2f}",
        r"\TableThreeKMeansHighDRank": f"{mr_hd['K-Means']:.2f}",
        r"\TableThreeStdConsHighDRank": f"{mr_hd['Standard_Consensus']:.2f}",
        r"\TableThreeIccVTwoTwelveRank": f"{mr_12['ICC_v2']:.2f}",
        r"\TableThreeDecTwelveRank": f"{mr_12['DEC']:.2f}",
        r"\TableThreeStdConsTwelveRank": f"{mr_12['Standard_Consensus']:.2f}",
        r"\TableThreeKMeansTwelveRank": f"{mr_12['K-Means']:.2f}",
        r"\TableThreeWardTwelveRank": f"{mr_12['Ward']:.2f}",
        r"\TableThreeIccVTwoGrandMean": f"{gm['ICC_v2']:.3f}",
        r"\GrandMeanARI": f"{gm['ICC_v2']:.3f}",
        r"\TableThreeDecGrandMean": f"{gm['DEC']:.3f}",
        r"\TableThreeStdConsGrandMean": f"{gm['Standard_Consensus']:.3f}",
        r"\TableThreeWardGrandMean": f"{gm['Ward']:.3f}",
        r"\TableThreeKMeansGrandMean": f"{gm['K-Means']:.3f}",
        r"\TableThreeFcagGrandMean": f"{gm['FCAG']:.3f}",
        r"\TableThreeFastMvcGrandMean": f"{gm['FastMVC']:.3f}",
        r"\TableThreeSpectralGrandMean": f"{gm['Spectral']:.3f}",
        r"\TableThreeIccVOneGrandMean": f"{gm['ICC_v1']:.3f}",
        r"\TableThreeLiGrandMean": f"{gm['Core_Halo_Consensus']:.3f}",
        r"\TableThreeFcmGrandMean": f"{gm['FCM']:.3f}",
        r"\ARIsrbct": f"{p_mean.loc['srbct', 'ICC_v2']:.3f}",
        r"\ARIleukemia": f"{p_mean.loc['leukemia', 'ICC_v2']:.3f}",
        r"\ARIovarian": f"{p_mean.loc['ovarian', 'ICC_v2']:.3f}",
        r"\MeanRankDEC": f"{mr_all['DEC']:.2f}",
        r"\MeanRankStdCons": f"{mr_all['Standard_Consensus']:.2f}",
        r"\MeanRankICCvTwo": f"{mr_all['ICC_v2']:.2f}",
        r"\RankBioICCvTwo": f"{mr_hd['ICC_v2']:.2f}",
        r"\RankBioDEC": f"{mr_hd['DEC']:.2f}",
        r"\RankBioStdCons": f"{mr_hd['Standard_Consensus']:.2f}",
        r"\LeukemiaTableThreeARI": f"{p_mean.loc['leukemia', 'ICC_v2']:.3f}",
        r"\LeukemiaTableThreeStd": f"{p_std.loc['leukemia', 'ICC_v2']:.3f}",
        r"\SrbctTableThreeARI": f"{p_mean.loc['srbct', 'ICC_v2']:.3f}",
        r"\SrbctTableThreeStd": f"{p_std.loc['srbct', 'ICC_v2']:.3f}",
        r"\OvarianTableThreeARI": f"{p_mean.loc['ovarian', 'ICC_v2']:.3f}",
    }

    new_num_lines = []
    for line in num_lines:
        matched = False
        for macro, val in macro_updates.items():
            if line.startswith(f"\\newcommand{{{macro[1:]}}}") or line.startswith(f"\\newcommand{{{macro}}}"):
                new_num_lines.append(f"\\newcommand{{{macro}}}{{{val}}}\n")
                matched = True
                break
        if not matched:
            new_num_lines.append(line)

    with open(NUMBERS_TEX, "w", encoding="utf-8") as f:
        f.writelines(new_num_lines)
    with open(PAPER_NUMBERS_TEX, "w", encoding="utf-8") as f:
        f.writelines(new_num_lines)
    print("Updated macros in numbers.tex.")


if __name__ == "__main__":
    main()
