"""
Applies all 3 must-fix items and smaller leftovers to springer_manuscript/main.tex and paper/main.tex.
"""

from pathlib import Path
import hashlib

def patch_file(path: Path):
    content = path.read_text(encoding="utf-8")
    original = content

    # 1. Must Fix #1: Fig. 2c caption
    old_fig2 = (
        r"\caption{Clustering under isotropic distractor noise ($N=300, K=3$, 20 stratified 80\% subsample draws "
        r"per noise level). (a) Accuracy (ARI against ground truth) collapses toward zero for all methods as distractor "
        r"dimensions grow, and subsample stability collapses alongside it under row resampling (dropping to "
        r"$\le 0.03$ for K-Means, GMM, FCM, and Ward; Spectral lingers at $0.17$). (b) The subsample stability--accuracy "
        r"gap ($\Delta = \text{Stability} - \text{ARI}$) remains near zero across noise scales. (c) Heatmap of the gap "
        r"across five noise distributions at $D_{\text{noise}}=1{,}000$, showing that the stability--accuracy gap "
        r"remains near zero across non-degenerate regimes (the $+0.79$ cell for Ward under sparse noise reflects "
        r"trivial 1-cluster collapse, where a single cluster holds $>97\%$ of points). Thus, evidence for "
        r"stability--accuracy discordance on non-degenerate partitions rests on real cohorts rather than "
        r"synthetic distractor simulations.}"
    )
    new_fig2 = (
        r"\caption{Clustering under isotropic distractor noise ($N=300, K=3$, 20 stratified 80\% subsample draws "
        r"per noise level). (a) Accuracy (ARI against ground truth) collapses toward zero for all methods as distractor "
        r"dimensions grow, and subsample stability collapses alongside it under row resampling (dropping to "
        r"$\le 0.03$ for K-Means, GMM, FCM, and Ward; Spectral lingers at $0.17$). (b) The subsample stability--accuracy "
        r"gap ($\Delta = \text{Stability} - \text{ARI}$) remains near zero across noise scales. (c) Heatmap of the gap "
        r"across five noise distributions at $D_{\text{noise}}=1{,}000$, showing that the stability--accuracy gap "
        r"remains small ($\le 0.20$) except Ward under sparse noise ($+0.79$, reflecting trivial 1-cluster collapse "
        r"where a single cluster holds $>97\%$ of points). Thus, evidence for stability--accuracy discordance on "
        r"non-degenerate partitions rests on real cohorts rather than synthetic distractor simulations.}"
    )
    assert old_fig2 in content, f"old_fig2 not found in {path}"
    content = content.replace(old_fig2, new_fig2)

    # 2. Must Fix #2: Section 3.2 non-degenerate cells breakdown
    old_sec32 = (
        r"Across all 60 non-degenerate method--cohort cells evaluated (out of 72 total model--cohort pairs, "
        r"excluding the 12 degenerate cells that fail Rule~(i')), excess stability over unstructured noise "
        r"($\text{Stab} - \text{Null}$) averages $+0.472$ (95\% CI: $[+0.368, +0.645]$), rising to "
        r"$\text{Stab} - \text{Null} \approx 0.671$ ($0.684 - 0.013$) across the nine persistently discordant "
        r"cells, while permuted-null stability stays near zero ($-0.003$ to $+0.049$)."
    )
    new_sec32 = (
        r"Across all 60 non-degenerate method--cohort cells evaluated (out of 72 total model--cohort pairs across "
        r"the 12 methods, excluding the 12 degenerate cells that fail Rule~(i'): K-Means [2], FCM [1], Ambient "
        r"Consensus [1], Core-Halo [2], CoHiRF [5], and Ungated AC [1]; Table~\ref{tab:degeneracy_audit}), excess "
        r"stability over unstructured noise ($\text{Stab} - \text{Null}$) averages $+0.472$ (95\% CI: "
        r"$[+0.368, +0.645]$), rising to $\text{Stab} - \text{Null} \approx 0.671$ ($0.684 - 0.013$) across "
        r"the nine persistently discordant cells, while permuted-null stability stays near zero ($-0.003$ to $+0.049$)."
    )
    assert old_sec32 in content, f"old_sec32 not found in {path}"
    content = content.replace(old_sec32, new_sec32)

    # 3. Must Fix #3: Section 3.2 Prostate overclaim
    old_prostate = (
        r"This confirms that the observed subsample stability reflects genuine data geometry rather than permutation "
        r"artifacts, even while partitions exhibit zero agreement with diagnostic truth."
    )
    new_prostate = (
        r"This confirms that the observed subsample stability reflects data-driven structure rather than permutation "
        r"artifacts, even while partitions exhibit zero agreement with diagnostic truth."
    )
    assert old_prostate in content, f"old_prostate not found in {path}"
    content = content.replace(old_prostate, new_prostate)

    # 4. Smaller Leftover: Section 3 Definitions paragraph (line 162)
    old_sec3_def = (
        r"In simulations, ARI collapses toward zero for every method as distractor dimensions grow "
        r"(Section~\ref{sec:sim_isotropic}); because seed-to-seed agreement is trivially perfect for deterministic "
        r"solvers, simulations are used to document the accuracy collapse and not to demonstrate discordance."
    )
    new_sec3_def = (
        r"In simulations, ARI collapses toward zero for every method as distractor dimensions grow and subsample "
        r"stability collapses alongside it (Section~\ref{sec:sim_isotropic}), so simulations document the accuracy "
        r"collapse rather than stability--accuracy discordance."
    )
    assert old_sec3_def in content, f"old_sec3_def not found in {path}"
    content = content.replace(old_sec3_def, new_sec3_def)

    # 5. Smaller Leftover: Section 6.2 dense-consensus sentence
    old_sec62 = (
        r"where dense consensus is confounded by base-clusterer instability on Leukemia."
    )
    new_sec62 = (
        r"where dense consensus is associated with base-clusterer instability on Leukemia."
    )
    assert old_sec62 in content, f"old_sec62 not found in {path}"
    content = content.replace(old_sec62, new_sec62)

    # 6. Smaller Leftover: Table 13 and Section 6.3 Holm correction clarification
    old_tab13 = r"Family-Wise Error Control & Holm-Bonferroni step-down & Strong control of FWER \\"
    new_tab13 = r"Family-Wise Error Control & Holm-Bonferroni step-down (benchmark pairwise tests) & Strong control of FWER \\"
    assert old_tab13 in content, f"old_tab13 not found in {path}"
    content = content.replace(old_tab13, new_tab13)

    old_sec63 = (
        r"Nevertheless, paired Wilcoxon signed-rank tests across these six cohorts reveal no statistically significant "
        r"differences once corrected via Holm-Bonferroni ($p_{\text{adj}} > 0.05$), reflecting the inherently modest "
        r"statistical power available when $n=6$."
    )
    new_sec63 = (
        r"Nevertheless, paired Wilcoxon signed-rank tests across these six cohorts reveal no statistically significant "
        r"differences once corrected via Holm-Bonferroni ($p_{\text{adj}} > 0.05$), reflecting the inherently modest "
        r"statistical power available when $n=6$. Holm-Bonferroni step-down correction is applied to the family of 11 "
        r"pairwise benchmark comparisons between GAC and baseline algorithms in the high-dimensional subgroup evaluation "
        r"(Section~\ref{sec:statistical_eval}); exploratory single-contrast hypothesis tests on BGSS gating "
        r"(Section~\ref{sec:exp3_benchmarks}) and the factorial interaction (Section~\ref{sec:factorial_ablation}) "
        r"are reported uncorrected."
    )
    assert old_sec63 in content, f"old_sec63 not found in {path}"
    content = content.replace(old_sec63, new_sec63)

    # 7. Code availability release tag
    old_code_avail = r"\textbf{Code availability}: \url{https://github.com/AkashKundu114/icc-clustering}"
    new_code_avail = r"\textbf{Code availability}: \url{https://github.com/AkashKundu114/icc-clustering} (v1.0.0 release tag; archived on Zenodo upon publication)"
    assert old_code_avail in content, f"old_code_avail not found in {path}"
    content = content.replace(old_code_avail, new_code_avail)

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
    assert h1 == h2, f"SHA256 mismatch: {p1} ({h1}) vs {p2} ({h2})"
    print(f"Verified byte-identical! SHA256: {h1}")

if __name__ == "__main__":
    main()
