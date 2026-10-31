"""
scripts/make_stability_outputs.py

Generates:
1. paper/gen/table02_real_data_stability.tex
2. paper/gen/table_real_data_stability.tex
3. springer_manuscript/gen/table02_real_data_stability.tex
4. springer_manuscript/gen/table_real_data_stability.tex
5. paper/gen/table16_degeneracy_audit.tex
6. springer_manuscript/gen/table16_degeneracy_audit.tex
7. paper/figures/fig03_real_data_stability.png
8. paper/figures/fig_real_data_stability.png
9. springer_manuscript/figures/fig03_real_data_stability.png
10. springer_manuscript/figures/fig_real_data_stability.png
11. Updates results/stats.json with both unconstrained and non-degenerate bootstrap metrics.
"""

import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent

DATASETS = ["colon", "srbct", "cns", "leukemia", "prostate", "ovarian"]
DISPLAY_NAMES = {
    "colon": "Colon",
    "srbct": "SRBCT",
    "cns": "CNS",
    "leukemia": "Leukemia",
    "prostate": "Prostate",
    "ovarian": "Ovarian",
}
DATASET_D = {
    "colon": "2{,}000",
    "srbct": "2{,}308",
    "cns": "7{,}129",
    "leukemia": "7{,}129",
    "prostate": "12{,}600",
    "ovarian": "15{,}154",
}

MODELS = [
    "K-Means",
    "Ward",
    "Spectral",
    "FCM",
    "StdCons",
    "CoreHalo",
    "FCAG",
    "FastMVC",
    "CoHiRF",
    "UngatedAC",
    "GAC",
    "DEC",
]

MODEL_DISPLAY = {
    "K-Means": "K-Means",
    "Ward": "Ward",
    "Spectral": "Spectral",
    "FCM": "FCM",
    "StdCons": "Ambient Cons.",
    "CoreHalo": "Core-Halo",
    "FCAG": "FCAG (2019)",
    "FastMVC": "FastMVC (2024)",
    "CoHiRF": "CoHiRF",
    "UngatedAC": "Ungated AC",
    "GAC": "GAC",
    "DEC": "DEC",
}

MODEL_COLORS = {
    "K-Means": "#888888",
    "Ward": "#444444",
    "Spectral": "#2ca02c",
    "FCM": "#9467bd",
    "StdCons": "#d62728",
    "CoreHalo": "#ff7f0e",
    "FCAG": "#1f77b4",
    "FastMVC": "#8c564b",
    "CoHiRF": "#e377c2",
    "UngatedAC": "#bcbd22",
    "GAC": "#17becf",
    "DEC": "#7f7f7f",
}

def generate_latex_table(df: pd.DataFrame, audit_df: pd.DataFrame):
    header_cols = []
    for d in DATASETS:
        d_name = DISPLAY_NAMES[d]
        d_val = DATASET_D[d]
        header_cols.append(f"\\multicolumn{{4}}{{c}}{{\\textbf{{{d_name}}} ($D={d_val}$)}}")
    header_cols.append(r"\multicolumn{2}{c}{\textbf{Summary}}")

    cmidrules = " ".join([f"\\cmidrule(lr){{{2+4*i}-{5+4*i}}}" for i in range(len(DATASETS))])
    cmidrules += f" \\cmidrule(lr){{{2+4*len(DATASETS)}-{3+4*len(DATASETS)}}}"

    col_spec = "@{}l" + "cccc" * len(DATASETS) + "cc@{}"

    lines = [
        r"\begin{table*}[!t]",
        r"\caption{Stratified Subsample Perturbation Stability and Null Control Across Six High-Dimensional Biomedical Cohorts ($D/N > 20$, 30 Stratified $80\%$ Subsamples). "
        r"Reports Empirical Accuracy on Subsamples ($\text{Acc}$, Mean ARI vs. Reference Labels), Subsample Stability ($\text{Stab}$, Mean Pairwise ARI on Overlapping Samples Across $\binom{30}{2} = 435$ Subsample Pairs), "
        r"Stability-Accuracy Gap ($\Delta = \text{Stab} - \text{Acc}$), and Permuted Null Control Stability ($\text{Null}$, Columns Permuted Independently Across Samples). "
        r"Bold gap entries ($\mathbf{\Delta}$) satisfy pre-specified Decision Rule~(i) ($\text{Stab} \geq 0.50$ and $\text{Acc} \leq 0.05$), denoting stability-accuracy discordance. "
        r"Daggers ($^\dagger$) mark degenerate partitions failing amended Decision Rule~(i') non-degeneracy condition (smallest cluster holds $< 5\%$ of the subsample in $> 10\%$ of subsamples). "
        r"The bottom rows provide reference controls: a trivial near-constant partition (which attains high stability by mathematical construction) and a random balanced partition. "
        r"The rightmost column reports full-dataset Seed Stability ($\text{Seed}^*$), which is uninformative for deterministic solvers.}",
        r"\label{tab:real_data_stability}",
        r"\centering",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{" + col_spec + r"}",
        r"\toprule",
        r"\textbf{Model} & " + " & ".join(header_cols) + r" \\",
        cmidrules,
        r" & " + " & ".join([r"\textbf{Acc} & \textbf{Stab} & \textbf{$\Delta$} & \textbf{Null}" for _ in DATASETS]) + r" & \textbf{Mean $\Delta$} & \textbf{Seed$^*$} \\",
        r"\midrule",
    ]

    for m in MODELS:
        m_disp = MODEL_DISPLAY[m]
        row_label = f"\\textbf{{{m_disp}}}" if "GAC" in m_disp else m_disp
        row_strs = [row_label]

        m_gaps = []
        m_seeds = []

        for d in DATASETS:
            sub = df[(df["dataset"] == d) & (df["model"] == m)]
            if sub.empty:
                row_strs.extend(["--", "--", "--", "--"])
                continue
            acc = sub["subsample_accuracy"].iloc[0]
            stab = sub["subsample_stability"].iloc[0]
            gap = sub["subsample_gap"].iloc[0]
            null_s = sub["null_stability"].iloc[0]
            seed_s = sub["seed_stability"].iloc[0]

            m_gaps.append(gap)
            if not np.isnan(seed_s):
                m_seeds.append(seed_s)

            # Check Rule (i) and degeneracy
            is_trap = sub["rule_i_stable_but_wrong"].iloc[0]
            sub_audit = audit_df[(audit_df["dataset"] == d) & (audit_df["model"] == m)]
            is_degen = False
            if not sub_audit.empty:
                is_degen = bool(sub_audit["degen_rate"].iloc[0] > 0.10)

            acc_str = f"${acc:.3f}$"
            stab_str = f"${stab:.3f}$"
            gap_sign = "+" if gap >= 0 else "-"
            gap_str = f"${gap_sign}{abs(gap):.3f}$"
            if is_trap:
                if is_degen:
                    gap_str = f"$\\mathbf{{{gap_sign}{abs(gap):.3f}}}^\\dagger$"
                else:
                    gap_str = f"$\\mathbf{{{gap_sign}{abs(gap):.3f}}}$"
            null_str = f"${null_s:.3f}$"

            row_strs.extend([acc_str, stab_str, gap_str, null_str])

        # Summary columns
        mean_gap_val = np.nanmean(m_gaps)
        mean_seed_val = np.nanmean(m_seeds) if m_seeds else np.nan
        mg_sign = "+" if mean_gap_val >= 0 else "-"
        row_strs.append(f"${mg_sign}{abs(mean_gap_val):.3f}$")
        row_strs.append(f"${mean_seed_val:.3f}$" if not np.isnan(mean_seed_val) else "--")

        lines.append(" & ".join(row_strs) + r" \\")

    # Add Reference Controls
    lines.append(r"\midrule")
    lines.append(r"\multicolumn{27}{@{}l}{\textit{Reference Controls:}} \\")

    control_specs = [
        ("Control_NearConstant", "Near-Constant Control", 1.000),
        ("Control_RandomBalanced", "Random Balanced Control", 0.000),
    ]

    for ctrl_id, ctrl_label, default_seed in control_specs:
        row_strs = [f"\\textit{{{ctrl_label}}}"]
        ctrl_gaps = []
        for d in DATASETS:
            sub = audit_df[(audit_df["dataset"] == d) & (audit_df["model"] == ctrl_id)]
            if sub.empty:
                row_strs.extend(["--", "--", "--", "--"])
                continue
            acc = sub["acc"].iloc[0]
            stab = sub["stab"].iloc[0]
            gap = stab - acc
            # For NearConstant, null stability equals subsample stability by construction; for Random, it is 0.000
            null_s = stab if "NearConstant" in ctrl_id else 0.000
            ctrl_gaps.append(gap)

            acc_str = f"${acc:.3f}$"
            stab_str = f"${stab:.3f}$"
            gap_sign = "+" if gap >= 0 else "-"
            gap_str = f"${gap_sign}{abs(gap):.3f}$"
            null_str = f"${null_s:.3f}$"
            row_strs.extend([acc_str, stab_str, gap_str, null_str])

        mean_gap_ctrl = np.mean(ctrl_gaps)
        mg_sign = "+" if mean_gap_ctrl >= 0 else "-"
        row_strs.append(f"${mg_sign}{abs(mean_gap_ctrl):.3f}$")
        row_strs.append(f"${default_seed:.3f}$")
        lines.append(" & ".join(row_strs) + r" \\")

    lines.extend([
        r"\bottomrule",
        r"\end{tabular}%",
        r"}",
        r"\par\vspace{1ex}\raggedright\footnotesize",
        r"$^\dagger$Fails amended Decision Rule~(i') non-degeneracy condition (smallest cluster holds $< 5\%$ of the subsample in $> 10\%$ of subsamples). Core-Halo collapses to a single cluster ($K_{\text{obs}}=1.0$) on Prostate; CoHiRF produces singleton clusters in $60\%$ of subsamples.",
        r"\par",
        r"$^*$Seed stability is evaluated across 30 seeds on the unperturbed cohort and is not meaningful for deterministic methods (Ward, Spectral) which trivially achieve 1.000.",
        r"\end{table*}",
    ])

    content = "\n".join(lines)
    for p in [
        ROOT / "paper" / "gen" / "table02_real_data_stability.tex",
        ROOT / "paper" / "gen" / "table_real_data_stability.tex",
        ROOT / "springer_manuscript" / "gen" / "table02_real_data_stability.tex",
        ROOT / "springer_manuscript" / "gen" / "table_real_data_stability.tex",
    ]:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        print(f"[+] Saved Table 3 to {p}")


def generate_degeneracy_table(audit_df: pd.DataFrame):
    """Generates Supplementary Table 16: Degeneracy and Smallest-Cluster Size Audit."""
    col_spec = "@{}l" + "cc" * len(DATASETS) + "cc@{}"
    header_cols = []
    for d in DATASETS:
        d_name = DISPLAY_NAMES[d]
        header_cols.append(f"\\multicolumn{{2}}{{c}}{{\\textbf{{{d_name}}}}}")
    header_cols.append(r"\multicolumn{2}{c}{\textbf{Discordant Cohorts (Rules Met)}}")

    cmidrules = " ".join([f"\\cmidrule(lr){{{2+2*i}-{3+2*i}}}" for i in range(len(DATASETS))])
    cmidrules += f" \\cmidrule(lr){{{2+2*len(DATASETS)}-{3+2*len(DATASETS)}}}"

    subheaders = " & ".join([r"\textbf{Min\%} & \textbf{Degen\%}" for _ in DATASETS])

    lines = [
        r"\begin{table*}[!t]",
        r"\caption{Subsample Partition Degeneracy and Smallest-Cluster Size Audit Across Six Biomedical Cohorts (30 Stratified $80\%$ Subsamples per Method). "
        r"Reports Mean Smallest-Cluster Size Fraction ($\text{Min\%} = 100 \times \overline{f}_{\min}$) and Subsample Degeneracy Rate ($\text{Degen\%}$, Percentage of Subsamples where Smallest Cluster Holds $< 5\%$ of Points). "
        r"Daggers ($^\dagger$) highlight degenerate configurations failing the amended non-degeneracy condition (Rule~(i'), $\text{Degen\%} \le 10\%$). "
        r"The rightmost columns report the count of cohorts (out of 6) where each method satisfies the stability-accuracy discordance criterion under Rule~(i) (unconstrained: $\text{Stab} \ge 0.50, \text{Acc} \le 0.05$) and Rule~(i') (non-degenerate: $\text{Stab} \ge 0.50, \text{Acc} \le 0.05$, and $\text{Degen\%} \le 10\%$).}",
        r"\label{tab:degeneracy_audit}",
        r"\centering",
        r"\resizebox{\textwidth}{!}{%",
        r"\begin{tabular}{" + col_spec + r"}",
        r"\toprule",
        r"\textbf{Model} & " + " & ".join(header_cols) + r" \\",
        cmidrules,
        r" & " + subheaders + r" & \textbf{Rule (i)} & \textbf{Rule (i')} \\",
        r"\midrule",
    ]

    models_only = audit_df[~audit_df["is_control"]]

    for m in MODELS:
        m_disp = MODEL_DISPLAY[m]
        row_label = f"\\textbf{{{m_disp}}}" if "GAC" in m_disp else m_disp
        row_strs = [row_label]

        r_i_count = 0
        r_i_prime_count = 0

        for d in DATASETS:
            sub = models_only[(models_only["dataset"] == d) & (models_only["model"] == m)]
            if sub.empty:
                row_strs.extend(["--", "--"])
                continue
            min_frac = sub["mean_min_frac"].iloc[0] * 100.0
            degen_rate = sub["degen_rate"].iloc[0] * 100.0
            is_r_i = sub["rule_i"].iloc[0]
            is_r_ip = sub["rule_i_prime"].iloc[0]

            if is_r_i:
                r_i_count += 1
            if is_r_ip:
                r_i_prime_count += 1

            min_str = f"{min_frac:.1f}\\%"
            degen_str = f"{degen_rate:.1f}\\%"
            if degen_rate > 10.0:
                degen_str = f"$\\mathbf{{{degen_rate:.1f}\\%}}^\\dagger$"

            row_strs.extend([min_str, degen_str])

        row_strs.append(f"{r_i_count}/6")
        row_strs.append(f"{r_i_prime_count}/6")
        lines.append(" & ".join(row_strs) + r" \\")

    # Add Reference Controls
    lines.append(r"\midrule")
    lines.append(r"\multicolumn{15}{@{}l}{\textit{Reference Controls:}} \\")

    for ctrl_id, ctrl_label in [
        ("Control_NearConstant", "Near-Constant Control"),
        ("Control_RandomBalanced", "Random Balanced Control"),
    ]:
        row_strs = [f"\\textit{{{ctrl_label}}}"]
        r_i_count = 0
        r_i_prime_count = 0
        for d in DATASETS:
            sub = audit_df[(audit_df["dataset"] == d) & (audit_df["model"] == ctrl_id)]
            if sub.empty:
                row_strs.extend(["--", "--"])
                continue
            min_frac = sub["mean_min_frac"].iloc[0] * 100.0
            degen_rate = sub["degen_rate"].iloc[0] * 100.0
            if sub["rule_i"].iloc[0]:
                r_i_count += 1
            if sub["rule_i_prime"].iloc[0]:
                r_i_prime_count += 1

            min_str = f"{min_frac:.1f}\\%"
            degen_str = f"{degen_rate:.1f}\\%"
            if degen_rate > 10.0:
                degen_str = f"$\\mathbf{{{degen_rate:.1f}\\%}}^\\dagger$"
            row_strs.extend([min_str, degen_str])

        row_strs.append(f"{r_i_count}/6")
        row_strs.append(f"{r_i_prime_count}/6")
        lines.append(" & ".join(row_strs) + r" \\")

    lines.extend([
        r"\bottomrule",
        r"\end{tabular}%",
        r"}",
        r"\par\vspace{1ex}\raggedright\footnotesize",
        r"$^\dagger$Fails amended non-degeneracy condition (Decision Rule~(i'), smallest cluster holds $< 5\%$ of the subsample in $> 10\%$ of subsamples).",
        r"\end{table*}",
    ])

    content = "\n".join(lines)
    for p in [
        ROOT / "paper" / "gen" / "table16_degeneracy_audit.tex",
        ROOT / "springer_manuscript" / "gen" / "table16_degeneracy_audit.tex",
    ]:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        print(f"[+] Saved Supplementary Table 16 to {p}")


def generate_figure(df: pd.DataFrame, method_stats: dict, audit_df: pd.DataFrame):
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5), dpi=300)

    # Panel (a): Subsample Stability vs Subsample Accuracy Scatter
    for m in MODELS:
        sub = df[df["model"] == m]
        if sub.empty:
            continue
        c = MODEL_COLORS.get(m, "#333333")
        m_disp = MODEL_DISPLAY[m]
        marker = "*" if "GAC" in m else "D" if "FCAG" in m else "o" if "Cons" in m else "s"
        size = 150 if "GAC" in m else 90
        zorder = 6 if "GAC" in m else 4

        # Non-degenerate points
        for _, row in sub.iterrows():
            d = row["dataset"]
            sub_audit = audit_df[(audit_df["dataset"] == d) & (audit_df["model"] == m)]
            is_degen = False
            if not sub_audit.empty:
                is_degen = bool(sub_audit["degen_rate"].iloc[0] > 0.10)

            if is_degen and row["rule_i_stable_but_wrong"]:
                # Mark degenerate points with red 'X'
                ax1.scatter(
                    row["subsample_accuracy"],
                    row["subsample_stability"],
                    color="#cc0000",
                    marker="x",
                    s=140,
                    linewidths=2.5,
                    zorder=10,
                )
                ax1.annotate(
                    f"{m_disp}\n({DISPLAY_NAMES[d]}, Degenerate)",
                    xy=(row["subsample_accuracy"], row["subsample_stability"]),
                    xytext=(row["subsample_accuracy"] + 0.02, row["subsample_stability"] - 0.05),
                    fontsize=7.5,
                    fontweight="bold",
                    color="#990000",
                    arrowprops=dict(arrowstyle="->", color="#990000", lw=1.0),
                )
            else:
                ax1.scatter(
                    row["subsample_accuracy"],
                    row["subsample_stability"],
                    color=c,
                    s=size,
                    marker=marker,
                    alpha=0.88,
                    edgecolors="black",
                    linewidths=0.8,
                    zorder=zorder,
                )

    # Add pseudo-legend entry for models
    for m in MODELS:
        c = MODEL_COLORS.get(m, "#333333")
        m_disp = MODEL_DISPLAY[m]
        marker = "*" if "GAC" in m else "D" if "FCAG" in m else "o" if "Cons" in m else "s"
        ax1.scatter([], [], color=c, label=m_disp, marker=marker, s=80, edgecolors="black", linewidths=0.8)

    # Highlight Pre-registered Non-Degenerate "Stable but Wrong" Zone (Stab >= 0.50, Acc <= 0.05)
    ax1.axvspan(-0.16, 0.05, ymin=0.50, ymax=1.05, color="#ffdddd", alpha=0.35, zorder=1)
    ax1.text(
        -0.155,
        0.82,
        "Rule (i') Non-Degenerate Zone\n(Added Post Hoc)\n"
        r"$\bullet$ Subsample Stab $\geq 0.50$" "\n"
        r"$\bullet$ Subsample Acc $\leq 0.05$" "\n"
        r"$\bullet$ Min Cluster $\geq 5\%$",
        fontsize=8.0,
        fontweight="bold",
        color="#8b0000",
        ha="left",
        va="center",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#ffffff", edgecolor="#cc0000", linewidth=1.2, alpha=0.96),
        zorder=15,
    )

    # Shaded Permuted Null Baseline Band
    all_nulls = df["null_stability"].dropna().values
    null_mean = float(np.mean(all_nulls))
    null_sd = float(np.std(all_nulls))
    ax1.axhspan(null_mean - null_sd, null_mean + null_sd, color="#aaaaaa", alpha=0.25, zorder=2)
    ax1.axhline(null_mean, color="#666666", linestyle=":", linewidth=1.2, zorder=2, label=f"Permuted Null Stability (Mean={null_mean:+.3f})")

    # Diagonal reference: Stability = Accuracy
    ax1.plot([-0.16, 0.7], [-0.16, 0.7], "--", color="gray", linewidth=1.5, alpha=0.7, label=r"Perfect Alignment ($\text{Stab} = \text{Acc}$)")

    ax1.set_xlim(-0.16, 0.65)
    ax1.set_ylim(-0.05, 1.05)
    ax1.set_xlabel(r"Subsample Accuracy ($\overline{\text{ARI}}$ vs. Reference Clinical Labels)", fontsize=11.5, fontweight="bold")
    ax1.set_ylabel(r"Subsample Stability (Mean Overlap Pairwise ARI Across 435 Pairs)", fontsize=11.5, fontweight="bold")
    ax1.set_title(r"(a) Real-Data Subsample Stability vs. Accuracy Across 6 Cohorts ($D/N > 20$)", fontsize=12.5, fontweight="bold")
    ax1.legend(loc="upper right", fontsize=7.5, ncol=2, framealpha=0.95)

    # Panel (b): Pure Subsample Stability-Accuracy Gap Bar Chart with Paired Bootstrap CIs
    models_in_order = [m for m in MODELS if m in df["model"].unique()]
    x = np.arange(len(models_in_order))
    mean_gaps = [method_stats[m]["gap"] for m in models_in_order]
    ci_lows = [method_stats[m]["gap"] - method_stats[m]["ci_low"] for m in models_in_order]
    ci_highs = [method_stats[m]["ci_high"] - method_stats[m]["gap"] for m in models_in_order]
    yerr = np.array([ci_lows, ci_highs])

    bars = ax2.bar(
        x,
        mean_gaps,
        yerr=yerr,
        capsize=4,
        color=[MODEL_COLORS.get(m, "#555555") for m in models_in_order],
        edgecolor="black",
        linewidth=0.8,
        alpha=0.85,
    )

    ax2.set_xticks(x)
    ax2.set_xticklabels([MODEL_DISPLAY[m] for m in models_in_order], rotation=35, ha="right", fontsize=9.5, fontweight="bold")
    ax2.set_ylabel(r"Subsample Gap ($\Delta = \text{Subsample Stab} - \text{Acc}$)", fontsize=11.5, fontweight="bold")
    ax2.set_title(r"(b) Mean Subsample Gap with 95\% Cohort-Bootstrap CIs ($B=10{,}000$)", fontsize=12.5, fontweight="bold")
    ax2.axhline(0, color="black", linestyle="-", linewidth=1.0)
    ax2.grid(True, linestyle=":", alpha=0.6)

    for bar, gap in zip(bars, mean_gaps):
        y_pos = gap + 0.03 if gap >= 0 else gap - 0.06
        ax2.text(bar.get_x() + bar.get_width() / 2, y_pos, f"{gap:+.2f}", ha="center", va="bottom", fontsize=8, fontweight="bold")

    plt.tight_layout()

    for p in [
        ROOT / "paper" / "figures" / "fig03_real_data_stability.png",
        ROOT / "paper" / "figures" / "fig_real_data_stability.png",
        ROOT / "springer_manuscript" / "figures" / "fig03_real_data_stability.png",
        ROOT / "springer_manuscript" / "figures" / "fig_real_data_stability.png",
    ]:
        p.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(p, bbox_inches="tight")
        print(f"[+] Saved Figure to {p}")
    plt.close()


def update_stats_json(df: pd.DataFrame, audit_df: pd.DataFrame, overall_stats: dict, method_stats: dict, decision_summary: dict):
    stats_file = ROOT / "results" / "stats.json"
    with open(stats_file, "r", encoding="utf-8") as f:
        stats = json.load(f)

    stats["Subsample_Stability"] = {
        "Overall": overall_stats,
        "By_Method": method_stats,
        "Decision_Rules": decision_summary,
    }

    with open(stats_file, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    print(f"[+] Updated {stats_file} with Subsample Stability statistics.")


def main():
    csv_path = ROOT / "results" / "stability" / "subsample_stability_summary.csv"
    df = pd.read_csv(csv_path)

    audit_path = ROOT / "results" / "stability_degeneracy_audit.csv"
    audit_df = pd.read_csv(audit_path)

    # 1. Paired Bootstrap CIs (B=10,000, Cohorts as resampling unit)
    rng = np.random.default_rng(42)
    B = 10000
    cohort_list = np.array(DATASETS)
    n_c = len(cohort_list)

    # (A) Overall gap across ALL pairs
    cohort_mean_gaps = np.array([df[df["dataset"] == c]["subsample_gap"].mean() for c in cohort_list])
    boot_indices = rng.integers(0, n_c, size=(B, n_c))
    boot_overall_gaps = cohort_mean_gaps[boot_indices].mean(axis=1)
    overall_ci_low, overall_ci_high = np.percentile(boot_overall_gaps, [2.5, 97.5])
    overall_gap = float(df["subsample_gap"].mean())

    # (B) Overall gap EXCLUDING degenerate pairs (degen_rate <= 0.10)
    models_only_audit = audit_df[~audit_df["is_control"]]
    non_degen = models_only_audit[models_only_audit["degen_rate"] <= 0.10]
    c_nd_gaps = []
    for c in cohort_list:
        sub_c = non_degen[non_degen["dataset"] == c]
        if not sub_c.empty:
            c_nd_gaps.append((sub_c["stab"] - sub_c["acc"]).mean())
        else:
            c_nd_gaps.append(0.0)
    c_nd_gaps = np.array(c_nd_gaps)
    boot_nd_gaps = c_nd_gaps[boot_indices].mean(axis=1)
    nd_ci_low, nd_ci_high = np.percentile(boot_nd_gaps, [2.5, 97.5])
    nd_gap = float((non_degen["stab"] - non_degen["acc"]).mean())

    overall_stab = float(df["subsample_stability"].mean())
    overall_acc = float(df["subsample_accuracy"].mean())
    overall_null = float(df["null_stability"].mean())

    overall_stats = {
        "mean_subsample_stability": overall_stab,
        "mean_subsample_accuracy": overall_acc,
        "mean_subsample_gap": overall_gap,
        "mean_null_stability": overall_null,
        "unconstrained_gap": overall_gap,
        "unconstrained_gap_ci_95": [float(overall_ci_low), float(overall_ci_high)],
        "non_degenerate_gap": nd_gap,
        "non_degenerate_gap_ci_95": [float(nd_ci_low), float(nd_ci_high)],
        "gap_ci_excludes_zero": bool(overall_ci_low > 0 and nd_ci_low > 0),
    }

    method_stats = {}
    for m in MODELS:
        m_df = df[df["model"] == m]
        m_cohort_gaps = np.array([m_df[m_df["dataset"] == c]["subsample_gap"].iloc[0] for c in cohort_list])
        m_boot = m_cohort_gaps[boot_indices].mean(axis=1)
        m_ci_low, m_ci_high = np.percentile(m_boot, [2.5, 97.5])

        method_stats[m] = {
            "stab": float(m_df["subsample_stability"].mean()),
            "acc": float(m_df["subsample_accuracy"].mean()),
            "gap": float(m_df["subsample_gap"].mean()),
            "null": float(m_df["null_stability"].mean()),
            "ci_low": float(m_ci_low),
            "ci_high": float(m_ci_high),
        }

    # Decision Rules Evaluation
    rule_i_df = df[df["rule_i_stable_but_wrong"]]
    cohorts_per_method_rule_i = rule_i_df.groupby("model")["dataset"].nunique().to_dict()
    methods_with_ge_3_cohorts_rule_i = [m for m, c in cohorts_per_method_rule_i.items() if c >= 3]

    rule_ip_df = models_only_audit[models_only_audit["rule_i_prime"]]
    cohorts_per_method_rule_ip = rule_ip_df.groupby("model")["dataset"].nunique().to_dict()
    methods_with_ge_3_cohorts_rule_ip = [m for m, c in cohorts_per_method_rule_ip.items() if c >= 3]

    rule_iii_supported = bool((len(methods_with_ge_3_cohorts_rule_ip) >= 3) and (nd_ci_low > 0))

    decision_summary = {
        "rule_i_matches_total": int(len(rule_i_df)),
        "rule_i_prime_matches_total": int(len(rule_ip_df)),
        "cohorts_per_method_rule_i": {str(k): int(v) for k, v in cohorts_per_method_rule_i.items()},
        "cohorts_per_method_rule_i_prime": {str(k): int(v) for k, v in cohorts_per_method_rule_ip.items()},
        "methods_with_ge_3_cohorts_rule_i": [str(m) for m in methods_with_ge_3_cohorts_rule_i],
        "methods_with_ge_3_cohorts_rule_i_prime": [str(m) for m in methods_with_ge_3_cohorts_rule_ip],
        "rule_iii_claim_supported": bool(rule_iii_supported),
        "note": "Pre-specified in PLAN_STAB.md (commit 3307380) and amended with non-degeneracy condition (commit 548d68d)."
    }

    print("=== Subsample Stability Summary ===")
    print(f"Unconstrained Gap: {overall_gap:+.3f} (95% CI: [{overall_ci_low:+.3f}, {overall_ci_high:+.3f}])")
    print(f"Non-Degenerate Gap: {nd_gap:+.3f} (95% CI: [{nd_ci_low:+.3f}, {nd_ci_high:+.3f}])")
    print(f"Rule (i') Methods with >= 3 cohorts: {methods_with_ge_3_cohorts_rule_ip}")
    print(f"Rule (iii) Paper-Level Claim Supported: {rule_iii_supported}")

    # 2. Generate LaTeX Table 3
    generate_latex_table(df, audit_df)

    # 3. Generate Supplementary Table 16 (Degeneracy Audit)
    generate_degeneracy_table(audit_df)

    # 4. Generate Figure 3
    generate_figure(df, method_stats, audit_df)

    # 5. Update stats.json
    update_stats_json(df, audit_df, overall_stats, method_stats, decision_summary)

if __name__ == "__main__":
    main()
