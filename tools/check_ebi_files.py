import json
import urllib.request

url = 'https://www.ebi.ac.uk/biostudies/api/v1/studies/E-GEOD-62254'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

print("Title:", data.get("title"))
section = data.get("section", {})
print("Section keys:", section.keys())

def find_files(obj):
    found = []
    if isinstance(obj, dict):
        if "files" in obj:
            found.extend(obj["files"])
        for v in obj.values():
            found.extend(find_files(v))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(find_files(item))
    return found

files = find_files(data)
print(f"Total files: {len(files)}")
for f in files[:10]:
    if isinstance(f, list):
        for sub_f in f:
            print("File:", sub_f.get("path") or sub_f.get("name"), sub_f.get("size"), sub_f.get("type"))
    elif isinstance(f, dict):
        print("File:", f.get("path") or f.get("name"), f.get("size"), f.get("type"))
