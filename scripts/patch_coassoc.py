from pathlib import Path

path = Path("src/icc/core.py")
text = path.read_text(encoding="utf-8")

old_code = """def pairwise_coassoc(labelings):
    \"\"\"Computes sample-by-sample consensus co-association matrix in [0, 1].\"\"\"
    n = len(labelings[0])
    S = np.zeros((n, n), dtype=float)
    for lab in labelings:
        S += (lab[:, None] == lab[None, :]).astype(float)
    S /= len(labelings)
    return S"""

new_code = """def pairwise_coassoc(labelings):
    \"\"\"Computes sample-by-sample consensus co-association matrix in [0, 1].\"\"\"
    n = len(labelings[0])
    m = len(labelings)
    max_k = max(int(np.max(lab)) for lab in labelings) + 1
    H_all = np.zeros((n, m * max_k), dtype=np.float32)
    for idx, lab in enumerate(labelings):
        valid = lab >= 0
        H_all[valid, idx * max_k + lab[valid]] = 1.0
    S = (H_all @ H_all.T).astype(float) / float(m)
    return S"""

assert old_code in text, "old_code not found"
path.write_text(text.replace(old_code, new_code), encoding="utf-8")
print("[OK] Successfully updated pairwise_coassoc in src/icc/core.py")
