from pathlib import Path

p = Path("scripts/replot_fig2_subsample.py")
text = p.read_text(encoding="utf-8")

text = text.replace(
    '(ax1, r"(a) Clustering Accuracy (ARI vs. Ground Truth)", "Adjusted Rand Index (ARI)")',
    '(ax1, r"Clustering Accuracy (ARI vs. Ground Truth)", "Adjusted Rand Index (ARI)")'
)
text = text.replace(
    '(ax2, r"(b) Subsample Stability (Stratified 80% Resampling)", "Subsample Stability (ARI)")',
    '(ax2, r"Subsample Stability (Stratified 80% Resampling)", "Subsample Stability (ARI)")'
)

p.write_text(text, encoding="utf-8")
print("Updated replot_fig2_subsample.py cleanly")
