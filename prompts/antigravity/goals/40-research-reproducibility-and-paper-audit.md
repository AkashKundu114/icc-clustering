# Goal: Research Reproducibility and Manuscript Evidence Audit

Audit whether code, experiments, datasets, and manuscript claims align.

## Review
- Research question, hypotheses, methods, assumptions, algorithms, proofs, baselines, metrics, splits, preprocessing, seeds, configs, and statistical procedures.
- Dataset provenance, license, permissions, consent/ethics constraints, data leakage, exclusion criteria, and class imbalance.
- Whether reported figures and tables can be regenerated from code and logged outputs.
- Whether each central manuscript claim has evidence, a valid citation, or an explicit limitation.
- Whether failed/negative results or deviations are missing from the record.

## Rules
- Never invent or modify results to match a claim.
- Do not call a claim validated unless the relevant experiment/proof was actually checked.
- Do not tune on held-out test data.
- Compare baselines under fair, documented conditions.
- Distinguish implementation bugs from scientific limitations.

## Deliverables
A claim-to-evidence matrix, reproducibility gaps, prioritized fixes, rerun commands, and a clear list of claims that must be weakened or removed unless new evidence is obtained.
