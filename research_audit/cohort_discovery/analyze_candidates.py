import csv
import json
from collections import Counter
from pathlib import Path

catalog_path = Path("research_audit/cohort_discovery/candidate_catalog.csv")
log_path = Path("research_audit/cohort_discovery/search_log.jsonl")

with log_path.open("r", encoding="utf-8") as f:
    logs = [json.loads(line) for line in f]

print("=== SEARCH LOG AUDIT ===")
print(f"Total search log queries recorded: {len(logs)}")
for i, entry in enumerate(logs, 1):
    print(f"Query {i}:")
    print(f"  Timestamp UTC : {entry.get('timestamp_utc')}")
    print(f"  Endpoint      : {entry.get('endpoint')}")
    print(f"  Status        : {entry.get('status')}")
    print(f"  UID count     : {entry.get('uid_count')}")
    print(f"  Term          : {entry.get('query')[:90]}...")

with catalog_path.open("r", encoding="utf-8") as f:
    records = list(csv.DictReader(f))

print("\n=== CANDIDATE CATALOG AUDIT ===")
print(f"Total unique GEO Series records: {len(records)}")
fieldnames = list(records[0].keys()) if records else []
print(f"Catalog columns ({len(fieldnames)}): {fieldnames}")

# Disease classification
categories = {
    "Breast": ["breast", "mammary", "brca", "gse25066", "gse2034", "gse42568"],
    "Colorectal / Gastric": ["colorectal", "colon", "rectal", "gastric", "stomach", "crc", "gse62254", "gse39582"],
    "Lung (NSCLC, LUAD, LUSC, SCLC)": ["lung", "nsclc", "luad", "lusc", "sclc", "pulmonary", "gse31210", "gse72094"],
    "Liver (HCC) / Pancreas (PDAC)": ["liver", "hepatocellular", "hcc", "hepatic", "pancrea", "pdac", "gse14520"],
    "Glioma / CNS / Neuro": ["glioma", "glioblastoma", "cns", "brain", "astrocytoma", "oligodendroglioma", "neuroblastoma", "gse49710", "medulloblastoma"],
    "Leukemia / Lymphoma": ["leukemia", "leukaemia", "lymphoma", "aml", "all", "cll", "cml", "dlbcl", "gse13159", "myeloma"],
    "Melanoma / Ovarian / Prostate": ["melanoma", "ovarian", "ovary", "prostate", "prostatic"],
}

disease_counts = Counter()
unclassified = []

for r in records:
    text = (r["title"] + " " + r["summary"] + " " + r["source_query"]).lower()
    matched = []
    for cat, kws in categories.items():
        if any(kw in text for kw in kws):
            matched.append(cat)
    if matched:
        for m in matched:
            disease_counts[m] += 1
    else:
        unclassified.append(r["geo_accession"])

print("\n=== DISEASE FAMILY BREAKDOWN (Query & Context Matched) ===")
for cat, count in disease_counts.most_common():
    print(f"  {cat:32s}: {count:3d} candidate series")
if unclassified:
    print(f"  Unclassified / General           : {len(unclassified):3d} candidate series")

# Sample count range
sample_nums = []
for r in records:
    val = r["n_samples"].strip()
    if val.isdigit():
        sample_nums.append(int(val))

sample_nums.sort()
print("\n=== SAMPLE COUNT RANGE ===")
print(f"  Series with sample counts : {len(sample_nums)} / {len(records)}")
print(f"  Min samples               : {min(sample_nums)}")
print(f"  Median samples            : {sample_nums[len(sample_nums)//2]}")
print(f"  Mean samples              : {sum(sample_nums)/len(sample_nums):.1f}")
print(f"  Max samples               : {max(sample_nums)}")
print(f"  Series with N >= 30       : {sum(1 for s in sample_nums if s >= 30)}")
print(f"  Series with N >= 100      : {sum(1 for s in sample_nums if s >= 100)}")

# Top landmark candidates
landmarks = [
    "GSE62254", "GSE39582", "GSE31210", "GSE72094", "GSE14520",
    "GSE25066", "GSE2034", "GSE49710", "GSE13159", "GSE42568"
]

print("\n=== LANDMARK BENCHMARK CANDIDATES ===")
for r in records:
    if r["geo_accession"] in landmarks:
        print(f"Accession : {r['geo_accession']}")
        print(f"  Title   : {r['title']}")
        print(f"  Samples : {r['n_samples']}")
        print(f"  Platform: {r['platforms']}")
        print(f"  PubMed  : {r['pubmed_ids']}")
        print(f"  URL     : {r['source_url']}")
        print()
