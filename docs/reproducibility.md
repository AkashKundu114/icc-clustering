# Reproducibility status

Reproducibility is reported in three separate tiers. Testing one tier does not establish a higher tier.

| Tier | Status for this repository snapshot | Inputs and environment | Command / expected output |
|---|---|---|---|
| Tier 1 — aggregate reproduction | **Not available in this snapshot.** An aggregate arithmetic check passed on an earlier repository snapshot, but its script and input were located with internal audit material and the derived result is not cleared for distribution. | Would require a rights-cleared aggregate CSV and a standard-library calculation script. | No Tier 1 command is supplied here. A public equivalent must be independently reviewed, relocated, and tested in a fresh clone before this tier can be called available. |
| Tier 2 — partition-level reproduction | **Unavailable.** | Exact cached features/labels, stable row mapping, 4,320 partitions, fit records, metric configuration, and a compatible environment. These are not in the public snapshot; data/derived-output rights are not cleared. | No command can run from this clone. |
| Tier 3 — full experimental reproduction | **Not run.** | Rights-cleared versioned datasets, recovered or newly specified experiment producer, frozen configuration, dependencies, seeds, sample IDs, and per-fit provenance. | No authenticated historical producer or full reproduction command is included. |

The package installed in a newly created Python 3.14.6 virtual environment from a fresh clone, and the synthetic smoke workflow completed. Two full-suite runs showed network dependence: one failed when the Yale B integration test's upstream mirror timed out; a subsequent run completed after the test suite downloaded multiple third-party dataset files and wrote local raw/cache artifacts. The unit and regression subset completed, with one optional TensorFlow test skipped. Review provider terms before running integration tests because they may acquire data. Dataset acquisition instructions are not redistribution permission. Do not download or distribute a dataset until you have checked its current provider terms and exact variant.

Portable recalculation scripts for researcher-supplied historical outputs are in [`reproduction/`](../reproduction/README.md). They do not bundle the inputs, so they do not change the current tier statuses above. Their outputs are explicitly classified as saved-output arithmetic, not fresh model execution or authenticated historical provenance.
