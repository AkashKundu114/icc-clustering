# Biological Cohort Discovery, Eligibility, and Integration Specification

**Status:** protocol for candidate discovery; not a declaration that any candidate is eligible  
**Scope:** independent human cancer bulk transcriptomic cohorts for ICC/GAC clustering evaluation  
**Primary benchmark stratum:** bulk expression microarray / bulk RNA-seq  
**Separate strata:** single-cell RNA-seq, proteomics, methylation, cell lines, spatial transcriptomics  
**Rule:** no cohort is promoted into a confirmatory benchmark by automated metadata screening alone.

## 1. Objectives and non-goals

Discover a broad, reproducible universe of public biological cohorts; establish provenance and biological-label validity; detect overlap and derivative datasets; acquire source files with checksums; preprocess without label leakage; and create a reviewable cohort registry.

The objective is not to maximize the dataset count. Do not combine incompatible assays or treat every clinical endpoint as a biological cluster label. Discovery is broad; confirmatory inclusion is conservative.

## 2. Discovery sources (search all, record query/date/version)

1. **NCBI GEO**: GSE series, sample metadata, processed series matrices, supplementary files, platform annotations. Use NCBI E-utilities and the GEO FTP hierarchy. Search expression profiling by array and by high-throughput sequencing, human organism, cancer/neoplasm terms, and disease-specific synonyms.
2. **EMBL-EBI ArrayExpress / BioStudies**: study metadata, MAGE-TAB IDF/SDRF, processed expression files, raw-data links. Preserve SDRF sample-to-file relationships. Sequencing FASTQ may be hosted by ENA.
3. **TCGA / NCI Genomic Data Commons (GDC)**: project, case, sample, file and workflow metadata. Prefer harmonized gene-level expression quantification for a TCGA stratum; record GDC release and workflow. Respect controlled-access boundaries; this pipeline must not attempt controlled files.
4. **P2M.db**: use the published accession-level screening table, source metadata and QC metadata as a discovery index, not as ground truth. Recheck every accession at its primary repository and original paper. The collection describes 86 bulk and 48 single-cell studies in its current dataset card; counts can change by release.
5. **Curated benchmark repositories**: datamicroarray and other curated microarray collections. Use them to identify accessions, then verify at GEO/ArrayExpress and in the primary paper.
6. **Publication supplements**: supplementary tables and author-hosted matrices may identify cohorts absent from repository keyword searches. Record DOI, supplement URL, and license.

Search terms should cover: cancer, carcinoma, adenocarcinoma, neoplasm, tumor/tumour, leukemia/leukaemia, lymphoma, myeloma, sarcoma, glioma, glioblastoma, melanoma, mesothelioma, neuroblastoma, medulloblastoma, and organ-specific terms. Also search by assay type and study design. Keep exact query strings, retrieval timestamp, source endpoint, response metadata and result count.

## 3. Cohort unit and independence

A cohort is a biologically and experimentally defined sample collection, not a file, platform, paper, or accession by itself.

- Distinguish study, series, subseries, platform, assay, specimen, patient, sample and aliquot.
- One paper may contain multiple cohorts; one cohort may be split across accessions/platforms.
- Detect repeated GSM/sample IDs, patient IDs, aliquots, paired specimens, repeated timepoints, and cross-study reuse.
- Build an overlap graph. Record known shared patients and uncertain overlap; do not count overlapping cohorts as independent evidence in pooled inference.
- If a dataset is a re-analysis or subset of an existing cohort, mark it derivative and exclude it from the independent-cohort count.
- Preserve paired primary/metastatic, tumor/normal, longitudinal and treatment-response structure in metadata. Do not silently collapse them.

## 4. Eligibility criteria

### 4.1 Mandatory gates (all must pass)

A. Human-origin samples, or a separately declared non-human validation stratum.  
B. Cancer tissue / tumour-derived biospecimen / cancer cell line, with specimen type explicit. Normal tissue controls may be retained as a separate contrast stratum.  
C. Expression-like numeric feature matrix at sample level (bulk microarray or bulk RNA-seq for the primary stratum).  
D. At least 30 independent biological samples after exclusions for the confirmatory primary analysis. Smaller cohorts may enter an exploratory appendix only.  
E. At least 500 measured features before any algorithm-specific feature selection. Record post-QC feature count.  
F. Sample identifiers map unambiguously to expression columns/rows and metadata records.  
G. Publicly downloadable files and documented terms permit academic research/reuse. If license or terms are unclear, quarantine pending review; public availability is not equivalent to an explicit open license.  
H. Original study/publication and primary repository accession are traceable.  
I. No fatal sample duplication, label corruption, or irreconcilable expression/metadata mismatch.

### 4.2 Label eligibility (critical)

Every label must be classified before it can be used in ARI/NMI/AMI evaluation:

- **B1: biological subtype / lineage / histopathology** — potentially suitable as external reference labels, with original source and annotation method.
- **B2: disease vs non-disease / tumour vs normal** — suitable only for a separate diagnostic-contrast stratum, not evidence of unsupervised tumour-subtype discovery.
- **B3: molecular alteration / mutation / receptor status** — separate molecular-phenotype stratum; record whether labels are mutually exclusive or overlapping.
- **B4: clinical outcome** (survival, recurrence, response, responder/non-responder) — not a biological ground-truth cluster label. Can be used only in downstream association analysis, never to select K, features, or tune clustering.
- **B5: batch, platform, centre, treatment arm, timepoint, patient ID** — technical/design metadata, not biological truth labels.
- **B6: inferred labels** (e.g. CMS, PAM50, cell types) — only eligible when the assignment method and input data are documented; check circularity if the same expression features define both labels and clusters.
- **Unknown / ambiguous** — quarantine; do not guess labels from title or class balance.

Primary clustering endpoint should prioritize B1. B2 and B3 are separately reported. B4/B5 are never used as primary cluster ground truth.

### 4.3 Quantitative suitability tiers

- **Tier A (confirmatory bulk high-D):** N >= 30, D >= 500, D/N >= 5, >=2 defensible B1 labels, sample-level expression, provenance and license clear.
- **Tier B (confirmatory bulk general):** N >= 30, D >= 500, >=2 defensible B1 labels, but D/N < 5 or label type B2/B3. Analyze in a distinct predeclared stratum.
- **Tier C (exploratory):** N 15-29, weak/partial labels, uncertain preprocessing, or small class sizes. Never mix into primary claims.
- **Separate stratum:** scRNA-seq, spatial, proteomics, methylation, cell-line panels, xenografts, cross-platform merged matrices. Do not pool with bulk tissue cohorts.
- **Reject:** no reproducible sample matrix, fewer than 15 independent samples, no meaningful biological labels for the proposed evaluation, non-human without separate scope, unclear provenance, or irreparable sample mapping errors.

The D/N threshold is a benchmark-design choice, not a biological truth. Report N, D, D/N, class sizes and post-QC dimensions; do not select cohorts based on observed ICC performance.

## 5. Data integrity and preprocessing

1. Preserve immutable source downloads under `data/raw/<cohort_id>/`; never commit large source matrices unless repository policy explicitly permits. Add source URL, retrieval timestamp, byte size, SHA-256, ETag/Last-Modified where available, and terms/license record.
2. Store raw sample metadata separately from expression values. Keep original sample IDs and feature/probe IDs.
3. For microarrays, identify platform (GPL), annotation release, preprocessing state (raw CEL vs RMA/normalized), log base, background correction, and probe-to-gene mapping. Do not merge platforms by naïve column concatenation. Document probe collapse (e.g. median per gene) and perform sensitivity analysis where mapping is ambiguous.
4. For RNA-seq, prefer raw counts or a documented normalized abundance matrix. Record genome build, gene annotation release, quantification pipeline, count unit and transformation. Use a prespecified transformation (e.g. DESeq2 VST or log2(TPM+offset)) consistently within the RNA-seq stratum. Do not z-score raw counts.
5. Do not combine microarray and RNA-seq into one feature matrix. Do not use batch correction across independent cohorts for the primary per-cohort benchmark.
6. Remove features with all missing / zero variance; apply a prespecified missingness rule. Imputation and scaling must be fitted within the training/evaluation protocol and must not use external labels.
7. No supervised differential-expression filtering, marker selection, outcome-informed filtering, label-informed feature ranking, or selection of features based on test labels.
8. Any label-based metric is computed only after clustering is complete. Labels must not enter preprocessing, hyperparameter selection, K selection, seed selection or stopping.
9. For single-cell: retain count layer, cell metadata, donor/patient ID, tissue/specimen role, cell annotation source and QC thresholds. Aggregate to patient/pseudobulk where the scientific unit is a patient; do not treat thousands of cells from one donor as independent biological cohorts. Cell-level and patient-level tasks are separate.
10. Report every exclusion with exact reason and sample ID; retain a machine-readable audit trail.

## 6. Duplicate and overlap audit

- Normalize sample accessions (GSM, E-MTAB sample IDs, GDC case/sample/aliquot IDs).
- Compare patient identifiers only where public metadata supports it; never infer identity from private or sensitive data.
- Compare exact expression vectors / sample hashes when matrices overlap; use correlation fingerprints only as a screening flag, not definitive identity.
- Search original publications for cohort reuse, external validation sets and prior-publication reuse.
- Produce `overlap_graph.graphml`, `overlap_pairs.csv`, and a narrative decision log.
- For pooled statistics, group dependent cohorts or retain one predeclared representative; do not count overlapping derivatives as independent studies.

## 7. Candidate scoring and adjudication

Score each candidate only after mandatory gates:
- biological label validity (0-3)
- provenance / publication traceability (0-3)
- sample mapping and matrix integrity (0-3)
- independent cohort status (0-3)
- dimensional suitability (0-3)
- license / access clarity (0-3)
- platform/preprocessing clarity (0-3)

Maximum 21. Tier A/B inclusion requires >=17 and no zero on label validity, provenance, matrix integrity, independence or access. Two reviewers adjudicate label and overlap fields. The score prioritizes audit effort; it must not override a failed mandatory gate.

## 8. Required registry schema

Each record must include:
`cohort_id, cohort_name, disease, histology, specimen_type, stratum, repository, accession, source_url, publication_doi, publication_url, platform, assay, genome_build, annotation_release, n_patients, n_samples, n_features_raw, n_features_qc, d_over_n, label_name, label_type, label_source, class_counts, independent_unit, patient_id_available, overlap_group, overlap_status, license, access_status, retrieval_date, file_manifest, sha256, preprocessing, exclusions, eligibility_tier, eligibility_decision, reviewer, decision_rationale`.

Use null for unknown values. Never fill missing values with guesses.

## 9. Proposed initial search priorities (candidate discovery only)

Search and validate, rather than assume inclusion:
- GEO/ArrayExpress bulk tumour expression studies in gastric, colorectal, lung, liver, pancreatic, ovarian, prostate, breast, melanoma, glioma, lymphoma, leukemia, sarcoma, endometrial, head-and-neck and renal cancers.
- Large independent cohorts such as GSE62254 (gastric), GSE39582 (colorectal), GSE31210 (lung), GSE72094 (melanoma), GSE14520 (hepatocellular carcinoma), and GSE25066 (breast) are *leads for metadata/label review*, not pre-approved ground-truth clustering cohorts. Their endpoint labels may be clinical or molecular rather than intrinsic subtypes.
- Curated sources such as P2M.db can accelerate accession discovery. Re-verify source accessions and all sample-level decisions against GEO/ArrayExpress/GDC and the original publication.
- TCGA projects are a separate RNA-seq stratum. Avoid treating tumour-type codes alone as within-cancer subtype labels.

## 10. Required deliverables

1. `research_audit/cohort_discovery/search_log.jsonl`: exact queries, endpoints, timestamps, counts.
2. `research_audit/cohort_discovery/candidate_catalog.csv`: every candidate, including rejected candidates.
3. `research_audit/cohort_discovery/eligibility_decisions.csv`: gate-by-gate pass/fail and rationale.
4. `research_audit/cohort_discovery/overlap_pairs.csv` and overlap graph.
5. `research_audit/cohort_discovery/download_manifest.csv`: URL, bytes, SHA-256, terms, retrieval date.
6. `research_audit/cohort_discovery/label_audit.md`: label type, biological interpretation, circularity risk.
7. `research_audit/cohort_discovery/preprocessing_audit.md`: assay-specific preprocessing and feature mapping.
8. `research_audit/cohort_discovery/final_cohort_registry.yaml`: only approved cohorts enabled for experiments; candidate/rejected entries remain separately recorded.
9. `research_audit/cohort_discovery/exclusion_log.csv`: every rejected sample/cohort and exact reason.
10. `research_audit/cohort_discovery/reproducibility.md`: commands, software versions, data versions, checksums, limitations.

## 11. Statistical design safeguards

- Freeze inclusion criteria and candidate universe before running ICC or baselines.
- Do not use ARI/NMI results to decide which cohorts enter the benchmark.
- Report per-cohort results and disease/platform-stratified summaries; avoid a single pooled mean that hides heterogeneity.
- Distinguish independent studies from multiple datasets within one study.
- Use cohort as the inferential unit for cross-cohort generalisation; seeds are repeated algorithmic runs, not independent biological replicates.
- Keep biological label type strata separate. Report all eligible cohorts, not only those favourable to ICC.
- Prespecify minimum class size and report imbalance. Do not discard rare classes after observing algorithm performance.
- Report uncertainty and multiple-comparison correction; avoid overclaiming from small numbers of cohorts.

## 12. Acceptance checklist

A cohort is enabled only when two reviewers can answer YES to: source accession verified; primary publication checked; sample IDs reconciled; independent biological unit established; label semantics and circularity assessed; assay/platform and preprocessing documented; license/terms reviewed; raw files checksummed; QC and exclusions reproducible; class sizes adequate; overlap status assigned; and registry metadata complete.

**Never auto-promote candidates.** The discovery script may find and download metadata/matrices, but a human-reviewed decision is required before a cohort enters confirmatory experiments.
