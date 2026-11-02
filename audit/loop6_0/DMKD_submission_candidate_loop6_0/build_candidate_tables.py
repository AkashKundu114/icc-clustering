"""Generate candidate tables and statistic macros from Loop 5.9 cell reconstruction.

Input: audit/loop5_9/statistics/cell_reconstruction.csv.
Outputs: aggregate_results.tex, aggregate_macros.tex, cohort_descriptives.csv,
cohort_descriptives.tex, aggregate_results.json. No model fitting occurs.
"""
from pathlib import Path
import csv, json, statistics
HERE=Path(__file__).resolve().parent
INPUT=HERE.parents[2]/"loop5_9"/"statistics"/"cell_reconstruction.csv"
rows=list(csv.DictReader(INPUT.open(encoding="utf-8-sig",newline="")))
required={"dataset","method","mean_stability","mean_external_ari","mean_gap","mean_null_stability"}
if len(rows)!=72 or not required.issubset(rows[0]):
    raise SystemExit(f"Expected 72 rows and required columns in {INPUT}")
cohorts=sorted({r["dataset"] for r in rows})
methods=sorted({r["method"] for r in rows})
if len(cohorts)!=6 or len(methods)!=12:
    raise SystemExit(f"Expected 6 cohorts and 12 methods; got {len(cohorts)}, {len(methods)}")
agg={k:statistics.mean(float(x[k]) for x in rows) for k in ("mean_stability","mean_external_ari","mean_gap","mean_null_stability")}
agg["median_gap"]=statistics.median(float(x["mean_gap"]) for x in rows)
agg.update(n_cells=len(rows),n_datasets=len(cohorts),n_methods=len(methods))
def val(x): return f"{x:.6f}"
macros={"AggStability":agg["mean_stability"],"AggARI":agg["mean_external_ari"],"AggGap":agg["mean_gap"],"AggMedianGap":agg["median_gap"],"AggNull":agg["mean_null_stability"]}
(HERE/"aggregate_macros.tex").write_text("% Generated from "+str(INPUT.as_posix())+"\n"+"".join(f"\\newcommand{{\\{k}}}{{{val(v)}}}\n" for k,v in macros.items()),encoding="utf-8")
(HERE/"aggregate_results.json").write_text(json.dumps({"source":INPUT.as_posix(),"aggregation":"equal-weight arithmetic across 72 cohort-method summaries; median across 72 cell gaps","results":agg},indent=2)+"\n",encoding="utf-8")
with (HERE/"aggregate_results.tex").open("w",encoding="utf-8") as f:
    f.write("% Generated from "+str(INPUT.as_posix())+"\n\\begin{table}[htbp]\n\\centering\n\\caption{Equal-cell descriptive summaries reconstructed from the 72 cohort--method rows.}\n\\label{tab:aggregate}\n\\begin{tabular}{lr}\\toprule\nQuantity & Value \\\\ \\midrule\n")
    for label,key in [("Number of cohort-method cells","n_cells"),("Mean pairwise subsample stability","mean_stability"),("Mean external reference-label ARI","mean_external_ari"),("Mean cell-wise difference (stability $-$ ARI)","mean_gap"),("Median cell-wise difference","median_gap"),("Mean column-permuted null stability","mean_null_stability")]:
        v=str(agg[key]) if key=="n_cells" else val(agg[key])
        f.write(f"{label} & {v} \\\\\n")
    f.write("\\bottomrule\\end{tabular}\n\\end{table}\n")
with (HERE/"cohort_descriptives.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f);w.writerow(["dataset","n_methods","mean_pairwise_subsample_stability","mean_external_ari","descriptive_difference_of_means","source"])
    for ds in cohorts:
        rr=[x for x in rows if x["dataset"]==ds]
        if len(rr)!=12: raise SystemExit(f"Expected 12 cells for {ds}; got {len(rr)}")
        nums=[statistics.mean(float(x[k]) for x in rr) for k in ("mean_stability","mean_external_ari","mean_gap")]
        w.writerow([ds,12,*[f"{x:.12f}" for x in nums],INPUT.as_posix()])
with (HERE/"cohort_descriptives.tex").open("w",encoding="utf-8") as f:
    f.write("% Generated from "+str(INPUT.as_posix())+"\n\\begin{table}[htbp]\n\\centering\n\\caption{Cohort summaries, equally averaging the 12 method-cell summaries within each cohort. Descriptive only.}\n\\label{tab:cohorts}\n\\small\n\\begin{tabular}{lrrr}\\toprule\nCohort & Mean stability & Mean external ARI & Mean cell difference \\\\ \\midrule\n")
    for ds in cohorts:
        rr=[x for x in rows if x["dataset"]==ds]
        nums=[statistics.mean(float(x[k]) for x in rr) for k in ("mean_stability","mean_external_ari","mean_gap")]
        f.write(f"{ds.upper()} & {nums[0]:.3f} & {nums[1]:.3f} & {nums[2]:.3f} \\\\\n")
    f.write("\\bottomrule\\end{tabular}\n\\end{table}\n")
print(f"cells={len(rows)} cohorts={len(cohorts)} methods={len(methods)}; generated candidate tables")
