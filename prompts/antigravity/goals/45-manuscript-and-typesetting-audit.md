# Goal: Manuscript Typesetting, Typography & BibTeX Citation Audit

Deploy this goal to audit camera-ready LaTeX documents, verify cross-referencing integrity, validate bibliography completeness, and resolve typographical warnings.

---

## Assigned Subagent Personas
1. **Typesetting & Typography Specialist (`roo_reviewer`)**: Inspects overfull `\hbox` warnings, column balancing, and float placements.
2. **Citation & Bibliography Auditor (`roo_ask`)**: Cross-checks every `\cite{}` key against `references.bib` and scholarly databases.
3. **Manuscript Build Engineer (`roo_coder`)**: Fixes table column constraints, wraps long equations, and automates PDF builds.

---

## Verification Protocol

### 1. Zero Undefined Citations or References
- Parse compiler `.log` and `.blg` files.
- **Fail condition:** Presence of any of the following:
  - `LaTeX Warning: Citation '...' on page ... undefined`
  - `LaTeX Warning: Reference '...' on page ... undefined`
  - Visual `??` artifacts in generated PDF text.
- Resolve missing entries in `references.bib` using verified scholarly metadata (DOIs, canonical author lists, publication years).

### 2. High-DPI Figure & Vector Format Verification
- Verify that every image included via `\includegraphics` exists in the local figures directory and satisfies venue resolution requirements:
  - Line art / plots: Native vector formats (`.pdf`, `.eps`) or raster `.png` at $\ge 300$ DPI.
  - No low-resolution, pixelated, or compressed artifacts.

### 3. Typography & Overflow Diagnostics
- Search `.log` output for:
  - `Overfull \hbox (... pt too wide)`
- For wide tables:
  - Apply `\resizebox{\columnwidth}{!}{...}` or adjust `\tabcolsep` / `\scriptsize`.
- For wide multi-line equations:
  - Break lines using `amsmath` environments (`align`, `split`, `multiline`).

### 4. Compilation Verification
- Execute clean compilation passes locally:
  ```bash
  pdflatex main.tex
  bibtex main
  pdflatex main.tex
  pdflatex main.tex
  ```
- Confirm zero fatal errors and clean PDF emission.
