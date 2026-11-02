# Audit determinism test

## Executed checks

- The included aggregate-only reproduction script was run twice against the same copied CSV. Both executions returned the same 72-row, 6-dataset, 12-method result and values: mean stability 0.5165860620823638; mean external ARI 0.0523121821722892; mean gap 0.46427387991007457; median gap 0.44840681694162077.
- The independent duplicate-forensics agent ran its SHA-256 census over 4,320 partition files and emitted 140 repeated digest groups/291 files. Each exact digest group is deterministic for fixed bytes. No independent second execution was performed by the lead; this classification is supported by the specialist script/output and is not represented as lead rerun.
- The bootstrap script was executed after reconciliation and generated CSV/JSON/prose from fixed local cell input. Seed sensitivity output explicitly varies seeds. The documented 10,000-resample fixed-seed values are reproducible for the current implementation; endpoints depend on RNG family/order and NumPy version.

## Limits

Audit inventory includes current timestamps and local absolute paths. Those fields are intentionally environment-specific; whole-manifest byte identity across machines is not expected. `bootstrap_estimand.py` imports standard scientific Python dependencies and consumes the reconstructed 72-cell CSV. Duplicate forensic script uses NumPy/Pandas/PyArrow/Scikit-learn-compatible artifacts. This audit did not pin a fresh environment and did not claim independent reproducibility of those scripts from public clone.

The historical Loop 5.6 chain is not deterministic as a report workflow because its aggregate-only and partition-level scripts write overlapping output names and order changes the final state. The Loop 5.8 workflow disambiguates which historical outputs are superseded and keeps new deliverables in a separate directory.

**Outcome:** Tier 1 arithmetic is deterministic and was rerun twice. Full Loop 5.8 manifest generation is content-hash verifiable, but a clean-clone run of the uncommitted Loop 5.8 scripts has not occurred. Do not claim complete deterministic public reproduction.
