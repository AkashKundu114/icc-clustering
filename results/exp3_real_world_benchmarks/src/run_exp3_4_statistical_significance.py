"""
Experiment 3.4: Rigorous Statistical Significance Testing (Expanded Benchmark).

Conducts:
1. Non-parametric Friedman Test across 13 multi-domain real-world benchmark datasets.
2. Pairwise post-hoc Wilcoxon Signed-Rank Tests with Holm-Bonferroni correction.
3. Publication Critical Difference (CD) Diagram following Demšar (JMLR 2006) for k=11 models.
"""

import os
import sys
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import friedmanchisquare, wilcoxon

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
FIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "figures")

INPUT_CSV_V2 = os.path.join(DATA_DIR, "exp3_1_benchmark_matrix_v2.csv")
INPUT_CSV_ORIG = os.path.join(DATA_DIR, "exp3_1_benchmark_matrix.csv")

OUTPUT_CSV_V2 = os.path.join(DATA_DIR, "exp3_4_statistical_significance_v2.csv")
FIG_PATH_V2 = os.path.join(FIG_DIR, "fig17_critical_difference_diagram_v2.png")

# Backwards compatible alias
FIG_PATH_ORIG = os.path.join(FIG_DIR, "fig17_critical_difference_diagram.png")


def run_sub_exp3_4(input_csv: Optional[str] = None, output_csv: Optional[str] = None):
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)

    if input_csv is None:
        input_csv = INPUT_CSV_V2 if os.path.exists(INPUT_CSV_V2) else INPUT_CSV_ORIG
    if output_csv is None:
        output_csv = OUTPUT_CSV_V2

    if not os.path.exists(input_csv):
        print(f"[!] Input file {input_csv} not found. Run Exp 3.1 first.")
        return

    df = pd.read_csv(input_csv)

    print("=" * 80)
    print("RUNNING SUB-EXPERIMENT 3.4: STATISTICAL SIGNIFICANCE & CRITICAL DIFFERENCE (V2)")
    print(f"Input: {input_csv} ({len(df)} total records)")
    print("=" * 80)

    # 1. Mean ARI Pivot Table (Datasets x Models)
    pivot = df.groupby(["dataset", "model"])["ari"].mean().unstack()
    datasets = pivot.index.tolist()
    models = pivot.columns.tolist()

    print(f"\nMean ARI across {len(datasets)} Datasets and {len(models)} Models:")
    print(pivot.round(4).to_string())

    # 2. Ranks per dataset (1 = highest ARI)
    ranks = pivot.rank(axis=1, ascending=False)
    mean_ranks = ranks.mean(axis=0).sort_values()
    print(f"\nAverage Ranks across {len(datasets)} Datasets (1 = Best):")
    for m, r in mean_ranks.items():
        print(f"  {m:<22}: {r:.2f}")

    # 3. Friedman Test
    f_stat, f_pval = friedmanchisquare(*[pivot[m].values for m in models])
    print(f"\nFriedman Test: Q = {f_stat:.4f}, p-value = {f_pval:.4e}")
    if f_pval < 0.05:
        print("[+] Rejection of null hypothesis: Statistically significant differences exist among clustering methods (p < 0.05).")

    # 4. Pairwise Wilcoxon Signed-Rank Tests (ICC-v2 vs Competitors)
    records = []
    if "ICC_v2" in pivot.columns:
        icc_scores = pivot["ICC_v2"].values
        competitors = [m for m in models if m != "ICC_v2"]

        for comp in competitors:
            comp_scores = pivot[comp].values
            diff = icc_scores - comp_scores
            if np.all(diff == 0):
                stat, pval = 0.0, 1.0
            else:
                try:
                    res = wilcoxon(icc_scores, comp_scores)
                    stat, pval = res.statistic, res.pvalue
                except Exception:
                    stat, pval = np.nan, 1.0

            records.append({
                "comparison": f"ICC_v2 vs {comp}",
                "competitor": comp,
                "icc_mean_rank": mean_ranks["ICC_v2"],
                "comp_mean_rank": mean_ranks[comp],
                "wilcoxon_stat": stat,
                "raw_p_value": pval,
            })

        # Holm-Bonferroni Correction
        df_wilc = pd.DataFrame(records)
        df_wilc = df_wilc.sort_values("raw_p_value").reset_index(drop=True)
        m_comp = len(df_wilc)
        df_wilc["holm_threshold"] = [0.05 / (m_comp - i) for i in range(m_comp)]
        df_wilc["significant_holm"] = df_wilc["raw_p_value"] < df_wilc["holm_threshold"]

        df_wilc.to_csv(output_csv, index=False)
        print(f"\nPairwise Wilcoxon Signed-Rank Tests vs ICC-v2 (with Holm Correction, m={m_comp}):")
        print(df_wilc[["comparison", "raw_p_value", "holm_threshold", "significant_holm"]].to_string())
        print(f"\n[+] Statistical test results saved to: {output_csv}")

    # 5. Plot Critical Difference Diagram
    plot_fig17_cd_diagram(mean_ranks, n_datasets=len(datasets), save_path=FIG_PATH_V2)
    # Save alias for fig17
    try:
        plot_fig17_cd_diagram(mean_ranks, n_datasets=len(datasets), save_path=FIG_PATH_ORIG)
    except Exception:
        pass


def plot_fig17_cd_diagram(
    mean_ranks: pd.Series,
    n_datasets: int = 13,
    save_path: str = FIG_PATH_V2,
):
    """
    Renders Demšar (JMLR 2006) Critical Difference Diagram and Rank Distribution
    across all evaluated clustering methods.
    """
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 9.5,
        "axes.labelsize": 10.0,
        "axes.titlesize": 11.0,
        "xtick.labelsize": 9.0,
        "ytick.labelsize": 9.0,
        "figure.dpi": 300,
    })

    fig = plt.figure(figsize=(14.5, 5.5), dpi=300)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.45], wspace=0.30)
    ax_bar = fig.add_subplot(gs[0])
    ax_cd = fig.add_subplot(gs[1])

    sorted_models = mean_ranks.index.tolist()
    sorted_r = mean_ranks.values
    k_models = len(sorted_models)

    # -------------------------------------------------------------------------
    # Panel (a): Non-Parametric Rank Order Bar Chart
    # -------------------------------------------------------------------------
    y_pos = np.arange(k_models)
    colors = []
    for m in sorted_models:
        if m == "ICC_v2":
            colors.append("#d62728")
        elif m == "ICC_v1":
            colors.append("#2ca02c")
        elif m in ("FCAG", "FastMVC"):
            colors.append("#8c564b")
        elif m == "DEC":
            colors.append("#9467bd")
        elif "Consensus" in m or "Li" in m:
            colors.append("#1f77b4")
        else:
            colors.append("#6c757d")

    bars = ax_bar.barh(
        y_pos,
        sorted_r,
        color=colors,
        edgecolor="black",
        linewidth=0.8,
        alpha=0.85,
        height=0.65,
    )
    ax_bar.set_yticks(y_pos)
    ax_bar.set_yticklabels(sorted_models, fontweight="bold")
    ax_bar.set_xlabel(f"Average Rank Across {n_datasets} Datasets (1 = Best)", fontweight="bold")
    ax_bar.set_title(f"(a) Average Empirical Rank Distribution across {n_datasets} Benchmarks", fontweight="bold")
    ax_bar.set_xlim(0, max(k_models + 0.5, np.max(sorted_r) + 1.2))
    ax_bar.invert_yaxis()
    ax_bar.grid(axis="x", linestyle=":", alpha=0.5)

    for i, r in enumerate(sorted_r):
        ax_bar.text(r + 0.15, i, f"{r:.2f}", va="center", ha="left", fontweight="bold", fontsize=9.0)

    # -------------------------------------------------------------------------
    # Panel (b): Demšar Critical Difference (CD) Diagram
    # -------------------------------------------------------------------------
    # Demšar (2006) critical values q_0.05 for two-tailed Nemenyi test:
    # k=2: 1.960, k=3: 2.343, k=4: 2.569, k=5: 2.728, k=6: 2.850,
    # k=7: 2.949, k=8: 3.031, k=9: 3.102, k=10: 3.164, k=11: 3.219
    q_alpha_table = {
        2: 1.960, 3: 2.343, 4: 2.569, 5: 2.728, 6: 2.850,
        7: 2.949, 8: 3.031, 9: 3.102, 10: 3.164, 11: 3.219,
    }
    q_val = q_alpha_table.get(k_models, 3.219)

    # CD = q_alpha * sqrt(k * (k + 1) / (6 * N))
    cd = q_val * np.sqrt((k_models * (k_models + 1)) / (6.0 * max(1, n_datasets)))

    ax_cd.set_xlim(-0.5, k_models + 1.5)
    ax_cd.set_ylim(-6.5, 2.5)
    ax_cd.axis("off")

    axis_y = 0.5
    ax_cd.plot([1, k_models], [axis_y, axis_y], color="black", linewidth=1.5)
    for t in range(1, k_models + 1):
        ax_cd.plot([t, t], [axis_y, axis_y + 0.12], color="black", linewidth=1.2)
        ax_cd.text(t, axis_y + 0.22, str(t), ha="center", va="bottom", fontweight="bold", fontsize=9.5)
    ax_cd.text((1 + k_models) / 2.0, axis_y + 0.65, "Average Rank", ha="center", va="bottom", fontweight="bold", fontsize=11)

    # CD interval bar
    cd_start = 1.0
    cd_end = min(k_models, cd_start + cd)
    cd_y = axis_y + 1.35
    ax_cd.plot([cd_start, cd_end], [cd_y, cd_y], color="#d62728", linewidth=2.5)
    ax_cd.plot([cd_start, cd_start], [cd_y - 0.1, cd_y + 0.1], color="#d62728", linewidth=2.0)
    ax_cd.plot([cd_end, cd_end], [cd_y - 0.1, cd_y + 0.1], color="#d62728", linewidth=2.0)
    ax_cd.text(
        (cd_start + cd_end) / 2.0,
        cd_y + 0.15,
        rf"$CD = {cd:.2f}$ (Nemenyi $\alpha=0.05$, $N={n_datasets}$)",
        ha="center",
        va="bottom",
        fontweight="bold",
        color="#d62728",
        fontsize=9.0,
    )

    # Partition models: left side (ranks <= mid), right side (ranks > mid)
    mid_rank = (1 + k_models) / 2.0
    left_models = [(sorted_models[i], sorted_r[i]) for i in range(k_models) if sorted_r[i] <= mid_rank]
    right_models = [(sorted_models[i], sorted_r[i]) for i in range(k_models) if sorted_r[i] > mid_rank]

    # Left side labels
    step_y_left = 4.8 / max(1, len(left_models))
    for idx, (m, r) in enumerate(left_models):
        y_line = axis_y - 0.60 - idx * step_y_left
        c = "#d62728" if m == "ICC_v2" else "#2ca02c" if m == "ICC_v1" else "#495057"
        ax_cd.plot([r, r], [axis_y, y_line], color=c, linewidth=1.2)
        ax_cd.plot([r, 0.30], [y_line, y_line], color=c, linewidth=1.2)
        ax_cd.text(0.20, y_line, f"{m} ({r:.2f})", ha="right", va="center", fontweight="bold", fontsize=9.0, color=c)
        ax_cd.plot(r, axis_y, marker="o", color=c, markersize=5.0)

    # Right side labels
    step_y_right = 4.8 / max(1, len(right_models))
    for idx, (m, r) in enumerate(right_models):
        y_line = axis_y - 0.60 - idx * step_y_right
        c = "#1f77b4" if "Consensus" in m or "Li" in m else "#495057"
        ax_cd.plot([r, r], [axis_y, y_line], color=c, linewidth=1.2)
        ax_cd.plot([r, k_models + 0.70], [y_line, y_line], color=c, linewidth=1.2)
        ax_cd.text(k_models + 0.80, y_line, f"({r:.2f}) {m}", ha="left", va="center", fontweight="bold", fontsize=9.0, color=c)
        ax_cd.plot(r, axis_y, marker="o", color=c, markersize=5.0)

    # Equivalence clique bar connecting methods whose difference <= CD
    clique_y = axis_y - 5.5
    best_rank = sorted_r[0]
    clique_end = min(k_models * 1.0, best_rank + cd)
    ax_cd.plot([best_rank, clique_end], [clique_y, clique_y], color="#343a40", linewidth=3.5, alpha=0.8)
    ax_cd.text(
        (best_rank + clique_end) / 2.0,
        clique_y - 0.35,
        rf"Equivalence Group ($\Delta R \leq CD = {cd:.2f}$)",
        ha="center",
        va="top",
        fontsize=8.5,
        fontstyle="italic",
        color="#343a40",
    )

    ax_cd.set_title(rf"(b) Demšar Critical Difference Diagram ($\alpha=0.05$, $k={k_models}$)", fontweight="bold", fontsize=11.0, pad=10)

    plt.suptitle(
        f"Non-Parametric Model Rankings & Statistical Separation Across {n_datasets} Real-World Benchmarks",
        fontweight="bold",
        fontsize=12.0,
        y=0.99,
    )
    plt.subplots_adjust(top=0.88)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved CD diagram to: {save_path}")


if __name__ == "__main__":
    run_sub_exp3_4()
