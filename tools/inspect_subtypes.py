import gzip
from collections import Counter
from pathlib import Path

def test_extract(acc, keyword):
    p = Path(f"data/raw/cohort_discovery/{acc}/{acc}_series_matrix.txt.gz")
    headers = {}
    accessions = []
    with gzip.open(p, "rt", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("!Sample_geo_accession"):
                accessions = [s.strip().strip('"') for s in line.strip().split("\t")[1:]]
            elif line.startswith("!Sample_"):
                parts = line.strip().split("\t")
                k = parts[0].strip()
                v = [x.strip().strip('"') for x in parts[1:]]
                if k not in headers:
                    headers[k] = v
                else:
                    headers[f"{k}__row_{len(headers)}"] = v
            elif line.startswith("!series_matrix_table_begin"):
                break
    labels = []
    for i in range(len(accessions)):
        sub = None
        for k, v in headers.items():
            if "characteristics" in k and i < len(v) and keyword in v[i]:
                sub = v[i].split(keyword)[1].strip()
                break
        labels.append(sub)
    print(f"{acc}: found {sum(l is not None for l in labels)}/{len(accessions)} labels.")
    print(f"{acc} label counts: {Counter(labels)}")

if __name__ == "__main__":
    test_extract("GSE21653", "molecular subtype:")
    test_extract("GSE32894", "molecular_subtype:")
