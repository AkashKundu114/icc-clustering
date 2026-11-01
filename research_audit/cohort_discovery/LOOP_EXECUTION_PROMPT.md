# Loop Mission: Expand ICC Biological Cohorts with Audited Discovery and Reproducible Integration

You are operating in the repository `AkashKundu114/icc-clustering` on branch `research/cohort-discovery`.

## Mission

Execute the protocol in `research_audit/cohort_discovery/COHORT_DISCOVERY_ELIGIBILITY_SPEC.md`. Discover a broad universe of independent public cancer expression cohorts, verify them at source, download suitable public files, and integrate only cohorts that pass the prespecified gates. Do not optimize for a large dataset count or favourable ICC results.

## Non-negotiable scientific safeguards

1. Freeze eligibility criteria before running ICC, GAC, baselines or any label-based metric.
2. Never infer biological labels from a title, class balance, sample names or clinical outcome.
3. Do not use clinical outcomes (survival, recurrence, response) as biological cluster ground truth.
4. Do not merge microarray, bulk RNA-seq, single-cell, proteomics, methylation or cell-line data into one benchmark stratum.
5. Do not count derivative/overlapping cohorts as independent studies.
6. No supervised feature selection, differential-expression filtering or label-informed preprocessing.
7. Keep all candidate/rejected cohorts in the discovery catalogue with explicit reasons.
8. Never alter existing frozen experiment results, canonical result stores, or the current main branch.
9. No large raw matrices in Git unless the repository's existing data policy explicitly allows it; use .gitignore/cache conventions and checksum manifests.
10. Do not run benchmark experiments until cohort registry and eligibility decisions have been reviewed and frozen.

## Required subagents

Use parallel subagents where available. Each agent must return evidence, accession IDs, source links, and unresolved issues—not just a list of dataset names.

### Agent 1 — GEO discovery
- Search NCBI GEO systematically for human bulk cancer microarray and bulk RNA-seq studies.
- Use disease synonyms across breast, colorectal, gastric, lung, liver/HCC, pancreatic, ovarian, prostate, melanoma, glioma/GBM, leukemia, lymphoma, sarcoma, endometrial, renal, bladder, head-and-neck, thyroid and oesophageal cancers.
- Run `python tools/discover_biological_cohorts.py discover --retmax 500` with multiple focused queries, save exact query logs.
- Inspect GEO Series matrix / supplementary files / GPL platform and sample-level metadata.
- Identify independent cohorts with candidate subtype/lineage labels, not merely survival endpoints.

### Agent 2 — ArrayExpress / BioStudies / ENA
- Search ArrayExpress/BioStudies and ENA for independent human cancer bulk expression cohorts.
- Retrieve and parse IDF/SDRF and sample-to-file mappings.
- Confirm primary accession, publication and terms.
- Avoid duplicate GEO deposits of the same cohort.

### Agent 3 — TCGA / GDC RNA-seq
- Discover projects with adequate sample numbers and within-cancer subtype labels (not just tumour vs normal).
- Record GDC release, workflow, genome build, gene annotation, sample type, aliquot/case relationships.
- Use only open-access harmonized files. Do not attempt controlled-access data.
- Treat TCGA as a separate bulk RNA-seq stratum and ensure no patient contributes multiple aliquots as independent samples.

### Agent 4 — Curated resources and literature
- Inspect P2M.db, datamicroarray and relevant benchmark reviews to identify accession leads.
- Verify every candidate against the primary repository and original publication.
- Extract cohort design, sample counts, labels, platform, preprocessing and known overlap.
- Treat named candidate accessions (e.g. GSE62254, GSE39582, GSE31210, GSE72094, GSE14520, GSE25066) as leads only. Do not assume their endpoint labels qualify.

### Agent 5 — Provenance, labels and overlap auditor
- Independently audit sample IDs, patient IDs, publication reuse, derivative cohorts, paired samples, longitudinal samples and platform overlap.
- Classify labels B1-B6 exactly as defined in the spec.
- Explicitly flag circularity when molecular labels were derived from the same expression matrix.
- Reject outcome labels as cluster truth.
- Produce overlap pairs and a cohort-independence graph.

### Agent 6 — Preprocessing and implementation auditor
- Review current `src/icc/datasets`, `data/registry.yaml`, `configs/datasets.yaml`, current loaders and cache format.
- Implement only the smallest backward-compatible changes needed.
- Ensure expression orientation is samples × features at the public ICC loader boundary, with IDs preserved.
- Ensure preprocessing is assay-specific and label-blind.
- Add unit tests for parser, metadata alignment, missing values, feature filtering, duplicate IDs, checksums, and refusal to download when license review is not YES.
- Do not rewrite existing loaders or registry entries unnecessarily.

### Integration agent
- Resolve duplicate candidates and conflicts.
- Freeze the final inclusion list before any algorithm runs.
- Produce a concise audit report listing included, exploratory, rejected and unresolved candidates separately.

## Discovery execution

1. Run the GEO discovery script with separate query families:
   - broad human cancer expression profiling;
   - disease-specific searches;
   - microarray-only;
   - bulk RNA-seq-only.
2. Do not rely only on GEO GDS summaries. Inspect primary GEO Series records and supplementary files.
3. Search ArrayExpress/BioStudies, GDC, P2M.db and curated benchmark collections.
4. Preserve exact search logs, source URLs, retrieval timestamps, source response metadata and versions.
5. Build a candidate catalogue containing all hits and deduplicate by accession, patient/sample IDs and publication.
6. Do not use guessed FTP URLs. Derive download URLs from official accession pages and verify HTTP status/content type.
7. Create a reviewed download manifest. Set `license_reviewed=YES` only after documented terms review.
8. Download files only via the script's explicit reviewed manifest mode; record byte size and SHA-256. Do not download controlled-access files.

## Candidate target and composition

Aim to identify at least 25 credible candidates, then retain the subset that actually passes. Do not lower criteria to hit a quota. Prioritize diversity:
- cancer families: breast, colorectal, gastric, lung, liver, pancreas, ovarian, prostate, melanoma, glioma, leukemia/lymphoma, sarcoma, endometrial, renal, head-and-neck;
- platforms: microarray and bulk RNA-seq;
- biology: lineage/subtype/histology labels where defensible;
- independent research groups and non-overlapping patient cohorts.

The primary high-dimensional benchmark should remain a prespecified bulk cohort stratum. TCGA RNA-seq and single-cell datasets are separate analyses.

## Integration rules

- Add new candidate metadata first; do not edit canonical registry as approved until human review passes.
- Use unique stable cohort IDs; never recycle existing names.
- Record N, D, D/N, class counts, label type, sample IDs, patient IDs, platform, preprocessing, source DOI, license, access date, checksums, overlap group and decision rationale.
- For microarrays, record GPL, raw/processed status, annotation version, probe mapping and collapse strategy.
- For RNA-seq, record counts/TPM/FPKM, genome build, gene annotation and normalization pipeline.
- Keep raw, interim and processed data separate.
- Add `enabled: false` until the eligibility decision is approved.
- Preserve an immutable manifest for all downloaded files.
- Never put a clinical outcome into the `y` ground-truth field for primary clustering evaluation.

## Required output files

Under `research_audit/cohort_discovery/`:
- `search_log.jsonl`
- `candidate_catalog.csv`
- `eligibility_decisions.csv`
- `overlap_pairs.csv`
- `overlap_graph.graphml`
- `download_manifest.csv`
- `label_audit.md`
- `preprocessing_audit.md`
- `final_cohort_registry.yaml`
- `exclusion_log.csv`
- `reproducibility.md`
- `execution_report.md`

Also:
- `tests/test_cohort_discovery.py`
- `docs/COHORT_DISCOVERY.md`
- update `data/README.md` only after reviewing current policy.

## Tests and acceptance criteria

Run targeted tests, the full fast suite, Ruff and the repository's existing consistency checker. Report exact commands and exit codes. Test no-network paths with fixtures; do not make CI depend on live GEO.

A candidate may be included in confirmatory experiments only if:
- mandatory gates all pass;
- label is B1 for the primary biological subtype analysis, or explicitly segregated B2/B3 stratum;
- sample-to-expression mapping is verified;
- independent biological unit is known;
- overlap status is resolved;
- license/terms and redistribution constraints are reviewed;
- preprocessing and checksums are reproducible;
- two reviewers agree on the decision.

## Final report format

1. Number of unique candidates discovered (by source and stratum).
2. Number included Tier A, Tier B, Tier C, rejected, and unresolved.
3. Exact accession list for each category.
4. Disease-family, platform and label-type distribution.
5. Overlap/derivative cohort findings.
6. Downloads completed, total bytes, checksums, license restrictions.
7. Preprocessing and sample exclusions.
8. Tests, lint, consistency-checker results.
9. Risks, unresolved issues and human decisions still required.
10. Explicit statement that no performance results were used to select cohorts.

Do not claim "25 validated cohorts" unless every cohort has passed all gates. A large candidate catalogue is not equivalent to a validated biological benchmark.
