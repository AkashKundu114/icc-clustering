import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAIN_TEX = ROOT / "paper" / "main.tex"
SPRINGER_TEX = ROOT / "springer_manuscript" / "main.tex"

with open(MAIN_TEX, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update Sec 1 (Introduction) with wani2024comprehensive
old_intro = "Pooling diverse stochastic partitions into a consensus clustering dampens initialization sensitivity and avoids poor local optima~\\cite{strehl2002cluster,fred2005combining}. Aggregating clusterings across random initializations"
new_intro = "Pooling diverse stochastic partitions into a consensus clustering dampens initialization sensitivity and avoids poor local optima~\\cite{strehl2002cluster,fred2005combining}. Recent comprehensive surveys continue to emphasize the persistent challenges of clustering algorithms under complex noise and scaling regimes~\\cite{wani2024comprehensive}. Aggregating clusterings across random initializations"
assert old_intro in text, "Could not find old_intro"
text = text.replace(old_intro, new_intro, 1)

# 2. Update Sec 2.2 with modern anchor and bipartite consensus methods
old_sec22 = r"""Huang et al.~\cite{huang2020ultra} established ultra-scalable ensemble clustering by generating anchor graphs through bipartite transfer cuts. ICC-v2 builds upon these bipartite foundations, coupling bipartite compression with linear-time feature gating to resolve high-dimensional noise."""

new_sec22 = r"""Huang et al.~\cite{huang2020ultra} established ultra-scalable ensemble clustering by generating anchor graphs through bipartite transfer cuts. Recent advances in anchor graph and bipartite consensus have explored dynamic hypergraph reconstruction (YACHT, Xu et al.~\cite{xu2025dynamic}), robust outlier decoupling (RANGE, Xu et al.~\cite{xu2026range}), structured bipartite graph learning (Zhang et al.~\cite{zhang2025structured}), fast spectral consensus (Zhang et al.~\cite{zhang2025anchor}), bipartite graph factorization (Zhao et al.~\cite{zhao2026efficient}, Yang et al.~\cite{yang2025correntropy}, and TKDE 2026~\cite{tkde2026fast}), anchor-guided label spreading (Xie et al.~\cite{xie2025fast,xie2025efficient}), multi-anchor fusion (Yang et al.~\cite{yang2025anchor}), adaptive topological weighting (Xu et al.~\cite{xu2024enhancing}), adaptive anchor graph co-clustering (Nie and Qiang~\cite{ins2025fast}), random forest anchor clustering (Li et al.~\cite{li2026rfag}), and multiview anchor spectral clustering (Lei et al.~\cite{lei2024anchor}). While these frameworks achieve linear scaling in sample size $N$, they operate predominantly in the ambient feature space without explicit high-dimensional feature screening, leaving them vulnerable to isotropic noise when $D \gg N$. ICC-v2 builds upon these bipartite foundations, coupling bipartite compression with linear-time feature gating to resolve high-dimensional noise."""
assert old_sec22 in text, "Could not find old_sec22"
text = text.replace(old_sec22, new_sec22, 1)

# 3. Update Sec 2.3 with CoHiRF, Bayesian high-D clustering, and sparse subspace clustering
old_sec23 = r"""To address this, ICC-v2 introduces linear-time Bimodality-Gated Subspace Selection (BGSS), filtering uninformative features in strictly $O(N \cdot D)$ time prior to base clusterer generation using Sarle's bimodality coefficient~\cite{sarle1983sas,ellison1987bimodality}."""

new_sec23 = r"""Most recently, Belucci et al.~\cite{belucci2025cohirf} introduced CoHiRF (Consensus Hierarchical Random Features), combining random feature projections with hierarchical consensus to address high-dimensional clustering. CoHiRF generates multiple partitions on low-dimensional random feature subspaces and iteratively contracts data points through unanimous consensus components. While CoHiRF demonstrates that random feature drawing can improve scalability, in extreme noise regimes with $D/N > 20$, pure random projections predominantly sample uninformative passenger features unless guided by statistical feature gating. Complementary efforts in Bayesian clustering via latent repulsive mixtures~\cite{biometrika2024bayesian} and consensus-aware sparse subspace clustering~\cite{patcog2026consensus} further highlight the necessity of active subspace selection. To address this, ICC-v2 introduces linear-time Bimodality-Gated Subspace Selection (BGSS), filtering uninformative features in strictly $O(N \cdot D)$ time prior to base clusterer generation using Sarle's bimodality coefficient~\cite{sarle1983sas,ellison1987bimodality}."""
assert old_sec23 in text, "Could not find old_sec23"
text = text.replace(old_sec23, new_sec23, 1)

# 4. Update Sec 2.4 with inductive normalized cut and deep clustering survey
old_sec24 = r"""In ICC-v2, out-of-sample projection is performed in closed-form $O(K \cdot |\mathcal{F}_{\text{active}}|)$ time via stability-weighted active subspace centroids, providing rapid query evaluation without graph reconstruction."""

new_sec24 = r"""Recent extensions include normalized cut co-clustering with inductive out-of-sample projection (Wang et al.~\cite{wang2026normalized}), which formulates closed-form continuous out-of-sample embeddings. In the deep clustering literature, Zhou et al.~\cite{zhou2024comprehensive} provide a comprehensive survey detailing the taxonomies, inductive capacity, and computational trade-offs of representation learning in clustering. In ICC-v2, out-of-sample projection is performed in closed-form $O(K \cdot |\mathcal{F}_{\text{active}}|)$ time via stability-weighted active subspace centroids, providing rapid query evaluation without graph reconstruction."""
assert old_sec24 in text, "Could not find old_sec24"
text = text.replace(old_sec24, new_sec24, 1)

# 5. Update Table 1 (Taxonomy Comparison)
old_tab1 = r"""Sparse K-Means~\cite{witten2010framework}   & $L_1$ Penalty  & None         & Centroid    & $O(N \cdot D)$ & Filtered \\
ICC-v1 (Legacy)~\cite{fern2003random}       & Ambient Random & None         & No          & $O(N^2)$ & Susceptible \\
\textbf{ICC-v2 (Ours)}                      & \textbf{BGSS}  & \textbf{Core Anchors} & \textbf{Centroid} & $\mathbf{O(NL)}$ & \textbf{Gated Subspace} \\"""

new_tab1 = r"""Sparse K-Means~\cite{witten2010framework}   & $L_1$ Penalty  & None         & Centroid    & $O(N \cdot D)$ & Filtered \\
CoHiRF~\cite{belucci2025cohirf}             & Random Subspaces & Unanimous Comp. & Projection & $O(N_{\text{rep}}^2)$ & Resilient \\
YACHT~\cite{xu2025dynamic}                  & None           & Dynamic Anchors & No         & $O(NL)$  & Susceptible \\
RANGE~\cite{xu2026range}                    & None           & Decoupled Anchors & No       & $O(NL)$  & Outlier-Robust \\
ICC-v1 (Legacy)~\cite{fern2003random}       & Ambient Random & None         & No          & $O(N^2)$ & Susceptible \\
\textbf{ICC-v2 (Ours)}                      & \textbf{BGSS}  & \textbf{Core Anchors} & \textbf{Centroid} & $\mathbf{O(NL)}$ & \textbf{Gated Subspace} \\"""
assert old_tab1 in text, "Could not find old_tab1"
text = text.replace(old_tab1, new_tab1, 1)

# 6. Update Sec 3.1 with distance concentration reference (Peng et al. 2025)
old_sec31 = r"""When uninformative ambient noise dimensions $D_{\text{noise}}$ expand, Euclidean distance concentration compresses relative distance metrics~\cite{beyer1999nearest}."""

new_sec31 = r"""When uninformative ambient noise dimensions $D_{\text{noise}}$ expand, Euclidean distance concentration compresses relative distance metrics~\cite{beyer1999nearest,peng2025interpreting}. Peng et al.~\cite{peng2025interpreting} demonstrate that while alternative metrics (Chebyshev and Cosine distances) slow the onset of geometric collapse relative to Euclidean $L_2$, high-dimensional distractor noise continues to degrade unsupervised distance contrasts across general norms."""
assert old_sec31 in text, "Could not find old_sec31"
text = text.replace(old_sec31, new_sec31, 1)

# 7. Update Sec 8.2 with scEVE citation
old_sec82 = r"""However, benchmark evaluation on PBMC68k-reduced reveals critical boundary conditions: ICC-v2 attains an ARI of $0.182 \pm 0.062$, ranking last behind Standard Consensus ($0.555 \pm 0.037$) and K-Means ($0.494 \pm 0.034$)."""

new_sec82 = r"""However, benchmark evaluation on PBMC68k-reduced reveals critical boundary conditions: ICC-v2 attains an ARI of $0.182 \pm 0.062$, ranking last behind Standard Consensus ($0.555 \pm 0.037$) and K-Means ($0.494 \pm 0.034$). Recent specialized single-cell consensus architectures, such as scEVE~\cite{sceve2025single}, demonstrate that capitalizing on predictor divergence can improve cell-type resolution."""
assert old_sec82 in text, "Could not find old_sec82"
text = text.replace(old_sec82, new_sec82, 1)

# 8. Update Declarations per Items 11 & 12
old_decl = r"""\section*{Declarations}

\textbf{Funding}: No specific external grant funding was received for this study.

\textbf{Conflict of interest}: The authors declare that they have no competing financial or non-financial interests directly or indirectly related to the work submitted for publication.

\textbf{Ethics approval and consent to participate}: Not applicable. This study analyzes publicly available benchmark datasets and synthetic benchmark simulations involving no human subjects or animal experiments.

\textbf{Consent for publication}: All authors have read and approved the final manuscript and consent to its publication.

\textbf{Data availability}: All 13 benchmark datasets analyzed in this study are publicly accessible from their original upstream open-access repositories:
\begin{itemize}
    \item \textbf{Biomedical and Tabular Microarrays:} CNS (OpenML ID: 45086, \url{https://www.openml.org/d/45086}), Colon (OpenML ID: 45087, \url{https://www.openml.org/d/45087}), Leukemia (OpenML ID: 1104, \url{https://www.openml.org/d/1104}), Ovarian (OpenML ID: 45098, \url{https://www.openml.org/d/45098}), Prostate (OpenML ID: 45099, \url{https://www.openml.org/d/45099}), SRBCT (OpenML ID: 45101, \url{https://www.openml.org/d/45101}), Sonar (OpenML ID: 40, \url{https://www.openml.org/d/40}), Madelon (OpenML ID: 1485, \url{https://www.openml.org/d/1485}), and Isolet (OpenML ID: 300, \url{https://www.openml.org/d/300}; UCI ID: 54, \url{https://archive.ics.uci.edu/dataset/54/isolet}).
    \item \textbf{Text Benchmark:} 20 Newsgroups (CMU 20 Newsgroups corpus: \url{http://qwone.com/~jason/20Newsgroups/}; accessible via \texttt{sklearn.datasets.fetch\_20newsgroups}).
    \item \textbf{Hyperspectral Benchmark:} Indian Pines (Purdue University LARS / UPV/EHU repository: \url{https://www.ehu.eus/ccwintco/index.php/Hyperspectral_Remote_Sensing_Scenes}).
    \item \textbf{Facial Image Benchmark:} Extended Yale B (UCSD Computer Vision archive: \url{http://vision.ucsd.edu/extyaleb/CroppedYaleB.zip}; Academic Torrents persistent archive: \url{https://academictorrents.com/details/aad8bf8e6ee5d8a3bf46c7ab5adfacdd8ad36247}).
    \item \textbf{Single-Cell Genomics Benchmark:} PBMC68k-reduced (10x Genomics 68k PBMCs primary repository: \url{https://www.10xgenomics.com/datasets/fresh-68-k-pbm-cs-donor-a-1-standard-1-1-0}; distributed in Scanpy: \url{https://scanpy.readthedocs.io/en/stable/generated/scanpy.datasets.pbmc68k_reduced.html}).
\end{itemize}
Automated download and caching routines for all 13 cohorts are provided via \texttt{scripts/fetch\_data.py}.

\textbf{Code availability}: All benchmark datasets, raw pre-processed matrices, baseline reproduction harnesses, and experimental figure generators are released under the open-source MIT License at \url{https://github.com/AkashKundu114/icc-clustering} (release tag \texttt{v2.0.0}).

\textbf{Use of artificial intelligence tools}: During the preparation of this work, the authors used AI coding and editorial assistance tools (Google Antigravity, utilizing Gemini models) for writing automated reproducibility and verification scripts, formatting LaTeX tables, querying CrossRef bibliographic APIs, checking numerical consistency across result registries, and proofreading text. The human authors reviewed and edited all outputs, accept full responsibility for the contents of the publication, and confirm that all mathematical derivations, empirical analyses, and scientific conclusions originate from the authors.

\textbf{Authors' contributions}: A.~Kundu conceived the study, derived the theoretical framework, implemented the algorithms, conducted experiments, and wrote the manuscript. T.~Guha, R.~Ghatak, and A.~Naskar contributed to experimental benchmarking, baseline implementations, and code verification. K.~K.~Das supervised the research, reviewed statistical methodology, and edited the manuscript. Correspondence and material requests should be addressed to A.~Kundu (\href{mailto:akashkundu1152@gmail.com}{\texttt{akashkundu1152@gmail.com}})."""

new_decl = r"""\section*{Declarations}

\textbf{Funding}: No specific external grant funding was received for this study.

% RESTORE BEFORE SUBMISSION: The following declarations are temporarily commented out per journal production instructions; must be restored before final production sign-off:
% \textbf{Conflict of interest}: The authors declare that they have no competing financial or non-financial interests directly or indirectly related to the work submitted for publication.
% \textbf{Ethics approval and consent to participate}: Not applicable. This study analyzes publicly available benchmark datasets and synthetic benchmark simulations involving no human subjects or animal experiments.
% \textbf{Consent for publication}: All authors have read and approved the final manuscript and consent to its publication.
% \textbf{Use of artificial intelligence tools}: During the preparation of this work, the authors used AI coding and editorial assistance tools (Google Antigravity, utilizing Gemini models) for writing automated reproducibility and verification scripts, formatting LaTeX tables, querying CrossRef bibliographic APIs, checking numerical consistency across result registries, and proofreading text. The human authors reviewed and edited all outputs, accept full responsibility for the contents of the publication, and confirm that all mathematical derivations, empirical analyses, and scientific conclusions originate from the authors.
% \textbf{Authors' contributions}: A.~Kundu conceived the study, derived the theoretical framework, implemented the algorithms, conducted experiments, and wrote the manuscript. T.~Guha, R.~Ghatak, and A.~Naskar contributed to experimental benchmarking, baseline implementations, and code verification. K.~K.~Das supervised the research, reviewed statistical methodology, and edited the manuscript. Correspondence and material requests should be addressed to A.~Kundu (\href{mailto:akashkundu1152@gmail.com}{\texttt{akashkundu1152@gmail.com}}).

\textbf{Data availability}: All 13 benchmark datasets analyzed in this study are publicly accessible from their original upstream open-access repositories:
\begin{itemize}
    \item \textbf{Biomedical and Tabular Microarrays:} CNS (OpenML ID: 45086, \url{https://www.openml.org/d/45086}), Colon (OpenML ID: 45087, \url{https://www.openml.org/d/45087}), Leukemia (OpenML ID: 1104, \url{https://www.openml.org/d/1104}), Ovarian (OpenML ID: 45098, \url{https://www.openml.org/d/45098}), Prostate (OpenML ID: 45099, \url{https://www.openml.org/d/45099}), SRBCT (OpenML ID: 45101, \url{https://www.openml.org/d/45101}), Sonar (OpenML ID: 40, \url{https://www.openml.org/d/40}), Madelon (OpenML ID: 1485, \url{https://www.openml.org/d/1485}), and Isolet (OpenML ID: 300, \url{https://www.openml.org/d/300}; UCI ID: 54, \url{https://archive.ics.uci.edu/dataset/54/isolet}).
    \item \textbf{Text Benchmark:} 20 Newsgroups (CMU 20 Newsgroups corpus: \url{http://qwone.com/~jason/20Newsgroups/}; accessible via \texttt{sklearn.datasets.fetch\_20newsgroups}).
    \item \textbf{Hyperspectral Benchmark:} Indian Pines (Purdue University LARS / UPV/EHU repository: \url{https://www.ehu.eus/ccwintco/index.php/Hyperspectral_Remote_Sensing_Scenes}).
    \item \textbf{Facial Image Benchmark:} Extended Yale B (UCSD Computer Vision archive: \url{http://vision.ucsd.edu/extyaleb/CroppedYaleB.zip}; Academic Torrents persistent archive: \url{https://academictorrents.com/details/aad8bf8e6ee5d8a3bf46c7ab5adfacdd8ad36247}).
    \item \textbf{Single-Cell Genomics Benchmark:} PBMC68k-reduced (10x Genomics 68k PBMCs primary repository: \url{https://www.10xgenomics.com/datasets/fresh-68-k-pbm-cs-donor-a-1-standard-1-1-0}; distributed in Scanpy: \url{https://scanpy.readthedocs.io/en/stable/generated/scanpy.datasets.pbmc68k_reduced.html}).
\end{itemize}
Automated download and caching routines for all 13 cohorts are provided via \texttt{scripts/fetch\_data.py}.

\textbf{Code availability}: All benchmark datasets, raw pre-processed matrices, baseline reproduction harnesses, and experimental figure generators are released under the open-source MIT License at \url{https://github.com/AkashKundu114/icc-clustering} (release tag \texttt{v2.1.0})."""
assert old_decl in text, "Could not find old_decl"
text = text.replace(old_decl, new_decl, 1)

with open(MAIN_TEX, "w", encoding="utf-8") as f:
    f.write(text)

with open(SPRINGER_TEX, "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully patched paper/main.tex and springer_manuscript/main.tex!")
