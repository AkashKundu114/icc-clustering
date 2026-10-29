"""
scripts/make_stability_outputs.py

Generates:
1. paper/gen/table_real_data_stability.tex
2. springer_manuscript/gen/table_real_data_stability.tex
3. paper/figures/fig_real_data_stability.png
4. springer_manuscript/figures/fig_real_data_stability.png

Directly computes metrics from saved label vectors in results/stability/labels/.
"""

import sys
from pathlib import Path
from itertools import combinations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn.metrics import adjusted_rand_score

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from icc.datasets.registry import load_dataset
from scripts.run_real_data_stability import (
    HIGH_D_DATASETS,
    OTHER_DATASETS,
    ALL_DATASETS,
    DISPLAY_NAMES,
    LABELS_DIR,
    get_seeds,
)

MODELS = [
    "K-Means",
    "Ward",
    "Spectral",
    "FCM",
    "Standard_Consensus",
    "Core_Halo_Consensus",
    "FCAG",
    "FastMVC",
    "CoHiRF",
    "Ungated_Anchor",
    "GAC_Pipeline",
]

MODEL_DISPLAY = {
    "K-Means": "K-Means",
    "Ward": "Ward",
    "Spectral": "Spectral",
    "FCM": "FCM",
    "Standard_Consensus": "StdCons",
    "Core_Halo_Consensus": "CoreHalo",
    "FCAG": "FCAG",
    "FastMVC": "FastMVC",
    "CoHiRF": "CoHiRF",
    "Ungated_Anchor": "Ungated AC",
    "GAC_Pipeline": "GAC (Ours)",
}

MODEL_COLORS = {
    "K-Means": "#1f77b4",
    "Ward": "#7f7f7f",
    "Spectral": "#17becf",
    "FCM": "#e377c2",
    "Standard_Consensus": "#3366cc",
    "Core_Halo_Consensus": "#ff7f0e",
    "FCAG": "#bcbd22",
    "FastMVC": "#8c564b",
    "CoHiRF": "#9467bd",
    "Ungated_Anchor": "#2ca02c",
    "GAC_Pipeline": "#d62728",
}


def load_all_metrics():
    records = []
    for d in ALL_DATASETS:
        seeds = get_seeds(d)
        # Check if dataset has labels
        test_file = LABELS_DIR / f"{d}_K-Means_seed_0.npy"
        if not test_file.exists():
            continue

        X, y, _ = load_dataset(d)
        for m in MODELS:
            labels_list = []
            for s in seeds:
                fpath = LABELS_DIR / f"{d}_{m}_seed_{s}.npy"
                if fpath.exists():
                    labels_list.append(np.load(fpath))
            if len(labels_list) < len(seeds):
                continue

            aris = [adjusted_rand_score(y, pred) for pred in labels_list]
            mean_ari = float(np.mean(aris))
            std_ari = float(np.std(aris, ddof=1)) if len(aris) > 1 else 0.0

            pair_aris = [
                adjusted_rand_score(labels_list[i], labels_list[j])
                for i, j in combinations(range(len(labels_list)), 2)
            ]
            stab = float(np.mean(pair_aris)) if len(pair_aris) > 0 else 1.0
            gap = stab - mean_ari

            records.append({
                "dataset": d,
                "dataset_display": DISPLAY_NAMES.get(d, d),
                "is_high_d": d in HIGH_D_DATASETS,
                "N": X.shape[0],
                "D": X.shape[1],
                "model": m,
                "model_display": MODEL_DISPLAY.get(m, m),
                "ARI": mean_ari,
                "std_ARI": std_ari,
                "Stability": stab,
                "Gap": gap,
            })
    return pd.DataFrame(records)


def generate_latex_table(df: pd.DataFrame):
    high_df = df[df["is_high_d"]].copy()
    if high_df.empty:
        print("[!] No high-D data to generate table.")
        return

    # Pivot table for High-D cohorts: rows = models, columns = datasets
    datasets = [d for d in HIGH_D_DATASETS if d in high_df["dataset"].unique()]

    header_cols = []
    for d in datasets:
        d_name = DISPLAY_NAMES[d]
        d_val = high_df[high_df["dataset"] == d]["D"].iloc[0]
        header_cols.append(f"\\multicolumn{{3}}{{c}}{{\\textbf{{{d_name}}} ($D={d_val}$)}}")

    cmidrules = " ".join([f"\\cmidrule(lr){{{2+3*i}-{4+3*i}}}" for i in range(len(datasets))])

    lines = [
        r"\begin{table*}[!t]",
        r"\caption{Real-Data Stability-Accuracy Gap on Biomedical Cohorts ($D/N > 20$, 30 Seeds). "
        r"Reports Empirical Accuracy ($\overline{\text{ARI}}$), Seed Stability (Mean Pairwise ARI Across Seeds, $\text{Stab}$), "
        r"and the Gap ($\Delta = \text{Stab} - \overline{\text{ARI}}$). Values with $\text{Stab} \ge 0.50$ and $\overline{\text{ARI}} \le 0.05$ "
        r"denote the severe ``Stable but Wrong'' pathology where algorithms converge with high agreement on spurious noise partitions.}",
        r"\label{tab:real_data_stability}",
        r"\centering",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{@{}l" + "ccc" * len(datasets) + r"@{}}",
        r"\toprule",
        r"\textbf{Model} & " + " & ".join(header_cols) + r" \\",
        cmidrules,
        r" & " + " & ".join([r"\textbf{ARI} & \textbf{Stab} & \textbf{Gap}" for _ in datasets]) + r" \\",
        r"\midrule",
    ]

    for m in MODELS:
        m_disp = MODEL_DISPLAY[m]
        row_strs = [f"\\textbf{{{m_disp}}}" if "GAC" in m_disp else m_disp]
        for d in datasets:
            sub = high_df[(high_df["dataset"] == d) & (high_df["model"] == m)]
            if sub.empty:
                row_strs.extend(["--", "--", "--"])
                continue
            ari_val = sub["ARI"].iloc[0]
            stab_val = sub["Stability"].iloc[0]
            gap_val = sub["Gap"].iloc[0]

            # Bold if stable but wrong
            is_trap = (stab_val >= 0.50 and ari_val <= 0.05)
            sign = "+" if gap_val >= 0 else "-"
            gap_str = f"${sign}{abs(gap_val):.3f}$"
            if is_trap:
                gap_str = f"$\\mathbf{{{sign}{abs(gap_val):.3f}}}$"

            ari_sign = "+" if ari_val >= 0 else "-"
            row_strs.append(f"${ari_sign}{abs(ari_val):.3f}$")
            row_strs.append(f"${stab_val:.3f}$")
            row_strs.append(gap_str)
        lines.append(" & ".join(row_strs) + r" \\")

    lines.extend([
        r"\bottomrule",
        r"\end{tabular}%",
        r"}",
        r"\end{table*}",
    ])

    out_tex = ROOT / "paper" / "gen" / "table_real_data_stability.tex"
    out_tex.parent.mkdir(parents=True, exist_ok=True)
    out_tex.write_text("\n".join(lines), encoding="utf-8")

    out_springer = ROOT / "springer_manuscript" / "gen" / "table_real_data_stability.tex"
    out_springer.parent.mkdir(parents=True, exist_ok=True)
    out_springer.write_text("\n".join(lines), encoding="utf-8")
    print(f"[+] Saved LaTeX table to: {out_tex} and {out_springer}")


def generate_figure(df: pd.DataFrame):
    high_df = df[df["is_high_d"]].copy()
    if high_df.empty:
        return

    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5), dpi=300)

    # Panel (a): Stability vs ARI Scatter with Pathology Quadrant
    for m in MODELS:
        sub = high_df[high_df["model"] == m]
        if sub.empty:
            continue
        c = MODEL_COLORS.get(m, "#333333")
        m_disp = MODEL_DISPLAY[m]
        marker = "*" if "GAC" in m else "o" if "Consensus" in m else "s"
        size = 140 if "GAC" in m else 80
        zorder = 5 if "GAC" in m else 3

        ax1.scatter(
            sub["ARI"],
            sub["Stability"],
            color=c,
            label=m_disp,
            s=size,
            marker=marker,
            alpha=0.85,
            edgecolors="black",
            linewidths=0.8,
            zorder=zorder,
        )

    # Shaded "Stable but Wrong" Zone
    ax1.axvspan(-0.15, 0.08, ymin=0.5, ymax=1.05, color="#ffdddd", alpha=0.35, zorder=1)
    ax1.text(
        -0.03,
        0.85,
        "STABLE BUT WRONG\nPATHOLOGY ZONE\n(High Stability, Near-Zero ARI)",
        fontsize=10.5,
        fontweight="bold",
        color="#cc0000",
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff5f5", edgecolor="#cc0000", alpha=0.9),
    )

    # Diagonal reference: Stability = ARI
    ax1.plot([-0.1, 0.7], [-0.1, 0.7], "--", color="gray", linewidth=1.5, alpha=0.7, label=r"Perfect Alignment ($\text{Stab} = \text{ARI}$)")

    ax1.set_xlim(-0.12, 0.68)
    ax1.set_ylim(-0.05, 1.05)
    ax1.set_xlabel(r"Empirical Clustering Accuracy ($\overline{\text{ARI}}$ vs. Ground Truth)", fontsize=12, fontweight="bold")
    ax1.set_ylabel(r"Seed Stability (Mean Pairwise ARI Across Seeds)", fontsize=12, fontweight="bold")
    ax1.set_title(r"(a) Real-Data Stability vs. Accuracy Across 6 High-$D$ Cohorts ($D/N > 20$)", fontsize=13, fontweight="bold")
    ax1.legend(loc="lower right", fontsize=8.5, ncol=2, framealpha=0.95)

    # Panel (b): Stability-Accuracy Gap (Bar chart grouped by Model)
    # Average gap per model across the 6 high-D datasets
    gap_summary = high_df.groupby("model").agg(
        mean_gap=("Gap", "mean"),
        std_gap=("Gap", "std"),
        mean_ari=("ARI", "mean"),
        mean_stab=("Stability", "mean"),
    ).loc[[m for m in MODELS if m in high_df["model"].unique()]]

    x = np.arange(len(gap_summary))
    bars = ax2.bar(
        x,
        gap_summary["mean_gap"],
        yerr=gap_summary["std_gap"],
        capsize=4,
        color=[MODEL_COLORS.get(m, "#555555") for m in gap_summary.index],
        edgecolor="black",
        linewidth=0.8,
        alpha=0.85,
    )

    ax2.set_xticks(x)
    ax2.set_xticklabels([MODEL_DISPLAY[m] for m in gap_summary.index], rotation=35, ha="right", fontsize=10, fontweight="bold")
    ax2.set_ylabel(r"Stability$-$Accuracy Gap ($\Delta = \text{Stability} - \overline{\text{ARI}}$)", fontsize=12, fontweight="bold")
    ax2.set_title(r"(b) Mean Stability$-$Accuracy Gap Across High-$D$ Noise Regimes", fontsize=13, fontweight="bold")
    ax2.axhline(0, color="black", linestyle="-", linewidth=1.0)
    ax2.grid(True, linestyle=":", alpha=0.6)

    # Annotations
    for bar, gap in zip(bars, gap_summary["mean_gap"]):
        y_pos = gap + 0.03 if gap >= 0 else gap - 0.06
        ax2.text(bar.get_x() + bar.get_width() / 2, y_pos, f"{gap:+.2f}", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    plt.tight_layout()
    out_fig1 = ROOT / "paper" / "figures" / "fig_real_data_stability.png"
    out_fig1.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_fig1, dpi=300, bbox_inches="tight")

    out_fig2 = ROOT / "springer_manuscript" / "figures" / "fig_real_data_stability.png"
    out_fig2.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_fig2, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved figure to: {out_fig1} and {out_fig2}")


def main():
    print("[*] Generating Real-Data Stability Table and Figure...")
    df = load_all_metrics()
    if df.empty:
        print("[!] No metrics found.")
        return
    print(f"[*] Loaded {len(df)} records across {df['dataset'].nunique()} datasets.")
    out_csv = ROOT / "results" / "stability" / "real_data_stability_summary.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    print(f"[+] Saved stability summary CSV to: {out_csv}")
    generate_latex_table(df)
    generate_figure(df)
    print("[+] Done.")


if __name__ == "__main__":
    main()
