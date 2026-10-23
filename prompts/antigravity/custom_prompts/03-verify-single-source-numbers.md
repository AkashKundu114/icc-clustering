# Custom Prompt: Single-Source Numbers Macro Synchronization

- **Target Systems:** Manuscript prose (`paper/*.tex`), macro definition files (`numbers.tex`), and result registries (`results/results.json`).
- **Assigned Persona:** `roo_reviewer` (Audit), `roo_coder` (Script Engineering).

---

## Technical Instructions
1. Inspect the macro generation script (e.g. `scripts/make_numbers.py`).
2. Verify that every macro defined in `numbers.tex` (e.g. `\TableThreeGrandMeanARI`, `\PropOneCriticalBound`) traces directly to a calculated field in `results/results.json` or experimental logs.
3. Search for any hardcoded raw floating-point numbers in manuscript tables or abstract:
   ```bash
   grep -E '[0-9]+\.[0-9]{2,}' paper/main.tex
   ```
4. Replace raw hardcoded empirical figures with explicit `\MacroName` declarations.
5. Re-run macro generator to ensure synchronization:
   ```bash
   python scripts/make_numbers.py
   ```

## Acceptance Criteria
- 100% of reported empirical metrics in the manuscript originate from `numbers.tex`.
- Zero manual floating-point number edits in LaTeX source files.
