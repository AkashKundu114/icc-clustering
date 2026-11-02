# Release process

This repository separates source control, GitHub releases, and archival DOI records. A Git tag alone is not proof that an archive was created; a DOI alone is not proof that the archive contains the intended source.

Before a release, maintainers should:

1. Confirm the exact public `main` commit and ensure private audits, manuscripts, restricted data, and local artifacts are absent from the tree.
2. Reconcile package, runtime, CFF, changelog, and release versions.
3. Run tests, build source and wheel distributions, inspect archive contents, and validate documented install/smoke commands.
4. Review dataset terms and avoid including uncleared inputs or sample-level derivatives.
5. Create a human-reviewed release note and tag on the approved stable commit.
6. If Zenodo integration is enabled, inspect the resulting record, metadata, and actual downloadable files; verify that the archive corresponds to that exact tag/commit.
7. Add DOI references only after the record is public, complete, and resolving.

The current GitHub–Zenodo integration archived release `v2.2.1` as [Zenodo DOI 10.5281/zenodo.23888368](https://doi.org/10.5281/zenodo.23888368); the archive was checked against the tag. This software archive does not include the historical research result package. The separate older DOI has no files and stale metadata, and no reproduction archive has been verified. Do not describe the software release as reproducing the historical paper analyses.
