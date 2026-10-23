from pathlib import Path

main_path = Path("springer_manuscript/main.tex")
text = main_path.read_text(encoding="utf-8")

# 1. Rename Zheng68k in Table 4
text = text.replace("Zheng68k ($700, 765, 10$)$^*", "PBMC68k-reduced ($700, 765, 10$)$^*")

# 2. Update intro text for Zheng68k / PBMC68k-reduced
old_text = "and single-cell RNA sequencing (Zheng68k~\\cite{zheng2017massively})"
new_text = "and single-cell RNA sequencing (PBMC68k-reduced~\\cite{zheng2017massively})"
text = text.replace(old_text, new_text)

# 3. Add subsampling discussion and N=12 CD formula
old_pbmc_desc = """For Zheng68k, evaluation follows the standard Scanpy benchmark demonstration subset (\\texttt{pbmc68k\\_reduced}, selected by Scanpy developers by random subsampling of $N=700$ cells across the 10 major immune populations and filtering to $D=765$ highly variable genes from the $68.6\\text{k}$ single-cell repository~\\cite{zheng2017massively}), while 20 Newsgroups ($N=18{,}846, D=10{,}000$) and Extended Yale B ($N=2{,}414, D=1{,}024$) are evaluated on their full catalog representations, as summarized in Table~\\ref{tab:benchmark_ari}."""

new_pbmc_desc = """For single-cell genomics, evaluation follows the standard Scanpy benchmark demonstration subset (\\texttt{pbmc68k\\_reduced}, selected by Scanpy developers by random subsampling of $N=700$ cells across the 10 major immune populations and filtering to $D=765$ highly variable genes from the $68.6\\text{k}$ single-cell repository~\\cite{zheng2017massively}). Because PBMC68k-reduced was curated via total-count normalization (\\texttt{normalize\\_total}), logarithmic transformation (\\texttt{log1p}), and highly variable gene dispersion selection, the pre-filtered feature space exhibits higher baseline cluster separation than raw uncurated count matrices, yet presents significant sparsity challenges for dense consensus aggregators. In contrast, 20 Newsgroups ($N=18{,}846, D=10{,}000$) and Extended Yale B ($N=2{,}414, D=1{,}024$) are evaluated on their full catalog representations, as summarized in Table~\\ref{tab:benchmark_ari}."""

assert old_pbmc_desc in text, "old_pbmc_desc not found"
text = text.replace(old_pbmc_desc, new_pbmc_desc)

old_stat = """Across the 13 benchmarks, Friedman omnibus testing~\\cite{demsar2006statistical} yields $\\chi_F^2 = 11.34$, $p = \\TableThreeFriedmanPValue$, indicating no statistically significant difference across the omnibus collection. Statistical comparisons were evaluated using the Dem\\v{s}ar Critical Difference framework (Fig.~\\ref{fig:exp3_demsar}). Under the two-tailed post-hoc Nemenyi test ($\\alpha=0.05, k=11, N=13$), the critical difference threshold is:
\\begin{equation}
    CD = q_\\alpha \\sqrt{\\frac{k(k+1)}{6N}} = 3.219 \\sqrt{\\frac{11 \\times 12}{6 \\times 13}} = \\TrueNemenyiCD.
\\end{equation}
DEC ($R=\\MeanRankDEC$), Standard Consensus ($R=\\MeanRankStdCons$), K-Means ($R=5.31$), Ward ($R=5.31$), and ICC-v2 ($R=\\MeanRankICCvTwo$) occupy the top five ranks without statistically significant separation across the omnibus collection. However, because ICC-v2 underperforms on the Scanpy demonstration subset PBMC68k-reduced ($N=700$, Rank \\#11, ARI $0.240$ vs. $0.561$ for Standard Consensus), excluding this single demonstration subset notably shifts the omnibus hierarchy: across the 12 full benchmark datasets, ICC-v2 advances to Rank \\#2 ($R=\\TableThreeIccVTwoTwelveRank$), trailing only DEC ($R=\\TableThreeDecTwelveRank$), while K-Means ranks third ($R=\\TableThreeKMeansTwelveRank$), Standard Consensus ranks fourth ($R=\\TableThreeStdConsTwelveRank$), and Ward ranks fifth ($R=\\TableThreeWardTwelveRank$)."""

new_stat = """Across all 13 benchmarks, Friedman omnibus testing~\\cite{demsar2006statistical} yields $\\chi_F^2 = 11.34$, $p = \\TableThreeFriedmanPValue$, indicating no statistically significant difference across the omnibus collection. Under the two-tailed post-hoc Nemenyi test ($\\alpha=0.05, k=11, N=13$), the critical difference threshold is:
\\begin{equation}
    CD_{N=13} = q_\\alpha \\sqrt{\\frac{k(k+1)}{6N}} = 3.219 \\sqrt{\\frac{11 \\times 12}{6 \\times 13}} = 4.19.
\\end{equation}
DEC ($R=\\MeanRankDEC$), Standard Consensus ($R=\\MeanRankStdCons$), K-Means ($R=5.31$), Ward ($R=5.31$), and ICC-v2 ($R=\\MeanRankICCvTwo$) occupy the top five ranks without statistically significant separation across the omnibus collection. However, because ICC-v2 underperforms on the demonstration subset PBMC68k-reduced ($N=700$, Rank \\#11, ARI $0.240$ vs. $0.561$ for Standard Consensus), we also evaluated omnibus ranks and critical difference excluding this subsample ($N=12$ full benchmark datasets). For $N=12$, the critical difference threshold expands to:
\\begin{equation}
    CD_{N=12} = 3.219 \\sqrt{\\frac{11 \\times 12}{6 \\times 12}} = 4.36,
\\end{equation}
with Friedman $\\chi_F^2 = 11.27, p = 0.34$. Across the 12 full benchmark datasets, ICC-v2 advances to Rank \\#2 ($R=\\TableThreeIccVTwoTwelveRank$), trailing only DEC ($R=\\TableThreeDecTwelveRank$), while K-Means ranks third ($R=\\TableThreeKMeansTwelveRank$), Standard Consensus ranks fourth ($R=\\TableThreeStdConsTwelveRank$), and Ward ranks fifth ($R=\\TableThreeWardTwelveRank$)."""

assert old_stat in text, "old_stat not found"
text = text.replace(old_stat, new_stat)

main_path.write_text(text, encoding="utf-8")
print("[OK] Successfully updated main.tex with PBMC68k-reduced renaming and N=12/13 statistical tests!")
