# Biological Cohort Discovery Utility

This document describes the metadata-first discovery and checksum download utility.

## Important distinction

The discovery command finds **candidate GEO Series records**. It does not establish that a cohort has valid biological subtype labels, independent patients, appropriate licensing, or eligibility for confirmatory clustering. All candidates remain `CANDIDATE_ONLY` until reviewed under `research_audit/cohort_discovery/COHORT_DISCOVERY_ELIGIBILITY_SPEC.md`.

## 1. Discover GEO candidates

From the repository root:

```bash
python tools/discover_biological_cohorts.py discover --retmax 500
```

Use focused queries as additional searches. Example:

```bash
python tools/discover_biological_cohorts.py discover \
  --query '("Homo sapiens"[Organism]) AND "Expression profiling by array"[DataSet Type] AND (breast OR mammary OR carcinoma)' \
  --query '("Homo sapiens"[Organism]) AND "Expression profiling by array"[DataSet Type] AND (colorectal OR colon OR rectal)' \
  --query '("Homo sapiens"[Organism]) AND "Expression profiling by high throughput sequencing"[DataSet Type] AND (cancer OR carcinoma OR tumor OR tumour)' \
  --retmax 500
```

Outputs:
- `research_audit/cohort_discovery/candidate_catalog.csv`
- `research_audit/cohort_discovery/search_log.jsonl`

The GEO E-utilities workflow searches and summarizes Entrez GEO DataSets metadata. Full Series records, supplementary files and matrices require a separate retrieval step; see [NCBI GEO programmatic access](https://www.ncbi.nlm.nih.gov/geo/info/geo_paccess.html) and [GEO download options](https://www.ncbi.nlm.nih.gov/geo/info/download.html).

## 2. Review candidates before downloading

For each GSE:
1. Open the linked GEO Series record and inspect all GSM sample records, GPL platforms, Series Matrix and supplementary files.
2. Read the linked primary publication and supplements.
3. Determine whether labels are biological subtype/lineage (B1), tumour-vs-normal (B2), molecular phenotype (B3), clinical outcome (B4), technical/design (B5), or inferred labels (B6).
4. Establish patient/sample independence and identify overlapping/derivative datasets.
5. Check license and terms. A freely downloadable file is not automatically licensed for unrestricted redistribution.
6. Enter only approved files into `download_manifest_template.csv`, setting `license_reviewed=YES` after documented review.

## 3. Download only reviewed files

Copy the template to a working manifest, fill official download URLs and paths, and run:

```bash
python tools/discover_biological_cohorts.py download \
  --manifest research_audit/cohort_discovery/download_manifest_reviewed.csv
```

Downloads are written under `data/raw/cohort_discovery/` by default. The downloader:
- refuses a row unless `license_reviewed=YES`;
- rejects absolute paths and path traversal;
- streams files to a temporary `.part` file;
- verifies a supplied SHA-256 when present;
- writes the computed SHA-256, byte size and retrieval timestamp to a report.

For first acquisition, `expected_sha256` can be blank; inspect and freeze the computed digest before later reproduction. Never silently overwrite a frozen file with a changed checksum.

## 4. GDC and ArrayExpress

This initial utility implements GEO discovery and a generic reviewed-file downloader. It does not yet implement native GDC or ArrayExpress discovery clients. For TCGA, use the official [GDC API](https://gdc.cancer.gov/developers/gdc-application-programming-interface-api); for ArrayExpress/BioStudies, inspect study IDF/SDRF and file mappings using the official [BioStudies/ArrayExpress data access guidance](https://www.ebi.ac.uk/training/online/courses/arrayexpress-in-biostudies/getting-data-from-the-arrayexpress-collection/). Do not treat those sources as if they share GEO's metadata schema.

## 5. Integration status

The utility deliberately does not update `data/registry.yaml` or `configs/datasets.yaml`. Registry promotion requires human-reviewed eligibility decisions, sample-to-expression alignment, preprocessing specification, overlap adjudication, checksum records and tests. Do not run confirmatory ICC experiments on the candidate catalogue.
