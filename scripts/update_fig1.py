from pathlib import Path

targets = [
    Path(r"D:\Final Year Project\springer_manuscript\main.tex"),
    Path(r"D:\Final Year Project\paper\main.tex")
]

old_caption_part = r"\caption{Conceptual overview of the high-dimensional noise dilemma and the Gated Anchor Consensus (GAC) diagnostic pipeline."
new_caption = (
    r"\caption{Conceptual dilemma of high-dimensional clustering and the stability-accuracy discordance trap. "
    r"(a) Ground-truth cluster geometry in a low-dimensional signal subspace ($d=2$). "
    r"(b) Geometric collapse when submerged in high-dimensional distractor noise ($D=2{,}000$), illustrating "
    r"distance concentration where pairwise contrast disappears ($(d_{\max}-d_{\min})/d_{\min} \to 0$ as $D \to \infty$) "
    r"and base clusterers repeatedly converge onto arbitrary noise manifolds. "
    r"(c) Marginal feature screening (BGSS) separating bimodal signal coordinates from unimodal background noise. "
    r"(d) Inductive query mapping assigning unseen observations in $O(K \cdot |\mathcal{F}_{\text{active}}|)$ time "
    r"without consensus graph recomputation (see Section~\ref{sec:methodology} and Algorithm~\ref{alg:iccv2} for the full execution flow).}"
)

for t in targets:
    txt = t.read_text(encoding="utf-8")
    # find \begin{figure*}[!t] around line 70
    start = txt.find(old_caption_part)
    if start != -1:
        end = txt.find(r"\label{fig:conceptual_overview}", start)
        txt = txt[:start] + new_caption + "\n" + txt[end:]
        t.write_text(txt, encoding="utf-8")
        print(f"Updated Fig 1 caption in {t}")
    else:
        print(f"Old Fig 1 not found in {t}")
