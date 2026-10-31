"""
Applies latest user requested fixes to springer_manuscript/main.tex and paper/main.tex.
"""

from pathlib import Path
import hashlib

def patch_file(path: Path):
    content = path.read_text(encoding="utf-8")
    original = content

    # 1. Section 6.3 broken cross-references
    old_sec63 = (
        r"Holm-Bonferroni step-down correction is applied to the family of 11 pairwise benchmark comparisons "
        r"between GAC and baseline algorithms in the high-dimensional subgroup evaluation "
        r"(Section~\ref{sec:statistical_eval}); exploratory single-contrast hypothesis tests on BGSS gating "
        r"(Section~\ref{sec:exp3_benchmarks}) and the factorial interaction (Section~\ref{sec:factorial_ablation}) "
        r"are reported uncorrected."
    )
    new_sec63 = (
        r"Holm-Bonferroni step-down correction is applied to the family of 11 pairwise benchmark comparisons "
        r"between GAC and baseline algorithms in the high-dimensional subgroup evaluation above; exploratory "
        r"single-contrast hypothesis tests on BGSS gating (Section~\ref{sec:benchmarks_suite}) and the factorial "
        r"interaction (Section~\ref{sec:exp2_knockout}) are reported uncorrected."
    )
    assert old_sec63 in content, f"old_sec63 not found in {path}"
    content = content.replace(old_sec63, new_sec63)

    # 2. Fig. 4 subfigure captions and main caption
    old_fig4 = (
        r"\begin{figure*}[!t]" "\n"
        r"\centering" "\n"
        r"\subfloat[Downstream Generalization with Oracle True Labels (50\% Core vs 100\% Full Training)\label{fig:exp1_oracle}]{%" "\n"
        r" \includegraphics[width=0.78\textwidth]{figures/fig04a_inductive_oracle_generalization.png}%" "\n"
        r"}" "\n"
        r"\\[1.0ex]" "\n"
        r"\subfloat[Downstream Generalization with Unsupervised Pseudo-Labels ($D_{\text{noise}} \le 3{,}000$)\label{fig:exp1_pseudo}]{%" "\n"
        r" \includegraphics[width=0.78\textwidth]{figures/fig04b_inductive_pseudolabel_generalization.png}%" "\n"
        r"}" "\n"
        r"\caption{Inductive generalization performance on held-out test splits ($20\%$). (a) When trained on 50\% high-determinacy core points, downstream classifiers achieve parity with 100\% full-data training under low-to-moderate noise ($D_{\text{noise}} \le 50$), while under high noise ($D_{\text{noise}} \ge 1{,}000$), core-only training exhibits a 5--21 percentage point deficit due to reduced training sample size in noise-dominated regimes. (b) Under heavy noise corruption ($D_{\text{noise}} \ge 1{,}000$), training on unguided pseudo-labels (both full and core subsets) degrades toward random chance accuracy ($33.6\%$--$36.0\%$ vs. $33.3\%$ chance level for $K=3$), demonstrating that high-determinacy filtering alone cannot rescue corrupted pseudo-labels without prior feature gating.}" "\n"
        r"\label{fig:exp1_results}" "\n"
        r"\end{figure*}"
    )
    new_fig4 = (
        r"\begin{figure*}[!t]" "\n"
        r"\centering" "\n"
        r"\subfloat[Downstream Generalization with Oracle True Labels\label{fig:exp1_oracle}]{%" "\n"
        r" \includegraphics[width=0.78\textwidth]{figures/fig04a_inductive_oracle_generalization.png}%" "\n"
        r"}" "\n"
        r"\\[1.0ex]" "\n"
        r"\subfloat[Downstream Generalization with Unsupervised Pseudo-Labels\label{fig:exp1_pseudo}]{%" "\n"
        r" \includegraphics[width=0.78\textwidth]{figures/fig04b_inductive_pseudolabel_generalization.png}%" "\n"
        r"}" "\n"
        r"\caption{Inductive generalization performance on held-out test splits ($20\%$). (a) Under oracle true labels, downstream classifiers achieve parity with 100\% full-data training when trained on 50\% high-determinacy core points under low-to-moderate noise ($D_{\text{noise}} \le 50$), while under high noise ($D_{\text{noise}} \ge 1{,}000$), core-only training exhibits a 5--21 percentage point deficit due to reduced effective sample size. (b) Under unsupervised pseudo-labels, performance collapses toward random chance ($33.6\%$--$36.0\%$ vs. $33.3\%$ chance level for $K=3$) when distractor dimensions dominate ($D_{\text{noise}} \ge 1{,}000$), demonstrating that determinacy core filtering alone cannot rescue corrupted pseudo-labels without prior feature gating.}" "\n"
        r"\label{fig:exp1_results}" "\n"
        r"\end{figure*}"
    )
    assert old_fig4 in content, f"old_fig4 not found in {path}"
    content = content.replace(old_fig4, new_fig4)

    # 3. Section 3.1 citing Table 3's Seed* column
    old_sec31 = (
        r"In contrast to seed-to-seed agreement on unperturbed data---which remains trivially at $1.0$ for deterministic "
        r"solvers---subsample stability demonstrates that isotropic noise erases both cluster accuracy and partition reproducibility."
    )
    new_sec31 = (
        r"In contrast to seed-to-seed agreement on unperturbed data---which remains trivially at $1.0$ for deterministic "
        r"solvers (reported as $\text{Seed}^*$ in Table~\ref{tab:real_data_stability})---subsample stability demonstrates "
        r"that isotropic noise erases both cluster accuracy and partition reproducibility."
    )
    assert old_sec31 in content, f"old_sec31 not found in {path}"
    content = content.replace(old_sec31, new_sec31)

    # 4. Contribution 1 wording
    old_contrib1 = (
        r"confirming that observed subsample stability reflects underlying sample covariance rather than permutation artifacts, "
        r"though this structure does not align with diagnostic reference classes."
    )
    new_contrib1 = (
        r"confirming that observed subsample stability is not a permutation artifact, "
        r"though this structure does not align with diagnostic reference classes."
    )
    assert old_contrib1 in content, f"old_contrib1 not found in {path}"
    content = content.replace(old_contrib1, new_contrib1)

    assert content != original, f"No changes made to {path}"
    path.write_text(content, encoding="utf-8")
    print(f"Successfully patched {path}")

def main():
    p1 = Path("springer_manuscript/main.tex")
    p2 = Path("paper/main.tex")
    patch_file(p1)
    patch_file(p2)

    h1 = hashlib.sha256(p1.read_bytes()).hexdigest()
    h2 = hashlib.sha256(p2.read_bytes()).hexdigest()
    assert h1 == h2, f"SHA mismatch: {p1} ({h1}) vs {p2} ({h2})"
    print(f"Verified byte-identical! SHA256: {h1}")

if __name__ == "__main__":
    main()
