"""
Plotting engine for Experiment 1 Suite: Inductive Generalization Tests.
Generates:
- fig9_inductive_generalization.png (True Labels on Sample Subsets)
- fig10_pseudolabel_generalization.png (Unsupervised Pseudo-Labels on Core vs Full)
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Add project root to sys.path
root_dir = Path(__file__).resolve().parents[3]
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from icc.viz_style import set_academic_style, clean_spines

set_academic_style()


def plot_exp1_figures():
    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"
    fig_dir = base_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    set_academic_style()

    # -------------------------------------------------------------------------
    # 1. Inductive Generalization under True Labels
    # -------------------------------------------------------------------------
    gen_csv = data_dir / "exp1_generalization_results.csv"
    if gen_csv.exists():
        df_gen = pd.read_csv(gen_csv)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.0, 5.0), dpi=300)

        ax1.plot(df_gen["d_noise"], df_gen["mean_full_100"], marker="o", color="#1f77b4",
                 linewidth=2.4, markersize=7, label="Full Training Set (100% samples)")
        ax1.plot(df_gen["d_noise"], df_gen["mean_random_50"], marker="s", color="#7f7f7f",
                 linewidth=2.0, linestyle="--", markersize=6, label="Random Subsample (50% control)")
        ax1.plot(df_gen["d_noise"], df_gen["mean_li2019_50"], marker="^", color="#ff7f0e",
                 linewidth=2.2, markersize=7, label="Li et al. (2019) Determinacy Core (50%)")
        ax1.plot(df_gen["d_noise"], df_gen["mean_icc_50"], marker="d", color="#2ca02c",
                 linewidth=2.6, markersize=8, label="Ungated AC Calibrated Core (50%)")

        ax1.set_title(r"(a) Out-of-Sample Generalization on Held-Out Test Set (20%)", fontsize=13.0, fontweight="bold")
        ax1.set_xlabel(r"Nuisance Distractor Dimensions ($D_{\text{noise}}$)", fontsize=12.0, fontweight="bold")
        ax1.set_ylabel("Test Accuracy on Raw Held-Out Data", fontsize=12.0, fontweight="bold")
        ax1.tick_params(labelsize=11.0)
        ax1.set_xscale("symlog", linthresh=10)
        ax1.set_ylim(0.25, 1.05)
        clean_spines(ax1)
        ax1.legend(loc="lower left", fontsize=10.5, framealpha=0.92, facecolor="white", edgecolor="#cccccc")

        # Advantage bar chart
        advantage = df_gen["icc_advantage_over_full"] * 100
        colors = ["#2ca02c" if h >= 0 else "#d95f02" for h in advantage]
        hatches = ["xx" if h >= 0 else "//" for h in advantage]
        bars = ax2.bar(range(len(df_gen)), advantage, color=colors, edgecolor="black", linewidth=0.8,
                       hatch=hatches, alpha=0.88, width=0.55)
        ax2.axhline(0, color="black", linestyle="-", linewidth=0.8)

        for rect in bars:
            h = rect.get_height()
            va = "bottom" if h >= 0 else "top"
            offset = 3 if h >= 0 else -14
            ax2.annotate(f"{h:+.1f}%", xy=(rect.get_x() + rect.get_width() / 2, h),
                         xytext=(0, offset), textcoords="offset points",
                         ha="center", va=va, fontsize=10.0, fontweight="bold")

        ax2.set_xticks(range(len(df_gen)))
        ax2.set_xticklabels([str(d) for d in df_gen["d_noise"]], fontsize=11.0, fontweight="bold")
        ax2.tick_params(axis="y", labelsize=11.0)
        ax2.set_title(r"(b) Sample Complexity Tradeoff: 50% Core vs 100% Full Training Set", fontsize=13.0, fontweight="bold")
        ax2.set_xlabel(r"Nuisance Distractor Dimensions ($D_{\text{noise}}$)", fontsize=12.0, fontweight="bold")
        ax2.set_ylabel("Absolute Test Accuracy Gain (% points)", fontsize=12.0, fontweight="bold")
        ax2.set_ylim(-26, 4)
        clean_spines(ax2)

        plt.tight_layout()
        plt.subplots_adjust(top=0.90)
        plt.suptitle("Downstream Classifier Generalization from Oracle True Labels",
                     fontweight="bold", fontsize=13.0, y=0.98)
        fig9_path = fig_dir / "fig9_inductive_generalization.png"
        plt.savefig(fig9_path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"  [Saved] {fig9_path}")

        # Supplementary NMI & AMI Inductive Generalization
        if "test_nmi" in df_gen.columns:
            fig_supp, (sax1, sax2) = plt.subplots(1, 2, figsize=(14.0, 5.0), dpi=300)
            if "full_test_nmi" in df_gen.columns:
                sax1.plot(df_gen["d_noise"], df_gen["full_test_nmi"], marker="o", color="#1f77b4",
                          linewidth=2.0, markersize=6, label="Full Training Set (100%)")
            if "li_test_nmi" in df_gen.columns:
                sax1.plot(df_gen["d_noise"], df_gen["li_test_nmi"], marker="^", color="#ff7f0e",
                          linewidth=2.0, markersize=6, label="Li et al. (2019) Core (50%)")
            sax1.plot(df_gen["d_noise"], df_gen["test_nmi"], marker="d", color="#2ca02c",
                      linewidth=2.2, markersize=7, label="Ungated AC Calibrated Core (50%)")

            sax1.set_title(r"(a) Held-Out Test NMI Across Noise Dimensions", fontweight="bold")
            sax1.set_xlabel(r"Nuisance Distractor Dimensions ($D_{\text{noise}}$)", fontweight="bold")
            sax1.set_ylabel("Normalized Mutual Information (NMI)", fontweight="bold")
            sax1.set_xscale("symlog", linthresh=10)
            sax1.set_ylim(-0.05, 1.05)
            sax1.grid(True, linestyle=":", alpha=0.5)
            sax1.legend(loc="lower left", framealpha=0.92, facecolor="white", edgecolor="#cccccc")

            if "full_test_ami" in df_gen.columns:
                sax2.plot(df_gen["d_noise"], df_gen["full_test_ami"], marker="o", color="#1f77b4",
                          linewidth=2.0, markersize=6, label="Full Training Set (100%)")
            if "li_test_ami" in df_gen.columns:
                sax2.plot(df_gen["d_noise"], df_gen["li_test_ami"], marker="^", color="#ff7f0e",
                          linewidth=2.0, markersize=6, label="Li et al. (2019) Core (50%)")
            if "test_ami" in df_gen.columns:
                sax2.plot(df_gen["d_noise"], df_gen["test_ami"], marker="d", color="#2ca02c",
                          linewidth=2.2, markersize=7, label="Ungated AC Calibrated Core (50%)")

            sax2.set_title(r"(b) Held-Out Test AMI Across Noise Dimensions", fontweight="bold")
            sax2.set_xlabel(r"Nuisance Distractor Dimensions ($D_{\text{noise}}$)", fontweight="bold")
            sax2.set_ylabel("Adjusted Mutual Information (AMI)", fontweight="bold")
            sax2.set_xscale("symlog", linthresh=10)
            sax2.set_ylim(-0.05, 1.05)
            sax2.grid(True, linestyle=":", alpha=0.5)
            sax2.legend(loc="lower left", framealpha=0.92, facecolor="white", edgecolor="#cccccc")

            plt.suptitle("Supplementary Information-Theoretic Inductive Generalization (NMI/AMI)",
                         fontweight="bold", fontsize=12.0, y=0.99)
            plt.tight_layout()
            fig9_supp_path = fig_dir / "fig9_supp_nmi_inductive_generalization.png"
            plt.savefig(fig9_supp_path, dpi=300, bbox_inches="tight")
            plt.close()
            print(f"  [Saved] {fig9_supp_path}")

    # -------------------------------------------------------------------------
    # 2. Pseudo-Label Inductive Generalization
    # -------------------------------------------------------------------------
    pseudo_csv = data_dir / "exp1_pseudolabel_results.csv"
    if pseudo_csv.exists():
        df_p = pd.read_csv(pseudo_csv)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.0, 5.0), dpi=300)

        ax1.plot(df_p["d_noise"], df_p["test_acc_full_pseudo"], marker="o", color="#1f77b4",
                 linewidth=2.4, markersize=7, label="Train on All Pseudo-Labels (100%)")
        ax1.plot(df_p["d_noise"], df_p["test_acc_core_pseudo"], marker="d", color="#2ca02c",
                 linewidth=2.6, markersize=8, label="Train on Core Pseudo-Labels Only (Ungated AC)")

        ax1.set_title(r"(a) Unsupervised Pseudo-Label Generalization to Test Set", fontsize=13.0, fontweight="bold")
        ax1.set_xlabel(r"Nuisance Distractor Dimensions ($D_{\text{noise}}$)", fontsize=12.0, fontweight="bold")
        ax1.set_ylabel("Test Accuracy on Unseen Test Split", fontsize=12.0, fontweight="bold")
        ax1.tick_params(labelsize=11.0)
        ax1.set_xscale("symlog", linthresh=10)
        ax1.set_ylim(0.20, 0.88)
        ax1.grid(True, linestyle=":", alpha=0.5)
        ax1.legend(loc="upper right", fontsize=10.5, framealpha=0.92, facecolor="white", edgecolor="#cccccc")

        # Advantage bar chart
        p_adv = df_p["core_advantage_acc"] * 100
        colors = ["#2ca02c" if x >= 0 else "#d95f02" for x in p_adv]
        hatches = ["xx" if x >= 0 else "//" for x in p_adv]
        bars2 = ax2.bar(range(len(df_p)), p_adv, color=colors, edgecolor="black", linewidth=0.8,
                        hatch=hatches, alpha=0.88, width=0.55)
        ax2.axhline(0, color="black", linestyle="-", linewidth=0.8)

        for rect in bars2:
            h = rect.get_height()
            va = "bottom" if h >= 0 else "top"
            offset = 3 if h >= 0 else -14
            ax2.annotate(f"{h:+.1f}%", xy=(rect.get_x() + rect.get_width() / 2, h),
                         xytext=(0, offset), textcoords="offset points",
                         ha="center", va=va, fontsize=10.0, fontweight="bold")

        ax2.set_xticks(range(len(df_p)))
        ax2.set_xticklabels([str(d) for d in df_p["d_noise"]], fontsize=11.0, fontweight="bold")
        ax2.tick_params(axis="y", labelsize=11.0)
        ax2.set_title(r"(b) Core Filtering Advantage under Corrupted Pseudo-Labels", fontsize=13.0, fontweight="bold")
        ax2.set_xlabel(r"Nuisance Distractor Dimensions ($D_{\text{noise}}$)", fontsize=12.0, fontweight="bold")
        ax2.set_ylabel("Core Pseudo-Label Gain (% points)", fontsize=12.0, fontweight="bold")
        ax2.set_ylim(-12, 7.0)
        ax2.grid(True, linestyle=":", alpha=0.5, axis="y")

        plt.tight_layout()
        plt.subplots_adjust(top=0.90)
        plt.suptitle("Downstream Generalization from Unsupervised Pseudo-Labels",
                     fontweight="bold", fontsize=13.0, y=0.98)
        fig10_path = fig_dir / "fig10_pseudolabel_generalization.png"
        plt.savefig(fig10_path, dpi=300, bbox_inches="tight")
        for target_dir in [base_dir.parents[1] / "springer_manuscript" / "figures",
                           base_dir.parents[1] / "paper" / "figures",
                           base_dir.parents[1] / "manuscript" / "figures"]:
            if target_dir.exists():
                plt.savefig(target_dir / "fig10_pseudolabel_generalization.png", dpi=300, bbox_inches="tight")
        plt.close()
        print(f"  [Saved] {fig10_path}")

    # -------------------------------------------------------------------------
    # 3. Figure 10b & 10c: Multi-Classifier Pseudo-Label Generalization
    # -------------------------------------------------------------------------
    mc_csv = data_dir / "exp1_multiclassifier_results.csv"
    if mc_csv.exists():
        df_mc = pd.read_csv(mc_csv)

        if "training_set" in df_mc.columns:
            df_full = df_mc[df_mc["training_set"] == "ALL"][["classifier", "d_noise", "trial", "test_accuracy"]].rename(columns={"test_accuracy": "acc_full"})
            df_core = df_mc[df_mc["training_set"] == "CORE"][["classifier", "d_noise", "trial", "test_accuracy"]].rename(columns={"test_accuracy": "acc_core"})
            df_plot = pd.merge(df_full, df_core, on=["classifier", "d_noise", "trial"])
            df_plot["acc_advantage"] = df_plot["acc_core"] - df_plot["acc_full"]
        else:
            df_plot = df_mc

        # Detect classifiers present
        present_clfs = [c for c in ["SVM", "RF", "MLP", "KNN", "DualRidge", "RandomForest"] if c in df_plot["classifier"].unique()]
        if not present_clfs:
            present_clfs = list(df_plot["classifier"].unique())[:4]
        classifiers = present_clfs[:4]
        d_noises = sorted(df_plot["d_noise"].unique())

        display_names = {
            "SVM": "Support Vector Machine (Linear SVM)",
            "RF": "Random Forest (100 Trees)",
            "MLP": "Multi-Layer Perceptron (100, 50)",
            "KNN": "K-Nearest Neighbors (k=5)",
            "DualRidge": "Dual Kernel Ridge / Linear SVM",
            "RandomForest": "Random Forest (100 Trees)",
        }

        # Fig 10b: 4-panel comparison
        fig, axes = plt.subplots(2, 2, figsize=(13.0, 9.0), dpi=300)
        axes = axes.flatten()

        for idx, cname in enumerate(classifiers):
            ax = axes[idx]
            df_c = df_plot[df_plot["classifier"] == cname]
            if df_c.empty:
                continue

            summary = df_c.groupby("d_noise").agg({
                "acc_full": ["mean", "std"],
                "acc_core": ["mean", "std"],
            }).reindex(d_noises)

            m_full = summary["acc_full"]["mean"].values
            s_full = summary["acc_full"]["std"].fillna(0).values
            m_core = summary["acc_core"]["mean"].values
            s_core = summary["acc_core"]["std"].fillna(0).values

            ax.plot(d_noises, m_full, "o--", color="#1f77b4", linewidth=2.0, label="Full Pseudo-Labels (100%)")
            ax.fill_between(d_noises, m_full - s_full, m_full + s_full, color="#1f77b4", alpha=0.12)

            ax.plot(d_noises, m_core, "s-", color="#2ca02c", linewidth=2.2, label="ICC Core Pseudo-Labels [Ours]")
            ax.fill_between(d_noises, m_core - s_core, m_core + s_core, color="#2ca02c", alpha=0.15)

            disp_title = display_names.get(cname, cname)
            ax.set_title(f"({chr(97 + idx)}) {disp_title}", fontweight="bold")
            ax.set_xlabel(r"Nuisance Distractor Dimensions ($D_{\text{noise}}$)", fontweight="bold")
            ax.set_ylabel("Held-Out Test Accuracy", fontweight="bold")
            ax.set_xscale("symlog", linthresh=10)
            ax.set_ylim(0.25, 1.05)
            ax.grid(True, linestyle=":", alpha=0.5)
            ax.legend(loc="lower left", framealpha=0.92)

        plt.suptitle("Downstream Multi-Classifier Inductive Generalization", fontweight="bold", fontsize=13.0)
        plt.tight_layout()
        fig10b_path = fig_dir / "fig10b_multiclassifier_generalization.png"
        plt.savefig(fig10b_path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"  [Saved] {fig10b_path}")

        # Fig 10c: Advantage Heatmap
        fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=300)
        pivot_table = df_plot.groupby(["classifier", "d_noise"])["acc_advantage"].mean().unstack() * 100
        pivot_table = pivot_table.reindex(classifiers)

        im = ax.imshow(pivot_table.values, cmap="RdYlGn", aspect="auto", vmin=-12, vmax=12)
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label("Core Accuracy Advantage (% points)", fontweight="bold")

        ax.set_xticks(range(len(d_noises)))
        ax.set_xticklabels([str(d) for d in d_noises], fontweight="bold")
        ax.set_yticks(range(len(classifiers)))
        ax.set_yticklabels([display_names.get(c, c) for c in classifiers], fontweight="bold")
        ax.set_xlabel(r"Nuisance Distractor Dimensions ($D_{\text{noise}}$)", fontweight="bold")
        ax.set_ylabel("Downstream Classifier", fontweight="bold")
        ax.set_title("Core Filtering Gain Across Classifiers (% Accuracy Delta)", fontweight="bold")

        for r in range(len(classifiers)):
            for c in range(len(d_noises)):
                val = pivot_table.values[r, c]
                if np.isnan(val):
                    continue
                color = "black" if abs(val) < 6 else "white"
                ax.text(c, r, f"{val:+.1f}%", ha="center", va="center", fontweight="bold", color=color, fontsize=10)

        plt.tight_layout()
        fig10c_path = fig_dir / "fig10c_multiclassifier_advantage_heatmap.png"
        plt.savefig(fig10c_path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"  [Saved] {fig10c_path}")


if __name__ == "__main__":
    plot_exp1_figures()
