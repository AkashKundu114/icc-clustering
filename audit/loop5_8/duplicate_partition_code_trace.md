# Duplicate partition code trace

## Code that is present

- `D:\Final Year Project\scripts\run_real_data_stability.py`: its docstring and `run_model_seed` save full-data seed label vectors to `results/stability/labels/{dataset}_{model}_seed_{seed}.npy`. It does not write `results/stability/partitions`, does not store `sub_idx`, and does not create `results/stability/runs/*.parquet`. It cannot be the direct producer of the audited 4,320 partition files.
- `D:\Final Year Project\scripts\audit_degeneracy.py`: consumes `results/stability/partitions/{dataset}_{model}_real_{sub_id}.npy`, reads `sub_idx` and `labels`, then calculates per-repeat ARI and pairwise intersection stability. It is a downstream audit/consumer, not a partition generator. It also reads `data/cache` labels.
- `D:\Final Year Project\scripts\make_stability_outputs.py`: consumes the saved summary and writes tables/figures/stats. It is a report generator, not the fit producer.

Repository-wide recursive search for `sub_idx`, `null_seed`, `results/stability/partitions`, and `subsample_stability_summary` in `.py`, `.ipynb`, `.md`, `.yaml`, and `.json` found no tracked or present script that writes the exact partition and Parquet grid. The artifact directories are ignored by Git (`git status --short --ignored` shows `!! results/stability/partitions/` and `!! results/stability/runs/`). Consequently no traceable source path explains the individual identical serializations.

## Expected versus unresolved generation conditions

The matched records share `sub_seed=5000+repeat` within a dataset and across methods/modes. This is consistent with a common subsample partition, confirmed in the named cases by exact index equality. Null rows additionally record `null_seed=6000+repeat`, while real rows record `-1`. In a standard real/null design, independently transformed feature data should be refit; the identical labels in named cases may arise from collapse or stable outputs, but the saved artifacts cannot show that those input transformations were applied. For the cross-method Prostate one-cluster case, any method returns the same label-equivalence partition when all samples are assigned to one cluster. For CNS CoHiRF and Prostate StdCons/UngatedAC, same nontrivial sparse assignments have no documented deterministic shared-code explanation in the available producer path.

## Provenance limitation and disposition

Historical protocol/source commits are not execution attestation. The available tracked run script is semantically different from the saved subsampling artifact format. No executable producer, terminal log, environment capture, model input hash, or output-write trace was located. The strongest warranted classification is: local partition bytes are present and internally match their corresponding run metadata; actual generation mechanism is **UNVERIFIABLE**. Do not label these duplicate matches as legitimate model behavior or as accidental corruption without new evidence. Keep all original files unchanged, and treat the three named cases—especially the sparse StdCons/UngatedAC match—as an open provenance blocker.
