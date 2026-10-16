from pathlib import Path
import pandas as pd
import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "experiments" / "exp3_real_world_benchmarks" / "data"
DEST_TEX = ROOT_DIR / "manuscript" / "supplementary_tables.tex"

def format_cell(mean_val, std_val=None, is_best=False):
    """Format numeric table cell."""
    if np.isnan(mean_val):
        return "--"
    txt = f"{mean_val:.3f}"
    if is_best:
        txt = f"\\textbf{{{txt}}}"
    return txt

def generate_metric_table(df_raw, metric_name, caption, label):
    """Generate LaTeX tabular string for given evaluation metric."""
    piv = df_raw.groupby(["dataset", "model"])[metric_name].mean().unstack("model")
    model_order = [
        "K-Means", "Ward", "Spectral", "FCM",
        "Standard_Consensus", "Li_et_al_2019",
        "DEC", "FCAG", "FastMVC",
        "ICC_v1", "ICC_v2"
    ]
    cols = [m for m in model_order if m in piv.columns]
    piv = piv[cols]

    lines = []
    lines.append("\\begin{table*}[!t]")
    lines.append(f"\\caption{{{caption}}}")
    lines.append(f"\\label{{{label}}}")
    lines.append("\\centering")
    lines.append("\\scriptsize")
    lines.append("\\setlength{\\tabcolsep}{3.5pt}")
    col_spec = "l" + "c" * len(cols)
    lines.append(f"\\begin{{tabular}}{{{col_spec}}}")
    lines.append("\\toprule")
    
    header = "Dataset & " + " & ".join([c.replace("_", " ") for c in cols]) + " \\\\"
    lines.append(header)
    lines.append("\\midrule")

    for ds, row in piv.iterrows():
        best_val = row.max()
        cells = [ds.capitalize()]
        for col in cols:
            val = row[col]
            is_best = (val == best_val and not np.isnan(val))
            cells.append(format_cell(val, is_best=is_best))
        lines.append(" & ".join(cells) + " \\\\")

    lines.append("\\midrule")
    mean_row = piv.mean(axis=0)
    best_mean = mean_row.max()
    mean_cells = ["\\textbf{Grand Mean}"]
    for col in cols:
        val = mean_row[col]
        is_best = (val == best_mean)
        mean_cells.append(format_cell(val, is_best=is_best))
    lines.append(" & ".join(mean_cells) + " \\\\")

    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append("\\end{table*}")
    lines.append("\n")

    return "\n".join(lines)

def main():
    """Main execution entry point."""
    csv_path = DATA_DIR / "exp3_1_benchmark_matrix_v2.csv"
    if not csv_path.exists():
        return

    df = pd.read_csv(csv_path)

    metrics = [
        ("ari", "Adjusted Rand Index (ARI) Across 13 Datasets and 11 Methods", "tab:supp_ari"),
        ("nmi", "Normalized Mutual Information (NMI) Across 13 Datasets and 11 Methods", "tab:supp_nmi"),
        ("ami", "Adjusted Mutual Information (AMI) Across 13 Datasets and 11 Methods", "tab:supp_ami"),
        ("v_measure", "V-Measure (Homogeneity-Completeness Harmonic Mean) Across 13 Datasets", "tab:supp_v_measure"),
        ("fm_index", "Fowlkes-Mallows Index (FM-Index) Across 13 Datasets", "tab:supp_fm_index"),
        ("runtime", "Wall-Clock Runtime (Seconds) Across 13 Datasets and 11 Methods", "tab:supp_runtime"),
    ]

    out_chunks = []

    for metric, caption, label in metrics:
        if metric in df.columns:
            tex_table = generate_metric_table(df, metric, caption, label)
            out_chunks.append(tex_table)

    DEST_TEX.parent.mkdir(parents=True, exist_ok=True)
    DEST_TEX.write_text("\n".join(out_chunks), encoding="utf-8")

if __name__ == "__main__":
    main()
