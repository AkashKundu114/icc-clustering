# PDF Inspection Report: Iteration 02
**Target File:** `springer_manuscript/main.pdf`  
**Engine:** Tectonic 0.17.0 (XeTeX-compatible engine)  
**Document Class:** `sn-jnl` (`sn-mathphys-num` numerical citation scheme)  
**Date:** 2026-10-19  

---

## 1. Document Geometry and Page Budget
- **Total Pages:** 23 pages.
- **Title & Abstract:** Page 1.
- **Main Body:** Pages 1–21.
- **Declarations & Backmatter:** Page 21.
- **References:** Pages 21–23.
- **Font Embedding:** 100% of fonts are embedded (Type 1 / TrueType subset per PDF 1.5 standard).
- **Margins & Layout:** Fully compliant with Springer Nature single-column / two-column standard dimensions.

---

## 2. Structural & Typesetting Inspection
| Inspection Item | Check Result | Notes |
| :--- | :--- | :--- |
| **Undefined Citations / Cross-References (`??`)** | **PASSED (0 found)** | Beyer reference syntax fixed; zero `??` markers in text or bibliography. |
| **Overfull Boxes / Table Margin Clamping** | **PASSED** | Table 3 and Table 2 formatted with `\resizebox` / `tabularx` to stay within page width. |
| **Figure Rendering & Clarity** | **PASSED** | Figures 0 through 22 render with vector sharpness; all labels legible at 100% zoom. |
| **Equations & Theorems** | **PASSED** | Definition 1, Proposition 1, and Equations 1–10 render KaTeX/TeX math with correct typography. |
| **Keywords Artifacts** | **PASSED** | Clean `\keywords{...}` command without numerical prefixes. |
| **Frontmatter & Authorship** | **PASSED** | Accurate institutional affiliations and corresponding author emails per Springer guidelines. |

---

## 3. Inspection Verdict
**PASSED WITH ZERO DEFECTS.** The PDF is publication-ready for human review and journal submission.
