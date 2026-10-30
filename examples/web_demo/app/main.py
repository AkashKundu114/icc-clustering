"""
CICC Interactive Web Application
================================
FastAPI backend and embedded interactive web interface for
Conformal Inductive Consensus Clustering (CICC).
"""

import os

import numpy as np
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.model_selection import train_test_split

from src.cicc.inductive import InductiveConsensusClusterer
from src.cicc.memory import InductiveConsensusMemory

app = FastAPI(title="CICC: Conformal Inductive Consensus Clustering", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_preset_dataset(name: str):
    """Load and prepare preset benchmark embeddings."""
    if name == "newsgroups":
        path = "data/cache/newsgroups20.npz"
        if not os.path.exists(path):
            raise FileNotFoundError("newsgroups20.npz not found")
        data = np.load(path)
        X_raw, y_raw = data["X"], data["y"]
        # 4 distinct topics: comp.graphics (1), rec.sport.baseball (9), sci.space (13), talk.politics.mideast (17)
        selected_classes = [1, 9, 13, 17]
        mask = np.isin(y_raw, selected_classes)
        X_sub, y_sub = X_raw[mask], y_raw[mask]
        label_map = {c: i for i, c in enumerate(selected_classes)}
        y = np.array([label_map[c] for c in y_sub])
        # Extract 256-dim SVD semantic embeddings for rapid interactive visualization
        svd = TruncatedSVD(n_components=256, random_state=42)
        X = svd.fit_transform(X_sub)
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        X = X / norms
        labels_names = ["comp.graphics", "rec.sport.baseball", "sci.space", "talk.politics.mideast"]
        return X[:1200], y[:1200], labels_names

    elif name == "synthetic_distractor":
        # 20 informative features + 80 distractor noise features
        rng = np.random.default_rng(42)
        N = 600
        K = 3
        D_info = 15
        D_noise = 85
        y = rng.choice(K, size=N)
        mu = np.array([[-2.0, 0.0], [2.0, 0.0], [0.0, 3.0]])
        X_info = np.zeros((N, D_info))
        for k in range(K):
            idx = (y == k)
            X_info[idx, :2] = rng.normal(size=(np.sum(idx), 2)) + mu[k]
            X_info[idx, 2:] = rng.normal(size=(np.sum(idx), D_info - 2)) * 0.5 + (k - 1)
        X_noise = rng.normal(size=(N, D_noise))
        X = np.hstack([X_info, X_noise])
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        X = X / norms
        labels_names = [f"Cluster {k+1}" for k in range(K)]
        return X, y, labels_names

    elif name == "isolet":
        path = "data/cache/isolet.npz"
        if not os.path.exists(path):
            raise FileNotFoundError("isolet.npz not found")
        data = np.load(path)
        X_raw, y_raw = data["X"], data["y"]
        # 4 letter classes
        mask = np.isin(y_raw, [0, 1, 2, 3])
        X = X_raw[mask][:800]
        y = y_raw[mask][:800]
        norms = np.linalg.norm(X, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        X = X / norms
        labels_names = ["Letter A", "Letter B", "Letter C", "Letter D"]
        return X, y, labels_names

    else:
        raise ValueError(f"Unknown preset dataset: {name}")


@app.get("/api/datasets")
def get_datasets():
    return {
        "datasets": [
            {
                "id": "newsgroups",
                "name": "20 Newsgroups Semantic Embeddings (D=256, 4 Topics)",
                "description": "High-dimensional text embeddings exhibiting representation anisotropy.",
            },
            {
                "id": "synthetic_distractor",
                "name": "High-Dim Distractor Benchmark (D=100, 15 Signal + 85 Noise)",
                "description": "Controlled benchmark evaluating Decoy FDR calibration under extreme noise.",
            },
            {
                "id": "isolet",
                "name": "ISOLET Spoken Letters Audio Features (D=617, 4 Classes)",
                "description": "Continuous high-dimensional acoustic spectral features.",
            },
        ]
    }


@app.post("/api/run_clustering")
def run_clustering_endpoint(
    dataset: str = Form("newsgroups"),
    alpha: float = Form(0.10),
    fdr_target: float = Form(0.10),
    n_clusters: int = Form(4),
    n_anchors: int = Form(30),
    enable_decoy: bool = Form(True),
):
    try:
        X, y_true, class_names = load_preset_dataset(dataset)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    N, D = X.shape
    K = min(n_clusters, len(np.unique(y_true)))

    # Split into train/discovery (70%) and holdout test (30%)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_true, test_size=0.30, random_state=42, stratify=y_true
    )

    # Initialize and fit CICC
    cicc = InductiveConsensusClusterer(
        n_clusters=K,
        n_anchors=n_anchors,
        n_base_models=15,
        enable_decoy_gating=enable_decoy,
        fdr_target=fdr_target,
        alpha=alpha,
        random_state=42,
    )
    cicc.fit(X_train, cal_ratio=0.35)

    # Hungarian alignment between discovered consensus clusters and ground truth classes
    from scipy.optimize import linear_sum_assignment
    from sklearn.metrics import confusion_matrix

    res_train = cicc.predict_conformal(X_train)
    res = cicc.predict_conformal(X_test, y_new=y_test)
    y_train_pred = np.argmax(res_train.probabilities, axis=1)
    cm = confusion_matrix(y_train, y_train_pred, labels=np.arange(K))
    row_ind, col_ind = linear_sum_assignment(-cm)
    cluster_to_class = {col: row for row, col in zip(row_ind, col_ind)}

    # Map test prediction sets using Hungarian assignment
    aligned_sets = []
    covered_count = 0
    for i in range(len(X_test)):
        orig_set = res.prediction_sets[i]
        mapped_set = sorted([int(cluster_to_class.get(k, k)) for k in orig_set])
        aligned_sets.append(mapped_set)
        if int(y_test[i]) in mapped_set:
            covered_count += 1

    empirical_cov = float(covered_count / len(X_test))

    # 2D projection for visualization (PCA for deterministic rapid layout)
    pca = PCA(n_components=2, random_state=42)
    coords_2d = pca.fit_transform(X_test)

    # Package sample points with conformal status
    points = []
    for i in range(len(X_test)):
        c_set = aligned_sets[i]
        status = "singleton" if len(c_set) == 1 else ("ambiguous" if len(c_set) > 1 else "abstention")
        points.append({
            "id": i,
            "x": float(coords_2d[i, 0]),
            "y": float(coords_2d[i, 1]),
            "true_label": int(y_test[i]),
            "true_name": class_names[y_test[i]] if y_test[i] < len(class_names) else f"Class {y_test[i]}",
            "prediction_set": c_set,
            "status": status,
            "cardinality": len(c_set),
            "max_prob": float(np.max(res.probabilities[i])),
            "probs": [float(p) for p in res.probabilities[i]],
        })

    # Decoy statistics for visualization
    decoy_data = None
    if cicc.decoy_gating_ is not None and cicc.decoy_gating_.W_ is not None:
        W = cicc.decoy_gating_.W_
        decoy_data = {
            "w_scores": [float(w) for w in W[:100]],  # First 100 features
            "tau": float(cicc.decoy_gating_.tau_) if cicc.decoy_gating_.tau_ is not None else 0.0,
            "selected_count": int(len(cicc.selected_features_)),
            "total_features": int(D),
            "estimated_fdr": float(cicc.decoy_gating_.estimated_fdr_) if cicc.decoy_gating_.estimated_fdr_ is not None else 0.0,
        }

    return {
        "metrics": {
            "nominal_coverage": float(1.0 - alpha),
            "empirical_coverage": empirical_cov,
            "average_set_size": float(res.average_set_size),
            "singleton_count": int(np.sum(res.is_singleton)),
            "singleton_rate": float(np.mean(res.is_singleton)),
            "ambiguous_count": int(np.sum(res.is_ambiguous)),
            "ambiguous_rate": float(np.mean(res.is_ambiguous)),
            "abstention_count": int(np.sum(res.is_abstention)),
            "abstention_rate": float(np.mean(res.is_abstention)),
            "q_hat": float(cicc.conformal_calibrator_.q_hat_),
            "n_test_samples": len(X_test),
        },
        "points": points,
        "decoy": decoy_data,
        "class_names": class_names,
    }


@app.post("/api/simulate_memory")
def simulate_memory_endpoint():
    """Simulate streaming data records with consolidation and novelty detection."""
    dim = 64
    rng = np.random.default_rng(42)
    mem_engine = InductiveConsensusMemory(dim=dim, alpha=0.10, similarity_threshold=0.35)

    scenarios = [
        ("Specimen A1: mRNA sequencing profile of B-cell acute lymphoblastic leukemia", rng.normal(size=dim)),
        ("Specimen A2: Replicate transcriptional assay exhibiting concordant markers", None),
        ("Spectral Scan S1: Reflectance spectrometry of agricultural soil matrix", rng.normal(size=dim)),
        ("Spectral Scan S2: Calibrated infrared re-measurement confirming absorption band", None),
        ("Clinical Bio-Assay C1: Elevated blast count with chromosomal translocation", rng.normal(size=dim)),
        ("Clinical Bio-Assay C2: Follow-up cytogenetics verifying gene fusion", None),
        ("Unrelated Reference: High-latitude geomagnetic telemetry background baseline", rng.normal(size=dim)),
    ]

    # Create correlated embeddings for conversational context
    embeddings = []
    base_vectors = {}
    for i, (text, vec) in enumerate(scenarios):
        if vec is not None:
            v = vec / np.linalg.norm(vec)
            base_vectors[i] = v
            embeddings.append(v)
        else:
            parent_v = base_vectors[i - 1]
            # High cosine similarity (corroborating or consolidating)
            v = parent_v + rng.normal(scale=0.08, size=dim)
            v = v / np.linalg.norm(v)
            embeddings.append(v)

    results = []
    for i, (text, _) in enumerate(scenarios):
        item = mem_engine.add_memory(text=text, embedding=embeddings[i])
        results.append({
            "id": item.id,
            "text": item.text,
            "assigned_cluster": item.assigned_cluster,
            "prediction_set": item.prediction_set,
            "action": item.action,
            "timestamp": item.timestamp,
        })

    stats = mem_engine.get_stats()
    return {"timeline": results, "stats": stats}


# Embedded Modern Single-Page Dashboard HTML
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CICC: Conformal Inductive Consensus Clustering</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; background-color: #0b0f19; color: #e2e8f0; }
        .glass-panel { background: rgba(17, 24, 39, 0.75); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); }
        .accent-gradient { background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%); }
        .metric-glow { box-shadow: 0 0 20px rgba(59, 130, 246, 0.15); }
    </style>
</head>
<body class="min-h-screen p-4 md:p-8">
    <div class="max-w-7xl mx-auto space-y-6">
        <!-- Header -->
        <header class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 glass-panel p-6 rounded-2xl">
            <div>
                <div class="flex items-center gap-3">
                    <span class="px-3 py-1 text-xs font-semibold rounded-full bg-blue-500/20 text-blue-400 border border-blue-500/30">Research Showcase</span>
                    <span class="text-xs text-gray-400 font-mono">v1.0.0</span>
                </div>
                <h1 class="text-2xl md:text-3xl font-bold tracking-tight mt-1 text-white flex items-center gap-2">
                    <i class="fa-solid fa-shapes text-blue-500"></i> Conformal Inductive Consensus Clustering
                </h1>
                <p class="text-sm text-gray-400 mt-1 max-w-3xl">
                    Distribution-free finite-sample coverage guarantees for out-of-sample cluster assignments with Decoy-calibrated FDR feature gating & dynamic streaming memory.
                </p>
            </div>
            <div class="flex items-center gap-3">
                <a href="https://github.com/AkashKundu114/icc-clustering" target="_blank" class="px-4 py-2 text-xs font-medium rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-200 border border-gray-700 transition flex items-center gap-2">
                    <i class="fa-brands fa-github text-sm"></i> GitHub Repository
                </a>
            </div>
        </header>

        <!-- Main Workspace -->
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
            <!-- Sidebar Controls -->
            <div class="lg:col-span-1 glass-panel p-6 rounded-2xl space-y-6">
                <div>
                    <h2 class="text-sm font-semibold uppercase tracking-wider text-gray-400 mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-sliders text-blue-400"></i> Parameters
                    </h2>
                    
                    <div class="space-y-4">
                        <div>
                            <label class="block text-xs font-medium text-gray-300 mb-1">Benchmark Corpus</label>
                            <select id="datasetSelect" class="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-xs text-gray-200 focus:outline-none focus:border-blue-500">
                                <option value="newsgroups">20 Newsgroups (D=256, 4 Topics)</option>
                                <option value="synthetic_distractor">Distractor Suite (D=100, 85% Noise)</option>
                                <option value="isolet">ISOLET Audio (D=617, 4 Letters)</option>
                            </select>
                        </div>

                        <div>
                            <div class="flex justify-between text-xs font-medium text-gray-300 mb-1">
                                <span>Target Error Rate (α)</span>
                                <span id="alphaVal" class="text-blue-400 font-mono">0.10 (90% Cov)</span>
                            </div>
                            <input type="range" id="alphaSlider" min="0.02" max="0.30" step="0.01" value="0.10" class="w-full h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500">
                        </div>

                        <div>
                            <div class="flex justify-between text-xs font-medium text-gray-300 mb-1">
                                <span>Decoy FDR Target (q)</span>
                                <span id="fdrVal" class="text-blue-400 font-mono">0.10 (10%)</span>
                            </div>
                            <input type="range" id="fdrSlider" min="0.05" max="0.30" step="0.01" value="0.10" class="w-full h-1 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500">
                        </div>

                        <div>
                            <label class="block text-xs font-medium text-gray-300 mb-1">Consensus Anchors (m)</label>
                            <input type="number" id="anchorsInput" value="30" min="10" max="100" class="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-xs text-gray-200 focus:outline-none focus:border-blue-500">
                        </div>

                        <div class="flex items-center gap-2 pt-1">
                            <input type="checkbox" id="enableDecoyCheck" checked class="rounded bg-gray-800 border-gray-700 text-blue-600 focus:ring-0">
                            <label for="enableDecoyCheck" class="text-xs text-gray-300 cursor-pointer">Enable Decoy Feature Gating</label>
                        </div>

                        <button id="runBtn" class="w-full accent-gradient text-white text-xs font-semibold py-2.5 rounded-lg shadow-lg hover:opacity-90 transition flex items-center justify-center gap-2">
                            <i class="fa-solid fa-play"></i> Run Conformal Consensus
                        </button>
                    </div>
                </div>

                <div class="border-t border-gray-800 pt-5">
                    <h2 class="text-sm font-semibold uppercase tracking-wider text-gray-400 mb-3 flex items-center gap-2">
                        <i class="fa-solid fa-database text-purple-400"></i> Streaming Memory
                    </h2>
                    <p class="text-xs text-gray-400 mb-3">Simulate inductive streaming memory consolidation & split triggers.</p>
                    <button id="simMemBtn" class="w-full bg-purple-600/20 hover:bg-purple-600/30 text-purple-300 border border-purple-500/40 text-xs font-semibold py-2.5 rounded-lg transition flex items-center justify-center gap-2">
                        <i class="fa-solid fa-rotate text-purple-400"></i> Simulate Memory Stream
                    </button>
                </div>
            </div>

            <!-- Content Area -->
            <div class="lg:col-span-3 space-y-6">
                <!-- Metrics Bar -->
                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
                    <div class="glass-panel p-4 rounded-xl metric-glow">
                        <div class="text-xs text-gray-400">Holdout Coverage</div>
                        <div id="metricCoverage" class="text-xl font-bold text-green-400 font-mono mt-1">--%</div>
                        <div class="text-[10px] text-gray-500 mt-0.5" id="metricNominal">Nominal: 90.0%</div>
                    </div>
                    <div class="glass-panel p-4 rounded-xl">
                        <div class="text-xs text-gray-400">Avg Set Cardinality</div>
                        <div id="metricSetSize" class="text-xl font-bold text-blue-400 font-mono mt-1">--</div>
                        <div class="text-[10px] text-gray-500 mt-0.5">Target: ~1.0</div>
                    </div>
                    <div class="glass-panel p-4 rounded-xl">
                        <div class="text-xs text-gray-400">Singletons (Confident)</div>
                        <div id="metricSingletons" class="text-xl font-bold text-cyan-400 font-mono mt-1">--%</div>
                        <div class="text-[10px] text-gray-500 mt-0.5">|C(x)| == 1</div>
                    </div>
                    <div class="glass-panel p-4 rounded-xl">
                        <div class="text-xs text-gray-400">Boundary Ambiguity</div>
                        <div id="metricAmbiguous" class="text-xl font-bold text-amber-400 font-mono mt-1">--%</div>
                        <div class="text-[10px] text-gray-500 mt-0.5">|C(x)| > 1</div>
                    </div>
                    <div class="glass-panel p-4 rounded-xl">
                        <div class="text-xs text-gray-400">Novel / Abstentions</div>
                        <div id="metricAbstention" class="text-xl font-bold text-rose-400 font-mono mt-1">--%</div>
                        <div class="text-[10px] text-gray-500 mt-0.5">|C(x)| == 0 (OOD)</div>
                    </div>
                </div>

                <!-- 2D Projection Chart -->
                <div class="glass-panel p-5 rounded-2xl space-y-3">
                    <div class="flex justify-between items-center">
                        <div>
                            <h3 class="text-sm font-semibold text-white flex items-center gap-2">
                                <i class="fa-solid fa-chart-scatter text-blue-400"></i> Out-of-Sample Conformal Cluster Embedding Manifold
                            </h3>
                            <p class="text-xs text-gray-400">Test points color-coded by assigned conformal prediction set and boundary ambiguity.</p>
                        </div>
                        <div class="flex gap-4 text-xs">
                            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-blue-500"></span> Confident (|C|=1)</span>
                            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span> Ambiguous (|C|>1)</span>
                            <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span> Novel / OOD (|C|=0)</span>
                        </div>
                    </div>
                    <div id="manifoldPlot" class="w-full h-[420px] rounded-lg"></div>
                </div>

                <!-- Secondary Visualizations: Decoy Gating & Streaming Memory -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Decoy FDR Chart -->
                    <div class="glass-panel p-5 rounded-2xl space-y-3">
                        <h3 class="text-sm font-semibold text-white flex items-center gap-2">
                            <i class="fa-solid fa-shield-halved text-green-400"></i> Decoy Competition Saliency W_j
                        </h3>
                        <p class="text-xs text-gray-400">Features exceeding threshold τ are retained with controlled False Discovery Rate.</p>
                        <div id="decoyPlot" class="w-full h-[220px]"></div>
                    </div>

                    <!-- Streaming Memory Timeline -->
                    <div class="glass-panel p-5 rounded-2xl space-y-3">
                        <h3 class="text-sm font-semibold text-white flex items-center gap-2">
                            <i class="fa-solid fa-clock-rotate-left text-purple-400"></i> Dynamic Streaming Memory Feed
                        </h3>
                        <p class="text-xs text-gray-400">Real-time memory consolidation vs novel cluster schema allocation.</p>
                        <div id="memoryLog" class="h-[220px] overflow-y-auto space-y-2 text-xs font-mono pr-2">
                            <div class="text-gray-500 italic p-2 text-center">Click "Simulate Memory Stream" to run streaming episodic intake.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // DOM Elements
        const alphaSlider = document.getElementById('alphaSlider');
        const alphaVal = document.getElementById('alphaVal');
        const fdrSlider = document.getElementById('fdrSlider');
        const fdrVal = document.getElementById('fdrVal');
        const runBtn = document.getElementById('runBtn');
        const simMemBtn = document.getElementById('simMemBtn');

        alphaSlider.addEventListener('input', (e) => {
            const val = parseFloat(e.target.value);
            alphaVal.textContent = `${val.toFixed(2)} (${((1 - val)*100).toFixed(0)}% Cov)`;
        });

        fdrSlider.addEventListener('input', (e) => {
            const val = parseFloat(e.target.value);
            fdrVal.textContent = `${val.toFixed(2)} (${(val*100).toFixed(0)}%)`;
        });

        async function runClustering() {
            runBtn.disabled = true;
            runBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Distilling...';

            const formData = new FormData();
            formData.append('dataset', document.getElementById('datasetSelect').value);
            formData.append('alpha', alphaSlider.value);
            formData.append('fdr_target', fdrSlider.value);
            formData.append('n_anchors', document.getElementById('anchorsInput').value);
            formData.append('enable_decoy', document.getElementById('enableDecoyCheck').checked);

            try {
                const res = await fetch('/api/run_clustering', { method: 'POST', body: formData });
                const data = await res.json();

                // Update Metrics
                document.getElementById('metricCoverage').textContent = `${(data.metrics.empirical_coverage * 100).toFixed(1)}%`;
                document.getElementById('metricNominal').textContent = `Nominal: ${(data.metrics.nominal_coverage * 100).toFixed(1)}%`;
                document.getElementById('metricSetSize').textContent = data.metrics.average_set_size.toFixed(2);
                document.getElementById('metricSingletons').textContent = `${(data.metrics.singleton_rate * 100).toFixed(1)}%`;
                document.getElementById('metricAmbiguous').textContent = `${(data.metrics.ambiguous_rate * 100).toFixed(1)}%`;
                document.getElementById('metricAbstention').textContent = `${(data.metrics.abstention_rate * 100).toFixed(1)}%`;

                // Render Manifold Plot
                renderManifold(data.points);

                // Render Decoy Plot
                if (data.decoy) {
                    renderDecoyPlot(data.decoy);
                }
            } catch (err) {
                console.error(err);
                alert('Error running clustering: ' + err.message);
            } finally {
                runBtn.disabled = false;
                runBtn.innerHTML = '<i class="fa-solid fa-play"></i> Run Conformal Consensus';
            }
        }

        function renderManifold(points) {
            const colors = {
                'singleton': '#3b82f6',
                'ambiguous': '#f59e0b',
                'abstention': '#ef4444'
            };

            const traces = ['singleton', 'ambiguous', 'abstention'].map(status => {
                const pts = points.filter(p => p.status === status);
                return {
                    x: pts.map(p => p.x),
                    y: pts.map(p => p.y),
                    mode: 'markers',
                    name: status.toUpperCase(),
                    marker: {
                        color: colors[status],
                        size: status === 'abstention' ? 9 : 6,
                        symbol: status === 'abstention' ? 'diamond' : 'circle',
                        opacity: 0.85
                    },
                    text: pts.map(p => `Point #${p.id}<br>True: ${p.true_name}<br>Set C(x): [${p.prediction_set.join(', ')}]<br>Card: ${p.cardinality}<br>Max P: ${p.max_prob.toFixed(3)}`),
                    hoverinfo: 'text'
                };
            });

            const layout = {
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                margin: { l: 30, r: 20, t: 10, b: 30 },
                xaxis: { showgrid: true, gridcolor: '#1e293b', zeroline: false, showticklabels: false },
                yaxis: { showgrid: true, gridcolor: '#1e293b', zeroline: false, showticklabels: false },
                legend: { orientation: 'h', y: 1.1, font: { color: '#94a3b8', size: 10 } },
                hovermode: 'closest'
            };

            Plotly.newPlot('manifoldPlot', traces, layout, { responsive: true, displayModeBar: false });
        }

        function renderDecoyPlot(decoy) {
            const x = decoy.w_scores.map((_, i) => `f${i}`);
            const y = decoy.w_scores;
            const colors = y.map(w => w >= decoy.tau ? '#10b981' : '#64748b');

            const trace = {
                x: x,
                y: y,
                type: 'bar',
                marker: { color: colors }
            };

            const layout = {
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                margin: { l: 30, r: 20, t: 10, b: 30 },
                xaxis: { showticklabels: false, showgrid: false },
                yaxis: { gridcolor: '#1e293b', font: { color: '#94a3b8', size: 9 } },
                shapes: [{
                    type: 'line',
                    y0: decoy.tau,
                    y1: decoy.tau,
                    x0: 0,
                    x1: x.length - 1,
                    line: { color: '#ef4444', width: 2, dash: 'dash' }
                }]
            };

            Plotly.newPlot('decoyPlot', [trace], layout, { responsive: true, displayModeBar: false });
        }

        async function simulateMemory() {
            simMemBtn.disabled = true;
            simMemBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Ingesting...';
            try {
                const res = await fetch('/api/simulate_memory', { method: 'POST' });
                const data = await res.json();
                const log = document.getElementById('memoryLog');
                log.innerHTML = '';
                
                data.timeline.forEach((item, idx) => {
                    const badgeClass = item.action === 'novel_cluster' ? 'bg-purple-500/20 text-purple-300 border-purple-500/30' :
                        (item.action === 'consolidated' ? 'bg-blue-500/20 text-blue-300 border-blue-500/30' : 'bg-amber-500/20 text-amber-300 border-amber-500/30');
                    
                    const el = document.createElement('div');
                    el.className = 'p-2.5 rounded-lg bg-gray-900/60 border border-gray-800 space-y-1';
                    el.innerHTML = `
                        <div class="flex justify-between items-center text-[10px]">
                            <span class="text-gray-400 font-mono">${item.id}</span>
                            <span class="px-2 py-0.5 rounded border ${badgeClass} uppercase font-semibold text-[9px]">${item.action.replace('_', ' ')}</span>
                        </div>
                        <div class="text-gray-300 text-xs">${item.text}</div>
                        <div class="text-[10px] text-gray-500">Cluster: ${item.assigned_cluster} | Set: [${item.prediction_set.join(', ')}]</div>
                    `;
                    log.appendChild(el);
                });
            } catch (err) {
                console.error(err);
            } finally {
                simMemBtn.disabled = false;
                simMemBtn.innerHTML = '<i class="fa-solid fa-rotate text-purple-400"></i> Simulate Memory Stream';
            }
        }

        runBtn.addEventListener('click', runClustering);
        simMemBtn.addEventListener('click', simulateMemory);
        // Initial run on page load
        window.addEventListener('load', runClustering);
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(content=HTML_CONTENT)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
