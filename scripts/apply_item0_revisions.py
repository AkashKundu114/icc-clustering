"""
scripts/apply_item0_revisions.py
Applies Item 0 changes:
- Formal title: "Cluster Stability and Feature-Gated Bipartite Ensemble Learning for High-Dimensional Noisy Data: An Empirical Analysis"
- Running head: "Cluster Stability and Feature-Gated Bipartite Ensemble Learning"
- Keywords: "cluster stability, ensemble learning, consensus clustering, high-dimensional noisy data, bipartite anchor graphs, feature gating, subsample stability, null control."
- PDF metadata (hypersetup)
- Terminology replacements across paper/main.tex, springer_manuscript/main.tex, gen/table02_real_data_stability.tex, scripts/make_stability_outputs.py, README.md, CITATION.cff, pyproject.toml, submission/COVER_LETTER.md, STATE.json, etc.
- Abstract constrained to <= 250 words without claiming "stable clustering" as a property of GAC.
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

NEW_TITLE = "Cluster Stability and Feature-Gated Bipartite Ensemble Learning for High-Dimensional Noisy Data: An Empirical Analysis"
NEW_RUNNING_HEAD = "Cluster Stability and Feature-Gated Bipartite Ensemble Learning"
NEW_KEYWORDS = "cluster stability, ensemble learning, consensus clustering, high-dimensional noisy data, bipartite anchor graphs, feature gating, subsample stability, null control."

NEW_ABSTRACT = (
    r"\abstract{Consensus clustering is widely assumed to resist high-dimensional noise. "
    r"We evaluate this premise across simulations and six biomedical cohorts ($D/N > 20$) "
    r"under a stratified $80\%$ subsampling protocol (30 draws) with column-permuted null controls. "
    r"Under isotropic noise ($D \gg N$), base clusterers converge stably onto arbitrary noise "
    r"partitions while Adjusted Rand Index (ARI) collapses toward zero. "
    r"On real cohorts, baselines exhibit pronounced stability-accuracy discordance: "
    r"three of twelve methods (FCAG, FCM, FastMVC) satisfy our pre-specified "
    r"stability-accuracy discordance (SAD) criterion ($\text{stability} \ge 0.50$, $\text{accuracy} \le 0.05$) "
    r"on $\ge 3$ cohorts; Ward and Spectral show high stability ($\ge 0.97$) yet near-zero accuracy "
    r"($\le 0.03$) on Prostate ($D=12{,}600$), where null stability drops to $\le 0.03$. "
    r"A paired bootstrap excludes zero for the overall gap ($+0.464$, $95\%$ CI: $[+0.363, +0.607]$), "
    r"indicating that high stability does not imply correctness. "
    r"We evaluate Gated Anchor Consensus (GAC), combining Bimodality-Gated Subspace Selection (BGSS), "
    r"random-subspace ensembles, bipartite anchor graphs, and centroid projection. "
    r"Across 13 benchmarks (3,000 fits), omnibus differences across methods are not statistically significant "
    r"(Friedman $p = 0.40$). GAC attains the highest mean ARI on the six $D/N > 20$ cohorts "
    r"($0.217$ vs. $0.065$ for FCAG and $0.037$ for ambient consensus), concentrated in "
    r"Leukemia ($0.600$) and SRBCT ($0.546$). Bipartite ensembling accounts for $+0.118$ (65.6\%) of this gain, "
    r"while BGSS adds $+0.062$ over matched random gating ($95\%$ CI: $[+0.013, +0.142]$). "
    r"Landmark determinacy yields an empirical null result over uniform sampling ($\Delta = +0.019$). "
    r"On Prostate and CNS, diffuse marginal distributions lead to partitions unrelated to reference labels "
    r"($\text{accuracy} \le 0.02$).}"
)

def update_main_tex(path: Path):
    content = path.read_text(encoding="utf-8")

    # Title & Running head
    content = re.sub(
        r"\\title\[.*?\]\{.*?\}",
        lambda m: f"\\title[{NEW_RUNNING_HEAD}]{{{NEW_TITLE}}}",
        content,
        count=1
    )

    # Keywords
    content = re.sub(
        r"\\keywords\{.*?\}",
        lambda m: f"\\keywords{{{NEW_KEYWORDS}}}",
        content,
        count=1
    )

    # Add hypersetup if not present
    if "hypersetup" not in content:
        hypersetup = (
            "\n\\hypersetup{\n"
            f"  pdftitle={{{NEW_TITLE}}},\n"
            f"  pdfkeywords={{{NEW_KEYWORDS}}}\n"
            "}\n"
        )
        content = content.replace("\\input{numbers.tex}", "\\input{numbers.tex}" + hypersetup)

    # Abstract
    content = re.sub(
        r"\\abstract\{.*?\}",
        lambda m: NEW_ABSTRACT,
        content,
        count=1,
        flags=re.DOTALL
    )

    # Contributions Item 1
    new_item1 = (
        r"\item \textbf{Stability-Accuracy Discordance in High Dimensions (Subsample Stability and Null Control):} "
        r"Controlled empirical evaluations under isotropic noise ($D \gg N$) and six real biomedical cohorts ($D/N > 20$, 30 stratified $80\%$ subsamples) "
        r"demonstrate that consensus stability remains high ($\text{subsample stability} \ge 0.50$ to $1.00$) while accuracy collapses near zero ($\text{ARI} \le 0.05$). "
        r"Paired bootstrap analysis across cohorts ($B=10{,}000$) confirms a positive subsample stability--accuracy gap ($+0.464$, $95\%$ CI: $[+0.363, +0.607]$), "
        r"while independent column-permuted null controls confirm that null stability collapses to zero (mean $+0.007$). "
        r"Three methods (FCAG, FCM, FastMVC) meet our pre-specified stability-accuracy discordance (SAD) criterion across at least 3 cohorts, "
        r"indicating that high stability does not imply partition correctness on real high-dimensional data."
    )
    content = re.sub(
        r"\\item \\textbf\{The Stability Trap in High Dimensions \(Subsample Stability and Null Control\):\} [^\n]+",
        lambda m: new_item1,
        content
    )

    # Contributions Item 3
    content = content.replace(
        "GAC attenuates but fails to overcome the noise trap, underscoring that consensus cannot salvage clustering without detectable marginal structure.",
        "GAC attenuates the gap but exhibits low accuracy without detectable marginal structure, underscoring that consensus cannot recover clusters without detectable marginal structure."
    )

    # Outline
    content = content.replace(
        "details the stability trap observed across biomedical cohorts",
        "details the stability-accuracy discordance observed across biomedical cohorts"
    )

    # Geometric contrast
    content = content.replace("denotes severe geometric overlap", "denotes substantial geometric overlap")
    content = content.replace("indicating severe geometric overlap", "indicating substantial geometric overlap")

    # Falsification discussion
    old_fals = (
        r"Under finite samples, base clusterers capture stochastic fluctuations in the noise dimensions. "
        r"This induces an empirical stability trap: base partitions repeatedly converge onto arbitrary noise boundaries "
        r"with deceptively high mutual agreement ($\text{Stability} > 0.8$), while true cluster recovery collapses ($\text{ARI} \to 0$, Fig.~\ref{fig:ari_stability})."
    )
    new_fals = (
        r"Under finite samples, base clusterers capture stochastic fluctuations in the noise dimensions. "
        r"This induces empirical stability-accuracy discordance: base partitions repeatedly converge onto arbitrary noise boundaries "
        r"with elevated mutual agreement ($\text{Stability} > 0.8$), while true cluster recovery collapses ($\text{ARI} \to 0$, Fig.~\ref{fig:ari_stability})."
    )
    content = content.replace(old_fals, new_fals)

    # Section 3.2 heading
    content = content.replace(
        r"\subsection{The Stability Trap on Real-World High-Dimensional Benchmarks}\label{sec:real_data_stability}",
        r"\subsection{Stability-Accuracy Discordance on Real-World High-Dimensional Benchmarks}\label{sec:real_data_stability}"
    )

    # Introductory question
    content = content.replace(
        "While synthetic isotropic distractors demonstrate the geometric mechanism of the stability trap, does this pathology manifest on real-world biomedical benchmarks?",
        "While synthetic isotropic distractors demonstrate the geometric mechanism of stability-accuracy discordance, does this behavior manifest on real-world biomedical benchmarks?"
    )

    # Fig 3 caption
    old_fig3_cap = (
        r"\caption{Real-world evidence of the stability trap across 6 high-dimensional biomedical cohorts ($D/N > 20$, 30 independent seeds per method). "
        r"(a) Empirical clustering accuracy ($\overline{\text{ARI}}$ vs. ground truth) plotted against seed stability (mean pairwise ARI across seeds). "
        r"The shaded region highlights the severe ``Stable but Wrong'' pathology ($\text{Stab} \ge 0.50$ and $\overline{\text{ARI}} \le 0.05$), "
        r"where algorithms converge with high mutual agreement onto arbitrary noise attractors. "
        r"(b) Mean stability-accuracy gap ($\Delta = \text{Stability} - \overline{\text{ARI}}$) across the six high-$D$ cohorts. "
        r"Graph-based methods (Ward, $\Delta = +0.968$; Spectral, $\Delta = +0.964$; FCAG, $\Delta = +0.842$) and consensus baselines "
        r"(Standard Consensus, $\Delta = +0.656$; Core-Halo, $\Delta = +0.612$) exhibit massive gaps, whereas GAC ($\Delta = +0.268$) attenuates the gap by screening out uninformative coordinates.}"
    )
    new_fig3_cap = (
        r"\caption{Real-world evidence of stability-accuracy discordance across 6 high-dimensional biomedical cohorts ($D/N > 20$, 30 stratified $80\%$ subsamples per method). "
        r"(a) Empirical clustering accuracy ($\overline{\text{ARI}}$ vs. ground truth) plotted against subsample stability (mean pairwise ARI on shared samples across subsamples). "
        r"The shaded region highlights the stability-accuracy discordance (SAD) criterion ($\text{Stab} \ge 0.50$ and $\overline{\text{ARI}} \le 0.05$), "
        r"where algorithms converge to partitions unrelated to reference labels. "
        r"(b) Mean subsample stability-accuracy gap ($\Delta = \text{Subsample Stability} - \overline{\text{ARI}}$) across the six high-$D$ cohorts with paired bootstrap confidence intervals. "
        r"Graph-based methods (Ward, $\Delta = +0.504$; Spectral, $\Delta = +0.590$; FCAG, $\Delta = +0.503$) and consensus baselines "
        r"(Standard Consensus, $\Delta = +0.534$; Core-Halo, $\Delta = +0.502$) exhibit large gaps, whereas GAC ($\Delta = +0.300$) attenuates the gap by screening uninformative coordinates.}"
    )
    content = content.replace(old_fig3_cap, new_fig3_cap)

    # Paragraph 1
    content = content.replace(
        r"\paragraph{1. Pervasive Entrapment Across Classical and Graph Baselines:}",
        r"\paragraph{1. Discordance Across Classical and Graph Baselines:}"
    )
    old_p1 = (
        r"Under stratified subsampling, classical and graph-based baselines repeatedly lock onto mutually agreeing yet clinically spurious partitions. "
        r"Across all six high-$D$ cohorts, three methods satisfy pre-specified Decision Rule~(i) (subsample stability $\ge 0.50$ and empirical accuracy $\le 0.05$) across at least three distinct cohorts: FCAG (Colon, CNS, Prostate), FCM (Colon, CNS, Ovarian), and FastMVC (Colon, CNS, Prostate). "
        r"On Prostate ($D=12{,}600$), ten of the twelve evaluated methods satisfy Rule~(i), led by Ward ($\text{Stab}=0.996, \text{Acc}=0.026, \Delta=+0.970$), Spectral ($\text{Stab}=0.971, \text{Acc}=-0.002, \Delta=+0.973$), and Core-Halo ($\text{Stab}=1.000, \text{Acc}=0.000, \Delta=+1.000$). "
        r"Under independent column-permuted null controls, stability on Prostate collapses to near zero (range $-0.001$ to $+0.049$). "
        r"This verifies that the elevated stability observed on real data reflects genuine, highly reproducible geometric attractors in the noise subspace that are completely orthogonal to clinical truth, directly validating the ``Stable but Wrong'' pathology. "
        r"Paired bootstrap resampling across cohorts ($B=10{,}000$) yields an overall mean stability--accuracy gap of $+0.464$ with a 95\% confidence interval of $[+0.363, +0.607]$, firmly excluding zero and supporting pre-specified Decision Rule~(iii)."
    )
    new_p1 = (
        r"Under stratified subsampling, classical and graph-based baselines repeatedly converge to mutually agreeing partitions that do not reflect clinical reference labels. "
        r"Across all six high-$D$ cohorts, three methods satisfy the pre-specified stability-accuracy discordance criterion (Decision Rule~(i): subsample stability $\ge 0.50$ and empirical accuracy $\le 0.05$) across at least three distinct cohorts: FCAG (Colon, CNS, Prostate), FCM (Colon, CNS, Ovarian), and FastMVC (Colon, CNS, Prostate). "
        r"On Prostate ($D=12{,}600$), ten of the twelve evaluated methods satisfy Rule~(i), led by Ward ($\text{Stab}=0.996, \text{Acc}=0.026, \Delta=+0.970$), Spectral ($\text{Stab}=0.971, \text{Acc}=-0.002, \Delta=+0.973$), and Core-Halo ($\text{Stab}=1.000, \text{Acc}=0.000, \Delta=+1.000$). "
        r"Under independent column-permuted null controls, stability on Prostate drops to near zero (range $-0.001$ to $+0.049$). "
        r"Null-permutation stability near zero indicates that this structure is not a permutation artifact, while the partitions show near-zero agreement with clinical reference labels. "
        r"Paired bootstrap resampling across cohorts ($B=10{,}000$) yields an overall mean stability--accuracy gap of $+0.464$ with a 95\% confidence interval of $[+0.363, +0.607]$, excluding zero and supporting pre-specified Decision Rule~(iii)."
    )
    content = content.replace(old_p1, new_p1)

    # Paragraph 3
    content = content.replace(
        r"\paragraph{3. Where Feature Gating Helps, and Where It Entraps GAC:}",
        r"\paragraph{3. Where Feature Gating Helps, and Boundary Conditions for GAC:}"
    )
    content = content.replace(
        "GAC breaks free from the stability trap: empirical accuracy matches or exceeds subsample stability.",
        "GAC achieves concordance between accuracy and stability: empirical accuracy matches or exceeds subsample stability."
    )
    content = content.replace(
        "on Prostate ($D=12{,}600$) and CNS ($D=7{,}129$), GAC also falls into the stability trap",
        "on Prostate ($D=12{,}600$) and CNS ($D=7{,}129$), GAC also exhibits stability-accuracy discordance"
    )

    # Limitations & Conclusion
    content = content.replace("Due to severe technical zero-inflation", "Due to high technical zero-inflation")
    content = content.replace("Severe sparsity induces a complementary failure mode", "High sparsity induces a complementary failure mode")
    content = content.replace("present a severe structural challenge", "present a substantial challenge")
    content = content.replace("demonstrate an empirical stability trap", "demonstrate empirical stability-accuracy discordance")

    path.write_text(content, encoding="utf-8")
    print(f"Updated {path}")

def update_table02():
    path = ROOT / "paper" / "gen" / "table02_real_data_stability.tex"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            "denoting severe `Stable but Wrong' entrapment.",
            "satisfying the stability-accuracy discordance (SAD) criterion."
        )
        path.write_text(text, encoding="utf-8")
        print(f"Updated {path}")
    
    # Also update springer_manuscript table
    path_sp = ROOT / "springer_manuscript" / "gen" / "table02_real_data_stability.tex"
    if path_sp.exists():
        text = path_sp.read_text(encoding="utf-8")
        text = text.replace(
            "denoting severe `Stable but Wrong' entrapment.",
            "satisfying the stability-accuracy discordance (SAD) criterion."
        )
        path_sp.write_text(text, encoding="utf-8")
        print(f"Updated {path_sp}")

def update_script_make_stability_outputs():
    path = ROOT / "scripts" / "make_stability_outputs.py"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            "denoting severe `Stable but Wrong' entrapment.",
            "satisfying the stability-accuracy discordance (SAD) criterion."
        )
        text = text.replace(
            "PRE-SPECIFIED RULE (i):\\nSTABLE BUT WRONG ZONE\\n(Subsample Stab $\\\\geq 0.50$, Acc $\\\\leq 0.05$)",
            "PRE-SPECIFIED RULE (i):\\nSAD DISCORDANCE ZONE\\n(Subsample Stab $\\\\geq 0.50$, Acc $\\\\leq 0.05$)"
        )
        path.write_text(text, encoding="utf-8")
        print(f"Updated {path}")

def update_metadata():
    # README.md
    readme = ROOT / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        text = re.sub(
            r"# Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes",
            lambda m: f"# {NEW_TITLE}",
            text
        )
        text = re.sub(
            r"\*\*\"Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes\"\*\*",
            lambda m: f'**"{NEW_TITLE}"**',
            text
        )
        text = re.sub(
            r"title\s*=\s*\{Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes\}",
            lambda m: f"title     = {{{NEW_TITLE}}}",
            text
        )
        readme.write_text(text, encoding="utf-8")
        print(f"Updated {readme}")

    # CITATION.cff
    cff = ROOT / "CITATION.cff"
    if cff.exists():
        text = cff.read_text(encoding="utf-8")
        text = re.sub(
            r'title:\s*"Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes"',
            lambda m: f'title: "{NEW_TITLE}"',
            text
        )
        cff.write_text(text, encoding="utf-8")
        print(f"Updated {cff}")

    # pyproject.toml
    pyproject = ROOT / "pyproject.toml"
    if pyproject.exists():
        text = pyproject.read_text(encoding="utf-8")
        text = re.sub(
            r'description\s*=\s*"Reference implementation: Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes"',
            lambda m: f'description = "Reference implementation: {NEW_TITLE}"',
            text
        )
        pyproject.write_text(text, encoding="utf-8")
        print(f"Updated {pyproject}")

    # submission/COVER_LETTER.md
    cover = ROOT / "submission" / "COVER_LETTER.md"
    if cover.exists():
        text = cover.read_text(encoding="utf-8")
        text = text.replace(
            'Feature-Gated Bipartite Graph Ensembles for Stable Clustering in High-Dimensional Extreme Noise Regimes',
            NEW_TITLE
        )
        text = text.replace("the **stability trap**.", "the **stability-accuracy discordance**.")
        text = text.replace("The Stability Trap on Real and Synthetic Manifolds", "Stability-Accuracy Discordance on Real and Synthetic Manifolds")
        cover.write_text(text, encoding="utf-8")
        print(f"Updated {cover}")

    # STATE.json
    state = ROOT / "STATE.json"
    if state.exists():
        text = state.read_text(encoding="utf-8")
        text = re.sub(
            r'"title":\s*".*?"',
            lambda m: f'"title": "{NEW_TITLE}"',
            text
        )
        state.write_text(text, encoding="utf-8")
        print(f"Updated {state}")

if __name__ == "__main__":
    update_main_tex(ROOT / "paper" / "main.tex")
    update_main_tex(ROOT / "springer_manuscript" / "main.tex")
    update_table02()
    update_script_make_stability_outputs()
    update_metadata()
    print("Item 0 updates complete.")
