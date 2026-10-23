# Custom Prompt: Bibliography Resolution & Citation Integrity Sweep

- **Target Systems:** Manuscript bibliography (`references.bib`), LaTeX source (`paper/main.tex` or `paper.tex`), and unverified references log (`UNVERIFIED_REFS.md`).
- **Assigned Persona:** `roo_ask` (Literature Research), `roo_coder` (BibTeX Engineering).

---

## Technical Instructions
1. Extract all citation keys present in LaTeX source files:
   ```bash
   grep -o '\\cite{[^}]*}' paper/*.tex
   ```
2. Verify that every key exists inside `references.bib` with complete scholarly metadata:
   - Complete author list (no premature `et al.` inside BibTeX fields).
   - Canonical journal or conference name.
   - Volume, issue, pages, publication year, and valid DOI.
3. Eliminate duplicate keys, conflicting year definitions, or malformed braces.
4. If any citation references an unpublished claim or hallucinated paper, flag it immediately, locate the canonical empirical reference, or remove the ungrounded citation.

## Acceptance Criteria
- Running `bibtex` produces 0 unresolved citations and 0 fatal warnings.
- Typeset document displays 0 `??` citation markers.
