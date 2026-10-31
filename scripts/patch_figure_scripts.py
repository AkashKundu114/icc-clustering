import re
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent

# 1. Patch src/icc/viz_style.py
viz_style_path = root / "src" / "icc" / "viz_style.py"
if viz_style_path.exists():
    text = viz_style_path.read_text(encoding="utf-8")
    text = text.replace('"ICC_v2 (Ours)": "#d62728",', '"GAC Pipeline": "#d62728",\n    "GAC": "#d62728",')
    text = text.replace('"ICC_v2 (Ours)": "*",', '"GAC Pipeline": "*",\n    "GAC": "*",')
    text = text.replace('"ICC_v2 (Ours)": "-",', '"GAC Pipeline": "-",\n    "GAC": "-",')
    viz_style_path.write_text(text, encoding="utf-8")
    print("Patched viz_style.py")

# 2. Patch exp1_inductive_generalization.py & plot_exp1_figures.py
exp1_path = root / "experiments" / "exp1_generalization" / "src" / "exp1_inductive_generalization.py"
if exp1_path.exists():
    text = exp1_path.read_text(encoding="utf-8")
    text = text.replace('label="ICC-v1 Calibrated Core (50%) [Ours]"', 'label="Calibrated Core (50%)"')
    text = text.replace('label="ICC-v1 Core (50%) [Ours]"', 'label="Calibrated Core (50%)"')
    exp1_path.write_text(text, encoding="utf-8")
    print("Patched exp1_inductive_generalization.py")

plot_exp1_path = root / "experiments" / "exp1_generalization" / "src" / "plot_exp1_figures.py"
if plot_exp1_path.exists():
    text = plot_exp1_path.read_text(encoding="utf-8")
    text = text.replace('label="ICC Core Pseudo-Labels [Ours]"', 'label="Ungated AC Core Pseudo-Labels"')
    text = text.replace('label="Ungated AC Calibrated Core (50%)"', 'label="Calibrated Core (50%)"')
    plot_exp1_path.write_text(text, encoding="utf-8")
    print("Patched plot_exp1_figures.py")

# 3. Patch run_exp3_1_benchmark_matrix.py (Fig 7)
bm_path = root / "experiments" / "exp3_real_world_benchmarks" / "src" / "run_exp3_1_benchmark_matrix.py"
if bm_path.exists():
    text = bm_path.read_text(encoding="utf-8")
    text = text.replace('"ICC-v1 (Anchor)",', '"Anchor Consensus (Ungated)",')
    text = text.replace('"ICC-v2 (BGSS+Anchor)",', '"GAC (BGSS+Anchor)",')
    bm_path.write_text(text, encoding="utf-8")
    print("Patched run_exp3_1_benchmark_matrix.py")

# 4. Patch run_exp3_4_statistical_significance.py (Fig 8)
stat_path = root / "experiments" / "exp3_real_world_benchmarks" / "src" / "run_exp3_4_statistical_significance.py"
if stat_path.exists():
    text = stat_path.read_text(encoding="utf-8")
    # Replace labels in CD diagram
    old_block = 'sorted_models = mean_ranks.index.tolist()'
    new_block = '''MODEL_DISPLAY_NAMES = {
        "ICC_v2": "GAC Pipeline",
        "ICC_v1": "Anchor Consensus (Ungated)",
        "Standard_Consensus": "Std Consensus",
        "Li_et_al_2019": "Core-Halo Cons.",
        "DEC": "DEC (ICML 2016)",
        "FCAG": "FCAG (TPAMI 2024)",
        "FastMVC": "FastMVC (TKDE 2023)",
    }
    raw_models = mean_ranks.index.tolist()
    sorted_models = [MODEL_DISPLAY_NAMES.get(m, m) for m in raw_models]'''
    if old_block in text and "MODEL_DISPLAY_NAMES" not in text:
        text = text.replace(old_block, new_block)
    # Also in color matching
    text = text.replace('if m == "ICC_v2":', 'if m in ("ICC_v2", "GAC Pipeline"):')
    text = text.replace('elif m == "ICC_v1":', 'elif m in ("ICC_v1", "Anchor Consensus (Ungated)"):')
    stat_path.write_text(text, encoding="utf-8")
    print("Patched run_exp3_4_statistical_significance.py")

# 5. Patch plot_audit_figures.py (Audit Fig 14 and Fig 17)
audit_path = root / "experiments" / "audit_controls" / "src" / "plot_audit_figures.py"
if audit_path.exists():
    text = audit_path.read_text(encoding="utf-8")
    text = text.replace('"ICC_v2_legacy": "ICC-v2 (Legacy 15%)",', '"ICC_v2_legacy": "GAC (Fixed 15%)",')
    text = text.replace('"ICC_v2_adaptive": "ICC-v2 (Adaptive Pool)",', '"ICC_v2_adaptive": "GAC (Adaptive)",')
    text = text.replace('"ICC_v1": "ICC-v1 (Anchor Only)",', '"ICC_v1": "Anchor Consensus (Ungated)",')
    text = text.replace('"ICC_v1": "ICC-v1",', '"ICC_v1": "Anchor Consensus",')
    text = text.replace('"ICC_v2_legacy": "ICC-v2 (15%)",', '"ICC_v2_legacy": "GAC (15%)",')
    text = text.replace('"ICC_v2_adaptive": "ICC-v2 (Adapt)",', '"ICC_v2_adaptive": "GAC (Adapt)",')
    audit_path.write_text(text, encoding="utf-8")
    print("Patched plot_audit_figures.py")

# 6. Patch plot_exp2_figures.py (Fig 9)
ablation_path = root / "experiments" / "exp2_ablation" / "src" / "plot_exp2_figures.py"
if ablation_path.exists():
    text = ablation_path.read_text(encoding="utf-8")
    text = text.replace('"V5: Full GAC Pipeline [Ours]"', '"V5: Full GAC Pipeline"')
    ablation_path.write_text(text, encoding="utf-8")
    print("Patched plot_exp2_figures.py")

print("All code patches applied successfully.")
