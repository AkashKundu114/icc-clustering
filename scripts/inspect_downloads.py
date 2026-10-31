from pathlib import Path

dl_dir = Path.home() / "scikit_learn_data" / "openml" / "openml.org" / "data" / "v1" / "download"

for f in ["22112152", "22112156", "22112161", "22112196"]:
    p = dl_dir / f
    if p.exists():
        with open(p, "r", encoding="utf-8", errors="ignore") as fp:
            first_lines = [fp.readline().strip() for _ in range(5)]
        print(f"File {f} ({p.stat().st_size} bytes):")
        for line in first_lines:
            if line:
                print(f"  {line[:80]}")
