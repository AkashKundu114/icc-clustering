# Software license and citation metadata audit

## Scope and evidence inspected

This is an internal Loop 6.1 review of repository metadata and the Loop 6.0 rights assessment. Inspected `LICENSE`, `CITATION.cff`, `pyproject.toml`, the top of `CHANGELOG.md`, Git tags, and `audit/loop6_0/release/data_rights_matrix.csv` / `release_manifest.json`. The review does not grant rights in any third-party dataset.

## Software license

The root `LICENSE` contains the MIT License, with copyright attributed to Akash Kundu and Techno India University (2026). `pyproject.toml` also declares MIT. This is evidence of the repository's declared software license. It must not be represented as licensing external datasets, upstream code, or third-party-derived data unless the relevant rights holders separately grant those rights. Each dataset's terms remain separate.

The package metadata labels the project “Production/Stable.” That classifier is a maturity assertion, not a license or reproducibility result; the release team should confirm it is appropriate before public release.

## Citation metadata consistency

`CITATION.cff` is valid-looking CFF 1.2.0 metadata with repository URL, MIT license, three listed authors, version 2.2.0, release date 2026-10-30, and no DOI. The version/date align with the `v2.2.0` tag, which points to commit `943e55e1bc965e17eeaae81359d5413baf4b7adc` (tagged commit timestamp 2026-10-30 09:56:43 +05:30).

The repository state inspected in this audit has conflicting project-version signals: `CHANGELOG.md` begins with 2.2.1 dated 2026-11-01, whereas `pyproject.toml` and `CITATION.cff` say 2.2.0. The CFF authors list Akash Kundu, Kalyan Kumar Das, and Anirban Mukhopadhyay; `pyproject.toml` lists only Akash Kundu as the package author. This audit did not independently validate the listed ORCID records or author contribution/consent. Do not silently update the citation metadata to 2.2.1 without deciding which repository version is the release candidate and reconciling authorship.

No DOI is recorded in `CITATION.cff`; no DOI should be invented. The Loop 6.0 release manifest says no release was created, so no software archive DOI is established by that evidence.

## Dataset rights conclusion

The Loop 6.0 matrix conservatively marks most raw data, processed caches, and sample-level partitions as not cleared. This reassessment found that some canonical UCI pages state CC BY 4.0, but those permissions cannot automatically be transferred to OpenML or scikit-learn variants without establishing exact dataset/version identity. Purdue's CC0 record for an original 220-band Indian Pines item does not establish rights for the EHU corrected 200-band variant recorded in the project registry. Yale's page expressly bars incorporating its images into a publicly distributed larger database without Yale permission. The old 10x PBMC 68k source and the 700x765 Scanpy reduced variant do not have verified redistribution terms here.

The machine-readable per-dataset disposition is in `dataset_rights_reassessment.csv`. “NOT CLEARED” means no affirmative permission was established in the inspected evidence; it is not a legal finding that redistribution is prohibited. “CONDITIONAL ONLY” means the canonical source page supplies a license but exact local variant identity or content-specific conditions remain unresolved.

## Recommendation to release owner

Keep MIT as the software license only. Reconcile package version and author metadata before making a tagged public release. In public documentation, link to official acquisition pages and cite sources, but do not bundle third-party inputs, caches, sample-level partitions, or derived records unless the exact variant's applicable rights are verified. Do not include private paper or internal audit material in the public repository.
