from pathlib import Path
import pandas as pd
import numpy as np

df = pd.read_csv("results/passE/fair_baselines_seeds0_9.csv")
p = df.groupby(["dataset", "model"])["ari"].agg(["mean", "std"])

dsets = ["cns", "colon", "leukemia", "ovarian", "prostate", "srbct"]
d_info = {
    "cns": "CNS ($60, 7.1\\text{k}, 2$)",
    "colon": "Colon ($62, 2.0\\text{k}, 2$)",
    "leukemia": "Leukemia ($72, 7.1\\text{k}, 2$)",
    "ovarian": "Ovarian ($253, 15.2\\text{k}, 2$)",
    "prostate": "Prostate ($102, 12.6\\text{k}, 2$)",
    "srbct": "SRBCT ($83, 2.3\\text{k}, 4$)"
}

part1_rows = []
for d in dsets:
    km_all_m, km_all_s = p.loc[(d, "K-Means_All"), "mean"], p.loc[(d, "K-Means_All"), "std"]
    km_vf_m, km_vf_s = p.loc[(d, "K-Means_VarFilt"), "mean"], p.loc[(d, "K-Means_VarFilt"), "std"]
    km_pca_m, km_pca_s = p.loc[(d, "K-Means_PCA"), "mean"], p.loc[(d, "K-Means_PCA"), "std"]
    km_ls_m, km_ls_s = p.loc[(d, "K-Means_LapScore"), "mean"], p.loc[(d, "K-Means_LapScore"), "std"]
    skm_m, skm_s = p.loc[(d, "SparseKMeans"), "mean"], p.loc[(d, "SparseKMeans"), "std"]

    b_val = max(km_all_m, km_vf_m, km_pca_m, km_ls_m, skm_m)
    def fmt(m, s, is_b):
        st = f"{m:+.3f} \\pm {s:.3f}"
        return f"$\\mathbf{{{st}}}$" if is_b else f"${st}$"

    row = f"{d_info[d]} & {fmt(km_all_m, km_all_s, km_all_m==b_val)} & {fmt(km_vf_m, km_vf_s, km_vf_m==b_val)} & {fmt(km_pca_m, km_pca_s, km_pca_m==b_val)} & {fmt(km_ls_m, km_ls_s, km_ls_m==b_val)} & {fmt(skm_m, skm_s, skm_m==b_val)} \\\\"
    part1_rows.append(row)

part1_latex = "\n".join(part1_rows)

part2_rows = []
for d in dsets:
    sc_all_m, sc_all_s = p.loc[(d, "StdCons_All"), "mean"], p.loc[(d, "StdCons_All"), "std"]
    sc_vf_m, sc_vf_s = p.loc[(d, "StdCons_VarFilt"), "mean"], p.loc[(d, "StdCons_VarFilt"), "std"]
    sc_pca_m, sc_pca_s = p.loc[(d, "StdCons_PCA"), "mean"], p.loc[(d, "StdCons_PCA"), "std"]
    icc_m, icc_s = p.loc[(d, "ICC_v2"), "mean"], p.loc[(d, "ICC_v2"), "std"]

    b_val = max(sc_all_m, sc_vf_m, sc_pca_m, icc_m)
    def fmt(m, s, is_b):
        st = f"{m:+.3f} \\pm {s:.3f}"
        return f"$\\mathbf{{{st}}}$" if is_b else f"${st}$"

    row = f"{d_info[d]} & {fmt(sc_all_m, sc_all_s, sc_all_m==b_val)} & {fmt(sc_vf_m, sc_vf_s, sc_vf_m==b_val)} & {fmt(sc_pca_m, sc_pca_s, sc_pca_m==b_val)} & {fmt(icc_m, icc_s, icc_m==b_val)} \\\\"
    part2_rows.append(row)

part2_latex = "\n".join(part2_rows)

means = df.groupby("model")["ari"].mean()
print("Subgroup means:")
print(means)

table5_latex = """\\begin{table*}[!t]
\\caption{Fair Feature-Matched Baseline Comparison Across High-Dimensional Regimes ($D/N > 20$, 10 Canonical Seeds, Mean $\\pm$ Standard Deviation ARI)}
\\label{tab:fair_baselines}
\\centering
\\tiny
\\setlength{\\tabcolsep}{2.0pt}

% Block 1: Single-model & feature selection
\\begin{tabular}{@{}lccccc@{}}
\\toprule
\\multicolumn{6}{c}{\\textbf{Part I: Feature-Selected K-Means and Sparse Clustering Baselines}} \\\\
\\midrule
\\textbf{Dataset ($N, D, K$)} & \\shortstack{\\textbf{K-Means}\\\\\\textbf{(Ambient)}} & \\shortstack{\\textbf{K-Means}\\\\\\textbf{(VarFilt)}} & \\shortstack{\\textbf{K-Means}\\\\\\textbf{(PCA)}} & \\shortstack{\\textbf{K-Means}\\\\\\textbf{(LapScore)}} & \\shortstack{\\textbf{Sparse}\\\\\\textbf{K-Means}} \\\\
\\midrule
""" + part1_latex + """
\\midrule
\\textbf{Subgroup Mean ($D/N > 20$)} & """ + f"{means['K-Means_All']:.3f}" + """ & \\FairBaselinesKmVarFiltHighDMean & \\FairBaselinesKmPcaHighDMean & """ + f"{means['K-Means_LapScore']:.3f}" + """ & \\FairBaselinesSparseKmHighDMean \\\\
\\bottomrule
\\end{tabular}

\\vspace{1.0ex}

% Block 2: Consensus variants and ICC-v2
\\begin{tabular}{@{}lcccc@{}}
\\toprule
\\multicolumn{5}{c}{\\textbf{Part II: Feature-Selected Consensus Ensembles and Proposed ICC-v2}} \\\\
\\midrule
\\textbf{Dataset ($N, D, K$)} & \\shortstack{\\textbf{Std Cons}\\\\\\textbf{(Ambient)}} & \\shortstack{\\textbf{Std Cons}\\\\\\textbf{(VarFilt)}} & \\shortstack{\\textbf{Std Cons}\\\\\\textbf{(PCA)}} & \\shortstack{\\textbf{ICC-v2}\\\\\\textbf{(Ours)}} \\\\
\\midrule
""" + part2_latex + """
\\midrule
\\textbf{Subgroup Mean ($D/N > 20$)} & """ + f"{means['StdCons_All']:.3f}" + """ & """ + f"{means['StdCons_VarFilt']:.3f}" + """ & \\FairBaselinesStdConsPcaHighDMean & \\textbf{""" + f"{means['ICC_v2']:.3f}" + """} \\\\
\\bottomrule
\\end{tabular}
\\end{table*}"""

main_path = Path("springer_manuscript/main.tex")
main_text = main_path.read_text(encoding="utf-8")

old_table5_start = "\\begin{table*}[!t]\n\\caption{Fair Feature-Matched Baseline Comparison Across High-Dimensional Regimes"
old_table5_end = "\\end{tabular}\n\\end{table*}"

idx_s = main_text.find(old_table5_start)
idx_e = main_text.find(old_table5_end, idx_s) + len(old_table5_end)
assert idx_s != -1 and idx_e != -1, "Table 5 block not found in main.tex"

main_text = main_text[:idx_s] + table5_latex + main_text[idx_e:]

main_path.write_text(main_text, encoding="utf-8")
print("[OK] Successfully updated main.tex with Table 5!")

# Update numbers.tex
num_path = Path("springer_manuscript/numbers.tex")
num_text = num_path.read_text(encoding="utf-8")

num_text = num_text.replace(r"\newcommand{\FairBaselinesIccVTwoHighDMean}{0.224}", r"\newcommand{\FairBaselinesIccVTwoHighDMean}{0.226}")
num_text = num_text.replace(r"\newcommand{\FairBaselinesIccVTwoHighDMedian}{0.040}", r"\newcommand{\FairBaselinesIccVTwoHighDMedian}{0.051}")
num_text = num_text.replace(r"\newcommand{\FairBaselinesKmVarFiltHighDMean}{0.050}", r"\newcommand{\FairBaselinesKmVarFiltHighDMean}{0.049}")
num_text = num_text.replace(r"\newcommand{\FairBaselinesKmPcaHighDMean}{0.042}", r"\newcommand{\FairBaselinesKmPcaHighDMean}{0.057}")
num_text = num_text.replace(r"\newcommand{\FairBaselinesSparseKmHighDMean}{0.044}", r"\newcommand{\FairBaselinesSparseKmHighDMean}{0.064}")
num_text = num_text.replace(r"\newcommand{\FairBaselinesStdConsPcaHighDMean}{0.036}", r"\newcommand{\FairBaselinesStdConsPcaHighDMean}{0.040}")

num_path.write_text(num_text, encoding="utf-8")
print("[OK] Successfully updated numbers.tex with Table 5 macros!")
