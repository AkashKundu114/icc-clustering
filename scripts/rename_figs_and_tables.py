"""
Renames figures and tables to professional, sequential Springer Nature submission names
and updates paper/main.tex and springer_manuscript/main.tex synchronously.
"""

import hashlib
import shutil
from pathlib import Path

# Mapping of figure files
FIG_MAP = {
    "figures/fig0_conceptual_framework.png": "figures/fig01_conceptual_overview.png",
    "figures/fig1_ari_stability.png": "figures/fig02a_ari_stability.png",
    "figures/fig2_gap.png": "figures/fig02b_stability_accuracy_gap.png",
    "figures/fig4_noisetype_heatmap.png": "figures/fig02c_noise_distribution_sensitivity.png",
    "figures/fig_real_data_stability.png": "figures/fig03_real_data_stability.png",
    "figures/fig9_inductive_generalization.png": "figures/fig04a_inductive_oracle_generalization.png",
    "figures/fig10_pseudolabel_generalization.png": "figures/fig04b_inductive_pseudolabel_generalization.png",
    "figures/fig18_sample_complexity_scaling.png": "figures/fig05a_sample_complexity_scaling.png",
    "figures/fig24_anchor_fidelity_quad.png": "figures/fig05b_scalability_breakdown.png",
    "figures/fig26_extreme_scale_quad.png": "figures/fig06_extreme_scale_quad.png",
    "figures/fig14_benchmark_matrix_13datasets.png": "figures/fig07_benchmark_matrix_13datasets.png",
    "figures/fig17_critical_difference_diagram_v2.png": "figures/fig08_critical_difference_diagram.png",
    "figures/fig11_ablation_curves.png": "figures/fig09a_ablation_curves.png",
    "figures/fig12_ablation_waterfall.png": "figures/fig09b_ablation_waterfall.png",
    "figures/fig22_vssg_interpretability_trinity.png": "figures/fig10_bgss_interpretability_audit.png",
}

# Mapping of table files
TABLE_MAP = {
    "gen/table_exp8d_distance.tex": "gen/table01_distance_geometries.tex",
    "gen/table_real_data_stability.tex": "gen/table02_real_data_stability.tex",
    "gen/table3_inductive.tex": "gen/table03_inductive_generalization.tex",
    "gen/table4_scaling_n.tex": "gen/table04_sample_scaling.tex",
    "gen/table5_extreme_scaling.tex": "gen/table05_extreme_scaling.tex",
    "gen/table7_omnibus_ari.tex": "gen/table06_omnibus_benchmark_ari.tex",
    "gen/table_exp8e_large_k.tex": "gen/table07_large_k_anchor_budget.tex",
    "gen/table8_matched_budget.tex": "gen/table08_matched_feature_budget.tex",
    "gen/table10_vargha_delaney.tex": "gen/table09_vargha_delaney_effect_sizes.tex",
    "gen/table11_seed_stability.tex": "gen/table10_seed_stability_diagnostics.tex",
    "gen/table13_ablation.tex": "gen/table11_ablation_variants.tex",
    "gen/table14_factorial.tex": "gen/table12_factorial_decomposition.tex",
    "gen/table15_component_contributions.tex": "gen/table13_component_contributions.tex",
    "gen/tableS1_foundational_refs.tex": "gen/table14_supplementary_foundations.tex",
    "gen/table16_case_studies.tex": "gen/table15_case_studies_synthesis.tex",
}


def apply_renames():
    root = Path(__file__).resolve().parent.parent

    # 1. Copy files in paper/ and springer_manuscript/
    print("1. Creating properly named figure files...")
    for old_fig, new_fig in FIG_MAP.items():
        src = root / "paper" / old_fig
        dst_paper = root / "paper" / new_fig
        dst_springer = root / "springer_manuscript" / new_fig
        assert src.exists(), f"Source figure {src} missing!"
        shutil.copy2(src, dst_paper)
        shutil.copy2(src, dst_springer)
        print(f"   {old_fig} -> {new_fig}")

    print("\n2. Creating properly named table files...")
    for old_tab, new_tab in TABLE_MAP.items():
        src = root / "paper" / old_tab
        dst_paper = root / "paper" / new_tab
        dst_springer = root / "springer_manuscript" / new_tab
        assert src.exists(), f"Source table {src} missing!"
        shutil.copy2(src, dst_paper)
        shutil.copy2(src, dst_springer)
        print(f"   {old_tab} -> {new_tab}")

    # 3. Update main.tex in paper/ and springer_manuscript/
    print("\n3. Updating paper/main.tex and springer_manuscript/main.tex...")
    tex = (root / "paper" / "main.tex").read_text(encoding="utf-8")

    # Replace figure paths
    for old_fig, new_fig in FIG_MAP.items():
        assert old_fig in tex, f"Figure reference {old_fig} not found in main.tex!"
        tex = tex.replace(old_fig, new_fig)

    # Replace table paths
    for old_tab, new_tab in TABLE_MAP.items():
        assert old_tab in tex, f"Table reference {old_tab} not found in main.tex!"
        tex = tex.replace(old_tab, new_tab)

    (root / "paper" / "main.tex").write_text(tex, encoding="utf-8")
    (root / "springer_manuscript" / "main.tex").write_text(tex, encoding="utf-8")

    # Verify byte equality
    b1 = (root / "paper" / "main.tex").read_bytes()
    b2 = (root / "springer_manuscript" / "main.tex").read_bytes()
    assert b1 == b2, "ERROR: paper/main.tex and springer_manuscript/main.tex are not identical!"
    print(f"   [OK] main.tex synchronized byte-for-byte! SHA256: {hashlib.sha256(b1).hexdigest()[:16]}")


if __name__ == "__main__":
    apply_renames()
