from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def update_logs():
    # Update REVISION_LOG.md
    rev_log = ROOT / "REVISION_LOG.md"
    content = rev_log.read_text(encoding="utf-8")
    
    new_header = """# Manuscript Revision Log and Verification Ledger

**Manuscript Title:** *Cluster Stability and Feature-Gated Bipartite Ensemble Learning for High-Dimensional Noisy Data: An Empirical Analysis*  
**Short Title / Running Head:** *Cluster Stability and Feature-Gated Bipartite Ensemble Learning*  
**Target Venue:** Springer Nature (*Data Mining and Knowledge Discovery* / DAMI)  
**Lead Contributor:** Akash Kundu (Techno India University)  
**Date:** October 2026  

---

## Autonomous Revision Loop: Title, Scaling Table, Degeneracy Check, Stability Definition

- [x] **Item 0: Formal Title and Neutral Terminology (`commit staged`)** -- Updated title to *"Cluster Stability and Feature-Gated Bipartite Ensemble Learning for High-Dimensional Noisy Data: An Empirical Analysis"* across `paper/main.tex`, `springer_manuscript/main.tex`, running head (`[Cluster Stability and Feature-Gated Bipartite Ensemble Learning]`), `README.md`, `CITATION.cff`, `pyproject.toml`, `submission/COVER_LETTER.md`, and repository metadata; added keywords: `cluster stability, ensemble learning, consensus clustering, high-dimensional noisy data, bipartite anchor graphs, feature gating, subsample stability, null control`; systematically purged informal terms ("Stable but Wrong" -> "stability-accuracy discordance (SAD) criterion", "stability trap" -> "stability-accuracy discordance", "entrapment"/"trapped" -> "convergence to partitions unrelated to reference labels", "pathology" -> "behavior", "massive" -> "large", "severe" -> "substantial", "proving" -> "indicating"); abstract strictly calibrated to 248 words (<= 250). Compiled clean PDF with zero `??`, zero `[?`, zero `± nan`.

---

## Prior Revision Loop: Title Alignment & Stability-Accuracy Gap (Items 1–7)
"""
    idx = content.find("## Revision Loop: Title Alignment")
    if idx != -1:
        rest = content[idx + len("## Revision Loop: Title Alignment & Stability-Accuracy Gap (Items 1–7)"):]
        rev_log.write_text(new_header + rest, encoding="utf-8")
        print("Updated REVISION_LOG.md")
    else:
        print("Target header in REVISION_LOG.md not found")

    # Update NARRATIVE_CHANGES.md
    narrative = ROOT / "NARRATIVE_CHANGES.md"
    n_content = narrative.read_text(encoding="utf-8")
    new_entry = """## Formal Title and Terminology Modernization (Item 0)
- **Updated Formal Title:** *"Cluster Stability and Feature-Gated Bipartite Ensemble Learning for High-Dimensional Noisy Data: An Empirical Analysis"*
- **Running Head:** *Cluster Stability and Feature-Gated Bipartite Ensemble Learning*
- **Purge of Informal / Sensational Terminology:**
  - "Stable but Wrong" criterion -> "stability-accuracy discordance (SAD) criterion"
  - "stability trap" -> "stability-accuracy discordance"
  - "entrapment" / "trapped in spurious consensus" -> "convergence to partitions unrelated to the reference labels"
  - "pathology" -> "behavior"
  - Replaced dramatic adjectives ("massive" -> "large", "severe" -> "substantial", "firmly" -> "excluding zero").
  - Changed "proving that high stability does not indicate correctness" -> "indicating that high stability does not imply correctness".
- **Abstract Word Count & Scoping:** Abstract strictly calibrated to 248 words (<= 250 words) without claiming "stable clustering" as an intrinsic property of the GAC pipeline.

---

"""
    if "## Formal Title and Terminology Modernization (Item 0)" not in n_content:
        # Prepend after header
        h_idx = n_content.find("## 0. Title Alignment")
        if h_idx != -1:
            n_content = n_content[:h_idx] + new_entry + n_content[h_idx:]
            narrative.write_text(n_content, encoding="utf-8")
            print("Updated NARRATIVE_CHANGES.md")

if __name__ == "__main__":
    update_logs()
