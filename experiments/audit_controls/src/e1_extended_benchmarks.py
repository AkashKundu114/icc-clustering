"""
Experiment 1: Extended Multi-Domain Benchmark Suite (>=20 Datasets).

Covers >=20 diverse real-world benchmarks across genomics, mass spectrometry,
computer vision, speech, hyperspectral imaging, text, and synthetic distractor regimes.

Features:
- Automated caching: downloads missing datasets from OpenML / public repositories
  and persists them to experiments/exp3_real_world_benchmarks/data/cache/<name>.npz
- Evaluates 10 clustering models across 5 trials per dataset:
  1. K-Means
  2. Ward Hierarchical
  3. Spectral Clustering
  4. Fuzzy C-Means (FCM)
  5. Standard Consensus (EAC)
  6. Li et al. (2019) Consensus
  7. FCAG (Fast Anchor Graph)
  8. ICC-v1 (Feature-Reliability Anchor Consensus)
  9. ICC-v2 (Legacy 15% Floor)
  10. ICC-v2 (Label-Free Adaptive Subspace Pool)
- Outputs full trial-level CSV to experiments/audit_controls/data/e1_extended_benchmarks.csv
  and summary matrix to experiments/audit_controls/data/e1_extended_summary.csv.
"""

import os
import sys
import time
import warnings
from pathlib import Path

# Ensure project root is on sys.path
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.datasets import fetch_openml
from sklearn.metrics import (
    adjusted_rand_score,
    normalized_mutual_info_score,
    adjusted_mutual_info_score,
    v_measure_score,
)

warnings.filterwarnings("ignore")

from icc.consensus_v2 import InvariantCoreConsensusV2
from icc.consensus import InvariantCoreConsensus as ICCv1
from icc.core import run_clusterer

CACHE_DIR = _ROOT / "experiments" / "exp3_real_world_benchmarks" / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR = _ROOT / "experiments" / "audit_controls" / "data"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Specification for 22 real-world benchmarks
DATASET_SPECS = [
    # 8 cached datasets
    {"name": "colon", "source": "cache", "domain": "genomics", "K": 2},
    {"name": "srbct", "source": "cache", "domain": "genomics", "K": 4},
    {"name": "cns", "source": "cache", "domain": "genomics", "K": 2},
    {"name": "leukemia", "source": "cache", "domain": "genomics", "K": 2},
    {"name": "prostate", "source": "cache", "domain": "genomics", "K": 2},
    {"name": "ovarian", "source": "cache", "domain": "proteomics", "K": 2},
    {"name": "madelon", "source": "cache", "domain": "synthetic", "K": 2},
    {"name": "sonar", "source": "cache", "domain": "acoustic", "K": 2},
    
    # 6 additional ultra-high-dimensional biological datasets (D >> N)
    {"name": "lung_cancer", "source": "openml", "openml_id": 1106, "domain": "genomics", "K": 2},
    {"name": "glioma", "source": "openml", "openml_id": 1107, "domain": "genomics", "K": 4},
    {"name": "breast_cancer_genomic", "source": "openml", "openml_id": 1120, "domain": "genomics", "K": 2},
    {"name": "lymphoma", "source": "openml", "openml_id": 1157, "domain": "genomics", "K": 3},
    
    # 8 diverse multi-class, imaging, audio, text & sensor benchmarks
    {"name": "isolet", "source": "openml", "openml_id": 300, "domain": "audio", "K": 26, "subsample": 2000},
    {"name": "usps", "source": "openml", "openml_id": 554, "domain": "image", "K": 10, "subsample": 2000},
    {"name": "waveform", "source": "openml", "openml_id": 60, "domain": "sensor", "K": 3, "subsample": 2000},
    {"name": "arrhythmia", "source": "openml", "openml_id": 5, "domain": "medical", "K": 16},
    {"name": "har", "source": "openml", "openml_id": 1478, "domain": "sensor", "K": 6, "subsample": 2000},
    {"name": "gisette", "source": "openml", "openml_id": 41027, "domain": "vision_noise", "K": 2, "subsample": 1000},
    {"name": "newsgroups20", "source": "registry", "domain": "text", "K": 20, "subsample": 2000},
    {"name": "indian_pines", "source": "registry", "domain": "hyperspectral", "K": 16, "subsample": 2000},
    {"name": "yale_b", "source": "registry", "domain": "vision", "K": 38, "subsample": 1000},
    {"name": "zheng68k", "source": "registry", "domain": "scrnaseq", "K": 10},
]


def load_or_fetch_dataset(spec):
    name = spec["name"]
    cache_file = CACHE_DIR / f"{name}.npz"
    
    if cache_file.exists():
        d = np.load(cache_file, allow_pickle=True)
        return d["X"].astype(np.float64), d["y"].astype(int)
        
    print(f"Fetching {name} from {spec['source']}...")
    if spec["source"] == "openml":
        data = fetch_openml(data_id=spec["openml_id"], as_frame=False)
        X = data.data
        if hasattr(X, "toarray"):
            X = X.toarray()
        X = np.nan_to_num(X, nan=np.nanmedian(X))
        y = LabelEncoder().fit_transform(data.target)
        
        if spec.get("subsample") and len(y) > spec["subsample"]:
            rng = np.random.default_rng(42)
            idx = rng.choice(len(y), size=spec["subsample"], replace=False)
            X, y = X[idx], y[idx]
            
        X = StandardScaler().fit_transform(X)
        np.savez_compressed(cache_file, X=X, y=y)
        return X, y
        
    elif spec["source"] == "registry":
        from icc.datasets.registry import load_dataset
        X, y, meta = load_dataset(name)
        if hasattr(X, "toarray"):
            X = X.toarray()
        X = np.nan_to_num(X, nan=0.0)
        y = LabelEncoder().fit_transform(y)
        
        if spec.get("subsample") and len(y) > spec["subsample"]:
            rng = np.random.default_rng(42)
            idx = rng.choice(len(y), size=spec["subsample"], replace=False)
            X, y = X[idx], y[idx]
            
        X = StandardScaler().fit_transform(X)
        np.savez_compressed(cache_file, X=X, y=y)
        return X, y
        
    raise ValueError(f"Unknown source: {spec['source']}")


def run_single_model(model_name, X, k, seed):
    N, D = X.shape
    t0 = time.time()
    
    if model_name == "K-Means":
        labels = run_clusterer("kmeans", X, k, seed=seed)
    elif model_name == "Ward":
        labels = run_clusterer("ward", X, k, seed=seed)
    elif model_name == "Spectral":
        labels = run_clusterer("spectral", X, k, seed=seed)
    elif model_name == "FCM":
        labels = run_clusterer("fcm", X, k, seed=seed)
    elif model_name == "Standard_Consensus":
        # Evidence Accumulation Clustering with 25 random subspaces
        rng = np.random.default_rng(seed)
        sub_d = max(2, int(0.3 * D))
        P = [run_clusterer("kmeans", X[:, rng.choice(D, size=sub_d, replace=False)], k, seed=int(rng.integers(1e6)))
             for _ in range(25)]
        from icc.core import pairwise_coassoc
        S = pairwise_coassoc(P)
        from sklearn.cluster import SpectralClustering
        sc = SpectralClustering(n_clusters=k, affinity="precomputed", random_state=seed, assign_labels="kmeans")
        labels = sc.fit_predict(S)
    elif model_name == "Li_et_al_2019":
        # Co-association matrix with dense spectral clustering
        rng = np.random.default_rng(seed)
        P = [run_clusterer("kmeans", X, k, seed=int(rng.integers(1e6))) for _ in range(25)]
        from icc.core import pairwise_coassoc
        S = pairwise_coassoc(P)
        from sklearn.cluster import SpectralClustering
        sc = SpectralClustering(n_clusters=k, affinity="precomputed", random_state=seed, assign_labels="kmeans")
        labels = sc.fit_predict(S)
    elif model_name == "FCAG":
        from icc.baselines.anchor import FastConsensusAnchorGraph
        model = FastConsensusAnchorGraph(n_clusters=k, n_anchors=min(30, N), random_state=seed)
        labels = model.fit_predict(X)
    elif model_name == "ICC_v1":
        model = ICCv1(n_clusters=k, n_base_models=25, n_anchors=min(30, N), random_state=seed)
        labels = model.fit_predict(X)
    elif model_name == "ICC_v2_legacy":
        model = InvariantCoreConsensusV2(n_clusters=k, n_base_models=25, n_anchors=min(30, N), pool_mode="legacy", random_state=seed)
        labels = model.fit_predict(X)
    elif model_name == "ICC_v2_adaptive":
        # Adaptive: 10% pool fraction based on E3 sensitivity findings
        model = InvariantCoreConsensusV2(n_clusters=k, n_base_models=25, n_anchors=min(30, N), pool_mode="bc_frac", pool_frac=0.10, random_state=seed)
        labels = model.fit_predict(X)
    else:
        raise ValueError(f"Unknown model: {model_name}")
        
    elapsed = time.time() - t0
    return labels, elapsed


def evaluate_trial(y_true, y_pred, elapsed):
    return {
        "ari": float(adjusted_rand_score(y_true, y_pred)),
        "nmi": float(normalized_mutual_info_score(y_true, y_pred)),
        "ami": float(adjusted_mutual_info_score(y_true, y_pred)),
        "v_measure": float(v_measure_score(y_true, y_pred)),
        "runtime_sec": float(elapsed),
    }


def main():
    models = [
        "K-Means",
        "Ward",
        "Spectral",
        "FCM",
        "Standard_Consensus",
        "Li_et_al_2019",
        "FCAG",
        "ICC_v1",
        "ICC_v2_legacy",
        "ICC_v2_adaptive",
    ]
    seeds = [42, 101, 202, 303, 404]
    
    rows = []
    print(f"Beginning Extended Benchmark Evaluation on {len(DATASET_SPECS)} Datasets across {len(models)} Models...")
    
    for spec in DATASET_SPECS:
        name = spec["name"]
        try:
            X, y = load_or_fetch_dataset(spec)
        except Exception as e:
            print(f"Skipping {name}: failed to load ({e})")
            continue
            
        N, D = X.shape
        K = len(np.unique(y))
        print(f"\n[Dataset: {name}] Domain: {spec['domain']}, N={N}, D={D}, K={K}")
        
        for mname in models:
            for s in seeds:
                try:
                    preds, dur = run_single_model(mname, X, K, seed=s)
                    metrics = evaluate_trial(y, preds, dur)
                    rows.append({
                        "dataset": name,
                        "domain": spec["domain"],
                        "N": N,
                        "D": D,
                        "K": K,
                        "model": mname,
                        "seed": s,
                        **metrics,
                    })
                except Exception as e:
                    print(f"  Error on {mname} (seed {s}): {e}")
                    
    df_raw = pd.DataFrame(rows)
    raw_path = RESULTS_DIR / "e1_extended_benchmarks.csv"
    df_raw.to_csv(raw_path, index=False)
    print(f"\nSaved raw trial results to {raw_path}")
    
    # Summary pivot table (Mean ARI by Dataset x Model)
    summary = df_raw.pivot_table(index="dataset", columns="model", values="ari", aggfunc="mean").round(4)
    summary_path = RESULTS_DIR / "e1_extended_summary.csv"
    summary.to_csv(summary_path)
    
    print("\n" + "=" * 90)
    print("EXTENDED BENCHMARK SUMMARY MATRIX (MEAN ARI)")
    print("=" * 90)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 220)
    print(summary.to_string())
    
    print("\n" + "-" * 90)
    print("GRAND MEAN ARI BY MODEL:")
    print("-" * 90)
    mean_by_model = df_raw.groupby("model")["ari"].mean().sort_values(ascending=False)
    for m, score in mean_by_model.items():
        print(f"  {m:<25}: {score:.4f}")


if __name__ == "__main__":
    main()
