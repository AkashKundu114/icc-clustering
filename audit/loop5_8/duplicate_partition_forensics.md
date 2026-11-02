# Duplicate partition forensics

## Scope and method

Read-only inspection of `D:\Final Year Project\results\stability\partitions` (4,320 `.npy` files) and `results/stability/runs` (4,320 `.parquet` files). The Loop 5.8 script `scripts/partition_forensics.py` dynamically computed SHA-256 from bytes, loaded NumPy object payloads (`sub_idx`, `labels`), and associated each name with its Parquet row by dataset, model, mode and repeat. No source partition, record or code was changed. The complete 291-file inventory is `duplicate_partition_inventory.csv`; it records file bytes/time, SHA-256, index/label hashes, cluster size distribution and matched fit row metadata. Named pair comparisons are saved in `named_duplicate_comparisons.json`.

## Census

The 4,320 partition files contain 4,169 unique SHA-256 digests. There are 140 digest groups with repeated bytes, containing 291 files (151 excess copies). Group sizes: 131 pairs, 7 triples, 2 groups of four. By group-level relation, 137 groups are cross-method only and 3 groups cross real/null mode; the latter also cross methods. No group consists of repeated partitions for different repeats within the same dataset-method-mode cell. All 291 files have an associated successful Parquet record. The partition files that share a digest have identical serialization, sample indices and assignments; SHA-256 equality is exact byte identity, not merely label permutation equivalence.

The duplicates are concentrated in collapsed / sparse partitions and in clusters with identical subset indices. This pattern is consistent with different algorithms yielding the same assignments on a shared cohort split, but cannot establish that the fit code executed as claimed. The run records have different model/mode metadata (and generally distinct runtimes); the duplicate `.npy` bytes do not contain those metadata. No run-level file digest or partition hash is embedded in the Parquet records.

## Three named cases

1. **CNS, CoHiRF, repeat 17, null vs real:** exact same 48 sample indices in the same order and exact same labels; K=2, sizes 47/1. Records both report `sub_seed=5017`, successful status and `n_samples=48`; null `null_seed=6017`, accuracy is NaN, real `null_seed=-1`, accuracy `-0.01870775035371797`. Equal split is expected by design. An identical real/null result is possible in principle because both fits can return the same nearly constant partition; the data do not reveal the relevant transformed input or intermediate. It is therefore **numerically verified, causally unverified**. The 1/47 collapse makes degeneracy a plausible explanation, not proven.
2. **Prostate, CoHiRF null repeat 5 vs CoreHalo real repeat 5:** exact same 81 indices and labels, K=1, size 81. Both successful, `sub_seed=5005`; null uses `null_seed=6005` and has NaN accuracy, real uses -1 and accuracy 0.0. This is an all-one-cluster output, so byte equality is a trivial partition equivalence, but exact file identity still cannot distinguish independent model results from copied/overwritten serialization. **Degenerate explanation plausible; provenance unresolved.**
3. **Prostate, StdCons null repeat 16 vs UngatedAC real repeat 16:** exact same 81 indices/order and labels, K=2, sizes 80/1. Both successful and share `sub_seed=5016`; null uses `null_seed=6016`, NaN accuracy; real uses -1, accuracy `0.0006176559204579692`. This sparse identical assignment across different methods and data modes is less explained by a one-cluster collapse. No saved generator trace or fit input hash distinguishes a genuine coincidence from assignment reuse, copy or overwrite. **Suspicious and unresolved; not proof of corruption.**

For each named pair, exact sample ordering and labels were compared directly. Since each NPY payload serializes the same `sub_idx` then `labels`, both index and assignment arrays are byte-identical. The Parquet records are not duplicates: their metadata differ as expected for different methods/modes.

## Effect on stability calculations

The reported within-cell stability for a method/mode is formed from pairs among its 30 repeat files. These repeated-hash groups are cross-method or cross-mode; none repeats within the same cohort-method-mode across distinct repeat IDs. Thus they do not add a duplicated observation pair inside a single cell's 435 pairwise comparisons. They can still reflect shared split design and algorithmic collapse. Stability remains computed from the saved partitions, and dependence among its 435 pair values remains; duplicate partitions across cells do not make those pair values independent.

## Adjudication

- **Verified:** census and byte identities for the local files; all associated fit records found and marked success; three named sample-index and assignment equalities; the Prostate CoreHalo/CoHiRF pair is degenerate K=1.
- **Conditionally supported:** duplicate assignments are plausible outputs under shared data splits and degenerate clustering. The records are metadata-compatible with the nominal design.
- **Unverified:** actual producer process for the partition grid; whether bytes were written independently or copied/overwritten; lineage from each saved fit to transformed input and model invocation.
- **No evidence of a malformed partition** in the 291 duplicate files (indices/labels lengths agree in inspected payloads). This is not a full validation of all 4,320 payloads beyond the earlier Loop 5.7 reconstruction.

Preserve all files. Before using this experiment as authenticated execution evidence, recover the actual partition-producing script/logs or rerun the protocol with per-fit input and output hashes.
