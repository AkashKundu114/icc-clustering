import gzip
import json
from pathlib import Path

json_dir = Path.home() / "scikit_learn_data" / "openml" / "openml.org" / "api" / "v1" / "json" / "data"

print(f"Inspecting metadata in {json_dir}...")
for f in sorted(json_dir.glob("*.gz")):
    try:
        with gzip.open(f, "rt", encoding="utf-8", errors="ignore") as gz:
            data = json.load(gz)
            desc = data.get("data_set_description", {})
            data_id = desc.get("id")
            name = desc.get("name")
            desc_text = desc.get("description", "")
            # First line of description
            first_desc = desc_text.split("\n")[0] if desc_text else ""
            print(f"ID {str(data_id):5s} (File {f.name:10s}): Name='{name}' | Desc: {first_desc[:80]}")
    except Exception as e:
        print(f"Error reading {f.name}: {e}")
