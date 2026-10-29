"""Fix missing \begin{enumerate} lines and remove NMI definition from paper/main.tex
"""
with open("paper/main.tex", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Restore \begin{enumerate} for Section 1 contributions
p1_before = "The principal contributions of this paper are organized as follows:\n\n    \\item \\textbf{Finite-sample falsification"
p1_after = "The principal contributions of this paper are organized as follows:\n\\begin{enumerate}\n    \\item \\textbf{Finite-sample falsification"
if p1_before not in text:
    # try single newline
    p1_before = "The principal contributions of this paper are organized as follows:\n    \\item \\textbf{Finite-sample falsification"
text = text.replace(p1_before, p1_after, 1)

# 2. Restore \begin{enumerate} for Remark 1
p2_before = "Assumption~\\ref{assump:multimodal} identifies four specific analytical regimes where marginal moment screening requires caution:\n\n    \\item \\textbf{Bounded Support"
p2_after = "Assumption~\\ref{assump:multimodal} identifies four specific analytical regimes where marginal moment screening requires caution:\n\\begin{enumerate}\n    \\item \\textbf{Bounded Support"
if p2_before not in text:
    p2_before = "Assumption~\\ref{assump:multimodal} identifies four specific analytical regimes where marginal moment screening requires caution:\n    \\item \\textbf{Bounded Support"
text = text.replace(p2_before, p2_after, 1)

# 3. Restore \begin{enumerate} for Parameter Configurations
p3_before = "Every stochastic component across all methods was systematically controlled through rigorous random seeding protocols:\n\n    \\item \\textbf{Benchmark Replications:}"
p3_after = "Every stochastic component across all methods was systematically controlled through rigorous random seeding protocols:\n\\begin{enumerate}\n    \\item \\textbf{Benchmark Replications:}"
if p3_before not in text:
    p3_before = "Every stochastic component across all methods was systematically controlled through rigorous random seeding protocols:\n    \\item \\textbf{Benchmark Replications:}"
text = text.replace(p3_before, p3_after, 1)

# 4. Remove NMI and keep only ARI under Evaluation Metrics
nmi_block_start = "Clustering partition recovery was quantitatively evaluated against ground-truth class labels using the chance-adjusted Adjusted Rand Index (ARI)~\\cite{hubert1985comparing}:"
nmi_block_end = "\\subsection{Statistical Analysis}\\label{sec:setup_stats}"

idx1 = text.find(nmi_block_start)
idx2 = text.find(nmi_block_end)

if idx1 != -1 and idx2 != -1:
    new_metrics = r"""Clustering partition recovery was quantitatively evaluated against ground-truth class labels using the chance-adjusted Adjusted Rand Index (ARI)~\cite{hubert1985comparing}:
\begin{equation}\label{eq:ari_def}
    \text{ARI}(\mathcal{U}, \mathcal{V}) = \frac{\sum_{i=1}^K \sum_{j=1}^C \binom{n_{ij}}{2} - \left[\sum_{i=1}^K \binom{a_i}{2} \sum_{j=1}^C \binom{b_j}{2}\right] / \binom{N}{2}}{\frac{1}{2}\left[\sum_{i=1}^K \binom{a_i}{2} + \sum_{j=1}^C \binom{b_j}{2}\right] - \left[\sum_{i=1}^K \binom{a_i}{2} \sum_{j=1}^C \binom{b_j}{2}\right] / \binom{N}{2}},
\end{equation}
where $n_{ij} = |u_i \cap v_j|$, $a_i = \sum_j n_{ij}$, and $b_j = \sum_i n_{ij}$ denote contingency overlaps between predicted clusters $\mathcal{U} = \{u_1, \dots, u_K\}$ and ground-truth classes $\mathcal{V} = \{v_1, \dots, v_C\}$. An ARI of $1.0$ indicates perfect agreement, $0.0$ corresponds to chance expectation under random assignment, and negative values denote recovery worse than chance.

"""
    text = text[:idx1] + new_metrics + text[idx2:]

# 5. Restore \begin{enumerate} for Convergence Analysis
p5_before = "To characterize algorithmic stability and resource efficiency, we analyzed the empirical convergence behavior of ICC-v2 across three primary operational parameters:\n\n    \\item \\textbf{Ensemble Size Convergence ($M$):}"
p5_after = "To characterize algorithmic stability and resource efficiency, we analyzed the empirical convergence behavior of ICC-v2 across three primary operational parameters:\n\\begin{enumerate}\n    \\item \\textbf{Ensemble Size Convergence ($M$):}"
if p5_before not in text:
    p5_before = "To characterize algorithmic stability and resource efficiency, we analyzed the empirical convergence behavior of ICC-v2 across three primary operational parameters:\n    \\item \\textbf{Ensemble Size Convergence ($M$):}"
text = text.replace(p5_before, p5_after, 1)

# 6. Restore \begin{enumerate} for Limitations failure modes
p6_before = "Our empirical examination establishes explicit structural failure modes of the ICC-v2 pipeline:\n\n    \\item \\textbf{Non-Linear Parity Structures (Madelon):}"
p6_after = "Our empirical examination establishes explicit structural failure modes of the ICC-v2 pipeline:\n\\begin{enumerate}\n    \\item \\textbf{Non-Linear Parity Structures (Madelon):}"
if p6_before not in text:
    p6_before = "Our empirical examination establishes explicit structural failure modes of the ICC-v2 pipeline:\n    \\item \\textbf{Non-Linear Parity Structures (Madelon):}"
text = text.replace(p6_before, p6_after, 1)

# 7. Restore \begin{enumerate} for Future Research Directions
p7_before = "These empirical limitations suggest concrete directions for future research:\n\n    \\item \\textbf{Non-Linear Subspace Gating:}"
p7_after = "These empirical limitations suggest concrete directions for future research:\n\\begin{enumerate}\n    \\item \\textbf{Non-Linear Subspace Gating:}"
if p7_before not in text:
    p7_before = "These empirical limitations suggest concrete directions for future research:\n    \\item \\textbf{Non-Linear Subspace Gating:}"
text = text.replace(p7_before, p7_after, 1)

with open("paper/main.tex", "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully updated paper/main.tex")
