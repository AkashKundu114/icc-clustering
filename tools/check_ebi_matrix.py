import json
import urllib.request

for c in ["GSE31210", "GSE10846", "GSE49710"]:
    acc = c.replace("GSE", "E-GEOD-")
    url = f"https://www.ebi.ac.uk/biostudies/api/v1/studies/{acc}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            
            def find_files(obj):
                f_list = []
                if isinstance(obj, dict):
                    if "files" in obj:
                        f_list.extend(obj["files"])
                    for v in obj.values():
                        f_list.extend(find_files(v))
                elif isinstance(obj, list):
                    for item in obj:
                        f_list.extend(find_files(item))
                return f_list

            files = find_files(data)
            flat = []
            for item in files:
                if isinstance(item, list):
                    flat.extend(item)
                elif isinstance(item, dict):
                    flat.append(item)
            
            names = [f.get("path") or f.get("name") for f in flat if isinstance(f, dict)]
            print(f"\n{c} ({acc}): {len(names)} files on EBI")
            matrix_files = [n for n in names if n and ("matrix" in n.lower() or "processed" in n.lower() or "sdrf" in n.lower())]
            print(f"Key files: {matrix_files[:10]}")
    except Exception as e:
        print(f"Error for {c}: {e}")
