"""
Benchmark model implementations for Experiment 3 (Real-World High-Dimensional Evaluation).

Thin compatibility wrapper around the modular src.icc.baselines package.
Preserves exact function signatures, return types, and the MODELS dictionary.
"""

import sys
from pathlib import Path

# Ensure project root is available on sys.path
_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.icc.baselines import get_model, list_models  # noqa: E402
from src.icc.baselines.anchor import run_fastmvc, run_fcag  # noqa: E402
from src.icc.baselines.classical import (  # noqa: E402
    run_single_fcm,
    run_single_kmeans,
    run_single_spectral,
    run_single_ward,
)
from src.icc.baselines.consensus import (  # noqa: E402
    run_icc_v1,
    run_icc_v2,
    run_li_et_al_2019,
    run_standard_consensus,
)
from src.icc.baselines.deep import run_dec  # noqa: E402
from src.icc.consensus_v2 import InvariantCoreConsensusV2  # noqa: E402
from src.icc.core import (  # noqa: E402
    pairwise_coassoc,
    run_clusterer,
)

MODELS = {
    "K-Means": run_single_kmeans,
    "Ward": run_single_ward,
    "Spectral": run_single_spectral,
    "FCM": run_single_fcm,
    "Standard_Consensus": run_standard_consensus,
    "Li_et_al_2019": run_li_et_al_2019,
    "ICC_v1": run_icc_v1,
    "ICC_v2": run_icc_v2,
    "DEC": run_dec,
    "FCAG": run_fcag,
    "FastMVC": run_fastmvc,
}

__all__ = [
    "MODELS",
    "run_single_kmeans",
    "run_single_ward",
    "run_single_spectral",
    "run_single_fcm",
    "run_standard_consensus",
    "run_li_et_al_2019",
    "run_icc_v1",
    "run_icc_v2",
    "run_dec",
    "run_fcag",
    "run_fastmvc",
    "InvariantCoreConsensusV2",
    "pairwise_coassoc",
    "run_clusterer",
    "get_model",
    "list_models",
]


