# Reproducibility status

Reproducibility is reported in three separate tiers. Testing one tier does not establish a higher tier.

| Tier | Status for this repository snapshot | Inputs and environment | Command / expected output |
|---|---|---|---|
| Tier 1 — aggregate reproduction | **Not available in this snapshot.** An aggregate arithmetic check passed on an earlier repository snapshot, but its script and input were located with internal audit material and the derived result is not cleared for distribution. | Would require a rights-cleared aggregate CSV and a standard-library calculation script. | No Tier 1 command is supplied here. A public equivalent must be independently reviewed, relocated, and tested in a fresh clone before this tier can be called available. |
| Tier 2 — partition-level reproduction | **Unavailable.** | Exact cached features/labels, stable row mapping, 4,320 partitions, fit records, metric configuration, and a compatible environment. These are not in the public snapshot; data/derived-output rights are not cleared. | No command can run from this clone. |
| Tier 3 — full experimental reproduction | **Not run.** | Rights-cleared versioned datasets, recovered or newly specified experiment producer, frozen configuration, dependencies, seeds, sample IDs, and per-fit provenance. | No authenticated historical producer or full reproduction command is included. |

The package installed in a newly created Python 3.14.6 virtual environment from a fresh clone, and the synthetic smoke workflow completed. The full test suite did not pass in that clone: the Yale B integration test attempted a network download and failed after the upstream mirror timed out; two tests for optional Scanpy/Zheng68K and TensorFlow dependencies were skipped. Unit and regression tests should be run separately as described in [setup](setup.md). Dataset acquisition instructions are not redistribution permission. Do not download or distribute a dataset until you have checked its current provider terms and the exact variant used.
