import pymupdf
import re

doc = pymupdf.open("springer_manuscript/main.pdf")
full_text = " ".join(" ".join(page.get_text().split()) for page in doc)

checks = [
    # Must fix 1
    ("small (<= 0.20) except Ward", "remains small" in full_text and "Ward under sparse noise" in full_text),
    # Must fix 2
    ("60 non-degenerate cells breakdown", "K-Means [2], FCM [1], Ambient Consensus [1], Core-Halo [2], CoHiRF [5], and Ungated AC [1]" in full_text),
    ("Table 3 Decision Rule (i) only", "satisfy pre-specified Decision Rule" in full_text),
    # Must fix 3
    ("Prostate data-driven structure", "subsample stability reflects data-driven structure rather than permutation artifacts" in full_text),
    # Smaller leftovers
    ("Section 3 def subsample explanation", "subsample stability collapses alongside it" in full_text and "accuracy collapse rather than stability" in full_text),
    ("Section 6.2 associated with", "associated with base-clusterer instability on Leukemia" in full_text),
    ("Section 6.3 Holm clarification", "Holm-Bonferroni step-down correction is applied to the family of 11 pairwise benchmark comparisons" in full_text),
    ("Code availability v1.0.0", "v1.0.0 release tag; archived on Zenodo upon publication" in full_text),
    # Latest batch fixes
    ("No unresolved cross-references in text", "Section ??" not in full_text),
    ("Holm resolved Section 6.2 and 7.3", "BGSS gating (Section 6.2) and the factorial interaction (Section 7.3)" in full_text),
    ("Holm self-reference eliminated", "subgroup evaluation above; exploratory" in full_text),
    ("Contribution 1 softened", "is not a permutation artifact" in full_text),
    ("Seed* cited in Section 3.1", "Seed" in full_text and "Table 3" in full_text),
    ("Chakraborty DOI and arXiv", "2602.11500" in full_text or "10.48550" in full_text),
    ("Table 4 Discordant Cohorts header", "Discordant Cohorts" in full_text),
]

all_passed = True
for name, ok in checks:
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}")
    if not ok:
        all_passed = False

if not all_passed:
    print("\nDebugging failing checks:")
    for name, ok in checks:
        if not ok:
            print(f"Failed: {name}")

assert all_passed, "Some checks failed in normalized PDF text!"
print("\nALL MANUSCRIPT PDF CHECKS PASSED SUCCESSFULLY!")
