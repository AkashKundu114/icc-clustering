import gzip
from pathlib import Path
from scipy.io import arff
import pandas as pd
import numpy as np

dl_dir = Path.home() / "scikit_learn_data" / "openml" / "openml.org" / "data" / "v1" / "download"

candidates = {
    "dlbcl": "DLBCL.arff.gz",
    "breast": "Breast.arff.gz",
    "su2001": "11_Tumors.arff.gz",
    "novartis": "9_Tumors.arff.gz",
    "gcm": "GCM.arff.gz",
    "endometrium": "AP_Endometrium_Kidney.arff.gz",
    "gli": "GLI.arff.gz",
    "leukemia3": "Leukemia-3.arff.gz"
}

print("Locating and loading local ARFF files...")
for name, filename in candidates.items():
    matches = list(dl_dir.glob(f"**/{filename}"))
    if matches:
        p = matches[0]
        try:
            with gzip.open(p, "rt", encoding="utf-8", errors="ignore") as gz:
                data, meta = arff.loadarff(gz)
            df = pd.DataFrame(data)
            target_col = df.columns[-1]
            n_samples = len(df)
            n_features = len(df.columns) - 1
            n_classes = df[target_col].nunique()
            print(f"[OK] {name:12s}: File={filename:22s} Path={p.parent.name} | N={n_samples:3d}, D={n_features:5d}, K={n_classes:2d}")
        except Exception as e:
            print(f"[ERR] {name}: {e}")
    else:
        print(f"[MISSING] {name}")
