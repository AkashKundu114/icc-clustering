from pathlib import Path
import pandas as pd
import json

df = pd.read_csv("results/passE/inductive_direct_seeds0_9.csv")
p_mean = df.groupby(["dataset", "method"])["ari"].mean().unstack("method")
p_std = df.groupby(["dataset", "method"])["ari"].std().unstack("method")

with open("results/passE/inductive_agreement.json", encoding="utf-8") as f:
    aggr = json.load(f)

# Datasets in Table 2 order
dsets = ["cns", "colon", "leukemia", "ovarian", "srbct", "isolet"]
dnames = {"cns": "CNS", "colon": "Colon", "leukemia": "Leukemia", "ovarian": "Ovarian", "srbct": "SRBCT", "isolet": "Isolet"}

table2_rows = []
for d in dsets:
    km_m, km_s = p_mean.loc[d, "KMeans_Direct"], p_std.loc[d, "KMeans_Direct"]
    wt_m, wt_s = p_mean.loc[d, "ICC_v2_CentroidFull"], p_std.loc[d, "ICC_v2_CentroidFull"]
    uw_m, uw_s = p_mean.loc[d, "ICC_v2_Pseudo_NearestCentroid"], p_std.loc[d, "ICC_v2_Pseudo_NearestCentroid"]
    rf_m, rf_s = p_mean.loc[d, "ICC_v2_Pseudo_RandomForest"], p_std.loc[d, "ICC_v2_Pseudo_RandomForest"]
    ny_m, ny_s = p_mean.loc[d, "ICC_v2_NystromSubspace"], p_std.loc[d, "ICC_v2_NystromSubspace"]

    # find best mean
    vals = [km_m, wt_m, uw_m, rf_m, ny_m]
    best_val = max(vals)

    def fmt(m, s, is_best):
        s_str = f"{m:+.3f} \\pm {s:.3f}"
        return f"$\\mathbf{{{s_str}}}$" if is_best else f"${s_str}$"

    row = f"{dnames[d]} & {fmt(km_m, km_s, km_m==best_val)} & {fmt(wt_m, wt_s, wt_m==best_val)} & {fmt(uw_m, uw_s, uw_m==best_val)} & {fmt(rf_m, rf_s, rf_m==best_val)} & {fmt(ny_m, ny_s, ny_m==best_val)} \\\\"
    table2_rows.append(row)

table2_latex = "\n".join(table2_rows)
print("Generated Table 2 rows:")
print(table2_latex)

# Read main.tex
main_path = Path("springer_manuscript/main.tex")
main_text = main_path.read_text(encoding="utf-8")

t_start = main_text.find(r"\begin{table}[!t]" + "\n" + r"\caption{Empirical Adjusted Rand Index (ARI)")
t_end = main_text.find(r"\end{table}", t_start) + len(r"\end{table}")

new_table2 = f"""\\begin{{table}}[!t]
\\caption{{Empirical Adjusted Rand Index (ARI) on Held-Out Test Splits ($20\\%$, Mean $\\pm$ Standard Deviation Across 10 Canonical Seeds)}}
\\label{{tab:inductive_direct}}
\\centering
\\tiny
\\setlength{{\\tabcolsep}}{{2.0pt}}
\\begin{{tabular}}{{@{{}}lccccc@{{}}}}
\\toprule
\\textbf{{Dataset}} & \\textbf{{Ambient KM}} & \\shortstack{{\\textbf{{Weighted Centroid}}\\\\\\textbf{{(Eqs.~6--7)}}}} & \\shortstack{{\\textbf{{Unweighted Near.}}\\\\\\textbf{{Centroid (Eq.~7)}}}} & \\textbf{{Rand. Forest}} & \\textbf{{Nystr\\"om Ext.}} \\\\
\\midrule
{table2_latex}
\\bottomrule
\\end{{tabular}}
\\end{{table}}"""

main_text = main_text[:t_start] + new_table2 + main_text[t_end:]
main_path.write_text(main_text, encoding="utf-8")
print("[OK] Successfully updated main.tex with Table 2!")

# Update numbers.tex
num_path = Path("springer_manuscript/numbers.tex")
num_text = num_path.read_text(encoding="utf-8")

num_text = num_text.replace(r"\newcommand{\InductiveLeukemiaNystromARI}{0.714}", r"\newcommand{\InductiveLeukemiaNystromARI}{0.296}")
num_text = num_text.replace(r"\newcommand{\InductiveLeukemiaKmDirectARI}{0.172}", r"\newcommand{\InductiveLeukemiaKmDirectARI}{0.146}")
num_text = num_text.replace(r"\newcommand{\InductiveSrbctNystromARI}{0.455}", r"\newcommand{\InductiveSrbctNystromARI}{0.367}")
num_text = num_text.replace(r"\newcommand{\InductiveSrbctKmDirectARI}{0.083}", r"\newcommand{\InductiveSrbctKmDirectARI}{0.033}")

num_path.write_text(num_text, encoding="utf-8")
print("[OK] Successfully updated numbers.tex with Table 2 macros!")
