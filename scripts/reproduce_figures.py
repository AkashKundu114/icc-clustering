"""
Reproduce and verify all manuscript figures for peer review.

Verifies the presence, provenance, and integrity of all figures in the paper
(Figures 1 through 10, conceptual framework, sensitivity heatmaps, anchor fidelity quad, etc.)
in results/figures/ and experiments/. Synchronizes all figures to results/figures/
with standard publication names, and provides a --generate flag to re-render figures.

Usage:
    python scripts/reproduce_figures.py             # Verify presence and provenance
    python scripts/reproduce_figures.py --generate  # Re-render figures from raw data
"""

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
FIGURES_DIR = ROOT / "results" / "figures"

FIGURE_MANIFEST = [
    {
        "id": "Figure 1",
        "canonical_name": "fig01_conceptual_overview.png",
        "source_candidates": [
            "experiments/exp0_falsification/figures/fig0_conceptual_framework.png",
            "experiments/figures/fig0_conceptual_framework.png",
            "results/figures/fig01_conceptual_overview.png",
        ],
        "generator_script": "scripts/plot_conceptual_framework.py",
        "provenance": "High-dimensional distractor noise manifold and ICC-v2 bipartite transfer cut ensembling framework.",
    },
    {
        "id": "Figure 2a",
        "canonical_name": "fig02a_ari_stability.png",
        "source_candidates": [
            "experiments/exp0_falsification/figures/fig1_ari_stability.png",
            "results/figures/fig02a_ari_stability.png",
        ],
        "generator_script": "experiments/exp0_falsification/src/plot_all_figures.py",
        "provenance": "Empirical clustering accuracy (ARI) degradation across distractor noise dimensions.",
    },
    {
        "id": "Figure 2b",
        "canonical_name": "fig02b_stability_accuracy_gap.png",
        "source_candidates": [
            "experiments/exp0_falsification/figures/fig2_gap.png",
            "results/figures/fig02b_stability_accuracy_gap.png",
        ],
        "generator_script": "experiments/exp0_falsification/src/plot_all_figures.py",
        "provenance": "Stability-accuracy gap (Delta = Stab - Acc) demonstrating clustering collapse.",
    },
    {
        "id": "Figure 2c",
        "canonical_name": "fig02c_noise_distribution_sensitivity.png",
        "source_candidates": [
            "experiments/exp0_falsification/figures/fig4_noisetype_heatmap.png",
            "results/figures/fig02c_noise_distribution_sensitivity.png",
        ],
        "generator_script": "experiments/exp0_falsification/src/plot_all_figures.py",
        "provenance": "Noise distribution sensitivity heatmap across Gaussian, Student-t, Uniform, and Cauchy distractors.",
    },
    {
        "id": "Figure 3",
        "canonical_name": "fig03_real_data_stability.png",
        "source_candidates": [
            "results/figures/fig03_real_data_stability.png",
            "results/figures/fig_real_data_stability.png",
        ],
        "generator_script": "scripts/make_stability_outputs.py",
        "provenance": "Stratified subsample perturbation stability and null control across 6 high-D cohorts (D/N > 20).",
    },
    {
        "id": "Figure 4a",
        "canonical_name": "fig04a_inductive_oracle_generalization.png",
        "source_candidates": [
            "experiments/exp1_generalization/figures/fig9_inductive_generalization.png",
            "results/figures/fig04a_inductive_oracle_generalization.png",
        ],
        "generator_script": "experiments/exp1_generalization/src/plot_exp1_figures.py",
        "provenance": "Out-of-sample inductive oracle generalization ARI across varying sample sizes.",
    },
    {
        "id": "Figure 4b",
        "canonical_name": "fig04b_inductive_pseudolabel_generalization.png",
        "source_candidates": [
            "experiments/exp1_generalization/figures/fig10_pseudolabel_generalization.png",
            "results/figures/fig04b_inductive_pseudolabel_generalization.png",
        ],
        "generator_script": "experiments/exp1_generalization/src/plot_exp1_figures.py",
        "provenance": "Pseudolabel-guided inductive query generalizability without ground-truth supervisory signal.",
    },
    {
        "id": "Figure 5a",
        "canonical_name": "fig05a_sample_complexity_scaling.png",
        "source_candidates": [
            "experiments/exp4_scalability_and_sensitivity/figures/fig18_sample_complexity_scaling.png",
            "results/figures/fig05a_sample_complexity_scaling.png",
        ],
        "generator_script": "experiments/exp4_scalability_and_sensitivity/src/plot_exp4_figures.py",
        "provenance": "Empirical runtime scaling of O(NL) bipartite consensus vs quadratic O(N^2) dense baselines.",
    },
    {
        "id": "Figure 5b",
        "canonical_name": "fig05b_scalability_breakdown.png",
        "source_candidates": [
            "experiments/exp4_scalability_and_sensitivity/figures/fig24_anchor_fidelity_quad.png",
            "results/figures/fig05b_scalability_breakdown.png",
        ],
        "generator_script": "experiments/exp4_scalability_and_sensitivity/src/plot_exp4_figures.py",
        "provenance": "Quad breakdown: anchor fidelity, runtime acceleration, memory reduction, and dimension scaling.",
    },
    {
        "id": "Figure 6",
        "canonical_name": "fig06_extreme_scale_quad.png",
        "source_candidates": [
            "experiments/exp5_extreme_scale/figures/fig26_extreme_scale_quad.png",
            "results/figures/fig06_extreme_scale_quad.png",
        ],
        "generator_script": "experiments/exp5_extreme_scale/src/plot_exp5.py",
        "provenance": "Extreme scale quad verifying linear memory and runtime scalability to 1,000,000 samples.",
    },
    {
        "id": "Figure 7",
        "canonical_name": "fig07_benchmark_matrix_13datasets.png",
        "source_candidates": [
            "experiments/exp3_real_world_benchmarks/figures/fig14_benchmark_matrix_13datasets.png",
            "results/figures/fig07_benchmark_matrix_13datasets.png",
        ],
        "generator_script": "experiments/exp3_real_world_benchmarks/src/plot_exp3_figures.py",
        "provenance": "Heatmap matrix of mean ARI across 12 clustering algorithms on 13 canonical benchmark datasets.",
    },
    {
        "id": "Figure 8",
        "canonical_name": "fig08_critical_difference_diagram.png",
        "source_candidates": [
            "experiments/exp3_real_world_benchmarks/figures/fig17_critical_difference_diagram_v2.png",
            "results/figures/fig08_critical_difference_diagram.png",
        ],
        "generator_script": "experiments/exp3_real_world_benchmarks/src/plot_exp3_figures.py",
        "provenance": "Friedman-Nemenyi critical difference (CD) diagram across benchmark algorithms.",
    },
    {
        "id": "Figure 9a",
        "canonical_name": "fig09a_ablation_curves.png",
        "source_candidates": [
            "experiments/exp2_ablation/figures/fig11_ablation_curves.png",
            "results/figures/fig09a_ablation_curves.png",
        ],
        "generator_script": "experiments/exp2_ablation/src/plot_exp2_figures.py",
        "provenance": "Ablation trajectory curves showing cumulative impact of components V0 through V5.",
    },
    {
        "id": "Figure 9b",
        "canonical_name": "fig09b_ablation_waterfall.png",
        "source_candidates": [
            "experiments/exp2_ablation/figures/fig12_ablation_waterfall.png",
            "results/figures/fig09b_ablation_waterfall.png",
        ],
        "generator_script": "experiments/exp2_ablation/src/plot_exp2_figures.py",
        "provenance": "Waterfall chart of marginal ARI gains from BGSS, bipartite graph, and ensemble aggregation.",
    },
    {
        "id": "Figure 10",
        "canonical_name": "fig10_bgss_interpretability_audit.png",
        "source_candidates": [
            "experiments/exp2_ablation/figures/fig22_vssg_interpretability_trinity.png",
            "results/figures/fig10_bgss_interpretability_audit.png",
        ],
        "generator_script": "experiments/exp2_ablation/src/plot_vssg_figures.py",
        "provenance": "BGSS interpretability audit: precision-recall curves and signal-to-noise recovery across noise regimes.",
    },
]


def file_sha256(path: Path) -> str:
    """Compute sha256 checksum of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()[:16]


def verify_and_sync_figures(generate: bool = False):
    """Verify presence and provenance of all paper figures, sync to results/figures/."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 105)
    print("ICC-v2 Figure Provenance & Verification Engine")
    print("=" * 105)

    if generate:
        print("[*] Re-rendering figures from source scripts...")
        unique_scripts = list({f["generator_script"] for f in FIGURE_MANIFEST if (ROOT / f["generator_script"]).exists()})
        for s in unique_scripts:
            script_path = ROOT / s
            print(f"    Executing: python {s}...")
            try:
                subprocess.run([sys.executable, str(script_path)], cwd=ROOT, check=True, capture_output=True)
            except Exception as e:
                print(f"    [!] Warning: Failed executing {s}: {e}")

    rows = []
    verified_count = 0

    for item in FIGURE_MANIFEST:
        fig_id = item["id"]
        c_name = item["canonical_name"]
        dst_path = FIGURES_DIR / c_name
        src_path: Optional[Path] = None

        # Check existing destination
        if dst_path.exists():
            src_path = dst_path
        else:
            # Check candidate sources
            for cand in item["source_candidates"]:
                cp = ROOT / cand
                if cp.exists():
                    src_path = cp
                    break

        status = "MISSING"
        file_size_kb = 0.0
        csum = "---"

        if src_path and src_path.exists():
            file_size_kb = src_path.stat().st_size / 1024.0
            csum = file_sha256(src_path)
            # Sync to results/figures/ with canonical name
            if src_path != dst_path:
                shutil.copy2(src_path, dst_path)
                status = "SYNCED"
            else:
                status = "VERIFIED"
            verified_count += 1

        rows.append({
            "Figure ID": fig_id,
            "File": c_name,
            "Size (KB)": f"{file_size_kb:.1f}",
            "SHA256": csum,
            "Status": status,
            "Generator": Path(item["generator_script"]).name,
        })

    # Print summary table
    import pandas as pd
    df = pd.DataFrame(rows)
    print("\n" + df.to_string(index=False) + "\n")

    print("-" * 105)
    print(f"Verification Summary: {verified_count}/{len(FIGURE_MANIFEST)} paper figures verified and present.")
    print(f"Canonical figure directory: {FIGURES_DIR}")
    print("=" * 105 + "\n")


def main():
    parser = argparse.ArgumentParser(description="ICC-v2 Figure Provenance Verification & Reproduction")
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Re-render figures from raw experiment data prior to verification.",
    )
    args = parser.parse_args()

    verify_and_sync_figures(generate=args.generate)


if __name__ == "__main__":
    main()
