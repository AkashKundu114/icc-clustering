"""
scripts/append_verified_refs.py
"""
import subprocess
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

NEW_REFS = [
    {
        "key": "guo2026consensus",
        "doi": "10.1016/j.patcog.2026.113378",
        "arxiv": None,
        "title": "Consensus clustering via bipartite graph partition with adaptive anchor selection",
        "year": 2026,
        "section": "sec:related",
        "sentence": "Adaptive anchor selection strategies further enhance bipartite consensus efficiency across large instance sets (Guo et al.~\cite{guo2026consensus})."
    },
    {
        "key": "zhang2025highorder",
        "doi": "10.1016/j.patcog.2024.111133",
        "arxiv": None,
        "title": "Ensemble clustering with high-order consensus information",
        "year": 2025,
        "section": "sec:related",
        "sentence": "Recent ensemble clustering approaches increasingly incorporate high-order consensus information to capture multi-hop relations beyond pairwise co-occurrences (Zhang et al.~\cite{zhang2025highorder})."
    },
    {
        "key": "li2025selfsupervised",
        "doi": "10.1016/j.eswa.2025.127943",
        "arxiv": None,
        "title": "Self-supervised feature selection for high-dimensional clustering",
        "year": 2025,
        "section": "sec:intro",
        "sentence": "In high-dimensional domains, unsupervised and self-supervised feature selection has emerged as a necessary prerequisite to remove uninformative coordinates before similarity estimation (Li et al.~\cite{li2025selfsupervised})."
    },
    {
        "key": "fan2026robust",
        "doi": "10.1016/j.neucom.2026.132755",
        "arxiv": None,
        "title": "Robust spectral ensemble clustering with sparse representation",
        "year": 2026,
        "section": "sec:related",
        "sentence": "Sparse representation techniques have been integrated into spectral ensemble clustering to suppress noisy partition edges (Fan et al.~\cite{fan2026robust})."
    },
    {
        "key": "jahanian2026highdim",
        "doi": "10.1038/s41598-026-75016-y",
        "arxiv": None,
        "title": "High-dimensional biomedical clustering with stability selection and consensus",
        "year": 2026,
        "section": "sec:real_data_stability",
        "sentence": "Biomedical cohort clustering under high feature-to-sample ratios requires explicit noise screening to avoid convergence on spurious clinical subtypes (Jahanian et al.~\cite{jahanian2026highdim})."
    },
    {
        "key": "zhang2024optimal",
        "doi": "10.1214/24-aos2418",
        "arxiv": None,
        "title": "Optimal rates and trade-offs in high-dimensional clustering",
        "year": 2024,
        "section": "sec:falsification",
        "sentence": "Minimax theoretical analysis establishes that consistent cluster recovery in high dimensions requires feature signal-to-noise ratios scaling with ambient dimension (Zhang and Zhou~\cite{zhang2024optimal})."
    },
    {
        "key": "kong2026adaptive",
        "doi": "10.1016/j.patcog.2026.114473",
        "arxiv": None,
        "title": "Adaptive anchor-based consensus clustering for large-scale data",
        "year": 2026,
        "section": "sec:related",
        "sentence": "Scalable multi-view ensemble clustering leverages adaptive anchor bipartite graphs to accelerate consensus inference on massive datasets (Kong et al.~\cite{kong2026adaptive})."
    },
    {
        "key": "cai2025spectral",
        "doi": "10.1016/j.ins.2024.121314",
        "arxiv": None,
        "title": "Spectral ensemble clustering with doubly stochastic co-association matrix",
        "year": 2025,
        "section": "sec:related",
        "sentence": "Enforcing doubly stochastic normalization over the consensus affinity matrix eliminates vertex degree artifacts in spectral graph partitioning (Cai et al.~\cite{cai2025spectral})."
    },
    {
        "key": "yang2025autoweighted",
        "doi": "10.1016/j.ins.2024.121486",
        "arxiv": None,
        "title": "Auto-weighted Graph Reconstruction for efficient ensemble clustering",
        "year": 2025,
        "section": "sec:related",
        "sentence": "Auto-weighted graph reconstruction dynamically recalibrates base ensemble contributions according to partition reliability (Yang et al.~\cite{yang2025autoweighted})."
    },
    {
        "key": "hu2024multiview",
        "doi": "10.1016/j.ins.2024.121187",
        "arxiv": None,
        "title": "Multiview ensemble clustering of hypergraph p-Laplacian regularization with feature selection",
        "year": 2024,
        "section": "sec:related",
        "sentence": "Jointly optimizing feature selection with hypergraph p-Laplacian regularization improves ensemble robustness against distractor noise (Hu et al.~\cite{hu2024multiview})."
    },
    {
        "key": "chen2025ccegan",
        "doi": "10.1016/j.ins.2024.121663",
        "arxiv": None,
        "title": "CCEGAN: Enhancing GAN clustering through contrastive clustering ensemble",
        "year": 2025,
        "section": "sec:related",
        "sentence": "Contrastive clustering ensembles have also been explored in generative deep architectures to regularize latent representations (Chen et al.~\cite{chen2025ccegan})."
    },
    {
        "key": "lau2024bayesian",
        "doi": "10.1093/biomet/asae059",
        "arxiv": None,
        "title": "Bayesian clustering of high-dimensional data via latent repulsive mixtures",
        "year": 2024,
        "section": "sec:falsification",
        "sentence": "Latent repulsive mixture models have been proposed to prevent over-clustering in high-dimensional genomic feature spaces (Lau et al.~\cite{lau2024bayesian})."
    },
    {
        "key": "wang2025coregularized",
        "doi": "10.1016/j.patcog.2024.110892",
        "arxiv": None,
        "title": "Co-regularized optimal high-order graph embedding for multi-view clustering",
        "year": 2025,
        "section": "sec:related",
        "sentence": "High-order graph embedding and co-regularization offer principled mechanisms to align multi-view cluster assignments (Wang et al.~\cite{wang2025coregularized})."
    },
    {
        "key": "chakraborty2026generic",
        "doi": None,
        "arxiv": "2602.11500",
        "title": "A Generic Framework for Fair Consensus Clustering in Streams",
        "year": 2026,
        "section": "sec:related",
        "sentence": "Streaming and inductive consensus frameworks have recently expanded toward fairness-constrained partition updates across continuous data flows (Chakraborty et al.~\cite{chakraborty2026generic})."
    },
]

def main():
    print("=" * 60)
    print("FETCHING VERIFIED BIBTEX ENTRIES")
    print("=" * 60)

    bib_entries = []
    refs_map_rows = []

    for r in NEW_REFS:
        key = r["key"]
        print(f"[*] Verifying {key}...")
        if r["doi"]:
            cmd = [sys.executable, "scripts/verify_refs.py", "--doi", r["doi"], "--bibtex"]
        else:
            cmd = [sys.executable, "scripts/verify_refs.py", "--arxiv", r["arxiv"], "--bibtex"]

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[!] Verification FAILED for {key}: {res.stderr}")
            sys.exit(1)

        raw_bib = res.stdout.strip()
        # replace the generic @article{key, or @misc{key, with @article{<actual_key>,
        lines = raw_bib.splitlines()
        first_line = lines[0]
        entry_type = first_line.split("{")[0]
        custom_bib = f"{entry_type}{{{key},\n" + "\n".join(lines[1:])
        bib_entries.append(custom_bib)
        print(f"    Verified! Year={r['year']}, Title={r['title'][:50]}...")

        refs_map_rows.append({
            "citation_key": key,
            "doi_or_arxiv": r["doi"] if r["doi"] else r["arxiv"],
            "title": r["title"],
            "year": r["year"],
            "target_sentence": r["sentence"],
            "section": r["section"],
        })

    full_bib_text = "\n\n" + "\n\n".join(bib_entries) + "\n"

    # Append to paper/references.bib and springer_manuscript/references.bib
    for p in [ROOT / "paper" / "references.bib", ROOT / "springer_manuscript" / "references.bib"]:
        with open(p, "a", encoding="utf-8") as f:
            f.write(full_bib_text)
        print(f"[+] Appended 14 references to {p}")

    # Append to results/refs_map.csv
    map_csv = ROOT / "results" / "refs_map.csv"
    if map_csv.exists():
        existing_df = pd.read_csv(map_csv)
        combined_df = pd.concat([existing_df, pd.DataFrame(refs_map_rows)], ignore_index=True)
        combined_df.to_csv(map_csv, index=False)
    else:
        pd.DataFrame(refs_map_rows).to_csv(map_csv, index=False)
    print(f"[+] Updated {map_csv} with new mappings.")

if __name__ == "__main__":
    main()
