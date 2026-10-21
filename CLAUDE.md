# Claude Instruction Addendum

See `AGENTS.md` for the canonical universal contract. This file contains Claude-specific environment guidance.

## Environment Commands
- Run test suite: `pytest tests/`
- Run typecheck: `mypy -p icc`
- Run linting: `ruff check src/ tests/`
- Run quick demo: `python demo.py`
- Synchronize LaTeX numbers: `python scripts/make_numbers.py`
- Compile Springer manuscript: `cd paper && pdflatex main.tex && bibtex main && pdflatex main.tex`

## Key Repository Rules
- Keep changes minimal, verifiable, and strictly aligned with `AGENTS.md`.
- Never commit large binaries (`*.npz`, `*.pdf`, `*.zip`, `figures/*`).
- Maintain single-source-of-truth macro numbers via `paper/numbers.tex`.
