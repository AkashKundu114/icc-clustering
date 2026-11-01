import gzip
from pathlib import Path
import numpy as np

def load_arff_data(file_path):
    with gzip.open(file_path, "rt", encoding="utf-8", errors="ignore") as gz:
        in_data = False
        attributes = []
        rows = []
        labels = []
        for line in gz:
            line_str = line.strip()
            if not line_str or line_str.startswith("%"):
                continue
            if line_str.upper().startswith("@ATTRIBUTE"):
                parts = line_str.split()
                attributes.append(parts[1])
            elif line_str.upper().startswith("@DATA"):
                in_data = True
                continue
            elif in_data:
                parts = line_str.split(",")
                features = [float(v) if v != "?" else np.nan for v in parts[:-1]]
                label = parts[-1].strip().strip("'\"")
                rows.append(features)
                labels.append(label)
    feature_names = attributes[:-1]
    X = np.array(rows, dtype=np.float64)
    y = np.array(labels)
    return X, y, feature_names

dl_dir = Path.home() / "scikit_learn_data" / "openml" / "openml.org" / "data" / "v1" / "download"

leuk_path = list(dl_dir.glob("**/Leukemia.arff.gz"))[0]
gcm_path = list(dl_dir.glob("**/GCM.arff.gz"))[0]

print("Loading Leukemia and GCM raw arrays...")
X_leuk, y_leuk, genes_leuk = load_arff_data(leuk_path)
X_gcm, y_gcm, genes_gcm = load_arff_data(gcm_path)

print(f"Leukemia: N={X_leuk.shape[0]}, D={X_leuk.shape[1]}")
print(f"GCM:      N={X_gcm.shape[0]}, D={X_gcm.shape[1]}")

# Find common genes between Leukemia and GCM
common_genes = [g for g in genes_leuk if g in genes_gcm]
print(f"Shared genes: {len(common_genes)} out of {len(genes_leuk)} Leukemia genes")

idx_leuk = [genes_leuk.index(g) for g in common_genes]
idx_gcm = [genes_gcm.index(g) for g in common_genes]

X_leuk_sub = X_leuk[:, idx_leuk]
X_gcm_sub = X_gcm[:, idx_gcm]

# Normalize rows to zero mean, unit variance for correlation
leuk_norm = (X_leuk_sub - np.nanmean(X_leuk_sub, axis=1, keepdims=True)) / np.nanstd(X_leuk_sub, axis=1, keepdims=True)
gcm_norm = (X_gcm_sub - np.nanmean(X_gcm_sub, axis=1, keepdims=True)) / np.nanstd(X_gcm_sub, axis=1, keepdims=True)

# Compute cross-correlation matrix (72 x 190)
corr_matrix = (leuk_norm @ gcm_norm.T) / (len(common_genes) - 1)

print(f"Max correlation found between any Leukemia sample and GCM sample: {np.nanmax(corr_matrix):.5f}")

# Find pairs with r > 0.95
high_corr_pairs = []
for i in range(len(X_leuk)):
    j = np.argmax(corr_matrix[i])
    r = corr_matrix[i, j]
    if r > 0.90:
        high_corr_pairs.append((i, j, r, y_leuk[i], y_gcm[j]))

print(f"\nNumber of Leukemia samples with near-identical matches (r > 0.90) in GCM: {len(high_corr_pairs)} / {len(X_leuk)}")
print("First 10 sample matches:")
for leuk_i, gcm_j, r, l_class, g_class in high_corr_pairs[:10]:
    print(f"  Leukemia #{leuk_i:2d} (class={l_class:4s}) <---> GCM #{gcm_j:3d} (class={g_class:10s}): Pearson r = {r:.5f}")
