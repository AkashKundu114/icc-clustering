import json
import urllib.request

cohorts = ["GSE31210", "GSE10846", "GSE39582", "GSE49710", "GSE13159"]
for c in cohorts:
    url = f"https://api.refine.bio/v1/experiments/{c}/"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            title = data.get("title", "")[:50]
            samples = data.get("num_processed_samples", 0)
            print(f"[+] {c}: {title}... Samples: {samples}")
    except Exception as e:
        print(f"[-] {c} error: {e}")
