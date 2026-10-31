import urllib.request
import json

for data_id in [45088, 45089, 45091, 45095, 45100, 45103]:
    try:
        url = f"https://www.openml.org/api/v1/json/data/{data_id}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            desc = data.get("data_set_description", {})
            print(f"ID {data_id}: name={desc.get('name')}, status={desc.get('status')}, format={desc.get('format')}")
    except Exception as e:
        print(f"ID {data_id} error: {e}")
