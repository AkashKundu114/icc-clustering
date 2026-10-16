# IEEE Manuscript Submission & Analyzer-Ready Suite

## Target Publication Venue
- **Primary Venue:** **IEEE Transactions on Knowledge and Data Engineering (TKDE)**
- **Document Class:** `\documentclass[10pt,journal,compsoc]{IEEEtran}` (IEEE Computer Society Transactions Format)
- **Bibliography Style:** `\bibliographystyle{IEEEtran}` with `references.bib`
- **Secondary Targets:** IEEE Transactions on Neural Networks and Learning Systems (TNNLS), IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI).
- **Venue Dossier:** See [`IEEE_VENUE_TARGET.md`](./IEEE_VENUE_TARGET.md) for complete submission criteria, scope alignment, and page constraints.

---

## Directory Organization

```
ieee_manuscript/
├── IEEE_VENUE_TARGET.md          # Full venue specification & submission criteria
├── README.md                     # This documentation file
├── IEEEtran.cls                  # Official IEEE Transactions LaTeX document class (v1.8b)
├── IEEEtran.bst                  # Official IEEE Transactions BibTeX style
├── IEEEtrantools.sty             # Official IEEEtrantools LaTeX helper package
├── IEEEabrv.bib                  # Official IEEE journal title abbreviations
├── main.tex                      # Complete, camera-ready IEEE Transactions manuscript
├── references.bib                # Fully resolved BibTeX bibliography
├── run_analyzer.bat              # 1-click Windows runner for IEEE compliance check
├── figures/                      # High-resolution (300 DPI) figures for LaTeX compilation
│   ├── fig1_ari_stability.png
│   ├── fig2_gap.png
│   ├── fig4_noisetype_heatmap.png
│   ├── fig9_inductive_generalization.png
│   ├── fig10_pseudolabel_generalization.png
│   ├── fig11_ablation_curves.png
│   ├── fig12_ablation_waterfall.png
│   ├── fig14_benchmark_matrix_8datasets.png
│   ├── fig17_critical_difference_diagram.png
│   ├── fig18_sample_complexity_scaling.png
│   ├── fig19_dimension_scaling.png
│   ├── fig20_ensemble_size_plateau.png
│   └── fig21_hyperparameter_sensitivity_map.png
├── scripts/
│   ├── analyze_ieee_compliance.py # Automated IEEE compliance & static analyzer
│   └── build_paper.py             # Build script (generates PDF locally or Overleaf zip)
└── dist/                          # Generated distribution packages and PDFs
```

---

## Automated IEEE Compliance Analyzer

We have equipped this suite with an automated static analyzer that checks all IEEE ScholarOne / PDF-eXpress requirements:
- Two-column Computer Society journal format (`\documentclass[10pt,journal,compsoc]{IEEEtran}`)
- Abstract length verification ($\le 200$ words)
- IEEE Taxonomy keywords validation ($4-8$ terms)
- 300+ DPI native image resolution validation across all figure inclusions
- Complete cross-reference integrity (validates all `\label`, `\ref`, and `\eqref` mappings)
- Citation integrity against `references.bib`
- Formal `booktabs` table formatting rules

To run the compliance analyzer:
```bash
python scripts/analyze_ieee_compliance.py
```
Or double-click `run_analyzer.bat`.

### Latest Analyzer Audit Score
```
================================================================================
           IEEE TRANSACTIONS MANUSCRIPT COMPLIANCE ANALYZER           
================================================================================
OVERALL STATUS: IEEE TRANSACTIONS COMPLIANT (Grade: A+)
Ready for IEEE ScholarOne Submission / Overleaf / IEEE PDF-eXpress
================================================================================
```

---

## How to Build the Manuscript

### Option A: Direct Overleaf Compilation (Recommended)
1. Run `python scripts/build_paper.py`.
2. This creates `dist/IEEE_TKDE_Manuscript_Submission_Package.zip`.
3. Open [Overleaf](https://www.overleaf.com), click **New Project** $\rightarrow$ **Upload Project**, and select this ZIP file.
4. Set compiler to **pdfLaTeX** and compile.

### Option B: Local Compilation (MiKTeX / TeX Live)
If you have a local TeX engine installed:
```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```
Or simply run:
```bash
python scripts/build_paper.py
```
