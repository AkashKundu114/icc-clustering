# -*- coding: utf-8 -*-
from pathlib import Path

edits = [
    (
        r"Materializing $S$ imposes quadratic memory scaling $O(N^2)$, becoming prohibitive on modern large-scale datasets ($N \ge 10^5$). Furthermore, the formulation is strictly transductive: assigning held-out query instances $\mathcal{X}_{\text{test}}$ necessitates reconstructing the co-association matrix and re-executing spectral graph partitioning over $N + |\mathcal{X}_{\text{test}}|$ vertices in $O((N + |\mathcal{X}_{\text{test}}|)^2)$ time.",
        r"Materializing $S$ imposes quadratic memory scaling $O(N^2)$, becoming prohibitive on large datasets ($N \ge 10^5$). In addition, canonical consensus is strictly transductive: assigning held-out query instances $\mathcal{X}_{\text{test}}$ requires reconstructing the co-association matrix and re-executing spectral graph partitioning over $N + |\mathcal{X}_{\text{test}}|$ vertices in $O((N + |\mathcal{X}_{\text{test}}|)^2)$ time."
    ),
    (
        r"On cohorts with weak marginal separation (Prostate $\text{ARI}=0.012$, CNS $\text{ARI}=0.021$), zero-inflated scRNA-seq counts, sparse text term-matrices, and non-linear parity (Madelon XOR), GAC attenuates the gap but exhibits low accuracy without detectable marginal structure, underscoring that consensus cannot recover clusters without detectable marginal structure.",
        r"On cohorts with weak marginal separation (Prostate $\text{ARI}=0.012$, CNS $\text{ARI}=0.021$), zero-inflated scRNA-seq counts, sparse text term-matrices, and non-linear parity (Madelon XOR), GAC attenuates the gap but exhibits low accuracy, showing that consensus cannot recover clusters when marginal separations are absent."
    ),
    (
        r"Furthermore, as detailed in Supplementary Table~\ref{tab:degeneracy_audit}, CoHiRF exhibits high subsample degeneracy across multiple cohorts",
        r"As detailed in Supplementary Table~\ref{tab:degeneracy_audit}, CoHiRF also exhibits high subsample degeneracy across multiple cohorts"
    ),
    (
        r"Furthermore, empirical ablation (Section~\ref{sec:ablation}, Table~\ref{tab:component_contributions}) confirms that determinacy-selected anchors achieve accuracy statistically indistinguishable from uniform random anchors ($V_5$ vs. $V_4$: $\Delta = +0.019$, 95\% CI: $[-0.039, +0.082]$), establishing that bipartite graph compression rather than determinacy anchor selection is the primary operational driver.",
        r"Empirical ablation (Section~\ref{sec:ablation}, Table~\ref{tab:component_contributions}) confirms that determinacy-selected anchors achieve accuracy statistically indistinguishable from uniform random anchors ($V_5$ vs. $V_4$: $\Delta = +0.019$, 95\% CI: $[-0.039, +0.082]$), showing that bipartite graph compression rather than determinacy anchor selection is the primary operational driver."
    ),
    (
        r"Furthermore, directly comparing BGSS against matched random subspace gating ($|\mathcal{F}_{\text{active}}| = \lfloor \alpha D \rfloor$, Exp~8c, evaluated on the 30 benchmark seeds $\{0, \dots, 29\}$ across the six cohorts) reveals that BGSS attains a subgroup mean of $0.217$ versus $0.155$ for random gating (a paired gain of $\Delta = +0.062$, 95\% dataset-clustered bootstrap CI $[+0.013, +0.142]$, Wilcoxon $W = 1.0, p = 0.0625$).",
        r"Direct comparison of BGSS against matched random subspace gating ($|\mathcal{F}_{\text{active}}| = \lfloor \alpha D \rfloor$, Exp~8c, evaluated on the 30 benchmark seeds $\{0, \dots, 29\}$ across the six cohorts) shows that BGSS attains a subgroup mean of $0.217$ versus $0.155$ for random gating (a paired gain of $\Delta = +0.062$, 95\% dataset-clustered bootstrap CI $[+0.013, +0.142]$, Wilcoxon $W = 1.0, p = 0.0625$)."
    ),
    (
        r"On the Leukemia cohort ($N=72, D=7{,}129$), GAC pipeline attains an ARI of $0.600 \pm 0.367$, with 22 of 30 seeds ($73.3\%$) exceeding $0.50$ recovery (median $0.787$). On SRBCT ($N=83, D=2{,}308$), it achieves $0.546 \pm 0.102$ ($21/30$ seeds above $0.50$). Furthermore, BGSS identifies 27 of 50 diagnostic markers ($54.0\%$) purely unsupervised.",
        r"On the Leukemia cohort ($N=72, D=7{,}129$), GAC pipeline attains an ARI of $0.600 \pm 0.367$, with 22 of 30 seeds ($73.3\%$) exceeding $0.50$ recovery (median $0.787$). On SRBCT ($N=83, D=2{,}308$), it achieves $0.546 \pm 0.102$ ($21/30$ seeds above $0.50$), with BGSS identifying 27 of 50 diagnostic markers ($54.0\%$) in an unsupervised manner."
    )
]

def main():
    for p in [Path('paper/main.tex'), Path('springer_manuscript/main.tex')]:
        text = p.read_text(encoding='utf-8')
        for i, (old, new) in enumerate(edits, 1):
            if old in text:
                text = text.replace(old, new)
                print(f"[+] Applied edit {i} in {p}")
            else:
                print(f"[-] Edit {i} target not found in {p}")
        p.write_text(text, encoding='utf-8')

if __name__ == '__main__':
    main()
