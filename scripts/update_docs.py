"""Update markdown documentation files across the repository for GitHub readiness."""

import re

def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Test badge
    old_badge = "[![Tests: Passing](https://img.shields.io/badge/pytest-86%2F86%20passed-brightgreen.svg)]()"
    new_badge = (
        "[![Tests: Passing](https://img.shields.io/badge/pytest-94%2F94%20passed-brightgreen.svg)]()\n"
        "[![References: 80.85% Recent (2024-2026)](https://img.shields.io/badge/references-80.85%25%20recent%20(2024--2026)-success.svg)]()"
    )
    if old_badge in content:
        content = content.replace(old_badge, new_badge)

    # 2. Reproducing references check
    old_reproduce = "python scripts/reproduce.py --scope smoke"
    new_reproduce = (
        "python scripts/reproduce.py --scope smoke\n\n"
        "# Verify bibliography against CrossRef and arXiv APIs (80.85% recent 2024-2026, exit code 0)\n"
        "python scripts/verify_refs.py refs.bib --out results/refs_report.csv --manual refs_manual.csv"
    )
    if old_reproduce in content and "python scripts/verify_refs.py" not in content:
        content = content.replace(old_reproduce, new_reproduce)

    # 3. Governance section
    old_gov = "100% CrossRef API reference verification audit ([`REFS_AUDIT.md`](governance/preregistration/REFS_AUDIT.md), [`REFS_AUDIT.csv`](governance/preregistration/REFS_AUDIT.csv))."
    new_gov = (
        "100% CrossRef & arXiv API verification audit: 47 references, 38 published 2024–2026 (80.85%), strictly single-cited at first mention "
        "([`REFCHECK_LOG.md`](REFCHECK_LOG.md), [`results/refs_report.csv`](results/refs_report.csv), [`results/refs_map.csv`](results/refs_map.csv))."
    )
    if old_gov in content:
        content = content.replace(old_gov, new_gov)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("README.md updated.")

def update_tests_readme():
    with open("tests/README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Update test count from 86 to 94
    content = content.replace("Total Tests:* 86 passing", "Total Tests:* 94 passing")
    content = content.replace("To run all 86 tests", "To run all 94 tests")
    content = content.replace("contains 13 modular test files:", "contains 14 modular test files:")

    # Add test_verify_refs.py to table if not present
    if "test_verify_refs.py" not in content:
        target_row = "| `test_exp1_multiclassifier.py` | Downstream Generalization | Downstream inductive classifier generalization across SVM, Random Forest, Multi-Layer Perceptron (MLP), and K-Nearest Neighbors (KNN). |"
        new_row = (
            target_row + "\n"
            "| `test_verify_refs.py` | Reference Verification Pipeline | Mocked CrossRef & arXiv API verification, field mismatch detection, fuzzy search fallback, published version redirects, and CLI integrity. |"
        )
        content = content.replace(target_row, new_row)

    # Add command to fast suites
    if "test_verify_refs.py" not in content.split("## Execution Guide")[-1]:
        old_suite = "# 6. Build-time macro and manuscript consistency\npytest tests/test_macro_consistency.py tests/test_pdf_allowlist.py"
        new_suite = (
            old_suite + "\n\n"
            "# 7. Automated CrossRef/arXiv reference verification test suite\n"
            "pytest tests/test_verify_refs.py"
        )
        content = content.replace(old_suite, new_suite)

    with open("tests/README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("tests/README.md updated.")

def update_contributing():
    with open("CONTRIBUTING.md", "r", encoding="utf-8") as f:
        content = f.read()

    if "make refs-check" not in content:
        old_test_sec = "* **Run all tests**:\n  ```bash\n  python -m pytest tests -q\n  ```"
        new_test_sec = (
            "* **Run all tests (94 passing)**:\n  ```bash\n  python -m pytest tests -q\n  ```\n\n"
            "* **Verify bibliography against live APIs**:\n  ```bash\n  make refs-check\n  # or: python scripts/verify_refs.py refs.bib --out results/refs_report.csv --manual refs_manual.csv\n  ```"
        )
        content = content.replace(old_test_sec, new_test_sec)

    with open("CONTRIBUTING.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("CONTRIBUTING.md updated.")

def update_paper_readme():
    with open("paper/README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Mention 47 entries, 80.85% recent, single-citation discipline
    old_bib = "- **Bibliography Style:** `sn-mathphys-num.bst` (Vancouver / numerical citation order)"
    new_bib = (
        "- **Bibliography Style:** `sn-mathphys-num.bst` (Vancouver / numerical citation order)\n"
        "- **Bibliography Hygiene:** Exactly 47 verified references (`refs.bib`), 38 published 2024–2026 (80.85% vintage). "
        "Strictly single-cited at first mention in manuscript text (47 citations in `.tex`, 0 duplicates, 0 missing, verified by `scripts/verify_refs.py`)."
    )
    if old_bib in content and "Bibliography Hygiene" not in content:
        content = content.replace(old_bib, new_bib)

    with open("paper/README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("paper/README.md updated.")

def update_changelog():
    with open("CHANGELOG.md", "r", encoding="utf-8") as f:
        content = f.read()

    entry = """## [2.2.0] - 2026-10-28

### Added
- **Automated CrossRef & arXiv Verification Suite (`scripts/verify_refs.py`, `tests/test_verify_refs.py`):** Live API client verifying DOIs, titles, first authors, publication years, volumes, and page ranges. Includes 8 unit tests testing matching, field mismatches, fuzzy title resolution, published version redirects, manual overrides, and CLI execution.
- **`make refs-check` Target:** Automated Makefile target asserting zero bibliographic discrepancies across all active references.
- **Reference Provenance Ledgers (`results/refs_report.csv`, `results/refs_map.csv`):** Complete traceability mapping every reference to its exact citing section, sentence, and scientific rationale.

### Changed
- **Modern Literature Overhaul (80.85% Recent Target):** Upgraded bibliography to 47 verified primary references, with 38 published between 2024 and 2026 (80.85% vintage) across leading journals (*IEEE TKDE*, *IEEE TNNLS*, *Pattern Recognition*, *Information Fusion*, *DAMI*, *JASA*), replacing textbook placeholders with contemporary surveys.
- **Strict Single-Citation Policy:** Audited `paper/main.tex` and `springer_manuscript/main.tex` to enforce single-mention citation discipline. Each of the 47 references is cited strictly once at its first occurrence, eliminating 39 redundant subsequent citations.
- **Test Suite Expansion:** Expanded automated test suite from 86 to 94 tests with 100% pass rate.
- **Empirical Narrative Reconciliation:** Synchronized manuscript narrative text with Pass F / Table 7 single source of truth (PBMC68k K-Means 0.494 / Std Cons 0.555; 20 Newsgroups DEC 0.008 / KM 0.063; Indian Pines SD ±0.030; Yale B SD ±0.007; Table 8 K-Means alignment; and qualified synergy gain with Wilcoxon test p ≈ 0.16).

---

"""
    if "## [2.2.0]" not in content:
        target = "## [2.1.0] - 2026-10-23"
        content = content.replace(target, entry + target)

    with open("CHANGELOG.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("CHANGELOG.md updated.")

def update_revision_log():
    with open("REVISION_LOG.md", "r", encoding="utf-8") as f:
        content = f.read()

    extra_items = """- [x] **Item 15: Reference vintage upgrade (>= 80% 2024-2026)** -- Curated bibliography to 47 verified references, with 38 published in 2024-2026 (80.85% vintage across IEEE TKDE, IEEE TNNLS, PR, InfFus, DAMI, JASA), verified with zero errors via `scripts/verify_refs.py`.
- [x] **Item 16: Single-citation policy enforcement** -- Audited `paper/main.tex` and `springer_manuscript/main.tex` to ensure every reference is cited exactly once at first mention (47 citations in `.tex`, 47 references in `.bib`, 0 duplicates, 0 missing).
- [x] **Item 17: Reference verification test suite** -- Implemented unit test suite `tests/test_verify_refs.py` (8 unit tests) and added `refs-check` target to `Makefile`. Total test suite passes cleanly at 94/94 tests (100%).
- [x] **Item 18: Narrative and table synchronization** -- Reconciled PBMC68k, 20 Newsgroups, Indian Pines, Yale B, and Table 8 K-Means numbers in narrative text with Pass F Table 7; accurately qualified synergy claim with Wilcoxon $p \\approx 0.16$ ($n=6$).
"""
    if "Item 15:" not in content:
        target = "- [x] **Item 14: Final build and polish**"
        lines = content.splitlines(True)
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if target in line:
                new_lines.append(extra_items)
        content = "".join(new_lines)

    with open("REVISION_LOG.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("REVISION_LOG.md updated.")

if __name__ == "__main__":
    update_readme()
    update_tests_readme()
    update_contributing()
    update_paper_readme()
    update_changelog()
    update_revision_log()
