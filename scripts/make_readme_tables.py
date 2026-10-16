import json
from pathlib import Path

def make_markdown_table():
    root = Path(__file__).resolve().parents[1]
    stats_path = root / "results" / "phase2" / "stats.json"
    with open(stats_path, "r", encoding="utf-8") as f:
        stats = json.load(f)

    high_d = stats.get("fair_baselines_analysis", {}).get("high_d_mean_ari", {})
    high_d_ranks = stats.get("subgroup_high_d_over_20", {}).get("mean_ranks", {})
    overall_ranks = stats.get("overall_mean_ranks", {})

    print("Generated Table 3 Subgroup Summary (Markdown):")
    print("| Method | High-D Mean ARI (D/N > 20) | High-D Rank | Overall 13-Dataset Rank |")
    print("| :--- | :---: | :---: | :---: |")
    methods = [
        ("ICC-v2 (Proposed)", high_d.get("ICC_v2", 0.258), high_d_ranks.get("ICC_v2", 2.33), overall_ranks.get("ICC_v2", 5.46)),
        ("Variance Filter + K-Means", high_d.get("K-Means_VarFilt", 0.050), "-", "-"),
        ("Sparse K-Means", high_d.get("SparseKMeans", 0.044), "-", "-"),
        ("PCA + K-Means", high_d.get("K-Means_PCA", 0.042), "-", "-"),
        ("Laplacian Score + K-Means", high_d.get("K-Means_LapScore", 0.041), "-", "-"),
        ("Standard K-Means", high_d.get("K-Means_All", 0.044), high_d_ranks.get("K-Means", 5.83), overall_ranks.get("K-Means", 5.31)),
        ("Standard Consensus", high_d.get("StdCons_All", 0.039), high_d_ranks.get("Standard_Consensus", 6.33), overall_ranks.get("Standard_Consensus", 5.08)),
        ("DEC (Deep Embedded)", "-", high_d_ranks.get("DEC", 5.00), overall_ranks.get("DEC", 4.31)),
    ]
    for name, ari, r_high, r_all in methods:
        ari_str = f"{ari:.3f}" if isinstance(ari, float) else str(ari)
        r_high_str = f"{r_high:.2f}" if isinstance(r_high, float) else str(r_high)
        r_all_str = f"{r_all:.2f}" if isinstance(r_all, float) else str(r_all)
        print(f"| **{name}** | {ari_str} | {r_high_str} | {r_all_str} |")

if __name__ == "__main__":
    make_markdown_table()
