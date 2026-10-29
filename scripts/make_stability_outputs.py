"""
scripts/make_stability_outputs.py

Generates:
1. paper/gen/table_real_data_stability.tex
2. springer_manuscript/gen/table_real_data_stability.tex
3. paper/figures/fig_real_data_stability.png
4. springer_manuscript/figures/fig_real_data_stability.png
5. Updates results/stats.json with pre-registered Item 1 subsample bootstrap metrics.
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
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
    "GAC": "GAC (Ours)",
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

def generate_latex_table(df: pd.DataFrame):
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
        r"Reports Empirical Accuracy on Subsamples ($\text{Acc}$, Mean ARI vs. True Labels), Subsample Stability ($\text{Stab}$, Mean Pairwise ARI on Overlapping Samples Across 435 Subsample Pairs), "
        r"Stability-Accuracy Gap ($\Delta = \text{Stab} - \text{Acc}$), and Permuted Null Control Stability ($\text{Null}$, Columns Permuted Independently Across Samples). "
        r"Bold gap entries ($\mathbf{\Delta}$) satisfy pre-specified Decision Rule~(i) ($\text{Stab} \geq 0.50$ and $\text{Acc} \leq 0.05$), denoting severe `Stable but Wrong' entrapment. "
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

            # Check Rule (i)
            is_trap = sub["rule_i_stable_but_wrong"].iloc[0]

            acc_str = f"${acc:.3f}$"
            stab_str = f"${stab:.3f}$"
            gap_sign = "+" if gap >= 0 else "-"
            gap_str = f"${gap_sign}{abs(gap):.3f}$"
            if is_trap:
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

    lines.extend([
        r"\bottomrule",
        r"\end{tabular}%",
        r"}",
        r"\par\vspace{1ex}\raggedright\footnotesize",
        r"$^*$Seed stability is evaluated across 30 seeds on the unperturbed cohort and is not meaningful for deterministic methods (Ward, Spectral) which trivially achieve 1.000.",
        r"\end{table*}",
    ])

    out_tex = ROOT / "paper" / "gen" / "table_real_data_stability.tex"
    out_tex.parent.mkdir(parents=True, exist_ok=True)
    out_tex.write_text("\n".join(lines), encoding="utf-8")

    out_springer = ROOT / "springer_manuscript" / "gen" / "table_real_data_stability.tex"
    out_springer.parent.mkdir(parents=True, exist_ok=True)
    out_springer.write_text("\n".join(lines), encoding="utf-8")
    print(f"[+] Saved LaTeX tables to {out_tex} and {out_springer}")


def generate_figure(df: pd.DataFrame, method_stats: dict):
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

        ax1.scatter(
            sub["subsample_accuracy"],
            sub["subsample_stability"],
            color=c,
            label=m_disp,
            s=size,
            marker=marker,
            alpha=0.88,
            edgecolors="black",
            linewidths=0.8,
            zorder=zorder,
        )

    # Highlight Pre-registered "Stable but Wrong" Zone (Stab >= 0.50, Acc <= 0.05)
    ax1.axvspan(-0.15, 0.05, ymin=0.50, ymax=1.05, color="#ffdddd", alpha=0.35, zorder=1)
    ax1.text(
        -0.03,
        0.82,
        "PRE-SPECIFIED RULE (i):\nSTABLE BUT WRONG ZONE\n(Subsample Stab $\\geq 0.50$, Acc $\\leq 0.05$)",
        fontsize=9.5,
        fontweight="bold",
        color="#cc0000",
        ha="center",
        va="center",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#fff5f5", edgecolor="#cc0000", alpha=0.9),
    )

    # Shaded Permuted Null Baseline Band (Mean null stability across all runs is ~0.005)
    all_nulls = df["null_stability"].dropna().values
    null_mean = float(np.mean(all_nulls))
    null_sd = float(np.std(all_nulls))
    ax1.axhspan(null_mean - null_sd, null_mean + null_sd, color="#aaaaaa", alpha=0.25, zorder=2)
    ax1.axhline(null_mean, color="#666666", linestyle=":", linewidth=1.2, zorder=2, label=f"Permuted Null Stability (Mean={null_mean:+.3f})")

    # Diagonal reference: Stability = Accuracy
    ax1.plot([-0.1, 0.7], [-0.1, 0.7], "--", color="gray", linewidth=1.5, alpha=0.7, label=r"Perfect Alignment ($\text{Stab} = \text{Acc}$)")

    ax1.set_xlim(-0.10, 0.65)
    ax1.set_ylim(-0.05, 1.05)
    ax1.set_xlabel(r"Subsample Accuracy ($\overline{\text{ARI}}$ vs. True Clinical Labels)", fontsize=11.5, fontweight="bold")
    ax1.set_ylabel(r"Subsample Stability (Mean Overlap Pairwise ARI)", fontsize=11.5, fontweight="bold")
    ax1.set_title(r"(a) Real-Data Subsample Stability vs. Accuracy Across 6 Cohorts ($D/N > 20$)", fontsize=12.5, fontweight="bold")
    ax1.legend(loc="upper right", fontsize=8, ncol=2, framealpha=0.95)

    # Panel (b): Subsample Stability-Accuracy Gap Bar Chart with Paired Bootstrap CIs
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

    out_fig1 = ROOT / "paper" / "figures" / "fig_real_data_stability.png"
    out_fig1.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_fig1, bbox_inches="tight")

    out_fig2 = ROOT / "springer_manuscript" / "figures" / "fig_real_data_stability.png"
    out_fig2.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_fig2, bbox_inches="tight")
    plt.close()
    print(f"[+] Saved Figures to {out_fig1} and {out_fig2}")


def update_stats_json(df: pd.DataFrame, overall_stats: dict, method_stats: dict, decision_summary: dict):
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

    # 1. Compute Paired Bootstrap CIs (B=10,000, Cohorts as resampling unit)
    np.random.seed(42)
    B = 10000
    cohort_list = DATASETS
    n_c = len(cohort_list)

    # Cohort means for overall gap
    cohort_mean_gaps = np.array([df[df["dataset"] == c]["subsample_gap"].mean() for c in cohort_list])
    boot_indices = np.random.randint(0, n_c, size=(B, n_c))
    boot_overall_gaps = cohort_mean_gaps[boot_indices].mean(axis=1)

    overall_ci_low, overall_ci_high = np.percentile(boot_overall_gaps, [2.5, 97.5])
    overall_gap = float(df["subsample_gap"].mean())
    overall_stab = float(df["subsample_stability"].mean())
    overall_acc = float(df["subsample_accuracy"].mean())
    overall_null = float(df["null_stability"].mean())

    overall_stats = {
        "mean_subsample_stability": overall_stab,
        "mean_subsample_accuracy": overall_acc,
        "mean_subsample_gap": overall_gap,
        "mean_null_stability": overall_null,
        "gap_ci_95": [float(overall_ci_low), float(overall_ci_high)],
        "gap_ci_excludes_zero": bool(overall_ci_low > 0),
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
    methods_with_ge_3_cohorts = [m for m, c in cohorts_per_method_rule_i.items() if c >= 3]

    rule_iii_supported = bool((len(methods_with_ge_3_cohorts) >= 3) and (overall_ci_low > 0))

    decision_summary = {
        "rule_i_matches_total": int(len(rule_i_df)),
        "cohorts_per_method_rule_i": {str(k): int(v) for k, v in cohorts_per_method_rule_i.items()},
        "methods_with_ge_3_cohorts": [str(m) for m in methods_with_ge_3_cohorts],
        "rule_iii_claim_supported": bool(rule_iii_supported),
        "note": "Pre-specified in PLAN_STAB.md: supported if >= 3 methods show Rule (i) on >= 3 cohorts and overall gap CI excludes 0."
    }

    print("=== Subsample Stability Summary ===")
    print(f"Overall Gap: {overall_gap:.3f} (95% CI: [{overall_ci_low:.3f}, {overall_ci_high:.3f}])")
    print(f"Rule (iii) Paper-Level Claim Supported: {rule_iii_supported} (Methods: {methods_with_ge_3_cohorts})")

    # 2. Generate LaTeX Table
    generate_latex_table(df)

    # 3. Generate Figure 3
    generate_figure(df, method_stats)

    # 4. Update stats.json
    update_stats_json(df, overall_stats, method_stats, decision_summary)

if __name__ == "__main__":
    main()
