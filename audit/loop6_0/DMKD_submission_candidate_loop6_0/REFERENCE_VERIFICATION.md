# Candidate LaTeX build and metadata verification

## Candidate scope

`main.tex` is a standalone, article-class research candidate under `audit/loop6_0/manuscript/candidate/`. It is not the canonical `paper/manuscript/main.tex`, and it is not the Springer `sn-jnl` submission class. It is deliberately limited to the evidence-bounded six-cohort saved-output study. The canonical manuscript SHA was rechecked and remains `A0C4274EC5DFBB40311D3D33D7AD8179B17DEE145851FD2E5B255E498054E75F`.

## Numerical linkage

`build_candidate_tables.py` reads `audit/loop5_9/statistics/cell_reconstruction.csv`, requires 72 rows, six cohort names, and 12 methods, then regenerates `aggregate_results.json`, `aggregate_macros.tex`, `aggregate_results.tex`, `cohort_descriptives.csv`, and `cohort_descriptives.tex`. The candidate source inputs the generated macros/tables. Re-execution yielded 72 cells; mean stability 0.5165860620823638; mean external ARI 0.0523121821722892; mean cell difference 0.46427387991007457; median gap 0.44840681694162077; mean null stability 0.00661968076299296. These exactly match the values computed from all 72 rows of the Loop 5.9 reconstructed CSV (pre-rounding). No model fitting occurred.

## Build attempt

Command attempted from the candidate directory: `pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex`. It could not start because `pdflatex` is not installed or on PATH (`The term 'pdflatex' is not recognized`). No PDF was produced; visual inspection was therefore not possible. Raw attempt output is preserved in `build/pdflatex_attempt.log`.

## Static checks

`python validate_candidate.py` passed: required included files exist; LaTeX environments are balanced; citations resolve to candidate bibliography keys; design count and aggregate macros match generated JSON/tables. These checks are not a substitute for TeX compilation or Springer template validation.

## Bibliographic metadata checked

- Amorim & Cardoso (2015), conference title and subtitle, IC3K/KDIR volume, pages 259–264, ISBN, and DOI were checked against the proceedings PDF: https://www.scitepress.org/Papers/2015/55977/55977.pdf and DOI 10.5220/0005597702590264.
- Hennig (2007), journal, volume 52(1), pages 258–271 and DOI 10.1016/j.csda.2006.11.025 were checked against the publication record and author manuscript.
- Liu, Yu & Blair (2022), journal, volume 14(6), e1575 and DOI 10.1002/wics.1575 were checked against Wiley's citation metadata: https://doi.org/10.1002/wics.1575.
- Ullmann, Hennig & Boulesteix (2021), title, authors, journal and e1444 identifier, and DOI 10.1002/widm.1444 were checked against the authors' arXiv record, which links the published version: https://arxiv.org/abs/2103.01281.

The candidate bibliography includes these four sources only. Full reference-style normalization to DMKD house style remains for the author/editorial pass.
