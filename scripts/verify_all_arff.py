import gzip
from pathlib import Path
import numpy as np

def parse_arff_gz(file_path):
    with gzip.open(file_path, "rt", encoding="utf-8", errors="ignore") as gz:
        in_data = False
        X_rows = []
        y_rows = []
        for line in gz:
            line_str = line.strip()
            if not line_str or line_str.startswith("%"):
                continue
            if line_str.upper().startswith("@DATA"):
                in_data = True
                continue
            if in_data:
                parts = line_str.split(",")
                # Features are all parts except last
                features = [float(val) if val != "?" else np.nan for val in parts[:-1]]
                label = parts[-1].strip().strip("'\"")
                X_rows.append(features)
                y_rows.append(label)
                
    X = np.array(X_rows, dtype=np.float64)
    y = np.array(y_rows)
    return X, y

dl_dir = Path.home() / "scikit_learn_data" / "openml" / "openml.org" / "data" / "v1" / "download"

datasets = {
    "dlbcl": "DLBCL.arff.gz",
    "breast": "Breast.arff.gz",
    "su2001": "11_Tumors.arff.gz",
    "novartis": "9_Tumors.arff.gz",
    "gcm": "GCM.arff.gz",
    "endometrium": "AP_Endometrium_Kidney.arff.gz",
    "gli": "GLI.arff.gz",
    "leukemia3": "Leukemia-3.arff.gz"
}

for name, filename in datasets.items():
    matches = list(dl_dir.glob(f"**/{filename}"))
    if matches:
        X, y = parse_arff_gz(matches[0])
        unique_y = np.unique(y)
        print(f"[VERIFIED] {name:12s}: N={X.shape[0]:3d}, D={X.shape[1]:5d}, K={len(unique_y):2d}, Classes={list(unique_y)[:4]}")
