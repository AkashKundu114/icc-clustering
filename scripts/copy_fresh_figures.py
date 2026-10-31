import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent

src_list = [
    # Fig 2
    (root / "experiments/exp0_falsification/figures/fig02a_ari_stability.png", "fig02a_ari_stability.png"),
    (root / "experiments/exp0_falsification/figures/fig02b_stability_accuracy_gap.png", "fig02b_stability_accuracy_gap.png"),
    (root / "experiments/exp0_falsification/figures/fig02c_noise_distribution_sensitivity.png", "fig02c_noise_distribution_sensitivity.png"),
    (root / "experiments/exp0_falsification/figures/fig02a_ari_stability.png", "fig1_ari_stability.png"),
    (root / "experiments/exp0_falsification/figures/fig02b_stability_accuracy_gap.png", "fig2_gap.png"),
    (root / "experiments/exp0_falsification/figures/fig02c_noise_distribution_sensitivity.png", "fig4_noisetype_heatmap.png"),
    # Fig 4
    (root / "experiments/exp1_generalization/figures/fig9_inductive_generalization.png", "fig04a_inductive_oracle_generalization.png"),
    (root / "experiments/exp1_generalization/figures/fig10_pseudolabel_generalization.png", "fig04b_inductive_pseudolabel_generalization.png"),
    (root / "experiments/exp1_generalization/figures/fig9_inductive_generalization.png", "fig9_inductive_generalization.png"),
    (root / "experiments/exp1_generalization/figures/fig10_pseudolabel_generalization.png", "fig10_pseudolabel_generalization.png"),
    # Fig 7
    (root / "experiments/exp3_real_world_benchmarks/figures/fig14_benchmark_matrix_13datasets.png", "fig07_benchmark_matrix_13datasets.png"),
    (root / "experiments/exp3_real_world_benchmarks/figures/fig14_benchmark_matrix_13datasets.png", "fig14_benchmark_matrix_13datasets.png"),
    # Fig 8
    (root / "experiments/exp3_real_world_benchmarks/figures/fig17_critical_difference_diagram_v2.png", "fig08_critical_difference_diagram.png"),
    (root / "experiments/exp3_real_world_benchmarks/figures/fig17_critical_difference_diagram_v2.png", "fig17_critical_difference_diagram_v2.png"),
    # Fig 9
    (root / "experiments/exp2_ablation/figures/fig11_ablation_curves.png", "fig09a_ablation_curves.png"),
    (root / "experiments/exp2_ablation/figures/fig12_ablation_waterfall.png", "fig09b_ablation_waterfall.png"),
    (root / "experiments/exp2_ablation/figures/fig11_ablation_curves.png", "fig11_ablation_curves.png"),
    (root / "experiments/exp2_ablation/figures/fig12_ablation_waterfall.png", "fig12_ablation_waterfall.png"),
]

dest_dirs = [
    root / "paper/figures",
    root / "springer_manuscript/figures",
    root / "submission/springer_nature_package/figures",
    root / "submission/overleaf_package/figures",
    root / "submission/arxiv_package/figures",
]

for src_path, filename in src_list:
    if not src_path.exists():
        print(f"[!] Source missing: {src_path}")
        continue
    for d in dest_dirs:
        if d.exists():
            dst = d / filename
            shutil.copy2(src_path, dst)
            print(f"Copied {filename} -> {d}")

print("All fresh figures copied successfully.")
