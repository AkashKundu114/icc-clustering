from pathlib import Path

for p in list(Path(".").glob("**/*.py")):
    if ".git" in str(p) or "__pycache__" in str(p): continue
    try:
        t = p.read_text(encoding="utf-8")
        if "critical_difference" in t or "fig08" in t or "fig17" in t or "CD" in t:
            for i, line in enumerate(t.splitlines()):
                if "5.46" in line or "4.31" in line or "Critical Difference" in line or "CD diagram" in line:
                    print(f"{p}:{i+1}: {line}")
    except Exception:
        pass
