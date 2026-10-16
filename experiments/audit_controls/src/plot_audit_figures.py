"""
Publication Figure Generator for Research Audit & Extended Benchmarks.
Generates:
1. fig27_pool_sensitivity_curve.png (E3: 8 datasets x 7 fractions, BC vs random pool control)
2. fig17_critical_difference_diagram_v2.png (E1: 21-dataset Demšar CD diagram & rank ordering)
3. fig14_benchmark_matrix_21datasets.png (E1: 21-dataset benchmark matrix heatmap)
"""

import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.stats import studentized_range

# Project root
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from icc.viz_style import set_academic_style, clean_spines

set_academic_style()

DATA_DIR = ROOT / "experiments" / "audit_controls" / "data"
FIG_EXP4 = ROOT / "experiments" / "exp4_scalability_and_sensitivity" / "figures"
FIG_EXP3 = ROOT / "experiments" / "exp3_real_world_benchmarks" / "figures"
FIG_IEEE = ROOT / "ieee_manuscript" / "figures"

FIG_EXP4.mkdir(parents=True, exist_ok=True)
FIG_EXP3.mkdir(parents=True, exist_ok=True)
FIG_IEEE.mkdir(parents=True, exist_ok=True)


def plot_fig27_pool_sensitivity_curve():
    """Figure 27: Pool-size sensitivity curve (E3: BC-ranked vs random control)."""
    csv_path = DATA_DIR / "e3_pool_curve.csv"
    if not csv_path.exists():
        print(f"[!] {csv_path} not found")
        return

    df = pd.read_csv(csv_path)

    # 1. Aggregate over datasets
    agg = df.groupby(["frac", "mode", "data"])["ari"].mean().reset_index()
    grand_mean = agg.groupby(["frac", "mode"])["ari"].agg(["mean", "std", "count"]).reset_index()
    grand_mean["sem"] = grand_mean["std"] / np.sqrt(grand_mean["count"])

    fractions = sorted(df["frac"].unique())
    frac_labels = [f"{int(f*100)}%" if f < 1.0 else "100%" for f in fractions]
    x = np.arange(len(fractions))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.0), dpi=300)

    # ---------------------------------------------------------
    # Panel (a): Grand Mean ARI vs Pool Fraction
    # ---------------------------------------------------------
    bc_sub = grand_mean[grand_mean["mode"] == "bc_frac"].set_index("frac").reindex(fractions)
    rnd_sub = grand_mean[grand_mean["mode"] == "random_frac"].set_index("frac").reindex(fractions)

    # Shade the 5% - 15% optimal window
    ax1.axvspan(1, 3, color="#2ca02c", alpha=0.12, label="Optimal Subspace Window (5%–15%)")
    ax1.axvline(3, color="#d62728", linestyle="--", alpha=0.7, linewidth=1.2, label="Legacy 15% Analytical Floor")

    # BC-Ranked Pool
    ax1.errorbar(
        x,
        bc_sub["mean"],
        yerr=bc_sub["sem"],
        marker="o",
        markersize=7,
        linewidth=2.2,
        capsize=4,
        capthick=1.2,
        color="#d62728",
        label="BC-Ranked Subspace Pool",
    )

    # Random Pool Control
    ax1.errorbar(
        x,
        rnd_sub["mean"],
        yerr=rnd_sub["sem"],
        marker="s",
        markersize=6,
        linewidth=1.8,
        linestyle="--",
        capsize=4,
        capthick=1.2,
        color="#1f77b4",
        label="Random Subspace Pool (Control)",
    )

    ax1.set_xticks(x)
    ax1.set_xticklabels(frac_labels, fontweight="bold")
    ax1.set_xlabel("Subspace Pool Fraction of Features ($\\rho = |\\mathcal{P}| / D$)", fontweight="bold")
    ax1.set_ylabel("Cross-Dataset Mean ARI Recovery", fontweight="bold")
    ax1.set_title("(a) Multi-Dataset Pool Fraction Sensitivity vs. Random Control", fontweight="bold", pad=10)
    ax1.grid(True, linestyle=":", alpha=0.5)
    ax1.set_ylim(-0.02, 0.24)
    ax1.legend(loc="upper right", framealpha=0.92, edgecolor="gray")
    clean_spines(ax1)

    # ---------------------------------------------------------
    # Panel (b): Per-Dataset Trajectories
    # ---------------------------------------------------------
    palette = {
        "srbct": "#d62728",
        "leukemia": "#9467bd",
        "colon": "#2ca02c",
        "cns": "#8c564b",
        "prostate": "#ff7f0e",
        "ovarian": "#17becf",
        "sonar": "#7f7f7f",
        "madelon": "#bcbd22",
    }
    names = {
        "srbct": "SRBCT (D=2,308)",
        "leukemia": "Leukemia (D=7,129)",
        "colon": "Colon (D=2,000)",
        "cns": "CNS (D=7,129)",
        "prostate": "Prostate (D=12,600)",
        "ovarian": "Ovarian (D=15,154)",
        "sonar": "Sonar (D=60)",
        "madelon": "Madelon (D=500)",
    }

    piv = agg[agg["mode"] == "bc_frac"].pivot(index="data", columns="frac", values="ari")

    for dname, color in palette.items():
        if dname in piv.index:
            vals = piv.loc[dname, fractions].values
            is_hero = dname in ("srbct", "leukemia", "colon")
            lw = 2.4 if is_hero else 1.2
            alpha = 1.0 if is_hero else 0.55
            ls = "-" if is_hero else ":"
            ax2.plot(
                x,
                vals,
                marker="o" if is_hero else "x",
                markersize=6 if is_hero else 4,
                linewidth=lw,
                alpha=alpha,
                linestyle=ls,
                color=color,
                label=names[dname],
            )

    ax2.axvspan(1, 3, color="#2ca02c", alpha=0.08)
    ax2.axhline(0, color="black", linestyle="-", linewidth=0.8, alpha=0.6)
    ax2.set_xticks(x)
    ax2.set_xticklabels(frac_labels, fontweight="bold")
    ax2.set_xlabel("Subspace Pool Fraction of Features ($\\rho$)", fontweight="bold")
    ax2.set_ylabel("Adjusted Rand Index (ARI)", fontweight="bold")
    ax2.set_title("(b) Domain-Specific Trajectories (Cancer Genomics vs. Sensor Data)", fontweight="bold", pad=10)
    ax2.grid(True, linestyle=":", alpha=0.5)
    ax2.legend(loc="upper right", framealpha=0.92, fontsize=8.5, ncol=2, edgecolor="gray")
    clean_spines(ax2)

    plt.tight_layout()

    out_paths = [
        FIG_EXP4 / "fig27_pool_sensitivity_curve.png",
        FIG_IEEE / "fig27_pool_sensitivity_curve.png",
    ]
    for p in out_paths:
        plt.savefig(p, dpi=300)
        print(f"[+] Saved Figure 27 to: {p}")
    plt.close()


def plot_fig17_critical_difference_21datasets():
    """Figure 17: Demšar Critical Difference Diagram for 21-dataset benchmark."""
    csv_path = DATA_DIR / "e1_extended_summary.csv"
    if not csv_path.exists():
        print(f"[!] {csv_path} not found")
        return

    df = pd.read_csv(csv_path).set_index("dataset")

    # Rename models for presentation
    model_map = {
        "ICC_v2_legacy": "ICC-v2 (Legacy 15%)",
        "ICC_v2_adaptive": "ICC-v2 (Adaptive Pool)",
        "ICC_v1": "ICC-v1 (Anchor Only)",
        "Standard_Consensus": "Standard Consensus",
        "Li_et_al_2019": "Li et al. (2019)",
        "K-Means": "K-Means",
        "Ward": "Ward Linkage",
        "Spectral": "Spectral",
        "FCM": "FCM",
    }
    cols = [c for c in model_map.keys() if c in df.columns]
    data = df[cols].rename(columns=model_map)

    n_datasets = len(data)
    n_models = len(cols)

    # Rank per dataset: 1 = best (highest ARI)
    ranks = data.rank(axis=1, ascending=False)
    mean_ranks = ranks.mean(axis=0).sort_values()

    # Critical Difference using Nemenyi test
    # CD = q_alpha * sqrt(k * (k + 1) / (6 * N))
    # q_alpha for alpha=0.05 at k=9 is approx 3.102
    # Studentized range statistic: q_nemenyi = q_studentized / sqrt(2)
    q_stud = studentized_range.ppf(0.95, n_models, np.inf)
    cd = (q_stud / np.sqrt(2)) * np.sqrt(n_models * (n_models + 1) / (6.0 * n_datasets))

    fig = plt.figure(figsize=(14.5, 5.5), dpi=300)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.45], wspace=0.30)
    ax_bar = fig.add_subplot(gs[0])
    ax_cd = fig.add_subplot(gs[1])

    # ---------------------------------------------------------
    # Panel (a): Mean Rank Order Horizontal Bars
    # ---------------------------------------------------------
    y_pos = np.arange(n_models)
    sorted_models = mean_ranks.index.tolist()
    sorted_r = mean_ranks.values

    colors = []
    for m in sorted_models:
        if "ICC-v2" in m:
            colors.append("#d62728")
        elif "ICC-v1" in m:
            colors.append("#2ca02c")
        elif "Consensus" in m or "Li" in m:
            colors.append("#1f77b4")
        else:
            colors.append("#6c757d")

    bars = ax_bar.barh(y_pos, sorted_r, color=colors, edgecolor="black", linewidth=0.8, alpha=0.85, height=0.65)
    ax_bar.set_yticks(y_pos)
    ax_bar.set_yticklabels(sorted_models, fontweight="bold", fontsize=9.5)
    ax_bar.invert_yaxis()
    ax_bar.set_xlabel(f"Average Rank across {n_datasets} Datasets (1 = Best)", fontweight="bold", fontsize=10.0)
    ax_bar.set_title(f"(a) Non-Parametric Rank Ordering ({n_datasets} Datasets)", fontweight="bold", fontsize=11.0, pad=10)
    ax_bar.grid(axis="x", linestyle=":", alpha=0.5)

    for bar, r in zip(bars, sorted_r):
        ax_bar.text(r + 0.12, bar.get_y() + bar.get_height() / 2, f"{r:.2f}", va="center", ha="left", fontsize=9.0, fontweight="bold")
    ax_bar.set_xlim(0, max(sorted_r) + 1.2)
    clean_spines(ax_bar)

    # ---------------------------------------------------------
    # Panel (b): Demšar Critical Difference Axis
    # ---------------------------------------------------------
    min_rank = 1.0
    max_rank = float(n_models)
    ax_cd.set_xlim(min_rank - 0.5, max_rank + 0.5)
    ax_cd.set_ylim(-0.8, 1.3)
    ax_cd.axhline(0, color="black", linewidth=1.4)

    # Main axis tick marks
    for r in range(1, n_models + 1):
        ax_cd.plot([r, r], [0, 0.05], color="black", linewidth=1.2)
        ax_cd.text(r, 0.12, str(r), ha="center", va="bottom", fontsize=9.5, fontweight="bold")

    # CD interval bar at the top
    cd_start = 1.0
    cd_end = cd_start + cd
    ax_cd.plot([cd_start, cd_end], [0.95, 0.95], color="#d62728", linewidth=2.5)
    ax_cd.plot([cd_start, cd_start], [0.90, 1.00], color="#d62728", linewidth=2.0)
    ax_cd.plot([cd_end, cd_end], [0.90, 1.00], color="#d62728", linewidth=2.0)
    ax_cd.text((cd_start + cd_end) / 2, 1.05, f"Critical Difference (CD = {cd:.2f}, Nemenyi $\\alpha=0.05$)", ha="center", va="bottom", fontsize=9.5, fontweight="bold", color="#d62728")

    # Split models into left and right sides of CD axis
    mid = n_models // 2
    left_models = [(m, mean_ranks[m]) for m in sorted_models[:mid]]
    right_models = [(m, mean_ranks[m]) for m in sorted_models[mid:]]

    y_left = np.linspace(-0.25, -0.75, len(left_models))
    for (m, r), y_l in zip(left_models, y_left):
        ax_cd.plot([r, r, min_rank - 0.2], [0, y_l, y_l], color="#555555", linewidth=0.9, linestyle="--")
        ax_cd.plot(r, 0, marker="o", markersize=6, color="#d62728" if "ICC" in m else "#1f77b4")
        ax_cd.text(min_rank - 0.25, y_l, f"{m} ({r:.2f})", ha="right", va="center", fontsize=8.8, fontweight="bold")

    y_right = np.linspace(-0.25, -0.75, len(right_models))
    for (m, r), y_r in zip(right_models, y_right):
        ax_cd.plot([r, r, max_rank + 0.2], [0, y_r, y_r], color="#555555", linewidth=0.9, linestyle="--")
        ax_cd.plot(r, 0, marker="o", markersize=6, color="#d62728" if "ICC" in m else "#1f77b4")
        ax_cd.text(max_rank + 0.25, y_r, f"({r:.2f}) {m}", ha="left", va="center", fontsize=8.8, fontweight="bold")

    ax_cd.set_axis_off()
    ax_cd.set_title(f"(b) Demšar Critical Difference Diagram (N={n_datasets}, K={n_models})", fontweight="bold", fontsize=11.0, pad=10)

    plt.tight_layout()

    out_paths = [
        FIG_EXP3 / "fig17_critical_difference_diagram_v2.png",
        FIG_EXP3 / "fig17_critical_difference_diagram.png",
        FIG_IEEE / "fig17_critical_difference_diagram_v2.png",
        FIG_IEEE / "fig17_critical_difference_diagram.png",
    ]
    for p in out_paths:
        plt.savefig(p, dpi=300)
        print(f"[+] Saved Figure 17 to: {p}")
    plt.close()


def plot_fig14_benchmark_matrix_21datasets():
    """Figure 14: Heatmap Matrix across 21 multi-domain datasets."""
    csv_path = DATA_DIR / "e1_extended_summary.csv"
    if not csv_path.exists():
        print(f"[!] {csv_path} not found")
        return

    df = pd.read_csv(csv_path).set_index("dataset")

    model_map = {
        "K-Means": "K-Means",
        "Ward": "Ward",
        "Spectral": "Spectral",
        "FCM": "FCM",
        "Standard_Consensus": "Std Cons",
        "Li_et_al_2019": "Li et al.",
        "ICC_v1": "ICC-v1",
        "ICC_v2_legacy": "ICC-v2 (15%)",
        "ICC_v2_adaptive": "ICC-v2 (Adapt)",
    }
    cols = [c for c in model_map.keys() if c in df.columns]
    data = df[cols].rename(columns=model_map)

    # Sort datasets: cancer genomics first, then others
    ds_order = [
        "leukemia", "srbct", "colon", "cns", "prostate", "ovarian", "glioma", "lung_cancer", "lymphoma", "breast_cancer_genomic",
        "sonar", "madelon", "gisette", "waveform", "yale_b", "isolet", "har", "usps", "indian_pines", "newsgroups20", "zheng68k"
    ]
    valid_ds = [d for d in ds_order if d in data.index] + [d for d in data.index if d not in ds_order]
    data = data.loc[valid_ds]

    fig, ax = plt.subplots(figsize=(12.0, 10.5), dpi=300)

    matrix = data.values
    im = ax.imshow(matrix, cmap="YlGnBu", aspect="auto", vmin=-0.05, vmax=0.85)

    ax.set_xticks(np.arange(len(cols)))
    ax.set_yticks(np.arange(len(valid_ds)))
    ax.set_xticklabels([model_map[c] for c in cols], fontweight="bold", fontsize=10.0, rotation=25, ha="right")
    ax.set_yticklabels([d.upper() for d in valid_ds], fontweight="bold", fontsize=9.5)

    # Text annotations in each cell
    for i in range(len(valid_ds)):
        best_val = np.max(matrix[i])
        for j in range(len(cols)):
            val = matrix[i, j]
            is_best = np.isclose(val, best_val, atol=1e-3)
            weight = "bold" if is_best else "normal"
            text_color = "white" if val > 0.45 else ("red" if is_best else "black")
            ax.text(j, i, f"{val:.3f}", ha="center", va="center", color=text_color, fontsize=8.5, fontweight=weight)

    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.03)
    cbar.set_label("Adjusted Rand Index (ARI)", fontweight="bold", fontsize=11.0)
    ax.set_title("Extended Multi-Domain Empirical Benchmark Matrix (21 Datasets $\\times$ 9 Methods)", fontweight="bold", fontsize=13.0, pad=15)

    plt.tight_layout()

    out_paths = [
        FIG_EXP3 / "fig14_benchmark_matrix_21datasets.png",
        FIG_IEEE / "fig14_benchmark_matrix_21datasets.png",
        FIG_IEEE / "fig14_benchmark_matrix_13datasets.png",  # Also update default figure reference
    ]
    for p in out_paths:
        plt.savefig(p, dpi=300)
        print(f"[+] Saved Figure 14 to: {p}")
    plt.close()


def main():
    print("[*] Generating Publication Figures for Audit & Extended Benchmarks...")
    plot_fig27_pool_sensitivity_curve()
    plot_fig17_critical_difference_21datasets()
    plot_fig14_benchmark_matrix_21datasets()
    print("[+] All Figures Generated Successfully!")


if __name__ == "__main__":
    main()
