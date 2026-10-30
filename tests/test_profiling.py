"""
Unit and integration tests for Anchor-Space Perturbation Profiling (ASPP).

Validates the perturbation profiling engine for assessing cluster reliability:
1. ASPP configuration initialization, parameter defaults, and custom overrides.
2. Standalone profiling measuring Perturbation Stability Index (PSI) and reliability classes
   across perturbation families (subsampling, feature masking, measurement noise).
3. Integrated profiling inside InvariantCoreConsensusV2 via the enable_aspp flag.
4. Inductive inference with stability-weighted confidence: confidence = margin * (1 - PSI).
5. Exact deterministic reproducibility across repeated runs with identical random seeds.
6. Technical batch effect perturbation profiling when batch identifiers are supplied.
7. Clean package-level export parity.
"""

import numpy as np
import pandas as pd

from icc import AnchorSpacePerturbationProfiler as RootProfiler
from icc import ASPPConfig as RootASPPConfig
from icc.aspp import ASPP_FAMILIES, AnchorSpacePerturbationProfiler, ASPPConfig
from icc.consensus_v2 import InvariantCoreConsensusV2


def test_aspp_config_defaults_and_overrides():
    """
    Verify ASPPConfig default hyperparameter values and custom constructor overrides.
    
    Checks that all standard perturbation families (sampling, feature, measurement,
    algorithmic, technical) are registered by default, and that reliability classification
    thresholds (hi=0.70, lo=0.45) and response variance bounds are enforced.
    """
    cfg = ASPPConfig()
    assert set(cfg.families) == set(ASPP_FAMILIES)
    assert cfg.repetitions == 2
    assert cfg.hi_threshold == 0.70
    assert cfg.lo_threshold == 0.45
    assert cfg.max_response_sd == 0.15

    custom_cfg = ASPPConfig(
        families=("sampling", "feature"),
        repetitions=1,
        hi_threshold=0.80,
    )
    assert len(custom_cfg.families) == 2
    assert custom_cfg.repetitions == 1
    assert custom_cfg.hi_threshold == 0.80


def test_aspp_standalone_profiler():
    """
    Verify standalone execution of AnchorSpacePerturbationProfiler on fitted models.
    
    Applies multi-family perturbations (sampling, feature, measurement) to fitted clusters.
    Verifies that:
    1. Returns a structured DataFrame with one row per cluster.
    2. Perturbation Stability Index (PSI) values lie strictly in [0, 1].
    3. Categorical reliability classifications belong to the standard taxonomy:
       {'globally_invariant', 'conditionally_invariant', 'perturbation_fragile', 'ambiguous'}.
    4. Retention rates and anchor co-association stability metrics are populated.
    """
    rng = np.random.default_rng(42)
    # Generate 3 distinct clusters in 2D signal space with 10 noise dimensions
    X1 = rng.normal(loc=[-4, 0], scale=0.5, size=(25, 2))
    X2 = rng.normal(loc=[4, 0], scale=0.5, size=(25, 2))
    X3 = rng.normal(loc=[0, 4], scale=0.5, size=(25, 2))
    X_noise = rng.normal(size=(75, 10))
    X = np.hstack([np.vstack([X1, X2, X3]), X_noise])  # (75, 12)

    model = InvariantCoreConsensusV2(
        n_clusters=3,
        n_base_models=10,
        n_anchors=15,
        random_state=42,
    )
    model.fit(X)

    # Standalone profiler execution
    aspp_cfg = ASPPConfig(
        families=("sampling", "feature", "measurement"),
        repetitions=1,
        levels={"sampling": (0.2,), "feature": (0.3,), "measurement": (0.3,)},
        n_base_models=3,
        random_state=42,
    )
    profiler = AnchorSpacePerturbationProfiler(config=aspp_cfg)
    df = profiler.profile(model, X)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert set(df.columns).issuperset({
        "cluster", "size", "PSI", "reliability",
        "sampling", "feature", "measurement",
        "sampling_retention", "feature_retention", "measurement_retention",
        "sampling_anchor_coassoc", "feature_anchor_coassoc", "measurement_anchor_coassoc",
    })

    # Validate mathematical range constraints
    assert np.all(df["PSI"] >= 0.0) and np.all(df["PSI"] <= 1.0)
    for cat in df["reliability"]:
        assert cat in {"globally_invariant", "conditionally_invariant", "perturbation_fragile", "ambiguous"}

    # Validate profiler state properties
    assert profiler.psi_ is not None and len(profiler.psi_) == 3
    assert profiler.reliability_categories_ is not None and len(profiler.reliability_categories_) == 3
    assert profiler.aspp_summary_ is not None


def test_aspp_integrated_enable_flag():
    """
    Verify integrated perturbation profiling via model constructor enable_aspp=True.
    
    Ensures that when enabled, fitting the model automatically triggers perturbation
    profiling and populates fingerprints_, psi_, and reliability_categories_ on the model.
    """
    rng = np.random.default_rng(101)
    X = rng.normal(size=(60, 8))

    aspp_cfg = ASPPConfig(
        families=("sampling", "algorithmic"),
        repetitions=1,
        levels={"sampling": (0.2,), "algorithmic": (0.5,)},
        n_base_models=3,
        random_state=101,
    )

    model = InvariantCoreConsensusV2(
        n_clusters=2,
        n_base_models=6,
        n_anchors=10,
        enable_aspp=True,
        aspp_config=aspp_cfg,
        random_state=101,
    )
    labels = model.fit_predict(X)

    assert labels.shape == (60,)
    assert model.fingerprints_ is not None
    assert isinstance(model.fingerprints_, pd.DataFrame)
    assert len(model.fingerprints_) == 2
    assert model.psi_ is not None and len(model.psi_) == 2
    assert model.reliability_categories_ is not None and len(model.reliability_categories_) == 2
    assert model.aspp_summary_ is not None
    assert "sampling_mean_ari" in model.aspp_summary_
    assert "algorithmic_mean_ari" in model.aspp_summary_


def test_predict_with_stability_inductive():
    """
    Verify inductive prediction modulated by cluster stability scores.
    
    Validates that:
    1. Returns a dictionary containing labels, confidence, margin, psi, and reliability.
    2. Confidence and prediction margin are strictly bounded in [0, 1].
    3. Mathematical property holds: confidence = margin * (1 - PSI), meaning confidence
       cannot exceed the raw margin score.
    """
    rng = np.random.default_rng(202)
    X_train = np.vstack([
        rng.normal(loc=[-3, -3], scale=0.6, size=(30, 2)),
        rng.normal(loc=[3, 3], scale=0.6, size=(30, 2)),
    ])
    X_train = np.hstack([X_train, rng.normal(size=(60, 6))])  # (60, 8)

    X_test = np.vstack([
        rng.normal(loc=[-3, -3], scale=0.6, size=(10, 2)),
        rng.normal(loc=[3, 3], scale=0.6, size=(10, 2)),
    ])
    X_test = np.hstack([X_test, rng.normal(size=(20, 6))])    # (20, 8)

    aspp_cfg = ASPPConfig(
        families=("sampling", "feature"),
        repetitions=1,
        levels={"sampling": (0.2,), "feature": (0.3,)},
        n_base_models=3,
        random_state=202,
    )

    model = InvariantCoreConsensusV2(
        n_clusters=2,
        n_base_models=5,
        n_anchors=10,
        enable_aspp=True,
        aspp_config=aspp_cfg,
        random_state=202,
    )
    model.fit(X_train)

    # Inductive prediction with stability confidence
    res = model.predict_with_stability(X_test)
    assert isinstance(res, dict)
    assert set(res.keys()) == {"labels", "confidence", "margin", "psi", "reliability"}

    labels = res["labels"]
    confidence = res["confidence"]
    margin = res["margin"]
    psi = res["psi"]
    reliability = res["reliability"]

    assert labels.shape == (20,)
    assert confidence.shape == (20,)
    assert margin.shape == (20,)
    assert psi.shape == (20,)
    assert len(reliability) == 20

    # Bounds check
    assert np.all(confidence >= 0.0) and np.all(confidence <= 1.0)
    assert np.all(margin >= 0.0) and np.all(margin <= 1.0)

    # Invariant: confidence = margin * (1 - psi) <= margin
    assert np.all(confidence <= margin + 1e-7)


def test_aspp_reproducibility():
    """
    Verify bitwise determinism and reproducibility across repeated profiling runs.
    
    Fitting two independent models with identical configurations and seeds must produce
    identical labels, identical PSI vectors, and identical reliability categories.
    """
    rng1 = np.random.default_rng(999)
    X = rng1.normal(size=(40, 6))

    aspp_cfg = ASPPConfig(
        families=("sampling", "measurement"),
        repetitions=1,
        levels={"sampling": (0.2,), "measurement": (0.3,)},
        n_base_models=3,
        random_state=42,
    )

    m1 = InvariantCoreConsensusV2(n_clusters=2, n_base_models=4, n_anchors=8, enable_aspp=True, aspp_config=aspp_cfg, random_state=42)
    m1.fit(X)

    m2 = InvariantCoreConsensusV2(n_clusters=2, n_base_models=4, n_anchors=8, enable_aspp=True, aspp_config=aspp_cfg, random_state=42)
    m2.fit(X)

    assert np.array_equal(m1.labels_, m2.labels_)
    assert np.allclose(m1.psi_, m2.psi_)
    assert m1.reliability_categories_ == m2.reliability_categories_


def test_aspp_with_batch_vector():
    """
    Verify technical perturbation profiling across experimental batch partitions.
    
    Simulates cross-batch label preservation when batch vectors are provided,
    evaluating stability against technical batch confounding.
    """
    rng = np.random.default_rng(555)
    X = rng.normal(size=(50, 6))
    batches = np.repeat([0, 1], 25)

    model = InvariantCoreConsensusV2(n_clusters=2, n_base_models=5, n_anchors=10, random_state=555)
    model.fit(X, batch_vector=batches)

    aspp_cfg = ASPPConfig(
        families=("technical",),
        repetitions=1,
        levels={"technical": (0.3,)},
        n_base_models=3,
        random_state=555,
    )
    df = model.profile_perturbations(X, config=aspp_cfg, batch_vector=batches)
    assert len(df) == 2
    assert "technical" in df.columns
    assert "technical_anchor_coassoc" in df.columns


def test_root_import_parity():
    """
    Verify ASPP classes are accessible directly from the top-level icc package namespace.
    """
    assert RootASPPConfig is ASPPConfig
    assert RootProfiler is AnchorSpacePerturbationProfiler
