"""
Apply the 6 checklist fixes to springer_manuscript/main.tex and paper/main.tex.
"""

from pathlib import Path
import hashlib

def patch_file(path: Path):
    content = path.read_text(encoding="utf-8")
    original = content

    # 1. Fig 2 caption panel (c)
    old_fig2_cap = r"\caption{Clustering under isotropic distractor noise ($N=300, K=3$, 20 stratified 80\% subsample draws per noise level). (a) Accuracy (ARI against ground truth) collapses toward zero for all methods as distractor dimensions grow, and subsample stability collapses alongside it under row resampling (dropping to $\le 0.03$ for K-Means, GMM, FCM, and Ward; Spectral lingers at $0.17$). (b) The subsample stability--accuracy gap ($\Delta = \text{Stability} - \text{ARI}$) remains near zero across noise scales. (c) Heatmap of the gap across five noise distributions at $D_{\text{noise}}=1{,}000$, confirming that stability--accuracy discordance does not emerge in isotropic distractor simulations and rests on real cohorts.}"
    new_fig2_cap = r"\caption{Clustering under isotropic distractor noise ($N=300, K=3$, 20 stratified 80\% subsample draws per noise level). (a) Accuracy (ARI against ground truth) collapses toward zero for all methods as distractor dimensions grow, and subsample stability collapses alongside it under row resampling (dropping to $\le 0.03$ for K-Means, GMM, FCM, and Ward; Spectral lingers at $0.17$). (b) The subsample stability--accuracy gap ($\Delta = \text{Stability} - \text{ARI}$) remains near zero across noise scales. (c) Heatmap of the gap across five noise distributions at $D_{\text{noise}}=1{,}000$, showing that the stability--accuracy gap remains near zero across non-degenerate regimes (the $+0.79$ cell for Ward under sparse noise reflects trivial 1-cluster collapse, where a single cluster holds $>97\%$ of points). Thus, evidence for stability--accuracy discordance on non-degenerate partitions rests on real cohorts rather than synthetic distractor simulations.}"
    assert old_fig2_cap in content, f"old_fig2_cap not found in {path}"
    content = content.replace(old_fig2_cap, new_fig2_cap)

    # 2. Section 3.1 gap sentence
    old_sec31 = (
        r"Consequently, the subsample stability--accuracy gap $\Delta = \text{Stability} - \text{ARI}$ remains "
        r"near zero across all noise scales (Fig.~\ref{fig:dist_gap}) and across diverse noise distributions "
        r"at $D_{\text{noise}}=1{,}000$ (Fig.~\ref{fig:noise_heatmap}), with minor elevation only under "
        r"correlated noise ($+0.05$ to $+0.20$) and sparse noise for Ward ($+0.79$, where single-point "
        r"chaining isolates outliers). In contrast to seed-to-seed agreement on unperturbed data---which "
        r"remains trivially at $1.0$ for deterministic solvers---subsample stability demonstrates that "
        r"isotropic noise erases both cluster accuracy and partition reproducibility."
    )
    new_sec31 = (
        r"Consequently, the subsample stability--accuracy gap $\Delta = \text{Stability} - \text{ARI}$ remains "
        r"near zero across all noise scales under isotropic noise (Fig.~\ref{fig:dist_gap}) and across four of "
        r"the five noise distributions at $D_{\text{noise}}=1{,}000$ (Fig.~\ref{fig:noise_heatmap}; "
        r"$\Delta \in [-0.002, +0.092]$ for centroid and fuzzy methods, $\le 0.06$ for Ward, and $\le 0.20$ "
        r"for Spectral). The sole exception is Ward linkage under zero-inflated sparse noise ($\Delta = +0.79$), "
        r"where isolated sparse bursts induce trivial 1-cluster collapse (a single background cluster "
        r"encompassing $> 97\%$ of points with singleton outliers, failing Rule~(i')), creating artificial "
        r"stability on uninformative partitions. In contrast to seed-to-seed agreement on unperturbed "
        r"data---which remains trivially at $1.0$ for deterministic solvers---subsample stability demonstrates "
        r"that isotropic noise erases both cluster accuracy and partition reproducibility."
    )
    assert old_sec31 in content, f"old_sec31 not found in {path}"
    content = content.replace(old_sec31, new_sec31)

    # 3. Section 3.2 non-degenerate count
    old_sec32 = (
        r"Across all 58 non-degenerate method--cohort cells evaluated, excess stability over unstructured noise "
        r"($\text{Stab} - \text{Null}$) averages $+0.472$ (95\% CI: $[+0.368, +0.645]$), rising to "
        r"$\text{Stab} - \text{Null} \approx 0.671$ ($0.684 - 0.013$) across the nine persistently discordant "
        r"cells, while permuted-null stability stays near zero ($-0.003$ to $+0.049$)."
    )
    new_sec32 = (
        r"Across all 60 non-degenerate method--cohort cells evaluated (out of 72 total model--cohort pairs, "
        r"excluding the 12 degenerate cells that fail Rule~(i')), excess stability over unstructured noise "
        r"($\text{Stab} - \text{Null}$) averages $+0.472$ (95\% CI: $[+0.368, +0.645]$), rising to "
        r"$\text{Stab} - \text{Null} \approx 0.671$ ($0.684 - 0.013$) across the nine persistently discordant "
        r"cells, while permuted-null stability stays near zero ($-0.003$ to $+0.049$)."
    )
    assert old_sec32 in content, f"old_sec32 not found in {path}"
    content = content.replace(old_sec32, new_sec32)

    # 4. Section 7.5
    old_sec75 = (
        r"By comparison, selecting the top 1,069 features by sample variance captures only 8 of the 50 markers "
        r"($16.0\%$), performing no better than random expectation because uninformative noise coordinates "
        r"exhibit substantial variance."
    )
    new_sec75 = (
        r"By comparison, selecting the top 1,069 features by sample variance captures only 8 of the 50 markers "
        r"($16.0\%$; hypergeometric $p = 0.481$), performing no better than random expectation because "
        r"uninformative noise coordinates exhibit substantial variance."
    )
    assert old_sec75 in content, f"old_sec75 not found in {path}"
    content = content.replace(old_sec75, new_sec75)

    # 5. Fig 10 caption
    old_fig10_cap = (
        r"whereas standard variance filtering captures only 8 of 50 markers ($16.0\%$).}"
    )
    new_fig10_cap = (
        r"whereas standard variance filtering captures only 8 of 50 markers ($16.0\%$, hypergeometric $p = 0.481$).}"
    )
    assert old_fig10_cap in content, f"old_fig10_cap not found in {path}"
    content = content.replace(old_fig10_cap, new_fig10_cap)

    assert content != original, f"No modifications made to {path}"
    path.write_text(content, encoding="utf-8")
    print(f"Successfully patched {path}")

def main():
    p1 = Path("springer_manuscript/main.tex")
    p2 = Path("paper/main.tex")
    patch_file(p1)
    patch_file(p2)

    h1 = hashlib.sha256(p1.read_bytes()).hexdigest()
    h2 = hashlib.sha256(p2.read_bytes()).hexdigest()
    assert h1 == h2, f"SHA256 mismatch between {p1} ({h1}) and {p2} ({h2})"
    print(f"Verified byte-identical! SHA256: {h1}")

if __name__ == "__main__":
    main()
