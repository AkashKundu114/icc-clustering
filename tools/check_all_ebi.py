import json
import urllib.request

cohorts = ["GSE62254", "GSE31210", "GSE10846", "GSE39582", "GSE49710", "GSE13159"]

for c in cohorts:
    acc = c.replace("GSE", "E-GEOD-")
    url = f"https://www.ebi.ac.uk/biostudies/api/v1/studies/{acc}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"[+] {c} ({acc}): Found on EBI BioStudies.")
    except Exception as e:
        print(f"[-] {c} ({acc}): {e}")
